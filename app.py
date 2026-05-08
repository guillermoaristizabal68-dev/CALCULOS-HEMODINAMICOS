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

if edad_unidad == "días":
    edad_anos = edad_numero / 365
elif edad_unidad == "meses":
    edad_anos = edad_numero / 12
else:
    edad_anos = edad_numero

# ---------------------------
# SUPERFICIE CORPORAL
# ---------------------------

st.header("Superficie corporal")

if peso > 0 and talla > 0:
    SC = 0.024265 * (peso ** 0.5378) * (talla ** 0.3964)
    st.success(f"Superficie corporal: {SC:.2f} m²")
else:
    SC = None
    st.info("Ingrese peso y talla para calcular superficie corporal.")

# ---------------------------
# HEMOGLOBINA GLOBAL
# ---------------------------

st.header("Hemoglobina")

hb = st.number_input("Hemoglobina (g/dL)", min_value=0.0)

if hb > 0 and (hb < 5 or hb > 25):
    st.warning("⚠️ Valor de hemoglobina fuera de rango fisiológico habitual. Verifique el dato.")

# ---------------------------
# VO2
# ---------------------------

st.header("Cálculo de VO₂")

metodo_vo2 = st.selectbox(
    "Método de cálculo de VO₂",
    ["VO₂ medido directamente", "Ecuación de Seckeler", "Ecuación de LaFarge"]
)

vo2_indexado = None

if metodo_vo2 == "VO₂ medido directamente":
    st.subheader("VO₂ medido directamente")

    vo2_indexado = st.number_input("VO₂ indexado (mL/min/m²)", min_value=0.0)

    if vo2_indexado > 0:
        st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")

elif metodo_vo2 == "Ecuación de Seckeler":
    st.subheader("Ecuación de Seckeler")

    st.latex(r"VO_2 = 138 - 11\ln(edad) - 0.022 \cdot FC + S - 4 \cdot Hb")

    fc_seckeler = st.number_input("Frecuencia cardíaca para Seckeler (lpm)", min_value=0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    if edad_anos > 0 and hb > 0:
        ln_edad = math.log(edad_anos)
        sexo_valor = 10 if sexo == "Masculino" else 0

        vo2_indexado = 138 - (11 * ln_edad) - (0.022 * fc_seckeler) + sexo_valor - (4 * hb)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        if edad_anos < 1:
            st.info("Edad <1 año: se usó edad en meses/12 o días/365 para evitar ln(0).")

        if edad_anos < 3:
            st.warning("⚠️ Mayor riesgo de inexactitud en menores de 3 años.")

        if hb < 10:
            st.warning("⚠️ La anemia puede afectar la precisión del VO₂ estimado.")
    else:
        st.info("Ingrese edad mayor de 0 y hemoglobina para calcular VO₂ con Seckeler.")

elif metodo_vo2 == "Ecuación de LaFarge":
    st.subheader("Ecuación de LaFarge-Miettinen")

    st.latex(r"VO_2 = 138.1 - 11.49\ln(edad) + 0.378 \cdot FC")

    fc_lafarge = st.number_input("Frecuencia cardíaca para LaFarge (lpm)", min_value=0)

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)

        vo2_indexado = 138.1 - (11.49 * ln_edad) + (0.378 * fc_lafarge)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        st.warning("⚠️ Método histórico. No recomendado como primera opción.")

        if edad_anos < 3:
            st.error("❌ Alta inexactitud esperada en menores de 3 años.")
    else:
        st.error("Ingrese edad mayor de 0 para calcular VO₂.")

# ---------------------------
# CONTENIDO DE OXÍGENO
# ---------------------------

st.header("Contenido de oxígeno")

st.latex(r"Contenido\ O_2 = Hb(g/L) \times 1.36 \times Sat + pO_2 \times 0.03")

fio2 = st.number_input("FiO₂ (%)", min_value=21.0, max_value=100.0, value=21.0)

if fio2 > 30:
    st.warning("⚠️ FiO₂ >30%: incluir oxígeno disuelto es importante.")

# Saturación venosa mixta dentro de contenido de O2

st.subheader("Saturación venosa mixta")

st.latex(r"SatVM = \frac{(3 \times SatVCS) + SatVCI}{4}")

metodo_vm = st.selectbox(
    "Método para estimar saturación venosa mixta",
    ["Usar solo VCS", "Calcular con VCS + VCI"]
)

sat_vm = None
po2_vm = None

