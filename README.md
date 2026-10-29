🛡️📋 Panel de Errores de QA en Cumplimiento de Productos

"Cada error documentado es una oportunidad para revisar mejor la próxima vez." 🔍

## 🌐 Demo en línea

👉 **[Abrir la aplicación en Render](https://qa-interactive-thingy.onrender.com/)**

Aplicación web interactiva para analizar las evaluaciones de QA de un equipo de Amazon que revisa la documentación de productos (certificados de conformidad, reportes de pruebas, hojas de seguridad y más). Ese equipo verifica que cada producto cuente con los permisos y pruebas necesarios antes de venderse en la plataforma.

El panel convierte cientos de registros de errores en información clara y accionable. Con él puedes responder preguntas como estas:

🌍 ¿En qué países y categorías se concentran los errores?
🚨 ¿Qué tan severos son y cuánto cuestan en dinero y en horas de resolución?
🧠 ¿Cuáles son las causas raíz más frecuentes: presión de tiempo, fatiga, falta de capacitación o guías poco claras?
👥 ¿Influyen el turno o la antigüedad del revisor?
✨ Funcionalidades principales
🎛️ Filtros dinámicos por rango de fechas, país, categoría, severidad y turno.
📌 Indicadores clave (KPIs): total de errores, costo total, horas promedio de resolución y errores críticos.
👀 Vista previa opcional de los datos filtrados.
📊 Gráfico de barras configurable (conteo, suma o promedio por cualquier categoría).
🍩 Gráfico de dona o pastel con la distribución porcentual.
📈 Histograma con curva KDE, línea de promedio y color por categoría.

💡 Todos los gráficos se actualizan al instante cuando cambias un filtro. ¡Explora sin miedo!

🚀 Instalación en local

Sigue estos pasos y tendrás el panel funcionando en pocos minutos ⏱️

1️⃣ Clona el repositorio
bash
git clone https://github.com/joyvillalobos/qa_investigation_official.git
cd qa_investigation_official
2️⃣ (Recomendado) Crea y activa un entorno virtual
bash
python -m venv venv

Actívalo según tu sistema operativo:

bash
# 🪟 Windows
venv\Scripts\activate

# 🍎 macOS / 🐧 Linux
source venv/bin/activate
3️⃣ Instala las dependencias
bash
pip install -r requirements.txt
4️⃣ Verifica que los datos estén en su lugar

El archivo de datos debe estar en esta ruta:

text
panel-qa-cumplimiento/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── datos.csv
5️⃣ ¡Inicia la aplicación! 🎉
bash
streamlit run app.py

El panel se abrirá automáticamente en tu navegador en http://localhost:8501 🌐

⚠️ ¿Algo no funcionó? Revisa que tengas Python 3.9 o superior (python --version) y que el entorno virtual esté activado antes de instalar las dependencias.

🧰 Tecnologías utilizadas
Tecnología	Uso en el proyecto
🐍 Python	Lenguaje principal de la aplicación
🐼 Pandas	Carga, limpieza y filtrado de los datos
🎈 Streamlit	Interfaz web interactiva: filtros, KPIs y diseño del panel
🌊 Seaborn	Gráficos estadísticos con un estilo profesional
📐 Matplotlib	Base de los gráficos y del gráfico de dona
👤 Autor

Desarrollado con ❤️ por Mago como parte de su portafolio de ciencia de datos.

🌟 ¿Te gustó el proyecto? Dale una ⭐ al repositorio y no dudes en abrir un issue con ideas o mejoras. ¡Toda retroalimentación suma!