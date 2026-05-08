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
