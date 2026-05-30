import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta

HISTORY_FILE = "quote_history.json"

def load_history():
    """過去の名言履歴を読み込む"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """名言履歴を保存する"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def clean_old_history(history):
    """30日以上古い履歴を削除する"""
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    return [h for h in history if h["date"] > thirty_days_ago]

def generate_quote():
    """名言を生成する"""
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    # 履歴を読み込む
    history = load_history()
    history = clean_old_history(history)
    
    # 過去30日の使用済み人物リスト
    used_authors = [h["author"] for h in history]
    avoid_text = ""
    if used_authors:
        avoid_text = f"・以下の人物は過去30日以内に使用済みなので必ず避けてください：{', '.join(used_authors)}"
    
    prompt = f"""
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
{avoid_text}

最後に必ず以下の形式で作者名を英語で出力してください（投稿文の後に改行して）：
AUTHOR: 作者名（英語）
"""
    
    response = model.generate_content(prompt)
    full_text = response.text.strip()
    
    # AUTHOR行を抽出して履歴に保存
    lines = full_text.split("\n")
    author_line = ""
    post_lines = []
    for line in lines:
        if line.startswith("AUTHOR:"):
            author_line = line.replace("AUTHOR:", "").strip()
        else:
            post_lines.append(line)
    
    post_text = "\n".join(post_lines).strip()
    
    # 履歴に追加
    if author_line:
        history.append({
            "author": author_line,
            "date": datetime.now().isoformat()
        })
        save_history(history)
    
    print(f"✅ 名言を生成しました（使用済み: {len(used_authors)}人）")
    print(f"---\n{post_text}\n---")
    return post_text