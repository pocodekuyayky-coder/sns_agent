import google.generativeai as genai
import os

def generate_quote():
    """名言を生成する"""
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    prompt = """
今日の海外の偉人の名言をひとつ紹介してください。
以下の順番・形式を厳守してください。

"Quote in English."

- Author Name

「日本語訳」

- 作者名（日本語）


#quoteoftheday #AuthorName

条件：
・名言は短めで印象的なもの
・ビジネス、人生、習慣、挑戦、継続、リーダーシップに関する名言を優先
・英語は自然で有名な原文を使用
・記号は「-」（半角ダッシュ）を使用
・余計な解説は不要
・" "は半角ダブルクォーテーションを使用
・名言と人名の間は1行空ける
・5回に1回以上は女性
・5回に1回は東洋人
・できるだけ知名度が高く、SNS投稿向きの名言を選ぶ
・全体を読みやすく改行する
・スマホ表示で見やすい文字量にする
・感情に刺さる言葉を優先
・堅すぎる哲学系より、直感的に伝わる名言を優先
・出力はコピペしやすいようシンプルにする
・300文字以内で収める
"""
    
    response = model.generate_content(prompt)
    quote_text = response.text.strip()
    
    print(f"✅ 名言を生成しました")
    print(f"---\n{quote_text}\n---")
    return quote_text