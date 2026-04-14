import json
from helper import llm
from helper.extract_json import extract_json
from data import db

with open(f"prompts/system_rules") as f:
    system_prompt_template = f.read()
with open(f"prompts/user") as f:
    user_prompt_template = f.read()


def addAnswer(model, clause):
    topics = db.getGroupedRules()

    hex_to_int = {}
    int_to_hex = {}
    current_id = 1

    ruletext = ""
    for topic, rules in topics.items():
        ruletext += f"### {topic}\n"
        for rule in rules:
            hex_to_int[rule["_id"]] = current_id
            int_to_hex[current_id] = rule["_id"]
            ruletext += f"- **ID**: {current_id} - {rule['text']}\n"
            current_id += 1
        ruletext += "\n"

    system_text = system_prompt_template.replace("###content###", ruletext)
    user_text = user_prompt_template.replace("###content###", clause["content"])

    for i in range(5):
        try:
            raw_answer = llm.getAnswer(model, system_text, user_text)
            parsed = extract_json(raw_answer)

            required_keys = ["result", "explanation", "hurt_rules"]
            missing_keys = [key for key in required_keys if key not in parsed]
            if missing_keys:
                raise Exception(f"Invalid format. Missing keys: {missing_keys}. Response: {raw_answer}")

            pred_label = parsed["result"]
            allowed_labels = ["valid", "void", "unfair"]

            if not isinstance(pred_label, str):
                raise Exception(
                    f"Invalid type for 'result'. Expected: str, Got: {type(pred_label)}. Response: {raw_answer}")

            if pred_label not in allowed_labels:
                raise Exception(
                    f"Invalid value for 'result': '{pred_label}'. Allowed: {allowed_labels}. Response: {raw_answer}")

            remapped_hurt_rules = []
            for rule_id in parsed["hurt_rules"]:
                try:
                    int_rule_id = int(rule_id)
                    if int_rule_id in int_to_hex:
                        remapped_hurt_rules.append(str(int_to_hex[int_rule_id]))
                except ValueError:
                    print(f"Warning: Invalid rule ID '{rule_id}' returned by LLM. Ignoring.")

            clause["pred_label"] = pred_label
            clause["pred_explanation"] = parsed["explanation"]
            clause["pred_hurt-rules"] = remapped_hurt_rules

            return clause

        except Exception as e:
            print(f"Error on attempt {i + 1}/5: {e}")
            if i < 4:
                print("RETRY")

    return None