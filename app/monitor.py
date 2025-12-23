import httpx
import time
from .database import SessionLocal
from .models import MonitorLog
from .notifications import send_telegram_alert

# Hafıza (Bellek): Sorun durumlarını burada tutacağız
# Uygulama çalıştığı sürece bu değişkenler durumu hatırlar
alert_states = {
    "latency": False,
    "zeytin": False,
    "offline": False
}

async def perform_check():
    global alert_states
    db = SessionLocal()
    url = "https://www.7bulut.com"
    
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        try:
            response = await client.get(url, timeout=10.0)
            latency = round((time.perf_counter() - start_time) * 1000, 2)
            zeytin_present = 'id="chatLauncher"' in response.text
            
            # --- 1. YAVAŞLIK KONTROLÜ ---
            if latency > 300:
                if not alert_states["latency"]: # Daha önce uyarmadıysak
                    await send_telegram_alert(f"⏳ Yavaşlık Başladı: {latency} ms")
                    alert_states["latency"] = True
            else:
                if alert_states["latency"]: # Sorun düzelmişse
                    await send_telegram_alert(f"✅ Hız Normale Döndü: {latency} ms")
                    alert_states["latency"] = False

            # --- 2. ZEYTİN AI KONTROLÜ ---
            if not zeytin_present:
                if not alert_states["zeytin"]:
                    await send_telegram_alert("🤖 Zeytin AI Kayboldu!")
                    alert_states["zeytin"] = True
            else:
                if alert_states["zeytin"]:
                    await send_telegram_alert("✅ Zeytin AI Tekrar Aktif!")
                    alert_states["zeytin"] = False

            # Site online olduğu için offline uyarısını sıfırla
            alert_states["offline"] = False

            # Veritabanı kaydı
            new_log = MonitorLog(
                is_online=response.status_code == 200,
                response_time=latency,
                zeytin_status=zeytin_present,
                status_code=response.status_code
            )
            db.add(new_log)
            db.commit()

        except Exception as e:
            if not alert_states["offline"]:
                await send_telegram_alert(f"🚨 Site Çöktü veya Bağlantı Koptu!")
                alert_states["offline"] = True
        finally:
            db.close()