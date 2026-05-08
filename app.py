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

vo2_indexado = None
vo2_absoluto = None

if metodo_vo2 == "VO₂ medido directamente":

    st.subheader("VO₂ medido directamente")

    st.markdown("""
    **Ventajas:**
    - Método más preciso.
    - No depende de ecuaciones predictivas.
    - Recomendado cuando se requiere mayor precisión.

    **Limitaciones:**
    - Requiere equipo especializado.

    **Referencia:**  
    Li J. *Accurate Measurement of Oxygen Consumption in Children Undergoing Cardiac Catheterization.*  
    Catheterization and Cardiovascular Interventions. 2013;81(1):125-32. PMID: 22488802.
    """)

    tipo_vo2_manual = st.selectbox(
        "Unidad del VO₂ medido",
        ["mL/min/m²", "mL/min"]
    )

    vo2_manual = st.number_input("Ingrese VO₂ medido", min_value=0.0)

    if vo2_manual > 0:
        if tipo_vo2_manual == "mL/min/m²":
            vo2_indexado = vo2_manual

            if superficie_corporal:
                vo2_absoluto = vo2_indexado * superficie_corporal
                st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")
                st.success(f"VO₂ absoluto: {vo2_absoluto:.2f} mL/min")
            else:
                st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")
                st.warning("Ingrese peso y talla para calcular VO₂ absoluto.")

        else:
            vo2_absoluto = vo2_manual

            if superficie_corporal:
                vo2_indexado = vo2_absoluto / superficie_corporal
                st.success(f"VO₂ absoluto: {vo2_absoluto:.2f} mL/min")
                st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")
            else:
                st.success(f"VO₂ absoluto: {vo2_absoluto:.2f} mL/min")
                st.warning("Ingrese peso y talla para calcular VO₂ indexado.")

elif metodo_vo2 == "Ecuación de Seckeler":

    st.subheader("Ecuación de Seckeler")

    st.latex(r"VO_2 = 138 - 11\ln(edad) - 0.022 \cdot FC + S - 4 \cdot Hb")

    st.markdown("""
    **Resultado:** VO₂ indexado en mL/min/m².

    **Variables:**
    - Edad en años.
    - FC: frecuencia cardíaca en lpm.
    - S: masculino = +10, femenino = 0.
    - Hb: hemoglobina en g/dL.

    **Referencia:**  
    Seckeler MD, Hirsch R, Beekman RH, Goldstein BH.  
    *A New Predictive Equation for Oxygen Consumption in Children and Adults With Congenital and Acquired Heart Disease.*  
    Heart. 2015;101(7):517-24. PMID: 25429053.
    """)

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)
    hb_seckeler = st.number_input("Hemoglobina para Seckeler (g/dL)", min_value=0.0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)
        sexo_valor = 10 if sexo == "Masculino" else 0

        vo2_indexado = 138 - (11 * ln_edad) - (0.022 * fc) + sexo_valor - (4 * hb_seckeler)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        if superficie_corporal:
            vo2_absoluto = vo2_indexado * superficie_corporal
            st.success(f"VO₂ absoluto estimado: {vo2_absoluto:.2f} mL/min")

        if edad_anos < 1:
            st.info("Edad <1 año: se usó edad en meses/12 o días/365 para evitar ln(0).")

        if edad_anos < 3:
            st.warning("⚠️ Mayor riesgo de inexactitud en menores de 3 años.")

        if hb_seckeler < 10 and hb_seckeler > 0:
            st.warning("⚠️ La anemia puede afectar la precisión del VO₂ estimado.")

    else:
        st.error("Ingrese una edad mayor de 0 para calcular VO₂ con Seckeler.")

elif metodo_vo2 == "Ecuación de LaFarge":

    st.subheader("Ecuación de LaFarge-Miettinen")

    st.latex(r"VO_2 = 138.1 - 11.49\ln(edad) + 0.378 \cdot FC")

    st.markdown("""
    **Resultado:** VO₂ indexado en mL/min/m².

    **Referencia:**  
    LaFarge CG, Miettinen OS.  
    *The estimation of oxygen consumption.*  
    Cardiovascular Research. 1970;4:23-30.
    """)

    fc_lafarge = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)

        vo2_indexado = 138.1 - (11.49 * ln_edad) + (0.378 * fc_lafarge)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        if superficie_corporal:
            vo2_absoluto = vo2_indexado * superficie_corporal
            st.success(f"VO₂ absoluto estimado: {vo2_absoluto:.2f} mL/min")

        st.warning("⚠️ Método histórico. No se recomienda como primera opción si hay VO₂ medido o Seckeler disponible.")

        if edad_anos < 3:
            st.error("❌ Alta inexactitud esperada en menores de 3 años.")

    else:
        st.error("Ingrese una edad mayor de 0 para calcular VO₂ con LaFarge.")

