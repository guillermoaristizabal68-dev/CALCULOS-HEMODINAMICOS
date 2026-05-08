import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Cálculos Hemodinámicos Pediátricos",
    layout="wide"
)

st.title("Cálculos Hemodinámicos Pediátricos")

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
import math

st.header("Cálculo de VO₂")

metodo_vo2 = st.selectbox(
    "Método de cálculo de VO₂",
    [
        "VO₂ medido directamente",
        "Ecuación de Seckeler",
        "Ecuación de Bergstra",
        "Ecuación de LaFarge"
    ]
)

# ---------------------------
# VO2 MEDIDO
# ---------------------------
if metodo_vo2 == "VO₂ medido directamente":
    vo2_manual = st.number_input("VO₂ (mL/min o mL/min/m²)", min_value=0.0)
    
    if vo2_manual > 0:
        st.success(f"VO₂ ingresado: {vo2_manual}")

# ---------------------------
# SECKELER
# ---------------------------
elif metodo_vo2 == "Ecuación de Seckeler":

    st.subheader("Variables para Seckeler")

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)
    hb = st.number_input("Hemoglobina (g/dL)", min_value=0.0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    # Conversión de edad a años
    if edad_unidad == "días":
        edad_anos = edad_numero / 365
    elif edad_unidad == "meses":
        edad_anos = edad_numero / 12
    else:
        edad_anos = edad_numero

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)

        if sexo == "Masculino":
            sexo_valor = 10
        else:
            sexo_valor = 0

        vo2_indexado = 138 - (11 * ln_edad) - (0.022 * fc) + sexo_valor - (4 * hb)

        st.success(f"VO₂ estimado (Seckeler): {vo2_indexado:.2f} mL/min/m²")

        # ALERTAS CLÍNICAS 🔥
        if edad_anos < 3:
            st.warning("⚠️ Mayor riesgo de inexactitud en menores de 3 años")

        if hb < 10:
            st.warning("⚠️ La anemia puede afectar la precisión del VO₂")

    else:
        st.error("Edad no válida para cálculo (evitar 0)")
