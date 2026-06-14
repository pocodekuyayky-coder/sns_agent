import google.generativeai as genai
import os
import json
import time
from pathlib import Path

HISTORY_FILE = "quote_history.json"
MAX_HISTORY = 30

def load_history():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def extract_author(text):
    """投稿テキストから著者名を抽出する"""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- ") and not line.startswith("- 作者") and not line.startswith("- ス") and not line.startswith("- 「"):
            candidate = line[2:].strip()
            if candidate and not any('\u3000' <= c <= '\u9fff' for c in candidate):
                return candidate
    return "Unknown"

def generate_quote():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    history = load_history()
    recent_authors = [item["author"] for item in history[-30:] if "author" in item and item["author"] != "Unknown"]

    author = "Unknown"
    quote_text = ""

    for attempt in range(3):
        exclude_note = ""
        if recent_authors:
            exclude_note = f"\n\n【絶対禁止】以下の著者は使用禁止です：{', '.join(recent_authors)}\n必ず別の著者を選んでください。Steve Jobs、Winston Churchill、Nelson Mandela、Eleanor Rooseveltなどの頻出人物は避け、あまり知られていない偉人や現代の著名人も積極的に選んでください。"

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
"""

        response = model.generate_content(prompt)
        quote_text = response.text.strip()
        author = extract_author(quote_text)

        print(f"試行{attempt + 1}: 著者={author}")

        if author in recent_authors:
            print(f"⚠️ {author} は履歴にあるため再生成します")
            recent_authors.append(author)
            time.sleep(10)
            continue

        break

    history.append({"author": author, "text": quote_text[:50]})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    save_history(history)

    print(f"✅ 名言を生成しました（著者: {author}）")
    print(f"---\n{quote_text}\n---")
    return quote_text