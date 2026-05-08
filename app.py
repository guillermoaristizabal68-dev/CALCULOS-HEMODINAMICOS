import streamlit as st
from datetime import date
import math

st.set_page_config(
    page_title="Calculadora Hemodinámica Cardiovascular",
    layout="wide"
)

st.title("Calculadora Hemodinámica Cardiovascular")

# =========================================================
# VARIABLES INICIALES
# =========================================================

SC = None
vo2_indexado = None

Ca = Cv = Cpv = Cpa = None
Qs_i = Qp_i = Qs = Qp = None

# =========================================================
# PESTAÑAS
# =========================================================

tab_datos, tab_medidas, tab_fick, tab_td, tab_ref = st.tabs(
    ["Datos", "Medidas", "Resultados Fick", "Termodilución", "Referencias"]
)

# =========================================================
# TAB 1 - DATOS
# =========================================================
with tab_datos:

    st.header("Datos básicos")

    col1, col2 = st.columns(2)

    with col1:
        edad_numero = st.number_input("Edad", min_value=0)
        edad_unidad = st.selectbox("Unidad de edad", ["días", "meses", "años"])

        peso = st.number_input("Peso (kg)", min_value=0.0)
        talla = st.number_input("Talla (cm)", min_value=0.0)

    with col2:
        hb = st.number_input("Hb (Hemoglobina) g/dL", min_value=0.0)

        fio2 = st.number_input(
            "FiO₂ (Fracción inspirada de oxígeno) %",
            min_value=21.0,
            max_value=100.0,
            value=21.0
        )

        FC = st.number_input("FC (Frecuencia cardíaca) lpm", min_value=1)

    # Edad en años
    if edad_unidad == "días":
        edad_anos = edad_numero / 365
    elif edad_unidad == "meses":
        edad_anos = edad_numero / 12
    else:
        edad_anos = edad_numero

    # Superficie corporal
    if peso > 0 and talla > 0:
        SC = 0.024265 * (peso ** 0.5378) * (talla ** 0.3964)
        st.success(f"SC (Superficie corporal): {SC:.2f} m²")
    else:
        SC = None
        st.info("Ingrese peso y talla para calcular SC.")

    if hb > 0 and (hb < 5 or hb > 25):
        st.warning("⚠️ Hemoglobina fuera de rango fisiológico habitual.")

    if fio2 > 30:
        st.warning("⚠️ FiO₂ >30%: considerar oxígeno disuelto.")

    st.header("Cálculo de VO₂")

    metodo_vo2 = st.selectbox(
        "Método de cálculo de VO₂",
        [
            "VO₂ medido directamente",
            "Ecuación de Seckeler",
            "Ecuación de LaFarge"
        ]
    )

    sexo = None

    if metodo_vo2 == "VO₂ medido directamente":

        vo2_indexado = st.number_input(
            "VO₂ indexado (mL/min/m²)",
            min_value=0.0
        )

        if vo2_indexado > 0:
            st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")

    elif metodo_vo2 == "Ecuación de Seckeler":

        st.latex(
            r"VO_2 = 138 - 11\ln(edad)"
            r" - 0.022 \cdot FC + S - 4 \cdot Hb"
        )

        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

        if edad_anos > 0 and hb > 0:
            sexo_valor = 10 if sexo == "Masculino" else 0

            vo2_indexado = (
                138
                - (11 * math.log(edad_anos))
                - (0.022 * FC)
                + sexo_valor
                - (4 * hb)
            )

            st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

            if edad_anos < 1:
                st.info("Edad <1 año: se usó edad en meses/12 o días/365.")

            if edad_anos < 3:
                st.warning("⚠️ Mayor riesgo de inexactitud en <3 años.")

            if hb < 10:
                st.warning("⚠️ La anemia puede afectar la precisión.")

    elif metodo_vo2 == "Ecuación de LaFarge":

        st.latex(
            r"VO_2 = 138.1 - 11.49\ln(edad)"
            r" + 0.378 \cdot FC"
        )

        if edad_anos > 0:
            vo2_indexado = (
                138.1
                - (11.49 * math.log(edad_anos))
                + (0.378 * FC)
            )

            st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

            st.warning("⚠️ Método histórico.")

            if edad_anos < 3:
                st.error("❌ Alta inexactitud esperada en <3 años.")

