import google.generativeai as genai
import os

def write_post(articles):
    """ニュースをもとにX投稿文を生成する"""
    
    # Geminiの設定
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    # ニュース一覧をテキスト化
    news_text = "\n".join([
        f"・{a['title']}"
        for a in articles
    ])
    
    # プロンプト（AIへの指示）
    prompt = f"""
以下のニュースの中から最も興味深いものを1つ選び、
X(Twitter)の投稿文を作成してください。

条件：
- 日本語で200文字以内（厳守）
- 読者が思わず読みたくなる書き出し
- 最後に関連ハッシュタグを2〜3個
- 絵文字を適度に使う

ニュース一覧：
{news_text}
"""
    
    response = model.generate_content(prompt)
    post_text = response.text
    
    print(f"✅ 投稿文を生成しました")
    print(f"---\n{post_text}\n---")
    return post_text