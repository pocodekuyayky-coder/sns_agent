import os
from atproto import Client

def post_to_bluesky(text):
    """Blueskyに投稿する"""
    
    client = Client()
    client.login(
        os.getenv("BLUESKY_EMAIL"),
        os.getenv("BLUESKY_PASSWORD")
    )
    
    client.send_post(text=text)
    print("✅ Blueskyへの投稿が完了しました！")