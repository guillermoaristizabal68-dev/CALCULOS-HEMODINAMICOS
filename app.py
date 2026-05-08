import streamlit as st
from datetime import date
import math

st.set_page_config(
    page_title="Calculadora Hemodinámica Cardiovascular",
    layout="wide"
)

st.title("Calculadora Hemodinámica Cardiovascular")

# ---------------------------
# DATOS DE IDENTIFICACIÓN
# ---------------------------

st.header("Datos de identificación")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre")
    apellidos = st.text_input("Apellidos")
    
    tipo_documento = st.selectbox(
        "Tipo de documento",
        ["Registro civil", "Tarjeta de identidad", "Cédula", "Pasaporte", "Otro"]
    )
    
    if tipo_documento == "Otro":
        tipo_documento_otro = st.text_input("Especifique tipo de documento")
    
    numero_documento = st.text_input("Número de documento")
    
    edad_numero = st.number_input("Edad", min_value=0)
    edad_unidad = st.selectbox("Unidad de edad", ["días", "meses", "años"])
    
    peso = st.number_input("Peso (kg)", min_value=0.0)

with col2:
    talla = st.number_input("Talla (cm)", min_value=0.0)
    
    institucion = st.text_input("Institución")
    aseguradora = st.text_input("Aseguradora / EPS")
    
    fecha = st.date_input("Fecha del estudio", value=date.today())

# ---------------------------
# SUPERFICIE CORPORAL
# ---------------------------

st.subheader("Superficie corporal")

if peso > 0 and talla > 0:
    superficie_corporal = 0.024265 * (peso ** 0.5378) * (talla ** 0.3964)
    st.success(f"Superficie corporal: {superficie_corporal:.2f} m²")
else:
    superficie_corporal = None
    st.info("Ingrese peso y talla para calcular la superficie corporal.")

# ---------------------------
# MÓDULO VO2
# ---------------------------

st.header("Cálculo de VO₂")

metodo_vo2 = st.selectbox(
    "Método de cálculo de VO₂",
    [
        "VO₂ medido directamente",
        "Ecuación de Seckeler",
        "Ecuación de LaFarge"
    ]
)

# ---------------------------
# VO2 MEDIDO
# ---------------------------
if metodo_vo2 == "VO₂ medido directamente":

    st.subheader("VO₂ medido directamente (Gold Standard)")

    st.markdown("""
    **Ventajas:**
    - Método más preciso
    - No depende de estimaciones
    - Recomendado en cardiopatías congénitas

    **Limitaciones:**
    - Requiere equipo especializado
    """)

    st.markdown("🔗 Referencia: https://pubmed.ncbi.nlm.nih.gov/")

    vo2 = st.number_input("VO₂ (mL/min o mL/min/m²)", min_value=0.0)

    if vo2 > 0:
        st.success(f"VO₂ ingresado: {vo2}")

# ---------------------------
# SECKELER
# ---------------------------
elif metodo_vo2 == "Ecuación de Seckeler":

    st.subheader("Ecuación de Seckeler")

    st.latex(r"VO_2 = 138 - 11\ln(edad) - 0.022 \cdot FC + S - 4 \cdot Hb")

    st.markdown("""
    **Variables:**
    - Edad (años)
    - FC: frecuencia cardíaca
    - Hb: hemoglobina
    - Sexo: Masculino = +10, Femenino = 0

    **Ventajas:**
    - Mejor correlación que LaFarge
    - Aplicable en 0–59 años
    - Incluye variables fisiológicas

    **Limitaciones:**
    - Error potencial >20%
    - Menor precisión en <3 años

    🔗 Referencia:
    https://pubmed.ncbi.nlm.nih.gov/25661062/
    """)

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)
    hb = st.number_input("Hemoglobina (g/dL)", min_value=0.0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    # Conversión edad a años
    if edad_unidad == "días":
        edad_anos = edad_numero / 365
    elif edad_unidad == "meses":
        edad_anos = edad_numero / 12
    else:
        edad_anos = edad_numero

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)
        sexo_valor = 10 if sexo == "Masculino" else 0

        vo2 = 138 - (11 * ln_edad) - (0.022 * fc) + sexo_valor - (4 * hb)

        st.success(f"VO₂ estimado: {vo2:.2f} mL/min/m²")

        if edad_anos < 3:
            st.warning("⚠️ Mayor riesgo de error en menores de 3 años")

        if hb < 10:
            st.warning("⚠️ La anemia puede afectar la precisión")

    else:
        st.error("Edad no válida")

# ---------------------------
# LAFARGE
# ---------------------------
elif metodo_vo2 == "Ecuación de LaFarge":

    st.subheader("Ecuación de LaFarge")

    st.latex(r"VO_2 = 138.1 - 11.49 \ln(edad) + 0.378 \cdot FC")

    st.markdown("""
    **Ventajas:**
    - Fácil de usar
    - Históricamente utilizada

    **Limitaciones:**
    - No recomendada actualmente
    - Alta inexactitud en <3 años
    - No incluye hemoglobina ni sexo

    🔗 Referencia:
    https://pubmed.ncbi.nlm.nih.gov/10971116/
    """)

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)

    if edad_unidad == "días":
        edad_anos = edad_numero / 365
    elif edad_unidad == "meses":
        edad_anos = edad_numero / 12
    else:
        edad_anos = edad_numero

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)

        vo2 = 138.1 - (11.49 * ln_edad) + (0.378 * fc)

        st.success(f"VO₂ estimado: {vo2:.2f} mL/min/m²")

        st.error("❌ Método no recomendado clínicamente")

        if edad_anos < 3:
            st.error("❌ Alta inexactitud en menores de 3 años")

    else:
        st.error("Edad no válida")
