from dotenv import load_dotenv
from news import fetch_news
from writer import write_post
from poster import post_to_bluesky

# .envファイルを読み込む
load_dotenv()

def main():
    print("🚀 SNS自動投稿を開始します")
    
    print("\n📰 Step1: ニュースを収集中...")
    articles = fetch_news(topic="人工知能")
    
    print("\n✍️  Step2: 投稿文を生成中...")
    post_text = write_post(articles)
    
    print("\n📤 Step3: Xに投稿中...")
    post_to_bluesky(post_text)
    
    print("\n🎉 完了！今日の投稿が完了しました")

if __name__ == "__main__":
    main()