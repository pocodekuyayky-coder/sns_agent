import requests
import os

def fetch_news(topic="人工知能"):
    """最新ニュースを3件取得する"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": 3,
        "language": "ja",
        "apiKey": os.getenv("NEWS_API_KEY")
    }
    
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    
    # タイトルと概要だけ抽出
    result = []
    for a in articles:
        result.append({
            "title": a["title"],
            "description": a["description"]
        })
    
    print(f"✅ ニュース{len(result)}件を取得しました")
    return result