from helper import llm, files
from helper import db


def addAnswer(clause):
    # Get active rules from the database
    topics = db.getGroupedRules()

    # Create a mapping from hex IDs to integers
    hex_to_int = {}
    int_to_hex = {}
    current_id = 1

    # Format rules as Markdown
    ruletext = ""
    for topic, rules in topics.items():
        ruletext += f"### {topic}\n"
        for rule in rules:
            hex_to_int[rule["_id"]] = current_id
            int_to_hex[current_id] = rule["_id"]
            ruletext += f"- **ID**: {current_id} - {rule['text']}\n"
            current_id += 1
        ruletext += "\n"

    # Replace placeholders in system and user text
    system_text = files.readText("prompts/system_rules").replace("###content###", ruletext)
    user_text = files.readText("prompts/user").replace("###content###", clause["content"])

    # Fetch the LLM answer
    answer = llm.getAnswer(system_text, user_text, True)
    remapped_hurt_rules = [str(int_to_hex[rule]) for rule in answer["hurt_rules"] if rule in int_to_hex]

    clause["pred_label"] = answer["result"]
    clause["pred_explanation"] = answer["explanation"]
    clause["pred_hurt-rules"] = remapped_hurt_rules

    return clause
