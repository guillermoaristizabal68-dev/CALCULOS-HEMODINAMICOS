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
# CONVERSIÓN DE EDAD A AÑOS
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

# ---------------------------
# VO2 MEDIDO DIRECTAMENTE
# ---------------------------

if metodo_vo2 == "VO₂ medido directamente":

    st.subheader("VO₂ medido directamente")

    st.markdown("""
    **Descripción:**  
    Ingreso manual del VO₂ medido directamente durante el procedimiento.

    **Ventajas:**
    - Método más preciso.
    - No depende de ecuaciones predictivas.
    - Recomendado cuando se requiere mayor precisión hemodinámica.
    - Especialmente útil en cardiopatías congénitas y pacientes complejos.

    **Limitaciones:**
    - Requiere equipo especializado.
    - No siempre está disponible en todos los laboratorios de hemodinamia.

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
                st.success(f"VO₂ absoluto estimado: {vo2_absoluto:.2f} mL/min")
            else:
                st.success(f"VO₂ indexado: {vo2_indexado:.2f} mL/min/m²")
                st.warning("Ingrese peso y talla para calcular VO₂ absoluto.")

        else:
            vo2_absoluto = vo2_manual

            if superficie_corporal:
                vo2_indexado = vo2_absoluto / superficie_corporal
                st.success(f"VO₂ absoluto: {vo2_absoluto:.2f} mL/min")
                st.success(f"VO₂ indexado estimado: {vo2_indexado:.2f} mL/min/m²")
            else:
                st.success(f"VO₂ absoluto: {vo2_absoluto:.2f} mL/min")
                st.warning("Ingrese peso y talla para calcular VO₂ indexado.")

# ---------------------------
# ECUACIÓN DE SECKELER
# ---------------------------

elif metodo_vo2 == "Ecuación de Seckeler":

    st.subheader("Ecuación de Seckeler")

    st.latex(r"VO_2 = 138 - 11\ln(edad) - 0.022 \cdot FC + S - 4 \cdot Hb")

    st.markdown("""
    **Resultado:** VO₂ indexado en mL/min/m².

    **Variables:**
    - Edad en años.
    - FC: frecuencia cardíaca en latidos por minuto.
    - S: sexo biológico, masculino = +10, femenino = 0.
    - Hb: hemoglobina en g/dL.

    **Ventajas:**
    - Diseñada en pacientes con cardiopatía congénita y adquirida.
    - Aplicable en niños y adultos.
    - Incluye variables fisiológicas relevantes como frecuencia cardíaca, sexo y hemoglobina.
    - Mejor desempeño que LaFarge en la población estudiada.

    **Limitaciones:**
    - Sigue siendo una estimación.
    - No reemplaza la medición directa de VO₂.
    - Puede ser menos precisa en menores de 3 años, pacientes con ventrículo único, anemia o pacientes críticamente enfermos.

    **Referencia:**  
    Seckeler MD, Hirsch R, Beekman RH, Goldstein BH.  
    *A New Predictive Equation for Oxygen Consumption in Children and Adults With Congenital and Acquired Heart Disease.*  
    Heart. 2015;101(7):517-24. PMID: 25429053.
    """)

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)
    hb = st.number_input("Hemoglobina (g/dL)", min_value=0.0)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)
        sexo_valor = 10 if sexo == "Masculino" else 0

        vo2_indexado = 138 - (11 * ln_edad) - (0.022 * fc) + sexo_valor - (4 * hb)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        if superficie_corporal:
            vo2_absoluto = vo2_indexado * superficie_corporal
            st.success(f"VO₂ absoluto estimado: {vo2_absoluto:.2f} mL/min")

        if edad_anos < 1:
            st.info("Edad <1 año: se usó edad en meses/12 o días/365 para evitar ln(0).")

        if edad_anos < 3:
            st.warning("⚠️ Mayor riesgo de inexactitud en menores de 3 años.")

        if hb < 10 and hb > 0:
            st.warning("⚠️ La anemia puede afectar la precisión del VO₂ estimado.")

    else:
        st.error("Ingrese una edad mayor de 0 para calcular VO₂ con Seckeler.")

# ---------------------------
# ECUACIÓN DE LAFARGE
# ---------------------------

elif metodo_vo2 == "Ecuación de LaFarge":

    st.subheader("Ecuación de LaFarge-Miettinen")

    st.latex(r"VO_2 = 138.1 - 11.49\ln(edad) + 0.378 \cdot FC")

    st.markdown("""
    **Resultado:** VO₂ indexado en mL/min/m².

    **Variables:**
    - Edad en años.
    - FC: frecuencia cardíaca en latidos por minuto.

    **Ventajas:**
    - Ecuación históricamente utilizada.
    - Fácil de aplicar.
    - Puede servir para comparación con cálculos antiguos.

    **Limitaciones:**
    - No recomendada como primera opción.
    - Menor precisión en pacientes pediátricos pequeños.
    - Especialmente problemática en menores de 3 años.
    - No incluye hemoglobina, sexo ni condición clínica del paciente.

    **Referencia:**  
    LaFarge CG, Miettinen OS.  
    *The estimation of oxygen consumption.*  
    Cardiovascular Research. 1970;4:23-30.
    """)

    fc = st.number_input("Frecuencia cardíaca (lpm)", min_value=0)

    if edad_anos > 0:
        ln_edad = math.log(edad_anos)

        vo2_indexado = 138.1 - (11.49 * ln_edad) + (0.378 * fc)

        st.success(f"VO₂ estimado indexado: {vo2_indexado:.2f} mL/min/m²")

        if superficie_corporal:
            vo2_absoluto = vo2_indexado * superficie_corporal
            st.success(f"VO₂ absoluto estimado: {vo2_absoluto:.2f} mL/min")

        st.warning("⚠️ Método histórico. No se recomienda como primera opción si hay VO₂ medido o Seckeler disponible.")

        if edad_anos < 3:
            st.error("❌ Alta inexactitud esperada en menores de 3 años.")

    else:
        st.error("Ingrese una edad mayor de 0 para calcular VO₂ con LaFarge.")
