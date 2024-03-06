import os
os.environ["OPENAI_API_KEY"] = 'sk-88'
os.environ["OPENAI_BASE_URL"] = 'https://daily.w-l-h.xyz/v1'
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(  
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a creative AI."},
        {"role": "user", "content": "请给我的花店起个名"},
    ],
  temperature=0.8,
  max_tokens=60
)
print(response.choices[0].message.content)
