*SentinelLog - Security Operations Center Dashboard*

Este proyecto consiste en una plataforma de monitoreo de seguridad en tiempo real diseñada para visualizar y analizar intentos de intrusión, escaneos de vulnerabilidades y tráfico de red sospechoso.

El sistema utiliza una arquitectura de pipeline de datos donde un motor de simulación genera registros de acceso persistentes que son procesados analíticamente para su visualización dinámica.



*Integrantes del Proyecto*
Este sistema fue desarrollado por ingenieros de software enfocados en soluciones de infraestructura y análisis de datos:

**Johan Espinoza (@JohanSolido1)**: Data & Security Specialist. Responsable del motor de generación de logs y el desarrollo de la lógica de detección de amenazas (Security Backend).

**Elias (@IddleMaster)**: Full Stack & Analytics Engineer. Responsable de la arquitectura del dashboard, la integración de flujos de datos en tiempo real y la experiencia de usuario (Data Visualization).



*Requisitos del Sistema*
Para el correcto funcionamiento de la plataforma, es necesario contar con Python 3.9 o superior. Las librerías principales utilizadas son:

Streamlit: Para la interfaz del dashboard.

Pandas: Para la manipulación y limpieza de estructuras de datos.

Plotly: Para la generación de gráficos interactivos de alta precisión.


*Instalacion*
Para instalar todas las dependencias necesarias, ejecute el siguiente comando en su terminal:
pip install -r requirements.txt

*Guia de Uso*
Para poner en marcha el ecosistema completo, se recomienda utilizar dos terminales independientes dentro del directorio raíz del proyecto.

Paso 1: Ejecutar el generador de Logs (Esto funciona a modo Tester, ya que la idea es que se utilice en un entorno Real y no ficticio, mientras se generen los Logs del programa/web en un archivo access.log el generador no será necesario, y sólo deberemos ir al Paso 2).
Este script simula el tráfico entrante al servidor y escribe de forma persistente en el archivo access.log.
python generator.py

Paso 2: Lanzar el Dashboard
Una vez que el generador esté enviando datos, inicie la interfaz de visualización con Streamlit.

streamlit run app.py


*Arquitectura y Caracteristicas*
El proyecto se divide en tres componentes modulares que permiten su escalabilidad:

1-Log Generator (generator.py): Produce entradas siguiendo el estándar de la industria (Timestamp, IP, Method, Path, Status, User-Agent).

2-Log Analyzer (analyzer.py): Clase encargada de la limpieza de datos (Data Cleaning) y la aplicación de firmas para detectar ataques de fuerza bruta y acceso a directorios sensibles.

3-Analytics Dashboard (app.py): Monitor interactivo que actualiza métricas de seguridad y gráficos temporales cada 2 segundos.


*Aplicaciones y Casos de Uso*
Este sistema puede ser adaptado para:

-Auditorías de seguridad perimetral.

-Monitoreo de APIs en entornos de desarrollo.

-Educación en ciberseguridad y análisis de patrones de ataque.