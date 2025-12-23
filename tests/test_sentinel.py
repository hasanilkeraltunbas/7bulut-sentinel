import pytest
from app.utils import get_ssl_expiry_days
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. SSL Fonksiyon Testi: Gerçekten gün sayısı döndürüyor mu?
def test_ssl_checker_logic():
    days = get_ssl_expiry_days("https://google.com")
    assert days is not None
    assert isinstance(days, int)
    assert days > 0

# 2. Güvenlik (Auth) Testi: Şifresiz girişi engelliyor mu?
def test_dashboard_unauthorized():
    response = client.get("/")
    assert response.status_code == 401  # Giriş izni yok demektir

# 3. Güvenlik (Auth) Testi: Doğru şifreyle giriyor mu?
def test_dashboard_authorized():
    # 'admin:7bulut123' bilgilerini header olarak gönderiyoruz
    from base64 import b64encode
    auth_bytes = b64encode(b"admin:7bulut123").decode("ascii")
    
    response = client.get("/", headers={"Authorization": f"Basic {auth_bytes}"})
    assert response.status_code == 200 # Giriş başarılı