# =========================================================
# TAB 2 - MEDIDAS
# =========================================================

with tab_medidas:

    st.header("Medidas de saturación, pO₂ y presiones")

    st.subheader("Saturación venosa mixta")

    metodo_vm = st.selectbox(
        "Método para estimar saturación venosa mixta",
        ["Usar solo VCS", "Calcular con VCS + VCI"]
    )

    sat_vm = None
    po2_vm = None

    if metodo_vm == "Usar solo VCS":

        colv1, colv2, colv3 = st.columns(3)

        with colv1:
            sat_vcs = st.number_input("Sat VCS (%)", min_value=0.0, max_value=100.0)

        with colv2:
            po2_vcs = st.number_input("pO₂ VCS (mmHg)", min_value=0.0)

        with colv3:
            presion_vcs = st.number_input("Presión VCS/RAP (mmHg)", min_value=0.0)

        if sat_vcs > 0:
            sat_vm = sat_vcs
            st.success(f"Sat venosa mixta estimada: {sat_vm:.1f}%")

        if po2_vcs > 0:
            po2_vm = po2_vcs
            st.success(f"pO₂ venosa mixta estimada: {po2_vm:.1f} mmHg")

    else:

        st.latex(r"SatVM = \frac{(3 \times SatVCS) + SatVCI}{4}")

        colv1, colv2 = st.columns(2)

        with colv1:
            sat_vcs = st.number_input("Sat VCS (%)", min_value=0.0, max_value=100.0)
            po2_vcs = st.number_input("pO₂ VCS (mmHg)", min_value=0.0)

        with colv2:
            sat_vci = st.number_input("Sat VCI (%)", min_value=0.0, max_value=100.0)
            po2_vci = st.number_input("pO₂ VCI (mmHg)", min_value=0.0)

        if sat_vcs > 0 and sat_vci > 0:
            sat_vm = ((3 * sat_vcs) + sat_vci) / 4
            st.success(f"Sat venosa mixta calculada: {sat_vm:.1f}%")

        if po2_vcs > 0 and po2_vci > 0:
            po2_vm = ((3 * po2_vcs) + po2_vci) / 4
            st.success(f"pO₂ venosa mixta calculada: {po2_vm:.1f} mmHg")

    st.subheader("Muestras principales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Aorta / sistémica**")
        sat_ao = st.number_input("Sat Ao (%)", min_value=0.0, max_value=100.0)
        pao2 = st.number_input("PaO₂ Ao (mmHg)", min_value=0.0)
        MAP = st.number_input("MAP / presión arterial media (mmHg)", min_value=0.0)

    with col2:
        st.markdown("**Arteria pulmonar**")
        sat_pa = st.number_input("Sat AP (%)", min_value=0.0, max_value=100.0)
        po2_pa = st.number_input("pO₂ AP (mmHg)", min_value=0.0)
        sPAP = st.number_input("sPAP (mmHg)", min_value=0.0)
        dPAP = st.number_input("dPAP (mmHg)", min_value=0.0)
        mPAP = st.number_input("mPAP (mmHg)", min_value=0.0)

    with col3:
        st.markdown("**Vena pulmonar / AI**")
        sat_pv = st.number_input(
            "Sat VP/AI (%)",
            min_value=0.0,
            max_value=100.0,
            value=98.0
        )
        po2_pv = st.number_input("pO₂ VP/AI (mmHg)", min_value=0.0)
        PAWP = st.number_input("PAWP / wedge / AI (mmHg)", min_value=0.0)
        RAP = st.number_input("RAP / AD media (mmHg)", min_value=0.0)

    st.header("Contenido de oxígeno")

    st.latex(r"Contenido\ O_2 = Hb(g/L) \times 1.36 \times Sat + pO_2 \times 0.03")

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
            st.success(f"Contenido venoso pulmonar / AI: {Cpv:.2f} mL/L")

        if sat_pa > 0:
            Cpa = contenido_oxigeno(hb, sat_pa, po2_pa)
            st.success(f"Contenido arteria pulmonar: {Cpa:.2f} mL/L")

    else:
        st.info("Ingrese hemoglobina en la pestaña Datos.")

