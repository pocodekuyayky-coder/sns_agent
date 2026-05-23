import tweepy
import os

def post_to_twitter(text):
    """X(Twitter)に投稿する"""
    
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
    )
    
    client.create_tweet(text=text)
    print("✅ Xへの投稿が完了しました！")