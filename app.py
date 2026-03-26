import streamlit as st
import pandas as pd
import time
import plotly.express as px
import os
from datetime import datetime
from analyzer import LogAnalyzer

st.set_page_config(page_title="SentinelLog | Cyber Security", layout="wide")

# --- AJUSTE DE RUTA ---
LOG_FILE = "access.log"

def main():
    st.title("🛡️ SentinelLog: Centro de Operaciones")
    
    # Usamos la clase de tu amigo
    analyzer = LogAnalyzer(LOG_FILE)

    # --- BLOQUE DEL REPORTE (SIDEBAR) ---
    with st.sidebar:
        st.header("📋 Auditoría Empresarial")
        if st.button("🚀 Generar Reporte Excel"):
            df_report = analyzer.load_data()
            if not df_report.empty:
                # Lógica de categorización para el reporte
                def clasificar(row):
                    path = str(row['path']).lower()
                    status = int(row['status'])
                    if status == 401:
                        return "ALTA", "Fuerza Bruta", "Bloquear IP y resetear pass"
                    if any(x in path for x in ['admin', '.env', 'config']):
                        return "CRÍTICA", "Escaneo de Rutas", "Revisar permisos de carpeta"
                    if status >= 500:
                        return "MEDIA", "Error de Aplicación", "Revisar logs internos"
                    return "BAJA", "Normal", "N/A"

                # Agregamos las columnas de inteligencia
                df_report[['Riesgo', 'Incidente', 'Recomendación']] = df_report.apply(
                    lambda r: pd.Series(clasificar(r)), axis=1
                )
                
                # Filtramos para mostrar solo lo importante en el Excel
                incidentes = df_report[df_report['Riesgo'] != "BAJO"]

                if not incidentes.empty:
                    # FIX PARA EXCEL: utf-8-sig para acentos y sep=';' para columnas
                    csv = incidentes.to_csv(index=False, sep=';', encoding='utf-8-sig')
                    
                    st.success(f"Hallazgos: {len(incidentes)}")
                    st.download_button(
                        label="📥 Descargar Reporte SOC",
                        data=csv,
                        file_name=f"Reporte_SOC_{datetime.now().strftime('%H%M')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No hay incidentes críticos.")
    # ------------------------------------

    # Contenedores para evitar duplicados
    metric_place = st.empty()
    alert_place = st.empty()
    chart_place = st.empty()
    log_place = st.empty()

    while True:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write(f"{datetime.now()}|127.0.0.1|GET|/|200|System\n")

        df = analyzer.load_data()
        
        if not df.empty:
            threats = analyzer.detect_threats(df)
            
            # 1. Alertas
            with alert_place.container():
                for ip, count in threats['brute_force'].items():
                    st.error(f"🚨 Ataque de Fuerza Bruta: {ip} ({count} intentos)")

            # 2. Métricas
            with metric_place.container():
                c1, c2, c3 = st.columns(3)
                c1.metric("Peticiones", len(df))
                c2.metric("Amenazas", len(threats['brute_force']))
                c3.metric("Rutas Críticas", len(threats['critical_paths']))

            # 3. Gráficos
            with chart_place.container():
                col_a, col_b = st.columns(2)
                fig1 = px.pie(df, names='status', title="Distribución HTTP", hole=0.4)
                col_a.plotly_chart(fig1, use_container_width=True, key=f"p_{time.time()}")
                
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df_counts = df.groupby('timestamp').size().reset_index(name='Peticiones')
                fig2 = px.line(df_counts, x='timestamp', y='Peticiones', title="Tráfico Real")
                col_b.plotly_chart(fig2, use_container_width=True, key=f"l_{time.time()}")

            # 4. Tabla
            with log_place.container():
                st.subheader("Últimos Registros")
                st.dataframe(df.tail(5), use_container_width=True)

        time.sleep(2)

if __name__ == "__main__":
    main()