if metodo_vm == "Usar solo VCS":

    sat_vcs = st.number_input("Saturación VCS (%)", min_value=0.0, max_value=100.0)
    po2_vcs = st.number_input("pO₂ VCS (mmHg)", min_value=0.0)

    if sat_vcs > 0:
        sat_vm = sat_vcs
        st.success(f"Saturación venosa mixta estimada: {sat_vm:.1f}%")

    if po2_vcs > 0:
        po2_vm = po2_vcs
        st.success(f"pO₂ venosa mixta estimada: {po2_vm:.1f} mmHg")

else:

    col_vm1, col_vm2 = st.columns(2)

    with col_vm1:
        sat_vcs = st.number_input("Saturación VCS (%)", min_value=0.0, max_value=100.0)
        po2_vcs = st.number_input("pO₂ VCS (mmHg)", min_value=0.0)

    with col_vm2:
        sat_vci = st.number_input("Saturación VCI (%)", min_value=0.0, max_value=100.0)
        po2_vci = st.number_input("pO₂ VCI (mmHg)", min_value=0.0)

    if sat_vcs > 0 and sat_vci > 0:
        sat_vm = ((3 * sat_vcs) + sat_vci) / 4
        st.success(f"Saturación venosa mixta calculada: {sat_vm:.1f}%")

    if po2_vcs > 0 and po2_vci > 0:
        po2_vm = ((3 * po2_vcs) + po2_vci) / 4
        st.success(f"pO₂ venosa mixta estimada: {po2_vm:.1f} mmHg")

# Muestras

st.subheader("Muestras para contenido de oxígeno")

col_o2_1, col_o2_2 = st.columns(2)

with col_o2_1:
    sat_ao = st.number_input("Saturación aórtica / sistémica (%)", min_value=0.0, max_value=100.0)
    pao2 = st.number_input("PaO₂ / pO₂ aórtica (mmHg)", min_value=0.0)

with col_o2_2:
    sat_pv = st.number_input(
        "Saturación venosa pulmonar / aurícula izquierda (%)",
        min_value=0.0,
        max_value=100.0,
        value=98.0
    )
    po2_pv = st.number_input("pO₂ venosa pulmonar / aurícula izquierda (mmHg)", min_value=0.0)

sat_pa = st.number_input("Saturación arteria pulmonar (%)", min_value=0.0, max_value=100.0)
po2_pa = st.number_input("pO₂ arteria pulmonar (mmHg)", min_value=0.0)

Ca = None
Cv = None
Cpv = None
Cpa = None

def contenido_oxigeno(hb_g_dl, sat_pct, po2):
    hb_g_l = hb_g_dl * 10
    sat_decimal = sat_pct / 100
    return (hb_g_l * 1.36 * sat_decimal) + (po2 * 0.03)

if hb > 0:

    if sat_ao > 0:
        Ca = contenido_oxigeno(hb, sat_ao, pao2)
        st.success(f"Contenido arterial sistémico / aórtico: {Ca:.2f} mL/L")

    if sat_vm is not None:
        Cv = contenido_oxigeno(hb, sat_vm, po2_vm if po2_vm is not None else 0)
        st.success(f"Contenido venoso mixto: {Cv:.2f} mL/L")

    if sat_pv > 0:
        Cpv = contenido_oxigeno(hb, sat_pv, po2_pv)
        st.success(f"Contenido venoso pulmonar / aurícula izquierda: {Cpv:.2f} mL/L")

    if sat_pa > 0:
        Cpa = contenido_oxigeno(hb, sat_pa, po2_pa)
        st.success(f"Contenido arteria pulmonar: {Cpa:.2f} mL/L")

else:
    st.info("Ingrese hemoglobina para calcular contenido de oxígeno.")

# ---------------------------
# FLUJOS INDEXADOS
# ---------------------------

st.header("Flujos indexados")

Qp_i = None
Qs_i = None

if vo2_indexado is not None and vo2_indexado > 0:

    if Ca is not None and Cv is not None and Cpv is not None and Cpa is not None:

        dif_sistemica = Ca - Cv
        dif_pulmonar = Cpv - Cpa

        if dif_sistemica > 0 and dif_pulmonar > 0:

            Qs_i = vo2_indexado / dif_sistemica
            Qp_i = vo2_indexado / dif_pulmonar

            st.success(f"Qs indexado: {Qs_i:.2f} L/min/m²")
            st.success(f"Qp indexado: {Qp_i:.2f} L/min/m²")
