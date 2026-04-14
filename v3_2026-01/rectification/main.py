import os
import json
from datetime import datetime
from rectification.agents.corrector import get_corrector_json_response
from rectification.agents.judge import get_judge_json_response
from data import db
from rectification import metrics as rectification_metrics

model = "gpt-4.1-2025-04-14"


def main():
    with open(f"prompts/corrector_system.md") as f:
        corrector_system_prompt = f.read()
    with open(f"prompts/corrector_user.md") as f:
        corrector_user_prompt = f.read()
    with open(f"prompts/robo_judge_system.md") as f:
        judge_system_prompt = f.read()
    with open(f"prompts/robo_judge_user.md") as f:
        judge_user_prompt = f.read()

    all_clauses = db.getClauses()

    # Load grouped rules and prepare mappings for the context window
    grouped_rules = db.getGroupedRules()
    rules_text, int_to_hex_map, hex_to_title_map = format_rules(grouped_rules)

    print(f"Model: {model}")
    print(f"Total clauses to process: {len(all_clauses)}")

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = f"logs/{model}/"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"correction_{date_str}.json")
    metrics_file_path = os.path.join(log_dir, f"correction_{date_str}.md")

    results = []
    processed_clause_contents = set()
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
                processed_clause_contents = {entry["content"] for entry in results}
            print(f"Loaded {len(results)} already processed clauses from {log_file_path}.")
        except json.JSONDecodeError:
            print(f"Warning: Could not parse existing log file {log_file_path}. Starting fresh.")
            results = []
            processed_clause_contents = set()
        except Exception as e:
            print(f"Error loading log file: {e}. Starting fresh.")
            results = []
            processed_clause_contents = set()

    for i, clause in enumerate(all_clauses):
        clause_content = clause["content"]

        if clause_content in processed_clause_contents:
            print(f"--- Skipping already processed clause {i + 1}/{len(all_clauses)}: {clause_content[:70]}... ---")
            continue

        print(f"\n--- Processing clause {i + 1}/{len(all_clauses)} ---")

        try:
            final_corrector_system_prompt = corrector_system_prompt.replace("###RULES###", rules_text)
            final_corrector_user_prompt = corrector_user_prompt.replace("###CLAUSE###", clause["content"])

            corrector_output = get_corrector_json_response(model, final_corrector_system_prompt,
                                                           final_corrector_user_prompt)

            if corrector_output is None:
                print(f"  -> Corrector LLM failed for clause. Skipping.")
                continue

            clause["pred_label"] = corrector_output["result"]
            clause["pred_explanation"] = corrector_output["explanation"]

            if clause["pred_label"] == "void":
                # Map the simple integer IDs returned by the LLM back to the original hex IDs
                raw_hurt_rules_ids = corrector_output["hurt_rules"]
                remapped_hurt_rules = []

                for rule_id in raw_hurt_rules_ids:
                    try:
                        int_rule_id = int(rule_id)
                        if int_rule_id in int_to_hex_map:
                            remapped_hurt_rules.append(str(int_to_hex_map[int_rule_id]))
                        else:
                            print(f"  -> Warning: LLM returned unknown rule ID '{int_rule_id}'. Ignoring.")
                    except (ValueError, TypeError):
                        print(
                            f"  -> Warning: LLM returned invalid (non-numeric) rule ID '{rule_id}'. Ignoring.")

                clause["pred_hurt-rules"] = remapped_hurt_rules

                clause["pred_correction"] = corrector_output["correction"]
                print("  -> Invoking Robo Judge...")

                if clause["true_label"] == "void":
                    reasons_list = [reason.strip() for reason in clause["true_explanation"].split(';') if
                                    reason.strip()]
                    formatted_explanation = "\n".join(f"{i + 1}. {reason}" for i, reason in enumerate(reasons_list))
                else:
                    formatted_explanation = "No defects present."

                judge_prompt = judge_user_prompt \
                    .replace("###ORIGINAL_CLAUSE###", clause["content"]) \
                    .replace("###TRUE_EXPLANATION###", formatted_explanation) \
                    .replace("###PRED_CORRECTION###", clause["pred_correction"]) \
                    .replace("###PRED_EXPLANATION###", clause["pred_explanation"])

                judge_output = get_judge_json_response(judge_system_prompt, judge_prompt)

                if judge_output is None:
                    print(f"  -> Robo Judge LLM failed for clause. Skipping.")
                    continue

                clause["robo_judge"] = judge_output

            elif clause["pred_label"] != "void" and clause["true_label"] == "void":
                print("  -> Predicted 'valid' but was 'void'. Logging 'misclassified' judge entry.")
                clause["robo_judge"] = {
                    "explanation": "misclassified",
                    "missed_problems": len(clause["true_hurt-rules"]),
                    "unnecessary_changes": 0
                }

            results.append(clause)

            with open(log_file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"  -> An unexpected error occurred while processing clause: {e}. Skipping.")
            continue

    print(f"\nDetailed results saved to {log_file_path}")

    metrics_output = rectification_metrics.calculate_metrics(results, hex_to_title_map)
    with open(metrics_file_path, 'w', encoding='utf-8') as f:
        f.write(metrics_output)
    print(f"Metrics saved to {metrics_file_path}")
    print("\nBenchmark complete.")


def format_rules(grouped_rules):
    int_to_hex = {}
    hex_to_title = {}
    current_id = 1
    formatted_list = []

    for topic, rules in grouped_rules.items():
        formatted_list.append(f"### {topic}")
        for rule in rules:
            hex_id = rule["_id"]
            int_to_hex[current_id] = hex_id

            rule_name = rule.get("name", rule.get("title", rule.get("text", "N/A")))
            hex_to_title[str(hex_id)] = rule_name

            # Format: {id}: {text}
            rule_text = f"{current_id}: {rule['text']}"
            formatted_list.append(rule_text)
            current_id += 1
        formatted_list.append("")

    return "\n".join(formatted_list), int_to_hex, hex_to_title


if __name__ == "__main__":
    main()