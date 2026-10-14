"""
🛡️ Panel de Errores de Revisión de Cumplimiento
App de Streamlit + Seaborn para explorar el archivo data/datos.csv

Cómo ejecutarla:
    pip install streamlit pandas seaborn matplotlib
    streamlit run app.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# ------------------------------------------------------------------
# 0. Configuración general de la página y del estilo de los gráficos
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Panel de Errores de Cumplimiento",
    page_icon="🛡️",
    layout="wide",
)

sns.set_theme(style="whitegrid", context="notebook", font_scale=0.95)
PALETA = "crest"  # paleta de Seaborn usada en todos los gráficos

RUTA_DATOS = "data/datos.csv"

# Nombres de columnas por si el CSV viene SIN encabezado.
# (Si tu archivo ya trae encabezado, se usan los nombres originales.)
COLUMNAS = [
    "error_id", "fecha_deteccion", "fecha_revision", "dias_hasta_deteccion",
    "revisor_id", "turno", "antiguedad_revisor_meses", "puntaje_calidad_revisor",
    "pais", "categoria", "tipo_documento", "norma", "tipo_vendedor",
    "num_documentos", "carga_diaria_revisor", "tiempo_revision_min",
    "tipo_error", "causa_raiz", "severidad", "metodo_deteccion",
    "horas_resolucion", "costo_usd",
    "indicador_1", "indicador_2", "indicador_3", "indicador_4", "indicador_5",
]


# ------------------------------------------------------------------
# 1. Cargar los datos
# ------------------------------------------------------------------
@st.cache_data
def cargar_datos(ruta):
    df = pd.read_csv(ruta)

    # Si la primera "columna" se llama ERR-xxxx, el archivo no tiene encabezado
    if str(df.columns[0]).startswith("ERR-"):
        df = pd.read_csv(ruta, header=None)
        if len(df.columns) == len(COLUMNAS):
            df.columns = COLUMNAS
        else:
            df.columns = [f"columna_{i + 1}" for i in range(len(df.columns))]

    # Convertir a fecha las columnas de texto con formato AAAA-MM-DD
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) and df[col].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}").all():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


try:
    df = cargar_datos(RUTA_DATOS)
except FileNotFoundError:
    st.error(f"❌ No encontré el archivo `{RUTA_DATOS}`. Revisa la ruta.")
    st.stop()

# Clasificar columnas según su tipo
cols_fecha = df.select_dtypes(include="datetime").columns.tolist()
cols_numericas = df.select_dtypes(include="number").columns.tolist()
cols_categoricas = [
    c for c in df.columns
    if (pd.api.types.is_string_dtype(df[c]) or pd.api.types.is_bool_dtype(df[c]))
    and 2 <= df[c].nunique() <= 30
    and df[c].nunique() < len(df)  # descarta IDs únicos como error_id
]


def elegir_por_defecto(opciones, preferida, posicion=0):
    """Devuelve el índice de la columna preferida si existe."""
    if preferida in opciones:
        return opciones.index(preferida)
    return min(posicion, len(opciones) - 1)


# ------------------------------------------------------------------
# 2. Título y subtítulo llamativos
# ------------------------------------------------------------------
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #0f4c5c, #2a9d8f);
                padding: 26px 30px; border-radius: 16px; margin-bottom: 18px;">
        <h1 style="color: white; margin: 0;">
            🛡️📋 Panel de Errores de Revisión de Cumplimiento 🔍⚠️
        </h1>
        <p style="color: #e0f2f1; font-size: 1.15rem; margin: 8px 0 0 0;">
            🌍 Certificados, normas y revisores bajo la lupa: descubre
            <b>dónde</b>, <b>por qué</b> y <b>cuánto cuesta</b> cada error 💸
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Filtros en la barra lateral
# ------------------------------------------------------------------
st.sidebar.header("🎛️ Filtros")
df_filtrado = df.copy()

# Filtro por rango de fechas (usa la primera columna de fecha)
if cols_fecha:
    col_f = cols_fecha[0]
    fecha_min = df[col_f].min().date()
    fecha_max = df[col_f].max().date()
    rango = st.sidebar.date_input(
        f"📅 Rango de {col_f}",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
    )
    if isinstance(rango, (list, tuple)) and len(rango) == 2:
        inicio, fin = pd.to_datetime(rango[0]), pd.to_datetime(rango[1])
        df_filtrado = df_filtrado[df_filtrado[col_f].between(inicio, fin)]

# Filtros de selección múltiple
preferidas = ["pais", "categoria", "severidad", "turno"]
cols_filtro = [c for c in preferidas if c in cols_categoricas] or cols_categoricas[:4]

for col in cols_filtro:
    opciones = sorted(df[col].dropna().unique().tolist())
    elegidas = st.sidebar.multiselect(f"🔹 {col}", opciones, default=opciones)
    df_filtrado = df_filtrado[df_filtrado[col].isin(elegidas)]

st.sidebar.markdown("---")
st.sidebar.caption(f"📦 Registros: **{len(df_filtrado)}** de {len(df)}")

if df_filtrado.empty:
    st.warning("⚠️ Ningún registro coincide con los filtros. Prueba a ampliarlos.")
    st.stop()

# ------------------------------------------------------------------
# Indicadores rápidos (KPIs)
# ------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("🧾 Errores", f"{len(df_filtrado):,}")
if "costo_usd" in df_filtrado:
    k2.metric("💸 Costo total", f"${df_filtrado['costo_usd'].sum():,.0f}")
if "horas_resolucion" in df_filtrado:
    k3.metric("⏱️ Horas prom. resolución", f"{df_filtrado['horas_resolucion'].mean():.1f}")
if "severidad" in df_filtrado:
    criticos = (df_filtrado["severidad"] == "Critical").sum()
    k4.metric("🚨 Críticos", f"{criticos}")

# ------------------------------------------------------------------
# 3. Vista previa del DataFrame filtrado
# ------------------------------------------------------------------
if st.checkbox("👀 Mostrar vista previa de los datos filtrados"):
    n_filas = st.slider("Número de filas", min_value=5, max_value=10, value=5)
    st.dataframe(df_filtrado.head(n_filas), width="stretch", hide_index=True)

st.markdown("---")

# ------------------------------------------------------------------
# 4. Gráficos
# ------------------------------------------------------------------
izq, der = st.columns(2)

# ---------- Gráfico 1: Barras horizontales ----------
with izq:
    st.subheader("📊 Ranking por categoría")
    c1, c2 = st.columns(2)
    col_barras = c1.selectbox(
        "Agrupar por", cols_categoricas,
        index=elegir_por_defecto(cols_categoricas, "tipo_error"), key="barras_cat",
    )
    medida = c2.selectbox(
        "Medida", ["Conteo"] + [f"Suma de {c}" for c in cols_numericas]
        + [f"Promedio de {c}" for c in cols_numericas],
        key="barras_medida",
    )

    if medida == "Conteo":
        datos_barras = df_filtrado[col_barras].astype(str).value_counts()
    else:
        tipo, col_num = medida.split(" de ", 1)
        agrupado = df_filtrado.groupby(df_filtrado[col_barras].astype(str))[col_num]
        datos_barras = agrupado.sum() if tipo == "Suma" else agrupado.mean()
        datos_barras = datos_barras.sort_values(ascending=False)

    datos_barras = datos_barras.reset_index()
    datos_barras.columns = [col_barras, "valor"]

    fig1, ax1 = plt.subplots(figsize=(7, max(3.5, 0.45 * len(datos_barras))))
    sns.barplot(
        data=datos_barras, x="valor", y=col_barras,
        hue=col_barras, palette=PALETA, legend=False, ax=ax1,
    )
    for contenedor in ax1.containers:
        ax1.bar_label(contenedor, fmt="%.0f" if medida == "Conteo" else "%.1f",
                      padding=3, fontsize=9)
    ax1.set_xlabel(medida)
    ax1.set_ylabel("")
    ax1.set_title(f"{medida} por {col_barras}", fontweight="bold", loc="left")
    sns.despine(left=True, bottom=True)
    fig1.tight_layout()
    st.pyplot(fig1, width="stretch")
    plt.close(fig1)

# ---------- Gráfico 2: Pie / Donut ----------
with der:
    st.subheader("🍩 Distribución porcentual")
    c1, c2 = st.columns([2, 1])
    col_pie = c1.selectbox(
        "Columna", cols_categoricas,
        index=elegir_por_defecto(cols_categoricas, "severidad", 1), key="pie_cat",
    )
    es_donut = c2.toggle("Donut", value=True)

    conteo = df_filtrado[col_pie].astype(str).value_counts()
    # Si hay muchas categorías, agrupar las pequeñas en "Otros"
    if len(conteo) > 7:
        conteo = pd.concat([conteo.iloc[:6], pd.Series({"Otros": conteo.iloc[6:].sum()})])

    colores = sns.color_palette(PALETA, n_colors=len(conteo))
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.pie(
        conteo.values,
        labels=conteo.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colores,
        pctdistance=0.78 if es_donut else 0.6,
        wedgeprops={"width": 0.42 if es_donut else 1, "edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 9},
    )
    if es_donut:
        ax2.text(0, 0, f"{conteo.sum()}\nregistros", ha="center", va="center",
                 fontsize=13, fontweight="bold", color="#0f4c5c")
    ax2.set_title(f"Distribución de {col_pie}", fontweight="bold", loc="left")
    ax2.axis("equal")
    fig2.tight_layout()
    st.pyplot(fig2, width="stretch")
    plt.close(fig2)

# ---------- Gráfico 3: Histograma (ancho completo) ----------
st.subheader("📈 Distribución de una variable numérica")
c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
col_hist = c1.selectbox(
    "Variable", cols_numericas,
    index=elegir_por_defecto(cols_numericas, "costo_usd"), key="hist_num",
)
color_por = c2.selectbox("Colorear por", ["(ninguno)"] + cols_categoricas, key="hist_hue")
bins = c3.slider("Barras (bins)", 5, 60, 20)
con_kde = c4.checkbox("Curva KDE", value=True)

fig3, ax3 = plt.subplots(figsize=(14, 4.5))
if color_por == "(ninguno)":
    sns.histplot(data=df_filtrado, x=col_hist, bins=bins, kde=con_kde,
                 color="#2a9d8f", edgecolor="white", ax=ax3)
else:
    datos_hist = df_filtrado.assign(**{color_por: df_filtrado[color_por].astype(str)})
    sns.histplot(data=datos_hist, x=col_hist, hue=color_por, bins=bins, kde=con_kde,
                 multiple="stack", palette=PALETA, edgecolor="white", ax=ax3)

ax3.axvline(df_filtrado[col_hist].mean(), color="#e76f51", linestyle="--", linewidth=1.5)
ax3.text(df_filtrado[col_hist].mean(), ax3.get_ylim()[1] * 0.95, "  promedio",
         color="#e76f51", fontsize=9, va="top")
ax3.set_title(f"Histograma de {col_hist}", fontweight="bold", loc="left")
ax3.set_xlabel(col_hist)
ax3.set_ylabel("Frecuencia")
sns.despine()
fig3.tight_layout()
st.pyplot(fig3, width="stretch")
plt.close(fig3)

st.caption("Hecho con ❤️ usando Python, Streamlit, Seaborn y trampillas")