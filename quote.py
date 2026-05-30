import google.generativeai as genai
import os
import json
from pathlib import Path

HISTORY_FILE = "quote_history.json"
MAX_HISTORY = 100  # 保持する履歴の最大件数

def load_history():
    """過去の名言履歴を読み込む"""
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """名言履歴を保存する"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_quote():
    """名言を生成する（重複防止付き）"""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    history = load_history()
    
    # 最近の著者リストを作成（プロンプトに渡す）
    recent_authors = []
    for item in history[-20:]:  # 直近20件の著者を除外
        if "author" in item:
            recent_authors.append(item["author"])
    
    exclude_note = ""
    if recent_authors:
        exclude_note = f"\n・以下の人物は最近使用済みなので避けてください: {', '.join(recent_authors)}"

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
・300文字以内で収める{exclude_note}

最後に必ず以下の形式でJSONを1行だけ出力してください（本文の後に追加）:
AUTHOR_JSON:{{"author": "英語著者名"}}
"""

    response = model.generate_content(prompt)
    full_text = response.text.strip()
    
    # AUTHOR_JSONを抽出して本文から除去
    author = "Unknown"
    lines = full_text.split("\n")
    quote_lines = []
    for line in lines:
        if line.startswith("AUTHOR_JSON:"):
            try:
                json_str = line.replace("AUTHOR_JSON:", "").strip()
                author_data = json.loads(json_str)
                author = author_data.get("author", "Unknown")
            except:
                pass
        else:
            quote_lines.append(line)
    
    quote_text = "\n".join(quote_lines).strip()
    
    # 履歴に追加して保存
    history.append({"author": author, "text": quote_text[:50]})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    save_history(history)

    print(f"✅ 名言を生成しました（著者: {author}）")
    print(f"---\n{quote_text}\n---")
    return quote_text