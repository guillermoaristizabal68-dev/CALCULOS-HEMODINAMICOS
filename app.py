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
# FLUJOS POR FICK
# ---------------------------

st.header("Flujos por método de Fick")

Qp_i = None
Qs_i = None
Qp = None
Qs = None

if vo2_indexado is not None and vo2_indexado > 0:

    if Ca is not None and Cv is not None and Cpv is not None and Cpa is not None:

        dif_sistemica = Ca - Cv
        dif_pulmonar = Cpv - Cpa

        if dif_sistemica > 0 and dif_pulmonar > 0:

            Qs_i = vo2_indexado / dif_sistemica
            Qp_i = vo2_indexado / dif_pulmonar

            st.subheader("Flujos indexados")
            st.success(f"Qs indexado / índice cardíaco sistémico: {Qs_i:.2f} L/min/m²")
            st.success(f"Qp indexado / índice pulmonar: {Qp_i:.2f} L/min/m²")

            if SC:
                Qs = Qs_i * SC
                Qp = Qp_i * SC

                st.subheader("Flujos no indexados")
                st.success(f"Qs no indexado / gasto cardíaco sistémico: {Qs:.2f} L/min")
                st.success(f"Qp no indexado / flujo pulmonar: {Qp:.2f} L/min")
            else:
                st.warning("Ingrese peso y talla para calcular Qs y Qp no indexados.")

            if Qs_i > 0:
                qp_qs = Qp_i / Qs_i
                st.subheader("Relación de cortocircuito")
                st.success(f"Qp/Qs: {qp_qs:.2f}")

        else:
            st.error("Las diferencias de contenido de oxígeno deben ser mayores de 0.")

    else:
        st.info("Complete los datos de contenido de oxígeno para calcular flujos.")

else:
    st.info("Calcule o ingrese VO₂ indexado para calcular flujos.")

# ---------------------------
# HEMODINÁMICA AVANZADA POR FICK
# ---------------------------

st.header("Hemodinámica avanzada por Fick")

col_pf1, col_pf2 = st.columns(2)

with col_pf1:

    sPAP_fick = st.number_input(
        "sPAP Fick (mmHg)",
        min_value=0.0
    )

    dPAP_fick = st.number_input(
        "dPAP Fick (mmHg)",
        min_value=0.0
    )

    mPAP_fick = st.number_input(
        "mPAP Fick (mmHg)",
        min_value=0.0
    )

    PAWP_fick = st.number_input(
        "PAWP / wedge Fick (mmHg)",
        min_value=0.0
    )

with col_pf2:

    MAP_fick = st.number_input(
        "MAP Fick (mmHg)",
        min_value=0.0
    )

    RAP_fick = st.number_input(
        "RAP Fick (mmHg)",
        min_value=0.0
    )

    FC_fick = st.number_input(
        "Frecuencia cardíaca Fick (lpm)",
        min_value=1
    )

# ---------------------------
# VALIDACIÓN
# ---------------------------

if Qs is not None and Qp is not None:

    st.subheader("Gasto cardíaco e índice cardíaco")

    st.success(f"Gasto cardíaco sistémico por Fick (Qs): {Qs:.2f} L/min")

    if Qs_i is not None:
        st.success(f"Índice cardíaco por Fick: {Qs_i:.2f} L/min/m²")

# ---------------------------
# VOLUMEN SISTÓLICO
# ---------------------------

if Qs is not None and Qs > 0 and FC_fick > 0:
    VS_fick = (Qs * 1000) / FC_fick

    st.subheader("Volumen sistólico")
    st.success(f"Volumen sistólico sistémico por Fick: {VS_fick:.2f} mL/latido")

    if SC:
        IVS_fick = VS_fick / SC
        st.success(f"Índice volumen sistólico por Fick: {IVS_fick:.2f} mL/latido/m²")

        if IVS_fick < 33:
            st.warning("⚠️ Índice volumen sistólico disminuido")
        elif IVS_fick <= 47:
            st.info("Índice volumen sistólico dentro de rango esperado")
        else:
            st.warning("Índice volumen sistólico elevado")
