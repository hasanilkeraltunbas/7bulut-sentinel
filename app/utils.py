import ssl
import socket
from datetime import datetime

def get_ssl_expiry_days(url):
    # URL'den 'https://' ve sonundaki '/' kısmını temizle
    hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Sertifika bitiş tarihini al
                expire_date_str = cert['notAfter']
                expire_date = datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
                
                # Kalan gün sayısını hesapla
                remaining = expire_date - datetime.utcnow()
                return max(0, remaining.days)
    except Exception as e:
        print(f"SSL Check Error for {hostname}: {e}")
        return None