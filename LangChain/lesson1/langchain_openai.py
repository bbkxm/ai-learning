import os
os.environ["OPENAI_API_KEY"] = 'sk-hsrQTEa5m0Iiy3y8F4Ed6cD45d0b4fBd9d815883CdF7394a'
os.environ["OPENAI_BASE_URL"] = 'https://freeapi.iil.im'
from langchain_openai import ChatOpenAI
chat = ChatOpenAI(model="gpt-3.5-turbo",
                    temperature=0.8,
                    max_tokens=60)
from langchain.schema import (
    HumanMessage,
    SystemMessage
)
messages = [
    SystemMessage(content="You are a creative AI."),
    HumanMessage(content="请给我的花店起个名")
]
response = chat(messages)
print(response)