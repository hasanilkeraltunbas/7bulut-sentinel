# 🛡️ 7Bulut Sentinel

**Professional Website Monitoring & SSL Certificate Tracking System**

7Bulut Sentinel is a modern monitoring system developed for 24/7 website tracking, performance analysis, and SSL certificate management. It ensures high availability and reliability for your web services.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🚀 Features

### 📊 **Real-Time Monitoring**
- ⏱️ **Automatic checks every 30 seconds**
- 🌐 **Site availability check**
- ⚡ **Response time measurement (ms)**
- 🤖 **Zeytin AI Bot presence verification**
- 🔐 **SSL certificate expiration tracking**

### 📈 **Advanced Analytics**
- 📊 **Hourly average performance charts**
- 📉 **24-hour uptime percentage**
- 🎯 **Performance categorization** (Excellent/Good/Fair/Slow)
- 📋 **Detailed log history**

### 🔔 **Smart Notification System**
- 📱 **Telegram integration for instant alerts**
- ⚠️ **Latency alerts (>300ms)**
- 🚨 **Site crash/downtime notifications**
- 🤖 **Zeytin AI loss/recovery alerts**
- 🔐 **SSL expiration warnings (30 days / 7 days)**
- 🧠 **Duplicate alert prevention system**

### 🎨 **Modern Dashboard**
- 🌙 **Dark mode design**
- 📱 **Responsive (mobile-friendly)**
- 🎯 **Real-time updates**
- 🔐 **Username/Password protection**
- 🏢 **7Bulut corporate theme**

### 🔒 **Security**
- 🛡️ **HTTP Basic Authentication**
- 🔑 **Encrypted login system**
- 🚫 **Unauthorized access prevention**

## 🏗️ Project Structure

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

## ⚡ Quick Start

### 📋 Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Telegram Bot Token** (for notifications)

### 🔧 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd 7bulut-sentinel
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# .env dosyası oluşturun
echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
echo "TELEGRAM_CHAT_ID=your_chat_id_here" >> .env
```

5. **Start the application:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the Dashboard:**
```
http://localhost:8000
```

**Login Credentials:**
- **Username:** `admin`
- **Password:** `7bulut123`

## 🐳 Running with Docker

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

## 📱 Telegram & Security Configuration

This project uses **Environment Variables to manage sensitive data (Tokens, Passwords).**

### 1. Creating a Bot
1. Message @BotFather on Telegram.
2. Send the `/newbot` command and follow the steps.
3. Save the **HTTP API Token** provided to you.

### 2. Finding Chat ID
1. Start a chat with your created bot (`/start`).
2. Go to this URL in your browser: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
3. Find the ID number in the JSON output: `"chat":{"id":123456789}.`

### 3. Defining Variables

⚠️ **IMPORTANT: Never upload your .env file or tokens to GitHub!**

#### A. Local Development
Create a .env file in the project root directory and enter your details:

```bash
# .env dosyası örneği
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789

## 🧪 Test Etme

🧪 **Testing**

### Unit Testleri Çalıştırma
```bash
# Tüm testleri çalıştır
pytest

# Detaylı çıktı ile
pytest -v

# Belirli bir test
pytest tests/test_sentinel.py::test_ssl_checker_logic
```

### Manual Test
```bash
# SSL kontrolü test et
python -c "from app.utils import get_ssl_expiry_days; print(get_ssl_expiry_days('https://google.com'))"

# Telegram bildirimi test et
python -c "import asyncio; from app.notifications import send_telegram_alert; asyncio.run(send_telegram_alert('Test mesajı'))"
```

## 📊 Monitored Metrics

| Metric | Description | Alert Threshold |
|--------|----------|--------------|
| **Site Status** | HTTP availability | When Offline |
| **Response Time** | In milliseconds | >300ms (Slow) |
| **Zeytin AI** | chatLauncher element presence | When missing |
| **SSL Certificate** | Days remaining | <30 days (Warning), <7 days (Critical) |
| **Uptime** | 24-hour availability percentage | - |

