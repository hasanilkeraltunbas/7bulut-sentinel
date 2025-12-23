import httpx
import time
from .database import SessionLocal
from .models import MonitorLog
from .notifications import send_telegram_alert
from .utils import get_ssl_expiry_days

# Hafıza (Bellek): Sorun durumlarını burada tutacağız
# Uygulama çalıştığı sürece bu değişkenler durumu hatırlar
alert_states = {
    "latency": False,
    "zeytin": False,
    "offline": False,
    "ssl": False  # SSL uyarısı için yeni state
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
            
            # --- SSL KONTROLÜ ---
            ssl_days = get_ssl_expiry_days(url)
            
            # SSL uyarıları
            if ssl_days is not None:
                if ssl_days <= 7:  # 7 gün veya daha az kaldıysa
                    if not alert_states["ssl"]:
                        await send_telegram_alert(f"🔐 SSL Sertifikası Sona Eriyor: {ssl_days} gün kaldı!")
                        alert_states["ssl"] = True
                elif ssl_days <= 30:  # 30 gün veya daha az kaldıysa (sadece bir kez uyar)
                    if not alert_states["ssl"]:
                        await send_telegram_alert(f"⚠️ SSL Sertifikası Yenilenmeli: {ssl_days} gün kaldı")
                        alert_states["ssl"] = True
                else:
                    # SSL durumu normale döndüyse (yenilendiyse)
                    if alert_states["ssl"]:
                        await send_telegram_alert(f"✅ SSL Sertifikası Yenilendi: {ssl_days} gün geçerli")
                        alert_states["ssl"] = False
            
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

            # Veritabanı kaydı (SSL bilgisi dahil)
            new_log = MonitorLog(
                is_online=response.status_code == 200,
                response_time=latency,
                zeytin_status=zeytin_present,
                status_code=response.status_code,
                ssl_days=ssl_days  # SSL bilgisini kaydet
            )
            db.add(new_log)
            db.commit()

        except Exception as e:
            # Hata durumunda SSL bilgisi olmadan kaydet
            if not alert_states["offline"]:
                await send_telegram_alert(f"🚨 Site Çöktü veya Bağlantı Koptu!")
                alert_states["offline"] = True
            
            # Hata durumunda da log kaydet
            error_log = MonitorLog(
                is_online=False,
                response_time=0,
                zeytin_status=False,
                status_code=0,
                ssl_days=None
            )
            db.add(error_log)
            db.commit()
            
        finally:
            db.close()