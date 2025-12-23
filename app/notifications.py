import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def send_telegram_alert(message: str):
    # DOĞRU KULLANIM: Environment variable adları
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Hata kontrolü ekle
    if not token or not chat_id:
        print("❌ Telegram token veya chat_id bulunamadı!")
        return
    
    print(f"📡 Telegram'a mesaj gönderiliyor: {message}")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        # Telegram'a mesajı gönder
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={
                "chat_id": chat_id, 
                "text": message
            })
            
            if response.status_code == 200:
                print("✅ Telegram mesajı başarıyla gönderildi!")
            else:
                print(f"❌ Telegram hatası: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")