# =========================================================
# TAB 3 - RESULTADOS FICK
# =========================================================

with tab_fick:

    st.header("Resultados por método de Fick")

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

                st.subheader("Flujos")

                colf1, colf2, colf3 = st.columns(3)

                with colf1:
                    st.metric("iQs", f"{Qs_i:.2f} L/min/m²")
                    st.metric("iQp", f"{Qp_i:.2f} L/min/m²")

                if SC:
                    Qs = Qs_i * SC
                    Qp = Qp_i * SC

                    with colf2:
                        st.metric("Qs", f"{Qs:.2f} L/min")
                        st.metric("Qp", f"{Qp:.2f} L/min")

                with colf3:
                    if Qs_i > 0:
                        qp_qs = Qp_i / Qs_i
                        st.metric("Qp/Qs", f"{qp_qs:.2f}")

                st.subheader("Hemodinámica avanzada Fick")

                if SC and Qs is not None and Qp is not None:

                    TPG = mPAP - PAWP

                    VS = (Qs * 1000) / FC
                    IVS = VS / SC

                    RVP = TPG / Qp
                    IRVP = RVP * SC

                    RPT = mPAP / Qp

                    RVS = (MAP - RAP) / Qs
                    IRVS = RVS * SC

                    colr1, colr2, colr3 = st.columns(3)

                    with colr1:
                        st.metric("TPG", f"{TPG:.2f} mmHg")
                        st.metric("VS", f"{VS:.2f} mL/latido")
                        st.metric("IVS", f"{IVS:.2f} mL/latido/m²")

                    with colr2:
                        st.metric("RVP", f"{RVP:.2f} WU")
                        st.metric("IRVP", f"{IRVP:.2f} WU·m²")
                        st.metric("RPT", f"{RPT:.2f} WU")

                    with colr3:
                        st.metric("RVS", f"{RVS:.2f} WU")
                        st.metric("IRVS", f"{IRVS:.2f} WU·m²")
                        if RVS > 0:
                            st.metric("RVP/RVS", f"{RVP/RVS:.2f}")

                    st.subheader("Compliance y PAPi")

                    colc1, colc2 = st.columns(2)

                    with colc1:
                        if (sPAP - dPAP) > 0:
                            CAP = VS / (sPAP - dPAP)
                            st.metric("CAP", f"{CAP:.2f} mL/mmHg")

                            if CAP < 2.3:
                                st.warning("⚠️ Compliance arterial pulmonar reducida.")

                    with colc2:
                        if RAP > 0:
                            PAPi = (sPAP - dPAP) / RAP
                            st.metric("PAPi", f"{PAPi:.2f}")

                            if PAPi < 1:
                                st.error("⚠️ PAPi severamente disminuido.")
                            elif PAPi < 1.5:
                                st.warning("⚠️ PAPi bajo.")
                            else:
                                st.info("PAPi conservado.")

                    if st.checkbox("Mostrar resistencias Fick en dyn·s·cm⁻⁵"):
                        st.info(f"RVP: {RVP * 80:.2f} dyn·s·cm⁻⁵")
                        st.info(f"RVS: {RVS * 80:.2f} dyn·s·cm⁻⁵")
                        st.info(f"IRVP: {IRVP * 80:.2f} dyn·s·cm⁻⁵·m²")
                        st.info(f"IRVS: {IRVS * 80:.2f} dyn·s·cm⁻⁵·m²")

                else:
                    st.info("Ingrese peso y talla para calcular parámetros no indexados y resistencias completas.")

            else:
                st.error("Las diferencias de contenido de oxígeno deben ser mayores de 0.")

        else:
            st.info("Complete los datos de contenido de oxígeno en la pestaña Medidas.")

    else:
        st.info("Ingrese o calcule VO₂ en la pestaña Datos.")

