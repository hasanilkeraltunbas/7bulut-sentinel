# 🛡️ 7Bulut Sentinel

**Profesyonel Website Monitoring & SSL Sertifika İzleme Sistemi**

7Bulut Sentinel, web sitelerinin 7/24 izlenmesi, performans analizi ve SSL sertifika takibi için geliştirilmiş modern bir monitoring sistemidir.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🚀 Özellikler

### 📊 **Gerçek Zamanlı İzleme**
- ⏱️ **30 saniyede bir otomatik kontrol**
- 🌐 **Site erişilebilirlik kontrolü**
- ⚡ **Yanıt süresi ölçümü (ms)**
- 🤖 **Zeytin AI Bot varlık kontrolü**
- 🔐 **SSL sertifika süre takibi**

### 📈 **Gelişmiş Analytics**
- 📊 **Saatlik ortalama performans grafikleri**
- 📉 **24 saat uptime yüzdesi**
- 🎯 **Performans kategorilendirme** (Mükemmel/İyi/Orta/Yavaş)
- 📋 **Detaylı log geçmişi**

### 🔔 **Akıllı Bildirim Sistemi**
- 📱 **Telegram entegrasyonu**
- ⚠️ **Yavaşlık uyarıları** (>300ms)
- 🚨 **Site çökme bildirimleri**
- 🤖 **Zeytin AI kaybolma/geri gelme uyarıları**
- 🔐 **SSL sertifika süre uyarıları** (30 gün / 7 gün)
- 🧠 **Tekrar uyarı önleme sistemi**

### 🎨 **Modern Dashboard**
- 🌙 **Dark mode tasarım**
- 📱 **Responsive (mobil uyumlu)**
- 🎯 **Real-time güncellemeler**
- 🔐 **Kullanıcı adı/şifre koruması**
- 🏢 **7Bulut kurumsal teması**

### 🔒 **Güvenlik**
- 🛡️ **HTTP Basic Authentication**
- 🔑 **Şifrelenmiş giriş sistemi**
- 🚫 **Yetkisiz erişim engelleme**

## 🏗️ Proje Yapısı

```
7bulut-sentinel/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI uygulaması & routing
│   ├── models.py            # SQLAlchemy veri modelleri
│   ├── database.py          # Veritabanı konfigürasyonu
│   ├── monitor.py           # İzleme motoru & kontrol sistemi
│   ├── notifications.py     # Telegram bildirim sistemi
│   └── utils.py             # SSL kontrol fonksiyonları
├── templates/
│   └── index.html           # Dashboard HTML template
├── static/
│   └── images/
│       └── 7bulutlogo-1.webp
├── tests/
│   ├── __init__.py
│   └── test_sentinel.py     # Unit testler
├── requirements.txt         # Python bağımlılıkları
├── Dockerfile              # Docker container konfigürasyonu
├── .env                    # Çevre değişkenleri (oluşturulacak)
└── README.md               # Bu dosya
```

## ⚡ Hızlı Başlangıç

### 📋 Gereksinimler

- **Python 3.11+**
- **pip** (Python paket yöneticisi)
- **Telegram Bot Token** (bildirimler için)

### 🔧 Kurulum

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd 7bulut-sentinel
```

2. **Virtual environment oluşturun:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Çevre değişkenlerini ayarlayın:**
```bash
# .env dosyası oluşturun
echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
echo "TELEGRAM_CHAT_ID=your_chat_id_here" >> .env
```

5. **Uygulamayı başlatın:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Dashboard'a erişin:**
```
http://localhost:8000
```

**Giriş Bilgileri:**
- **Kullanıcı Adı:** `admin`
- **Şifre:** `7bulut123`

## 🐳 Docker ile Çalıştırma

### Docker Build & Run
```bash
# Docker image oluştur
docker build -t 7bulut-sentinel .

# Container'ı çalıştır
docker run -d \
  --name sentinel \
  -p 8000:8000 \
  -e TELEGRAM_TOKEN=your_bot_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  7bulut-sentinel
```

### Docker Compose (Önerilen)
```yaml
version: '3.8'
services:
  sentinel:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TELEGRAM_TOKEN=your_bot_token_here
      - TELEGRAM_CHAT_ID=your_chat_id_here
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## 📱 Telegram Bot Kurulumu

### 1. Bot Oluşturma
1. Telegram'da [@BotFather](https://t.me/botfather)'a mesaj atın
2. `/newbot` komutunu gönderin
3. Bot adını ve kullanıcı adını belirleyin
4. Aldığınız **Bot Token**'ı kaydedin

### 2. Chat ID Bulma
1. Bot'unuzla konuşmaya başlayın (`/start`)
2. Bu URL'yi browser'da açın:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```
3. JSON'da `"chat":{"id":XXXXXXX}` değerini bulun

### 3. .env Dosyasını Güncelleyin
```bash
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

## 🧪 Test Etme

### Unit Testleri Çalıştırma
```bash
# Tüm testleri çalıştır
pytest

# Detaylı çıktı ile
pytest -v

# Belirli bir test
pytest tests/test_sentinel.py::test_ssl_checker_logic
```

### Manuel Test
```bash
# SSL kontrolü test et
python -c "from app.utils import get_ssl_expiry_days; print(get_ssl_expiry_days('https://google.com'))"

# Telegram bildirimi test et
python -c "import asyncio; from app.notifications import send_telegram_alert; asyncio.run(send_telegram_alert('Test mesajı'))"
```

