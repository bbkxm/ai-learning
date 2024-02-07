# import os
# os.environ["OPENAI_API_KEY"] = 'sk-888'
# from openai import OpenAI
# client = OpenAI()
# response = client.chat.completions.create(  
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a creative AI."},
#         {"role": "user", "content": "请给我的花店起个名"},
#     ],
#   temperature=0.8,
#   max_tokens=60
# )
# print(response.choices[0].message.content)

# import os
# os.environ["OPENAI_API_KEY"] = 'sk-888'
# from langchain_openai import ChatOpenAI
# chat = ChatOpenAI(model="gpt-3.5-turbo",
#                     temperature=0.8,
#                     max_tokens=60)
# from langchain.schema import (
#     HumanMessage,
#     SystemMessage
# )
# messages = [
#     SystemMessage(content="You are a creative AI."),
#     HumanMessage(content="请给我的花店起个名")
# ]
# response = chat(messages)
# print(response)

# import os
# # 设置网络代理
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"


import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'
from langchain import HuggingFaceHub
llm = HuggingFaceHub(repo_id="bigscience/bloom-1b7")
resp = llm.predict("请给我的花店起个名")
print(resp)