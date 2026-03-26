import time
import random
from datetime import datetime

# IPs de prueba (algunas sospechosas)
ips = ["192.168.1.1", "185.122.45.1", "45.33.22.10", "103.21.244.2", "172.16.0.5"]
paths = ["/", "/index.html", "/login", "/admin", "/wp-admin.php", "/.env", "/api/data"]
methods = ["GET", "POST"]

print("🚀 Generador iniciado. Escribiendo en access.log...")

while True:
    with open("access.log", "a") as f:
        # Generamos una línea de log aleatoria
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = random.choice(ips)
        method = random.choice(methods)
        path = random.choice(paths)
        
        # Simulamos un ataque: si es la IP sospechosa, siempre da 401
        if ip == "185.122.45.1":
            status = 401
        else:
            status = random.choice([200, 200, 200, 404, 500])
            
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        
        log_line = f"{timestamp}|{ip}|{method}|{path}|{status}|{ua}\n"
        f.write(log_line)
        f.flush() # Importante para que Streamlit lo vea al instante
        
    time.sleep(random.uniform(0.5, 2.0)) # Escribe cada 1 o 2 segundos