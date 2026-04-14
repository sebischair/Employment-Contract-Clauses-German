from helper import llm, extract_json


def get_corrector_json_response(model, system_prompt, user_prompt):
    for attempt in range(5):
        try:
            answer = llm.getAnswer(model, system_prompt, user_prompt)
            parsed = extract_json.extract_json(answer)

            # 2. Validation of mandatory keys
            required_keys = ["explanation", "result"]
            missing_keys = [key for key in required_keys if key not in parsed]
            if missing_keys:
                raise Exception(f"Missing mandatory keys: {missing_keys}. Response: {answer}")

            # 3. Type validation of fields
            pred_label = parsed["result"]
            pred_explanation = parsed["explanation"]
            pred_hurt_rules = parsed.get("hurt_rules")
            pred_correction = parsed.get("correction")

            if not isinstance(pred_label, str):
                raise Exception(f"Invalid type for 'result' (expected: str). Response: {answer}")
            if not isinstance(pred_explanation, str):
                raise Exception(f"Invalid type for 'explanation' (expected: str). Response: {answer}")
            if pred_hurt_rules is not None and not isinstance(pred_hurt_rules, list):
                raise Exception(f"Invalid type for 'hurt_rules' (expected: list or None). Response: {answer}")
            if pred_hurt_rules is not None and not all(isinstance(item, int) for item in pred_hurt_rules):
                raise Exception(f"Invalid content for 'hurt_rules' (expected: list[int]). Response: {answer}")
            if pred_correction is not None and not isinstance(pred_correction, str):
                raise Exception(f"Invalid type for 'correction' (expected: str or None). Response: {answer}")

            # 4. Content validation for 'result'
            valid_results = ["valid", "void", "unfair"]
            if pred_label not in valid_results:
                raise Exception(f"Invalid value for 'result': {pred_label}. Expected: {valid_results}")

            # 5. Conditional logic validation (according to prompt)

            if pred_label == "void":
                # If 'void', 'hurt_rules' MUST be populated AND 'correction' MUST exist (and not be empty)
                if not pred_hurt_rules:
                    raise Exception(f"'result' is 'void', but 'hurt_rules' is empty. Response: {answer}")
                if not pred_correction:  # Checks for None or ""
                    raise Exception(f"'result' is 'void', but 'correction' is missing or empty. Response: {answer}")

            elif pred_label in ["valid", "unfair"]:
                # If 'valid' or 'unfair', 'hurt_rules' MUST be empty
                if pred_hurt_rules:
                    raise Exception(f"'result' is '{pred_label}', but 'hurt_rules' is not empty. Response: {answer}")
                # And 'correction' should not be present (None) or empty
                if pred_correction:  # Checks if not None and not ""
                    raise Exception(f"'result' is '{pred_label}', but 'correction' is present. Response: {answer}")

            # All checks passed
            return parsed

        except Exception as e:
            print(f"    -> Attempt {attempt + 1}: Validation error: {e}")

    print(f"  -> LLM could not produce valid JSON according to rules after {5} attempts.")
    return None