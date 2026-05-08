import streamlit as st
from datetime import date

st.title("Cálculos Hemodinámicos Pediátricos")

st.header("Datos de identificación")

nombre = st.text_input("Nombre")
apellidos = st.text_input("Apellidos")

tipo_documento = st.selectbox(
    "Tipo de documento",
    ["Registro civil", "Tarjeta de identidad", "Cédula", "Pasaporte"]
)

numero_documento = st.text_input("Número de documento")

edad_numero = st.number_input("Edad", min_value=0)
edad_unidad = st.selectbox("Unidad", ["días", "meses", "años"])

peso = st.number_input("Peso (kg)", min_value=0.0)
talla = st.number_input("Talla (cm)", min_value=0.0)

institucion = st.text_input("Institución")
aseguradora = st.text_input("Aseguradora")

fecha = st.date_input("Fecha", value=date.today())

# Superficie corporal
if peso > 0 and talla > 0:
    sc = 0.024265 * (peso ** 0.5378) * (talla ** 0.3964)
    st.success(f"Superficie corporal: {sc:.2f} m²")
