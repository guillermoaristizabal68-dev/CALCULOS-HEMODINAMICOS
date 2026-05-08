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
    [
        "Datos",
        "Medidas",
        "Resultados Fick",
        "Termodilución",
        "Referencias"
    ]
)

# =========================================================
# TAB 1 - DATOS
# =========================================================

with tab_datos:

    st.header("Datos del paciente")

    col1, col2 = st.columns(2)

    with col1:

        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")

        tipo_documento = st.selectbox(
            "Tipo de documento",
            [
                "Registro civil",
                "Tarjeta de identidad",
                "Cédula",
                "Pasaporte",
                "Otro"
            ]
        )

        if tipo_documento == "Otro":
            tipo_documento_otro = st.text_input(
                "Especifique tipo de documento"
            )

        numero_documento = st.text_input("Número de documento")

        edad_numero = st.number_input(
            "Edad",
            min_value=0
        )

        edad_unidad = st.selectbox(
            "Unidad de edad",
            ["días", "meses", "años"]
        )

    with col2:

        peso = st.number_input(
            "Peso (kg)",
            min_value=0.0
        )

        talla = st.number_input(
            "Talla (cm)",
            min_value=0.0
        )

        institucion = st.text_input("Institución")

        aseguradora = st.text_input(
            "Aseguradora / EPS"
        )

        fecha = st.date_input(
            "Fecha del estudio",
            value=date.today()
        )

    # Edad en años
    if edad_unidad == "días":
        edad_anos = edad_numero / 365

    elif edad_unidad == "meses":
        edad_anos = edad_numero / 12

    else:
        edad_anos = edad_numero

    st.header("Datos fisiológicos")

    col3, col4 = st.columns(2)

    with col3:

        hb = st.number_input(
            "Hb (Hemoglobina) g/dL",
            min_value=0.0
        )

        fio2 = st.number_input(
            "FiO₂ (Fracción inspirada de oxígeno) %",
            min_value=21.0,
            max_value=100.0,
            value=21.0
        )

        FC = st.number_input(
            "FC (Frecuencia cardíaca) lpm",
            min_value=1
        )

    with col4:

        if peso > 0 and talla > 0:

            SC = (
                0.024265
                * (peso ** 0.5378)
                * (talla ** 0.3964)
            )

            st.success(
                f"SC (Superficie corporal): "
                f"{SC:.2f} m²"
            )

        else:
            SC = None

            st.info(
                "Ingrese peso y talla "
                "para calcular SC."
            )

        if hb > 0 and (hb < 5 or hb > 25):

            st.warning(
                "⚠️ Hemoglobina fuera "
                "de rango fisiológico habitual."
            )

        if fio2 > 30:

            st.warning(
                "⚠️ FiO₂ >30%: considerar "
                "oxígeno disuelto."
            )

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

    # =====================================================
    # VO2 DIRECTO
    # =====================================================

    if metodo_vo2 == "VO₂ medido directamente":

        vo2_indexado = st.number_input(
            "VO₂ indexado (mL/min/m²)",
            min_value=0.0
        )

        if vo2_indexado > 0:

            st.success(
                f"VO₂ indexado: "
                f"{vo2_indexado:.2f} mL/min/m²"
            )

    # =====================================================
    # SECKELER
    # =====================================================

    elif metodo_vo2 == "Ecuación de Seckeler":

        st.latex(
            r"VO_2 = 138 - 11\ln(edad)"
            r" - 0.022 \cdot FC + S - 4 \cdot Hb"
        )

        sexo = st.selectbox(
            "Sexo",
            ["Masculino", "Femenino"]
        )

        if edad_anos > 0 and hb > 0:

            sexo_valor = 10 if sexo == "Masculino" else 0

            vo2_indexado = (
                138
                - (11 * math.log(edad_anos))
                - (0.022 * FC)
                + sexo_valor
                - (4 * hb)
            )

            st.success(
                f"VO₂ estimado indexado: "
                f"{vo2_indexado:.2f} mL/min/m²"
            )

            if edad_anos < 1:

                st.info(
                    "Edad <1 año: se usó "
                    "edad en meses/12 o días/365."
                )

            if edad_anos < 3:

                st.warning(
                    "⚠️ Mayor riesgo de "
                    "inexactitud en <3 años."
                )

            if hb < 10:

                st.warning(
                    "⚠️ La anemia puede afectar "
                    "la precisión."
                )

    # =====================================================
    # LAFARGE
    # =====================================================

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

            st.success(
                f"VO₂ estimado indexado: "
                f"{vo2_indexado:.2f} mL/min/m²"
            )

            st.warning(
                "⚠️ Método histórico."
            )

            if edad_anos < 3:

                st.error(
                    "❌ Alta inexactitud "
                    "esperada en <3 años."
                )

# =========================================================
# TAB 2 - MEDIDAS
# =========================================================

with tab_medidas:

    st.header(
        "Medidas de saturación, "
        "pO₂ y presiones"
    )

    st.subheader(
        "Saturación venosa mixta"
    )

    metodo_vm = st.selectbox(
        "Método para estimar saturación venosa mixta",
        [
            "Usar solo VCS",
            "Calcular con VCS + VCI"
        ]
    )

    sat_vm = None
    po2_vm = None

    # =====================================================
    # SOLO VCS
    # =====================================================

    if metodo_vm == "Usar solo VCS":

        colv1, colv2, colv3 = st.columns(3)

        with colv1:

            sat_vcs = st.number_input(
                "Sat VCS (Saturación vena cava superior) %",
                min_value=0.0,
                max_value=100.0
            )

        with colv2:

            po2_vcs = st.number_input(
                "pO₂ VCS (Presión parcial O₂ VCS) mmHg",
                min_value=0.0
            )

        with colv3:

            presion_vcs = st.number_input(
                "RAP (Presión auricular derecha) mmHg",
                min_value=0.0
            )

        if sat_vcs > 0:

            sat_vm = sat_vcs

            st.success(
                f"Sat VM (Saturación venosa mixta): "
                f"{sat_vm:.1f}%"
            )

        if po2_vcs > 0:

            po2_vm = po2_vcs

            st.success(
                f"pO₂ VM: {po2_vm:.1f} mmHg"
            )

    # =====================================================
    # VCS + VCI
    # =====================================================

    else:

        st.latex(
            r"SatVM = \frac{(3 \times SatVCS)"
            r" + SatVCI}{4}"
        )

        colv1, colv2 = st.columns(2)

        with colv1:

            sat_vcs = st.number_input(
                "Sat VCS (%)",
                min_value=0.0,
                max_value=100.0
            )

            po2_vcs = st.number_input(
                "pO₂ VCS (mmHg)",
                min_value=0.0
            )

        with colv2:

            sat_vci = st.number_input(
                "Sat VCI (Saturación vena cava inferior) %",
                min_value=0.0,
                max_value=100.0
            )

            po2_vci = st.number_input(
                "pO₂ VCI (mmHg)",
                min_value=0.0
            )

        if sat_vcs > 0 and sat_vci > 0:

            sat_vm = (
                (3 * sat_vcs) + sat_vci
            ) / 4

            st.success(
                f"Sat VM: {sat_vm:.1f}%"
            )

        if po2_vcs > 0 and po2_vci > 0:

            po2_vm = (
                (3 * po2_vcs)
                + po2_vci
            ) / 4

            st.success(
                f"pO₂ VM: {po2_vm:.1f} mmHg"
            )

# =========================================================
# RESTO DE LA APP
# =========================================================

st.info(
    "Continúa usando exactamente el mismo "
    "patrón:\n\n"
    "Abreviatura + nombre completo entre paréntesis."
)
