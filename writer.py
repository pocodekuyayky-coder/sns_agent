import google.generativeai as genai
import os

def write_post(articles):
    """ニュースをもとにBluesky投稿文を生成する"""
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    if articles:
        news_text = "\n".join([
            f"・タイトル: {a['title']}\n  URL: {a['url']}"
            for a in articles
        ])
    else:
        news_text = "本日の注目AIトピックについて自由に投稿してください"
    
    prompt = f"""
あなたはAI・テクノロジー専門のSNSライターです。
以下のニュースを参考にBluesky投稿文を日本語で作成してください。

条件：
- 150文字以内（URLを含めるので短めに）
- 読者が興味を持つ具体的な書き出し
- ハッシュタグを2個
- 絵文字を適度に使う
- 投稿文のみ出力する
- 最後にニュースのURLを1つ載せる

参考ニュース：
{news_text}
"""
    
    response = model.generate_content(prompt)
    post_text = response.text.strip()
    
    print(f"✅ 投稿文を生成しました")
    print(f"---\n{post_text}\n---")
    return post_text