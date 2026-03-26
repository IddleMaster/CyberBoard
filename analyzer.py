import pandas as pd
import os

class LogAnalyzer:
    def __init__(self, log_file="access.log"):
        self.log_file = log_file

    def load_data(self):
        try:
            if not os.path.exists(self.log_file):
                return pd.DataFrame()
            
            # Leemos el archivo usando el separador '|'
            df = pd.read_csv(self.log_file, sep='|', 
                             names=['timestamp', 'ip', 'method', 'path', 'status', 'user_agent'],
                             on_bad_lines='skip',
                             engine='python'
                             )
            
            # Limpieza básica
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df['status'] = pd.to_numeric(df['status'], errors='coerce').fillna(0).astype(int)
            return df.dropna(subset=['timestamp']) # Eliminamos líneas mal formadas
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return pd.DataFrame()

    def detect_threats(self, df):
        if df.empty:
            return {'brute_force': {}, 'critical_paths': []}
        
        # 1. Fuerza Bruta (Más de 3 fallos 401 por IP)
        failed_attempts = df[df['status'] == 401]['ip'].value_counts()
        brute_force = failed_attempts[failed_attempts >= 3].to_dict()
        
        # 2. Rutas Críticas
        sensitive_patterns = ['/admin', '/wp-admin', '.env', '/config', '/etc/passwd']
        critical_paths = df[df['path'].str.contains('|'.join(sensitive_patterns), na=False)]['path'].unique().tolist()
        
        return {'brute_force': brute_force, 'critical_paths': critical_paths}