## 📊 İzlenen Metrikler

| Metrik | Açıklama | Uyarı Eşiği |
|--------|----------|--------------|
| **Site Durumu** | HTTP erişilebilirlik | Offline olduğunda |
| **Yanıt Süresi** | Milisaniye cinsinden | >300ms (yavaşlık) |
| **Zeytin AI** | chatLauncher element varlığı | Kaybolduğunda |
| **SSL Sertifika** | Kalan gün sayısı | <30 gün (uyarı), <7 gün (kritik) |
| **Uptime** | 24 saatlik erişilebilirlik yüzdesi | - |

## 🔧 Konfigürasyon

### Monitoring Ayarları
```python
# app/monitor.py içinde değiştirilebilir
LATENCY_THRESHOLD = 300  # ms
CHECK_INTERVAL = 30      # saniye
SSL_WARNING_DAYS = 30    # gün
SSL_CRITICAL_DAYS = 7    # gün
```

### Güvenlik Ayarları
```python
# app/main.py içinde değiştirilebilir
ADMIN_USER = "admin"
ADMIN_PASS = "7bulut123"
```

## 📈 Dashboard Özellikleri

### Ana Metrikler Kartları
- 🟢 **Site Durumu**: ONLINE/OFFLINE + Uptime %
- 🔵 **Yanıt Süresi**: Mevcut + 1h/24h ortalama
- 🟣 **Zeytin AI**: AKTİF/DEVRE DIŞI + Uptime %
- 🔐 **SSL Sertifika**: Kalan gün + Durum
- 🟡 **Toplam Kontrol**: 24h kontrol sayısı + saat/kontrol

### Grafikler
- 📊 **Saatlik Yanıt Süresi**: Son 24 saatin saatlik ortalaması
- 🥧 **Durum Dağılımı**: Online/Offline yüzde dağılımı

### Kontrol Tablosu
- ⏰ **Zaman**: Her kontrolün zamanı
- 🌐 **Durum**: HTTP status code
- ⚡ **Yanıt Süresi**: Milisaniye + performans ikonu
- 🤖 **Zeytin AI**: Varlık durumu
- 🔐 **SSL**: Kalan gün sayısı
- 📊 **Performans**: Kategorik değerlendirme

## 🚨 Uyarı Sistemi

### Telegram Bildirimleri
- ⏳ **Yavaşlık Başladı**: `>300ms` yanıt süresi
- ✅ **Hız Normale Döndü**: Yavaşlık düzeldi
- 🤖 **Zeytin AI Kayboldu**: chatLauncher elementi yok
- ✅ **Zeytin AI Tekrar Aktif**: Element geri geldi
- 🚨 **Site Çöktü**: HTTP bağlantı hatası
- ⚠️ **SSL Sertifikası Yenilenmeli**: <30 gün kaldı
- 🔐 **SSL Sertifikası Sona Eriyor**: <7 gün kaldı
- ✅ **SSL Sertifikası Yenilendi**: Süre uzatıldı

### Akıllı Uyarı Önleme
- Aynı sorun için tekrar uyarı gönderilmez
- Sorun düzeldiğinde "normale döndü" bildirimi
- Hafıza tabanlı durum takibi

## 🔄 Otomatik İşlemler

### Cron Jobs
- **Her 30 saniye**: Site kontrolü ve metrik toplama
- **Her gece 03:00**: Eski log temizleme (7+ gün)

### Veri Saklama
- **SQLite veritabanı**: Tüm kontrol logları
- **Otomatik temizlik**: 7 günden eski kayıtlar silinir
- **Türkiye saati**: Tüm zaman damgaları UTC+3

## 🛠️ Geliştirme

### Yeni Özellik Ekleme
1. **Model güncellemesi**: `app/models.py`
2. **İzleme mantığı**: `app/monitor.py`
3. **Dashboard görünümü**: `templates/index.html`
4. **Test yazma**: `tests/test_sentinel.py`

### Kod Yapısı
- **MVC Pattern**: Model-View-Controller ayrımı
- **Async/Await**: Non-blocking I/O operasyonları
- **Type Hints**: Kod okunabilirliği için tip belirteçleri
- **Error Handling**: Kapsamlı hata yakalama

## 📝 Changelog

### v1.0.0 (Mevcut)
- ✅ Temel site izleme
- ✅ Yanıt süresi ölçümü
- ✅ Zeytin AI kontrolü
- ✅ SSL sertifika takibi
- ✅ Telegram bildirimleri
- ✅ Modern dashboard
- ✅ Kullanıcı authentication
- ✅ Docker desteği
- ✅ Unit testler

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Destek

### Sorun Giderme
- **Dashboard açılmıyor**: Port 8000'in kullanımda olup olmadığını kontrol edin
- **Telegram bildirimleri gelmiyor**: Bot token ve chat ID'yi kontrol edin
- **SSL kontrolü çalışmıyor**: İnternet bağlantısını ve firewall ayarlarını kontrol edin

### İletişim
- 📧 **E-posta**: [destek@7bulut.com](mailto:destek@7bulut.com)
- 🌐 **Website**: [www.7bulut.com](https://www.7bulut.com)
- 📱 **Telegram**: [@7bulut_destek](https://t.me/7bulut_destek)

---

**7Bulut Sentinel** ile web sitenizin sağlığını 7/24 takip edin! 🛡️✨

*Made with ❤️ by 7Bulut Team*
