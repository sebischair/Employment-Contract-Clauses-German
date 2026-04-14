from openai import OpenAI
from google import genai
from google.genai import types
import anthropic
import time

openai_client = OpenAI(api_key="")
deepseek_client = OpenAI(api_key="", base_url="https://api.deepseek.com")
anthropic_client = anthropic.Anthropic(api_key="")
gemini_client = genai.Client(api_key="")

def getAnswer(model, system_message, user_message):
    waiting_time = 5
    while True:
        try:
            if model.startswith("gpt"):
                response = openai_client.responses.create(
                    model=model,
                    input=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    store=False,
                    reasoning={
                        "effort": "medium"
                    }
                )
                return response.output_text

            if model.startswith("claude"):
                response = anthropic_client.messages.create(
                    model=model,
                    max_tokens=8192,
                    system=system_message,
                    messages=[
                        {"role": "user", "content": user_message},
                    ]
                )
                return response.content[0].text

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
                return response.choices[0].message.content

            elif model.startswith("gemini"):
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=user_message),
                        ],
                    ),
                ]

                generate_content_config = types.GenerateContentConfig(
                    #thinking_config=types.ThinkingConfig(
                    #    thinking_budget=0,
                    #),
                    system_instruction=[
                        types.Part.from_text(text=system_message),
                    ],
                )

                response = gemini_client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=generate_content_config,
                )
                return response.text
        except Exception as e:
            print(f"LLM Request failed: {e}. Retrying in {waiting_time} seconds...")
            time.sleep(waiting_time)
            #waiting_time += 5
