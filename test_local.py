import json
from openai import OpenAI

# Step 1: Client बनाउने (bracket ठीकसँग बन्द गर्नुहोस्)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Step 2: Model र messages लाई अलग variable मा राख्ने
model = "qwen2.5:7b"
# model = "gpt-4o-mini"

messages = [
    {"role": "system", "content": "You are a terse travel assistant for Nepal."},
    {"role": "user",   "content": 'Extract the name and city. Respond with JSON only.\n'
         'Text: "Ram Thapa runs a trekking shop in Pokhara."'},
]

temperature = 0

# Step 3: API call गर्ने (temperature यहाँ पास गर्नुहोस्)
resp = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature,
)

print(resp.choices[0].message.content)