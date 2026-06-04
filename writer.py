import google.generativeai as genai
import os

MAX_CHARS = 280  # Blueskyの上限300に余裕を持たせる

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
- 本文は80文字以内（絵文字含む）
- URLやハッシュタグを含めた全体で必ず280文字以内に収めること（厳守）
- 読者が興味を持つ具体的な書き出し
- ハッシュタグを2個
- 絵文字を適度に使う
- 本文の後に改行してURLを1つ載せる
- URLの後に空行を1行入れてからハッシュタグを載せる
- 投稿文のみ出力する（説明文不要）

参考ニュース：
{news_text}
"""
    
    response = model.generate_content(prompt)
    post_text = response.text.strip()
    
    # 文字数オーバーの場合は強制トリミング
    if len(post_text) > MAX_CHARS:
        lines = post_text.split("\n")
        result = []
        count = 0
        for line in lines:
            if count + len(line) + 1 > MAX_CHARS:
                break
            result.append(line)
            count += len(line) + 1
        post_text = "\n".join(result).strip()
    
    print(f"✅ 投稿文を生成しました（{len(post_text)}文字）")
    print(f"---\n{post_text}\n---")
    return post_text