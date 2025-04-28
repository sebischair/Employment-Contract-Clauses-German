from helper import llm, files
from helper import db
import random
import os

SOURCES_PATH = "../data/sources/"

def addAnswer(clause):
    rules = db.getRules()
    sources = []

    if "true_hurt-rules" in clause:
        for ruleId in clause["true_hurt-rules"]:
            rule = next((item for item in rules if item["_id"] == ruleId), None)
            for ref in rule["references"]:
                if any(s["ref"] == ref for s in sources):
                    continue
                filename = ref.replace('.', '_').replace('/', '+')+".md"
                filepath = os.path.join(SOURCES_PATH, filename)
                with open(filepath, 'r') as file:
                    text = file.read()
                    sources.append({"ref": ref, "text": text})
        print(f"Fitting sources: {len(sources)}")

    if not sources:
        matching_rules = [r for r in rules if r["topic"] == clause["topic"]]
        if not matching_rules:
            matching_rules = rules

        all_refs = []
        for r in matching_rules:
            all_refs.extend(r["references"])
        unique_refs = list(set(all_refs))

        if unique_refs:
            for ref in random.sample(unique_refs, min(2, len(unique_refs))):
                filename = ref.replace('.', '_').replace('/', '+')+".md"
                filepath = os.path.join(SOURCES_PATH, filename)
                with open(filepath, 'r') as file:
                    text = file.read()
                    sources.append({"ref": ref, "text": text})

        print(f"Random sources: {len(sources)}")

    sourcetext = ""
    for s in sources:
        sourcetext += f"**{s['ref']}**\n{s['text']}\n\n---\n\n"

    system_text = files.readPromptTemplate("system_sources").replace("###content###", sourcetext)
    user_text = files.readPromptTemplate("user").replace("###content###", clause["content"])

    answer = llm.getAnswer(system_text, user_text, False)

    clause["pred_label"] = answer["result"]
    clause["pred_explanation"] = answer["explanation"]

    return clause
