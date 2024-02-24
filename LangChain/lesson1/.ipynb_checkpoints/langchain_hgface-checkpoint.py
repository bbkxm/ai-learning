# import os
# 设置网络代理
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = 'hf_888'
from langchain import HuggingFaceHub
llm = HuggingFaceHub(repo_id="bigscience/bloom-1b7")
resp = llm.predict("请给我的花店起个名")
print(resp)
