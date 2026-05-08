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

    edad_numero = st.number_input("Edad", min_value=0)
    edad_unidad = st.selectbox("Unidad de edad", ["días", "meses", "años"])

    peso = st.number_input("Peso (kg)", min_value=0.0)

with col2:
    talla = st.number_input("Talla (cm)", min_value=0.0)
    fecha = st.date_input("Fecha", value=date.today())

# ---------------------------
# EDAD A AÑOS
# ---------------------------

if edad_unidad == "días":
    edad_anos = edad_numero / 365
elif edad_unidad == "meses":
    edad_anos = edad_numero / 12
else:
    edad_anos = edad_numero

# ---------------------------
# SUPERFICIE CORPORAL
# ---------------------------

if peso > 0 and talla > 0:
    SC = 0.024265 * (peso ** 0.5378) * (talla ** 0.3964)
    st.success(f"Superficie corporal: {SC:.2f} m²")
else:
    SC = None

# ---------------------------
# VO2
# ---------------------------

st.header("VO₂")

metodo = st.selectbox("Método", ["Directo", "Seckeler", "LaFarge"])

vo2_indexado = None

if metodo == "Directo":
    vo2_indexado = st.number_input("VO₂ (mL/min/m²)", min_value=0.0)

elif metodo == "Seckeler":

    st.latex(r"VO_2 = 138 - 11\ln(edad) - 0.022 \cdot FC + S - 4 \cdot Hb")

    fc = st.number_input("FC", min_value=0)
    hb = st.number_input("Hb (g/dL)", min_value=0.0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    if edad_anos > 0:
        ln = math.log(edad_anos)
        s = 10 if sexo == "Masculino" else 0
        vo2_indexado = 138 - (11 * ln) - (0.022 * fc) + s - (4 * hb)

        st.success(f"VO₂: {vo2_indexado:.2f} mL/min/m²")

elif metodo == "LaFarge":

    st.latex(r"VO_2 = 138.1 - 11.49\ln(edad) + 0.378 \cdot FC")

    fc = st.number_input("FC", min_value=0)

    if edad_anos > 0:
        ln = math.log(edad_anos)
        vo2_indexado = 138.1 - (11.49 * ln) + (0.378 * fc)

        st.success(f"VO₂: {vo2_indexado:.2f}")

# ---------------------------
# SATURACIÓN VENOSA MIXTA
# ---------------------------

st.header("Saturación venosa mixta")

metodo_vm = st.selectbox("Método VM", ["VCS", "VCS + VCI"])

if metodo_vm == "VCS":
    sat_vm = st.number_input("Sat VCS (%)", 0.0, 100.0)
    po2_vm = st.number_input("pO₂ VCS", 0.0)

else:
    sat_vcs = st.number_input("Sat VCS (%)", 0.0, 100.0)
    sat_vci = st.number_input("Sat VCI (%)", 0.0, 100.0)
    po2_vcs = st.number_input("pO₂ VCS", 0.0)
    po2_vci = st.number_input("pO₂ VCI", 0.0)

    sat_vm = (3 * sat_vcs + sat_vci) / 4
    po2_vm = (3 * po2_vcs + po2_vci) / 4

    st.success(f"Sat VM: {sat_vm:.1f}%")

# ---------------------------
# CONTENIDO DE O2
# ---------------------------

st.header("Contenido de oxígeno")

hb = st.number_input("Hb (g/dL)", min_value=0.0)

sat_a = st.number_input("Sat arterial (%)", 0.0, 100.0)
po2_a = st.number_input("PaO₂", 0.0)

sat_pv = st.number_input("Sat venosa pulmonar (%)", 0.0, 100.0, value=98.0)
po2_pv = st.number_input("pO₂ venosa pulmonar", 0.0)

sat_pa = st.number_input("Sat arteria pulmonar (%)", 0.0, 100.0)
po2_pa = st.number_input("pO₂ arteria pulmonar", 0.0)

def contenido(hb, sat, po2):
    return (hb * 10 * 1.36 * (sat/100)) + (po2 * 0.03)

if hb > 0:

    Ca = contenido(hb, sat_a, po2_a)
    Cv = contenido(hb, sat_vm, po2_vm)
    Cpv = contenido(hb, sat_pv, po2_pv)
    Cpa = contenido(hb, sat_pa, po2_pa)

    st.success(f"Ca: {Ca:.2f}")
    st.success(f"Cv: {Cv:.2f}")
    st.success(f"Cpv: {Cpv:.2f}")
    st.success(f"Cpa: {Cpa:.2f}")

# ---------------------------
# FLUJOS INDEXADOS
# ---------------------------

st.header("Flujos indexados")

if vo2_indexado and hb > 0 and SC:

    if (Ca - Cv) != 0 and (Cpv - Cpa) != 0:

        Qs_i = vo2_indexado / (Ca - Cv)
        Qp_i = vo2_indexado / (Cpv - Cpa)

        st.success(f"Qs indexado: {Qs_i:.2f}")
        st.success(f"Qp indexado: {Qp_i:.2f}")

        if Qs_i > 0:
            st.success(f"Qp/Qs: {Qp_i/Qs_i:.2f}")

# ---------------------------
# PRESIONES Y RESISTENCIAS
# ---------------------------

st.header("Resistencias")

PAPm = st.number_input("PAP media", 0.0)
LAP = st.number_input("LAP", 0.0)
MAP = st.number_input("MAP", 0.0)
RAP = st.number_input("RAP", 0.0)

if Qp_i and Qs_i:

    TPG = PAPm - LAP
    st.success(f"TPG: {TPG:.2f}")

    PVR_i = TPG / Qp_i
    SVR_i = (MAP - RAP) / Qs_i

    st.success(f"PVR indexado: {PVR_i:.2f}")
    st.success(f"SVR indexado: {SVR_i:.2f}")

    if st.checkbox("Convertir a dinas"):
        st.info(f"PVR: {PVR_i*80:.2f}")
        st.info(f"SVR: {SVR_i*80:.2f}")

# ---------------------------
# REFERENCIA
# ---------------------------

st.markdown("""
Wilkinson JL. *Haemodynamic calculations in the catheter laboratory.* Heart. 2001.
""")
