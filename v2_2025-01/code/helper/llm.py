from openai import OpenAI
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from pydantic import BaseModel, ValidationError
import anthropic
import time
import json
import re

openai_client = OpenAI(api_key='')
deepseek_client = OpenAI(api_key="", base_url="https://api.deepseek.com")
grok_client = OpenAI(api_key="",base_url="https://api.x.ai/v1")
anthropic_client = anthropic.Anthropic(api_key="")
genai.configure(api_key="")

# model = "gpt-4o-2024-11-20"
# model = "gpt-4o-mini-2024-07-18"
# model = "gemini-exp-1206"
# model = "gemini-1.5-pro-002"
model = "deepseek-chat"
# model = "grok-2-1212"
# model = "claude-3-5-sonnet-20241022"
# model = "deepseek-reasoner"

def getAnswer(system_message, user_message, with_rules):
    # print("----------------------------------------------------")
    # print(system_message)
    # print(user_message)
    waiting_time = 5
    while True:
        try:
            if model.startswith("gpt"):
                response = openai_client.beta.chat.completions.parse(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    seed=1000,
                    response_format=SchemaRules if with_rules else Schema,
                )
                return json.loads(response.choices[0].message.content)

            if model.startswith("grok"):
                response = grok_client.beta.chat.completions.parse(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    seed=1000,
                    response_format=SchemaRules if with_rules else Schema,
                )
                return json.loads(response.choices[0].message.content)

            if model.startswith("claude"):
                response = anthropic_client.messages.create(
                    model=model,
                    max_tokens=8192,
                    system=system_message,
                    messages=[
                        {"role": "user", "content": user_message},
                    ]
                )
                match = re.search(r"\{.*\}", response.content[0].text, re.DOTALL)
                if match:
                    json_string = match.group(0)
                    json_object = json.loads(json_string)
                else:
                    raise ValueError(f"Contains no json")
                validate_json(json_object, SchemaRules if with_rules else Schema)
                return json_object

            elif model.startswith("deepseek"):
                response = deepseek_client.beta.chat.completions.parse(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    seed=1000,
                    # response_format=SchemaRules if with_rules else Schema,
                )
                parsed = json.loads(response.choices[0].message.content[7:-3])
                validate_json(parsed, SchemaRules if with_rules else Schema)
                return parsed

            elif model.startswith("gemini"):
                gemini = genai.GenerativeModel(
                    model_name=model,
                    generation_config={
                        "response_schema": google_schema_rules if with_rules else google_schema,
                        "response_mime_type": "application/json",
                    },
                    system_instruction=system_message,
                )
                chat_session = gemini.start_chat(
                    history=[]
                )
                response = chat_session.send_message(user_message)
                return json.loads(response.text)
        except Exception as e:
            print(f"LLM Request failed: {e}. Retrying in {waiting_time} seconds...")
            time.sleep(waiting_time)
            #waiting_time += 5


def validate_json(json_obj, schema_class):
    try:
        schema_class(**json_obj)
    except ValidationError as e:
        raise ValueError(f"JSON does not match the schema.")


class Schema(BaseModel):
    explanation: str
    result: str


class SchemaRules(BaseModel):
    explanation: str
    result: str
    hurt_rules: list[int]


google_schema = content.Schema(
    type=content.Type.OBJECT,
    enum=[],
    required=["explanation", "result"],
    properties={
        "explanation": content.Schema(
            type=content.Type.STRING,
        ),
        "result": content.Schema(
            type=content.Type.STRING,
        ),
    },
)

google_schema_rules = content.Schema(
    type=content.Type.OBJECT,
    enum=[],
    required=["explanation", "result", "hurt_rules"],
    properties={
        "explanation": content.Schema(
            type=content.Type.STRING,
        ),
        "result": content.Schema(
            type=content.Type.STRING,
        ),
        "hurt_rules": content.Schema(
            type=content.Type.ARRAY,
            items=content.Schema(
                type=content.Type.INTEGER,
            ),
        ),
    },
)
