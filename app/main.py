from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import engine, Base, get_db, SessionLocal
from .models import MonitorLog
from .monitor import perform_check
import aiocron
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(title="7Bulut Sentinel")

# Static files ve templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- GÜVENLİK AYARLARI ---
security = HTTPBasic()
ADMIN_USER = "admin"
ADMIN_PASS = "7bulut123"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hatalı kullanıcı adı veya şifre",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- BAŞLANGIÇ İŞLEMLERİ ---
@app.on_event("startup")
async def startup_event():
    print("🚀 7Bulut Sentinel başlatılıyor...")
    
    # Her 30 saniyede bir monitoring
    @aiocron.crontab('*/30 * * * * *') 
    async def periodic_check():
        await perform_check()
    
    # Her gece saat 03:00'te eski kayıtları temizle
    @aiocron.crontab('0 3 * * *') 
    async def cleanup_old_logs():
        db = SessionLocal()
        try:
            # 7 gün öncesini hesapla
            threshold = datetime.now(timezone.utc) - timedelta(days=7)
            
            # Eski kayıtları sil
            deleted_count = db.query(MonitorLog).filter(
                MonitorLog.timestamp < threshold
            ).delete()
            db.commit()
            
            if deleted_count > 0:
                print(f"🧹 Temizlik: {deleted_count} eski kayıt silindi (7+ gün öncesi)")
                
        except Exception as e:
            print(f"❌ Temizlik hatası: {e}")
            db.rollback()
        finally:
            db.close()
    
    print("✅ Monitoring sistemi aktif!")

# --- YARDIMCI FONKSİYONLAR ---
def safe_float(value, default=0.0):
    """Güvenli float dönüşümü"""
    if value is None:
        return default
    if isinstance(value, Decimal):
        return float(value)
    return float(value)

def calculate_stats(db: Session):
    """İstatistikleri hesapla"""
    TR_TIME = timezone(timedelta(hours=3))
    try:
        now = datetime.now(TR_TIME)
        # Veritabanındaki UTC zamanlarıyla uyumlu olması için UTC kullanıyoruz
        now_utc = datetime.now(timezone.utc)
        
        last_24h = now_utc - timedelta(hours=24)
        last_1h = now_utc - timedelta(hours=1)
        
        # 24 Saatlik Ortalama Yanıt Süresi
        avg_24h_raw = db.query(func.avg(MonitorLog.response_time)).filter(
            MonitorLog.timestamp >= last_24h,
            MonitorLog.is_online == True
        ).scalar()
        avg_24h = round(safe_float(avg_24h_raw), 2)
        
        # 1 Saatlik Ortalama Yanıt Süresi
        avg_1h_raw = db.query(func.avg(MonitorLog.response_time)).filter(
            MonitorLog.timestamp >= last_1h,
            MonitorLog.is_online == True
        ).scalar()
        avg_1h = round(safe_float(avg_1h_raw), 2)
        
        # Uptime (Erişilebilirlik)
        total_checks_24h = db.query(MonitorLog).filter(
            MonitorLog.timestamp >= last_24h
        ).count()
        
        online_checks_24h = db.query(MonitorLog).filter(
            MonitorLog.timestamp >= last_24h,
            MonitorLog.is_online == True
        ).count()
        
        uptime_percentage = round((online_checks_24h / total_checks_24h * 100), 2) if total_checks_24h > 0 else 0
        
        # Zeytin AI Uptime
        zeytin_online_24h = db.query(MonitorLog).filter(
            MonitorLog.timestamp >= last_24h,
            MonitorLog.zeytin_status == True
        ).count()
        
        zeytin_uptime = round((zeytin_online_24h / total_checks_24h * 100), 2) if total_checks_24h > 0 else 0
        
        # Saatlik Grafik Verileri
        hourly_data = []
        for i in range(24):
            hour_start = now_utc - timedelta(hours=i+1)
            hour_end = now_utc - timedelta(hours=i)
            
            hour_avg_raw = db.query(func.avg(MonitorLog.response_time)).filter(
                MonitorLog.timestamp >= hour_start,
                MonitorLog.timestamp < hour_end,
                MonitorLog.is_online == True
            ).scalar()
            
            hour_avg = round(safe_float(hour_avg_raw), 2)
            
            # Grafikte Türkiye saatiyle göstermek için +3 ekliyoruz
            display_hour = (now + timedelta(hours=-i)).strftime('%H:00')
            
            hourly_data.append({
                'hour': display_hour,
                'avg_response': hour_avg
            })
        
        return {
            'avg_24h': avg_24h,
            'avg_1h': avg_1h,
            'uptime_percentage': uptime_percentage,
            'zeytin_uptime': zeytin_uptime,
            'total_checks_24h': total_checks_24h,
            'hourly_data': list(reversed(hourly_data))
        }
        
    except Exception as e:
        print(f"Stats calculation error: {e}")
        return {
            'avg_24h': 0.0,
            'avg_1h': 0.0,
            'uptime_percentage': 0.0,
            'zeytin_uptime': 0.0,
            'total_checks_24h': 0,
            'hourly_data': []
        }

# --- DASHBOARD ROTASI ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    try:
        # En son kayıt
        last_log = db.query(MonitorLog).order_by(MonitorLog.id.desc()).first()
        
        # --- KRİTİK KISIM: LİMİT ---
        # Sayfanın uzamasını engellemek için sadece son 50 kaydı çekiyoruz.
        history = db.query(MonitorLog).order_by(MonitorLog.id.desc()).limit(50).all()
        
        # İstatistikler
        stats = calculate_stats(db)
        
        # Eğer hiç log yoksa fake data oluştur
        if not last_log:
            class FakeLog:
                def __init__(self):
                    self.is_online = False
                    self.response_time = 0
                    self.zeytin_status = False
                    self.timestamp = datetime.now(timezone.utc)
                    self.status_code = 0
                    self.ssl_days = 0
            
            last_log = FakeLog()
            
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "data": last_log,
            "history": history,
            "stats": stats,
            "user": user 
        })
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "data": None,
            "history": [],
            "stats": None,
            "user": user
        })