# ---------------------------
# SATURACIÓN VENOSA MIXTA
# ---------------------------

st.header("Saturación venosa mixta y pO₂ venosa mixta")

st.markdown("""
Según Wilkinson, cuando se dispone de saturación en VCS y VCI, una aproximación práctica para la saturación venosa mixta es:
""")

st.latex(r"SatVM = \frac{(3 \times SatVCS) + SatVCI}{4}")

st.markdown("""
Si solo se dispone de VCS, la app permite usar la saturación de VCS como aproximación de la saturación venosa mixta.

**Referencia:**  
Wilkinson JL. *Haemodynamic calculations in the catheter laboratory.* Heart. 2001;85:113–120.
""")

metodo_vm = st.selectbox(
    "Método para estimar saturación venosa mixta",
    [
        "Usar solo VCS",
        "Calcular con VCS + VCI"
    ]
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

# ---------------------------
# DATOS PARA CONTENIDO DE OXÍGENO
# ---------------------------

st.header("Datos para contenido de oxígeno")

st.markdown("""
Cuando se usa oxígeno con FiO₂ mayor de 30%, debe considerarse el oxígeno disuelto para evitar errores importantes en el cálculo de flujo pulmonar y resistencias. :contentReference[oaicite:0]{index=0}
""")

fio2 = st.number_input("FiO₂ (%)", min_value=21.0, max_value=100.0, value=21.0)
hb_contenido = st.number_input("Hemoglobina para contenido de O₂ (g/dL)", min_value=0.0)

st.markdown("### Muestras principales")

col_o2_1, col_o2_2 = st.columns(2)

with col_o2_1:
    sat_ao = st.number_input("Saturación aórtica / sistémica (%)", min_value=0.0, max_value=100.0)
    pao2 = st.number_input("PaO₂ / pO₂ aórtica (mmHg)", min_value=0.0)

with col_o2_2:
    sat_pv = st.number_input("Saturación venosa pulmonar o aurícula izquierda (%)", min_value=0.0, max_value=100.0, value=98.0)
    po2_pv = st.number_input("pO₂ venosa pulmonar / aurícula izquierda (mmHg)", min_value=0.0)

sat_pa = st.number_input("Saturación arteria pulmonar (%)", min_value=0.0, max_value=100.0)
po2_pa = st.number_input("pO₂ arteria pulmonar (mmHg)", min_value=0.0)

if fio2 > 30:
    st.warning("⚠️ FiO₂ >30%: es importante incluir oxígeno disuelto en los cálculos.")

if hb_contenido > 0:
    st.subheader("Contenido de oxígeno calculado")

    def contenido_oxigeno(hb_g_dl, sat_pct, po2):
        hb_g_l = hb_g_dl * 10
        sat_decimal = sat_pct / 100
        return (hb_g_l * 1.36 * sat_decimal) + (po2 * 0.03)

    if sat_ao > 0:
        cao2 = contenido_oxigeno(hb_contenido, sat_ao, pao2)
        st.success(f"Contenido arterial sistémico / aórtico: {cao2:.2f} mL/L")

    if sat_vm is not None:
        cvm_o2 = contenido_oxigeno(hb_contenido, sat_vm, po2_vm if po2_vm else 0)
        st.success(f"Contenido venoso mixto: {cvm_o2:.2f} mL/L")

    if sat_pv > 0:
        cpv_o2 = contenido_oxigeno(hb_contenido, sat_pv, po2_pv)
        st.success(f"Contenido venoso pulmonar / aurícula izquierda: {cpv_o2:.2f} mL/L")

    if sat_pa > 0:
        cpa_o2 = contenido_oxigeno(hb_contenido, sat_pa, po2_pa)
        st.success(f"Contenido arteria pulmonar: {cpa_o2:.2f} mL/L")
else:
    st.info("Ingrese hemoglobina para calcular contenido de oxígeno.")

# ---------------------------
# REFERENCIA PRINCIPAL
# ---------------------------

st.header("Referencia principal para cálculos hemodinámicos")

st.markdown("""
Wilkinson JL. *Haemodynamic calculations in the catheter laboratory.*  
Heart. 2001;85:113–120.
""")
