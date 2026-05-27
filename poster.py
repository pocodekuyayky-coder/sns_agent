import os
from atproto import Client, models

def post_to_bluesky(text):
    """Blueskyに投稿する"""
    
    client = Client()
    client.login(
        os.getenv("BLUESKY_EMAIL"),
        os.getenv("BLUESKY_PASSWORD")
    )
    
    # URLを検出してリンクとして設定
    import re
    facets = []
    url_pattern = re.compile(r'https?://[^\s]+')
    
    for match in url_pattern.finditer(text):
        url = match.group()
        start = match.start()
        end = match.end()
        
        # バイト位置に変換
        byte_start = len(text[:start].encode('utf-8'))
        byte_end = len(text[:end].encode('utf-8'))
        
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=url)],
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byte_start=byte_start,
                    byte_end=byte_end
                )
            )
        )
    
    client.send_post(text=text, facets=facets if facets else None)
    print("✅ Blueskyへの投稿が完了しました！")