if SC:
    Qs = Qs_i * SC
    Qp = Qp_i * SC

    st.success(f"Qs no indexado / gasto cardíaco sistémico: {Qs:.2f} L/min")
    st.success(f"Qp no indexado / flujo pulmonar: {Qp:.2f} L/min")
            
            if Qs_i > 0:
                qp_qs = Qp_i / Qs_i
                st.success(f"Qp/Qs: {qp_qs:.2f}")

        else:
            st.error("Las diferencias de contenido de oxígeno deben ser mayores de 0.")

    else:
        st.info("Complete los datos de contenido de oxígeno para calcular flujos.")

else:
    st.info("Calcule o ingrese VO₂ indexado para calcular flujos.")

# ---------------------------
# PRESIONES Y RESISTENCIAS
# ---------------------------

st.header("Gradiente transpulmonar y resistencias")

PVR_i = None
SVR_i = None
PVR = None
SVR = None

col_p1, col_p2 = st.columns(2)

with col_p1:
    PAPm = st.number_input("Presión pulmonar media / PAPm (mmHg)", min_value=0.0)
    LAP = st.number_input("Presión aurícula izquierda / wedge / LAP (mmHg)", min_value=0.0)

with col_p2:
    MAP = st.number_input("Presión arterial media sistémica / MAP (mmHg)", min_value=0.0)
    RAP = st.number_input("Presión aurícula derecha / RAP (mmHg)", min_value=0.0)

if Qp_i is not None and Qs_i is not None:

    TPG = PAPm - LAP

    st.subheader("Gradiente transpulmonar")
    st.success(f"Gradiente transpulmonar: {TPG:.2f} mmHg")

    if Qp_i > 0:
        PVR_i = TPG / Qp_i
        st.subheader("Resistencia vascular pulmonar")
        st.success(f"RVP indexada: {PVR_i:.2f} Wood·m²")

        if SC:
            PVR = PVR_i / SC
            st.success(f"RVP no indexada: {PVR:.2f} Wood units")

    if Qs_i > 0:
        SVR_i = (MAP - RAP) / Qs_i
        st.subheader("Resistencia vascular sistémica")
        st.success(f"RVS indexada: {SVR_i:.2f} Wood·m²")

        if SC:
            SVR = SVR_i / SC
            st.success(f"RVS no indexada: {SVR:.2f} Wood units")

    if PVR_i is not None and SVR_i is not None and SVR_i > 0:
        relacion_pvr_svr = PVR_i / SVR_i
        st.subheader("Relación RVP/RVS")
        st.success(f"Relación RVP/RVS: {relacion_pvr_svr:.2f}")

    mostrar_dinas = st.checkbox("Mostrar resistencias en dyn·s·cm⁻⁵")

    if mostrar_dinas:
        if PVR is not None:
            st.info(f"RVP no indexada: {PVR * 80:.2f} dyn·s·cm⁻⁵")
        if SVR is not None:
            st.info(f"RVS no indexada: {SVR * 80:.2f} dyn·s·cm⁻⁵")
        if PVR_i is not None:
            st.info(f"RVP indexada: {PVR_i * 80:.2f} dyn·s·cm⁻⁵·m²")
        if SVR_i is not None:
            st.info(f"RVS indexada: {SVR_i * 80:.2f} dyn·s·cm⁻⁵·m²")

else:
    st.info("Calcule primero Qp y Qs indexados para obtener resistencias.")

# ---------------------------
# REFERENCIA
# ---------------------------

st.header("Referencias principales")

st.markdown("""
**Contenido de oxígeno, Qp/Qs, flujos y resistencias:**  
Wilkinson JL. *Haemodynamic calculations in the catheter laboratory.* Heart. 2001;85:113–120.

**VO₂ medido:**  
Li J. *Accurate Measurement of Oxygen Consumption in Children Undergoing Cardiac Catheterization.*  
Catheterization and Cardiovascular Interventions. 2013;81(1):125-32. PMID: 22488802.

**Ecuación de Seckeler:**  
Seckeler MD, Hirsch R, Beekman RH, Goldstein BH.  
*A New Predictive Equation for Oxygen Consumption in Children and Adults With Congenital and Acquired Heart Disease.*  
Heart. 2015;101(7):517-24. PMID: 25429053.

**Ecuación de LaFarge-Miettinen:**  
LaFarge CG, Miettinen OS. *The estimation of oxygen consumption.*  
Cardiovascular Research. 1970;4:23-30.
""")