else:
    st.info("Ingrese Qs y frecuencia cardíaca válidos para calcular volumen sistólico.")
    # ---------------------------
    # GRADIENTE TRANSPULMONAR
    # ---------------------------

    TPG_fick = mPAP_fick - PAWP_fick

    st.subheader("Gradiente transpulmonar")

    st.success(f"TPG: {TPG_fick:.2f} mmHg")

    # ---------------------------
    # RVP
    # ---------------------------

    if Qp > 0:

        PVR_fick = TPG_fick / Qp

        st.subheader("Resistencia vascular pulmonar")

        st.latex(r"PVR = \frac{mPAP - PAWP}{Qp}")

        st.success(f"RVP no indexada: {PVR_fick:.2f} Wood units")

        if SC:

            PVRI_fick = PVR_fick * SC

            st.success(f"RVP indexada: {PVRI_fick:.2f} Wood·m²")

    # ---------------------------
    # RPT
    # ---------------------------

    if Qp > 0:

        TPR_fick = mPAP_fick / Qp

        st.subheader("Resistencia pulmonar total")

        st.success(f"RPT: {TPR_fick:.2f} Wood units")

    # ---------------------------
    # RVS
    # ---------------------------

    if Qs > 0:

        SVR_fick = (MAP_fick - RAP_fick) / Qs

        st.subheader("Resistencia vascular sistémica")

        st.success(f"RVS no indexada: {SVR_fick:.2f} Wood units")

        if SC:

            SVRI_fick = SVR_fick * SC

            st.success(f"RVS indexada: {SVRI_fick:.2f} Wood·m²")

    # ---------------------------
    # RELACIÓN RVP/RVS
    # ---------------------------

    if Qp > 0 and Qs > 0:

        relacion_pvr_svr_fick = PVR_fick / SVR_fick

        st.subheader("Relación RVP/RVS")

        st.success(f"Relación RVP/RVS: {relacion_pvr_svr_fick:.2f}")

    # ---------------------------
    # COMPLIANCE PULMONAR
    # ---------------------------

    if (sPAP_fick - dPAP_fick) > 0:

        CAP_fick = VS_fick / (sPAP_fick - dPAP_fick)

        st.subheader("Compliance arterial pulmonar")

        st.latex(r"CAP = \frac{VS}{sPAP - dPAP}")

        st.success(f"Compliance arterial pulmonar: {CAP_fick:.2f} mL/mmHg")

        if CAP_fick < 2.3:
            st.warning("⚠️ Compliance pulmonar reducida")

    # ---------------------------
    # PAPi
    # ---------------------------

    if RAP_fick > 0:

        PAPi_fick = (sPAP_fick - dPAP_fick) / RAP_fick

        st.subheader("Pulmonary Artery Pulsatility Index (PAPi)")

        st.latex(r"PAPi = \frac{sPAP - dPAP}{RAP}")

        st.success(f"PAPi: {PAPi_fick:.2f}")

        if PAPi_fick < 1:
            st.error("⚠️ PAPi severamente disminuido")

        elif PAPi_fick < 1.5:
            st.warning("⚠️ PAPi bajo")

        else:
            st.info("PAPi conservado")

    # ---------------------------
    # DYN·S·CM⁻⁵
    # ---------------------------

    mostrar_dyn_fick = st.checkbox(
        "Mostrar resistencias Fick en dyn·s·cm⁻⁵"
    )

    if mostrar_dyn_fick:

        st.subheader("Conversión dyn·s·cm⁻⁵")

        st.info(f"RVP: {PVR_fick * 80:.2f} dyn·s·cm⁻⁵")
        st.info(f"RVS: {SVR_fick * 80:.2f} dyn·s·cm⁻⁵")

        if SC:
            st.info(f"RVPI: {PVRI_fick * 80:.2f} dyn·s·cm⁻⁵·m²")
            st.info(f"RVSI: {SVRI_fick * 80:.2f} dyn·s·cm⁻⁵·m²")

else:

    st.info(
        "Calcule primero flujos por Fick para obtener hemodinámica avanzada."
    )

# ---------------------------
# HEMODINÁMICA AVANZADA / TERMODILUCIÓN
# ---------------------------

st.header("Hemodinámica avanzada / Termodilución")

st.warning(
    "La termodilución es útil para estimar gasto cardíaco cuando no hay cortocircuitos intracardíacos significativos. "
    "No debe usarse como método principal para calcular Qp/Qs en presencia de shunts."
)

usar_td = st.checkbox("Calcular parámetros por termodilución")

