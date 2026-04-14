import json

def extract_json(s):
    pos = 0  # Current position in the string

    while pos < len(s):
        # Find the next opening curly brace
        start_index = s.find('{', pos)

        # If no opening brace is found, no JSON object exists
        if start_index == -1:
            raise ValueError("No JSON object found")

        counter = 1  # Counter for matching braces
        end_index = start_index + 1  # Position after opening brace

        # Find the matching closing brace
        while end_index < len(s) and counter > 0:
            if s[end_index] == '{':
                counter += 1  # Increment for nested opening brace
            elif s[end_index] == '}':
                counter -= 1  # Decrement for closing brace
            end_index += 1

        # If we found a matching closing brace (counter reached 0)
        if counter == 0:
            # Extract the potential JSON string
            json_str = s[start_index:end_index]
            try:
                # Attempt to parse the extracted string as JSON
                return json.loads(json_str)  # Return the parsed object if successful
            except json.JSONDecodeError:
                # If parsing fails, continue searching from next position
                pos = start_index + 1
        else:
            # If no matching brace found, move to next position
            pos = start_index + 1

    # If we exit the loop without finding a valid JSON object
    raise ValueError("No valid JSON object found")