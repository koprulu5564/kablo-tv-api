#!/usr/bin/env python3
# kablo_api.py - Kablo TV API M3U Oluşturucu
import requests
import json
from datetime import datetime

# API Ayarları
API_URL = "https://core-api.kablowebtv.com/api/channels"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer eyJhbGci...",  # API Token
    "Referer": "https://tvheryerde.com"
}

def main():
    try:
        # API'den veri çek
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()

        # M3U Oluştur
        m3u_content = ["#EXTM3U"]
        for channel in data.get('Data', {}).get('AllChannels', []):
            if not channel.get('StreamData', {}).get('HlsStreamUrl'):
                continue
                
            m3u_content.append(
                f'#EXTINF:-1 tvg-id="{channel["Id"]}" tvg-name="{channel["Name"]}" '
                f'tvg-logo="{channel.get("PrimaryLogoImageUrl", "")}" '
                f'group-title="{channel.get("Categories", [{}])[0].get("Name", "Genel")}",'
                f'{channel["Name"]}\n{channel["StreamData"]["HlsStreamUrl"]}'
            )

        # Dosyaya yaz
        with open("kablo_tv.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_content))
            
        print("✅ M3U oluşturuldu!")
    except Exception as e:
        print(f"❌ Hata: {e}")
        with open("error.log", "a") as f:
            f.write(f"[{datetime.now()}] {e}\n")
        raise

if __name__ == "__main__":
    main()