if usar_td:

    col_td1, col_td2 = st.columns(2)

    with col_td1:
        CO_td = st.number_input("Gasto cardíaco por termodilución / CO (L/min)", min_value=0.0)
        FC_td = st.number_input("Frecuencia cardíaca para termodilución (lpm)", min_value=1)

        sPAP_td = st.number_input("sPAP TD (mmHg)", min_value=0.0)
        dPAP_td = st.number_input("dPAP TD (mmHg)", min_value=0.0)
        mPAP_td = st.number_input("mPAP TD (mmHg)", min_value=0.0)

    with col_td2:
        RAP_td = st.number_input("RAP TD (mmHg)", min_value=0.0)
        PAWP_td = st.number_input("PAWP / wedge TD (mmHg)", min_value=0.0)
        MAP_td = st.number_input("MAP TD (mmHg)", min_value=0.0)

    if CO_td > 0:

        st.subheader("Gasto cardíaco e índice cardíaco")

        st.success(f"Gasto cardíaco por termodilución: {CO_td:.2f} L/min")

        if SC:
            CI_td = CO_td / SC
            st.success(f"Índice cardíaco por termodilución: {CI_td:.2f} L/min/m²")

            if CI_td < 2.0:
                st.error("⚠️ Índice cardíaco severamente disminuido.")
            elif CI_td < 2.5:
                st.warning("⚠️ Índice cardíaco bajo.")
            elif CI_td <= 4.0:
                st.info("Índice cardíaco dentro de rango esperado.")
            else:
                st.warning("Índice cardíaco elevado.")
        else:
            CI_td = None
            st.warning("Ingrese peso y talla para calcular índice cardíaco.")

        st.subheader("Volumen sistólico")

        SV_td = (CO_td * 1000) / FC_td
        st.success(f"Volumen sistólico: {SV_td:.2f} mL")

        if SC:
            SVI_td = SV_td / SC
            st.success(f"Índice de volumen sistólico: {SVI_td:.2f} mL/m²")
        else:
            SVI_td = None

        st.subheader("Gradiente transpulmonar")

        TPG_td = mPAP_td - PAWP_td
        st.success(f"Gradiente transpulmonar TD: {TPG_td:.2f} mmHg")

        st.subheader("Resistencia vascular pulmonar")

        PVR_td = TPG_td / CO_td
        st.latex(r"RVP = \frac{mPAP - PAWP}{CO}")
        st.success(f"RVP no indexada TD: {PVR_td:.2f} Wood units")

        if SC:
            PVRI_td = PVR_td * SC
            st.success(f"RVP indexada TD: {PVRI_td:.2f} Wood·m²")
        else:
            PVRI_td = None

        st.subheader("Resistencia pulmonar total")

        TPR_td = mPAP_td / CO_td
        st.latex(r"RPT = \frac{mPAP}{CO}")
        st.success(f"RPT TD: {TPR_td:.2f} Wood units")

        st.subheader("Resistencia vascular sistémica")

        SVR_td = (MAP_td - RAP_td) / CO_td
        st.success(f"RVS no indexada TD: {SVR_td:.2f} Wood units")

        if SC:
            SVRI_td = SVR_td * SC
            st.success(f"RVS indexada TD: {SVRI_td:.2f} Wood·m²")
        else:
            SVRI_td = None

        if SVR_td > 0:
            st.subheader("Relación RVP/RVS")
            st.success(f"Relación RVP/RVS TD: {PVR_td / SVR_td:.2f}")

        st.subheader("Compliance arterial pulmonar")

        if (sPAP_td - dPAP_td) > 0:
            PAC_td = SV_td / (sPAP_td - dPAP_td)
            st.latex(r"CAP = \frac{VS}{sPAP - dPAP}")
            st.success(f"Compliance arterial pulmonar TD: {PAC_td:.2f} mL/mmHg")

            if PAC_td < 2.3:
                st.warning("⚠️ Compliance arterial pulmonar reducida.")
        else:
            st.info("Ingrese sPAP y dPAP válidas para calcular compliance arterial pulmonar.")

        st.subheader("Pulmonary Artery Pulsatility Index (PAPi)")

        if RAP_td > 0:
            PAPi_td = (sPAP_td - dPAP_td) / RAP_td
            st.latex(r"PAPi = \frac{sPAP - dPAP}{RAP}")
            st.success(f"PAPi TD: {PAPi_td:.2f}")

            if PAPi_td < 1:
                st.error("⚠️ PAPi severamente disminuido.")
            elif PAPi_td < 1.5:
                st.warning("⚠️ PAPi bajo.")
            else:
                st.info("PAPi conservado.")
        else:
            st.info("Ingrese RAP mayor de 0 para calcular PAPi.")

        mostrar_dyn_td = st.checkbox("Mostrar termodilución en dyn·s·cm⁻⁵")

        if mostrar_dyn_td:
            st.subheader("Conversión a dyn·s·cm⁻⁵")

            st.info(f"RVP TD: {PVR_td * 80:.2f} dyn·s·cm⁻⁵")
            st.info(f"RVS TD: {SVR_td * 80:.2f} dyn·s·cm⁻⁵")

            if PVRI_td is not None:
                st.info(f"RVP indexada TD: {PVRI_td * 80:.2f} dyn·s·cm⁻⁵·m²")

            if SVRI_td is not None:
                st.info(f"RVS indexada TD: {SVRI_td * 80:.2f} dyn·s·cm⁻⁵·m²")

    else:
        st.info("Ingrese gasto cardíaco por termodilución para calcular parámetros.")

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

**Hipertensión pulmonar:**  
Humbert M, Kovacs G, Hoeper MM, et al.  
*2022 ESC/ERS Guidelines for the Diagnosis and Treatment of Pulmonary Hypertension.*  
European Respiratory Journal. 2023.
""")