# =========================================================
# TAB 4 - TERMODILUCIÓN
# =========================================================

with tab_td:

    st.header("Termodilución")

    st.warning(
        "La termodilución es útil cuando no hay cortocircuitos intracardíacos significativos. "
        "No debe usarse como método principal para Qp/Qs en presencia de shunts."
    )

    coltd1, coltd2 = st.columns(2)

    with coltd1:
        CO_td = st.number_input("CO por termodilución (L/min)", min_value=0.0)
        sPAP_td = st.number_input("sPAP TD (mmHg)", min_value=0.0)
        dPAP_td = st.number_input("dPAP TD (mmHg)", min_value=0.0)
        mPAP_td = st.number_input("mPAP TD (mmHg)", min_value=0.0)

    with coltd2:
        PAWP_td = st.number_input("PAWP / wedge TD (mmHg)", min_value=0.0)
        RAP_td = st.number_input("RAP TD (mmHg)", min_value=0.0)
        MAP_td = st.number_input("MAP TD (mmHg)", min_value=0.0)
        FC_td = st.number_input("FC TD (lpm)", min_value=1)

    if CO_td > 0 and SC:

        CI_td = CO_td / SC
        VS_td = (CO_td * 1000) / FC_td
        IVS_td = VS_td / SC

        TPG_td = mPAP_td - PAWP_td

        RVP_td = TPG_td / CO_td
        IRVP_td = RVP_td * SC

        RPT_td = mPAP_td / CO_td

        RVS_td = (MAP_td - RAP_td) / CO_td
        IRVS_td = RVS_td * SC

        coltdr1, coltdr2, coltdr3 = st.columns(3)

        with coltdr1:
            st.metric("CO", f"{CO_td:.2f} L/min")
            st.metric("IC", f"{CI_td:.2f} L/min/m²")
            st.metric("VS", f"{VS_td:.2f} mL/latido")
            st.metric("IVS", f"{IVS_td:.2f} mL/latido/m²")

        with coltdr2:
            st.metric("TPG", f"{TPG_td:.2f} mmHg")
            st.metric("RVP", f"{RVP_td:.2f} WU")
            st.metric("IRVP", f"{IRVP_td:.2f} WU·m²")
            st.metric("RPT", f"{RPT_td:.2f} WU")

        with coltdr3:
            st.metric("RVS", f"{RVS_td:.2f} WU")
            st.metric("IRVS", f"{IRVS_td:.2f} WU·m²")

            if RVS_td > 0:
                st.metric("RVP/RVS", f"{RVP_td/RVS_td:.2f}")

        st.subheader("Compliance y PAPi")

        colcap, colpapi = st.columns(2)

        with colcap:
            if (sPAP_td - dPAP_td) > 0:
                CAP_td = VS_td / (sPAP_td - dPAP_td)
                st.metric("CAP", f"{CAP_td:.2f} mL/mmHg")

        with colpapi:
            if RAP_td > 0:
                PAPi_td = (sPAP_td - dPAP_td) / RAP_td
                st.metric("PAPi", f"{PAPi_td:.2f}")

        if st.checkbox("Mostrar TD en dyn·s·cm⁻⁵"):
            st.info(f"RVP: {RVP_td * 80:.2f} dyn·s·cm⁻⁵")
            st.info(f"RVS: {RVS_td * 80:.2f} dyn·s·cm⁻⁵")
            st.info(f"IRVP: {IRVP_td * 80:.2f} dyn·s·cm⁻⁵·m²")
            st.info(f"IRVS: {IRVS_td * 80:.2f} dyn·s·cm⁻⁵·m²")

    else:
        st.info("Ingrese CO por termodilución y superficie corporal.")

# =========================================================
# TAB 5 - REFERENCIAS
# =========================================================

with tab_ref:

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
