from helper import llm, extract_json


def get_judge_json_response(system_prompt, user_prompt):
    for attempt in range(5):
        try:
            answer = llm.getAnswer("gemini-2.5-pro", system_prompt, user_prompt)
            parsed = extract_json.extract_json(answer)

            # 2. Validation of mandatory keys
            required_keys = ["explanation", "missed_problems", "unnecessary_changes"]
            missing_keys = [key for key in required_keys if key not in parsed]
            if missing_keys:
                raise Exception(f"Missing mandatory keys: {missing_keys}. Response: {answer}")

            # 3. Type validation of fields
            explanation = parsed["explanation"]
            missed_problems = parsed["missed_problems"]
            unnecessary_changes = parsed["unnecessary_changes"]

            if not isinstance(explanation, str):
                raise Exception(f"Invalid type for 'explanation' (expected: str). Response: {answer}")
            if not isinstance(missed_problems, int):
                raise Exception(f"Invalid type for 'missed_problems' (expected: int). Response: {answer}")
            if not isinstance(unnecessary_changes, int):
                raise Exception(f"Invalid type for 'unnecessary_changes' (expected: int). Response: {answer}")

            return parsed

        except Exception as e:
            print(f"    -> Attempt {attempt + 1}: Validation error: {e}")

    print(f"  -> LLM could not produce valid JSON according to rules after {5} attempts.")
    return None