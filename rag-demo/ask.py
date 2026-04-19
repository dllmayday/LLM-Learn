import requests

res = requests.get(
    "http://127.0.0.1:8000/ask",
    params={"q": "What did Lincoln say about the Union?"}
)

print("状态码:", res.status_code)
print("返回内容:", res.text)   # ⭐关键