## 🔧 Configuration

### Monitoring Settings
```python
# app/monitor.py içinde değiştirilebilir
LATENCY_THRESHOLD = 300  # ms
CHECK_INTERVAL = 30      # saniye
SSL_WARNING_DAYS = 30    # gün
SSL_CRITICAL_DAYS = 7    # gün
```

### Security Settings
```python
# app/main.py içinde değiştirilebilir
ADMIN_USER = "admin"
ADMIN_PASS = "7bulut123"
```

## 📈 Dashboard Features

### Main Metric Cards
- 🟢 **Site Status**: ONLINE/OFFLINE + Uptime %
- 🔵 **Response Time**: Current + 1h/24h average
- 🟣 **Zeytin AI**: ACTIVE/INACTIVE + Uptime %
- 🔐 **SSL Certificate**: Days remaining + Status
- 🟡 **Total Checks**: 24h check count + checks/hour

### Charts
- 📊 **Hourly Response Time**: Hourly average of the last 24 hours
- 🥧 **Status Distribution**: Online/Offline percentage distribution

### Control Table
- ⏰ **Time**: Timestamp of each check
- 🌐 **Status**: HTTP status code
- ⚡ **Response**: Milliseconds + performance icon
- 🤖 **Zeytin AI**: Presence status
- 🔐 **SSL**: Days remaining
- 📊 **Performance**: Categorical evaluation

## 🚨 Alert System

### Telegram Notifications
- ⏳ **Slowness Started**: `>300ms` response time
- ✅ **Speed Returned to Normal**: Slowness resolved
- 🤖 **Zeytin AI Lost**: chatLauncher element missing
- ✅ **Zeytin AI Active Again**: Element reappeared
- 🚨 **Site Crashed**: HTTP connection error
- ⚠️ **SSL Renewal Needed**: <30 days remaining
- 🔐 **SSL Expiring Soon**: <7 days remaining
- ✅ **SSL Renewed**: Expiration date extended

### Smart Alert Prevention
- No duplicate alerts for the same ongoing issue.
- "Returned to normal" notification when the issue is resolved.
- Memory-based state tracking.

## 🔄 Automatic Operations

### Cron Jobs
- **Every 30 seconds**: Site check and metric collection.
- **Every night at 03:00**: Old log cleanup (7+ days).

### Data Retention
- **SQLite database**: Stores all check logs.
- **Auto-cleanup**: Deletes records older than 7 days.
- **Timezone**: All timestamps are UTC+3 (Turkey Time).

## 🛠️ Development

### Adding New Features
1. **Model update**: `app/models.py`
2. **Monitoring logic**: `app/monitor.py`
3. **Dashboard view**: `templates/index.html`
4. **Writing tests**: `tests/test_sentinel.py`

### Code Structure
- **MVC Pattern**: Model-View-Controller separation
- **Async/Await**: Non-blocking I/O operations
- **Type Hints**: Type indicators for code readability
- **Error Handling**: Comprehensive error catching

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Basic site monitoring
- ✅ Response time measurement
- ✅ Zeytin AI check
- ✅ SSL certificate tracking
- ✅ Telegram notifications
- ✅ Modern dashboard
- ✅ User authentication
- ✅ Docker support
- ✅ Unit tests

## 🤝 Contributing

1. Fork the repository
2. Create a Feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 Licence

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🆘 Support

### Troubleshooting
- **Dashboard not opening**: Check if port 8000 is in use.
- **Telegram notifications not arriving**: Check Bot token and Chat ID.
- **SSL check not working**: Check internet connection and firewall settings.

### Contact
- 📧 **Email**: [info@7bulut.com](mailto:info@7bulut.com)
- 🌐 **Website**: [www.7bulut.com](https://www.7bulut.com)

---

**7Bulut Sentinel** Keeping your services healthy 24/7! 🛡️✨

*Made with ❤️ by 7Bulut Team*
