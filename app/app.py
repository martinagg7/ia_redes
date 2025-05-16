import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import joblib

# ----------------------------
# Cargar modelo, scaler y columnas
# ----------------------------
@st.cache_resource
def cargar_artifacts():
    modelo = load_model("model/baseline_model_tf.keras")
    scaler = joblib.load("model/scaler.save")
    columnas_modelo = [
        'cancer', 'gastos_salud', 'enfermedad_cardiaca', 'creatinina', 'epoc',
        'hipertension', 'diabetes', 'leucocitos', 'fumador', 'glucosa',
        'colesterol', 'edad', 'actividad_fisica', 'obesidad',
        'ingresos_mensuales'
    ]
    return modelo, scaler, columnas_modelo

modelo, scaler, columnas_modelo = cargar_artifacts()

# ----------------------------
# Función de predicción
# ----------------------------
def predecir_supervivencia(input_df):
    vars_a_escalar = [
        'gastos_salud', 'creatinina', 'leucocitos', 'glucosa',
        'colesterol', 'edad', 'ingresos_mensuales'
    ]
    input_df[vars_a_escalar] = scaler.transform(input_df[vars_a_escalar])
    input_df = input_df.reindex(columns=columnas_modelo)
    return modelo.predict(input_df)[0][0]

# ----------------------------
# Interfaz Streamlit
# ----------------------------
st.set_page_config(page_title="Asistente de Riesgo Clínico", layout="centered")
st.sidebar.title("Asistente de Riesgo Clínico")
menu = st.sidebar.radio("Ir a:", ["📊 Predicción"])

if menu == "📊 Predicción":
    st.title("📊 Predicción de Supervivencia")
    st.markdown("Introduce los datos del paciente:")

    # Entradas numéricas
    edad = st.slider("Edad", 18, 100, 60)
    ingresos = st.number_input("Ingresos mensuales (€)", 0, 10000, 1500)
    gastos = st.number_input("Gastos en salud (€)", 0, 5000, 300)
    glucosa = st.number_input("Glucosa (mg/dL)", 50, 300, 100)
    colesterol = st.number_input("Colesterol (mg/dL)", 100, 400, 200)
    creatinina = st.number_input("Creatinina (mg/dL)", 0.1, 10.0, 1.2)
    leucocitos = st.number_input("Leucocitos", 3000, 20000, 7000)

    # Entradas binarias
    cancer = st.selectbox("¿Tiene cáncer?", ["No", "Sí"])
    cardiaca = st.selectbox("¿Tiene enfermedad cardíaca?", ["No", "Sí"])
    epoc = st.selectbox("¿Tiene EPOC?", ["No", "Sí"])
    hipertension = st.selectbox("¿Tiene hipertensión?", ["No", "Sí"])
    diabetes = st.selectbox("¿Tiene diabetes?", ["No", "Sí"])
    fumador = st.selectbox("¿Fumador?", ["No", "Sí"])
    obesidad = st.selectbox("¿Tiene obesidad?", ["No", "Sí"])

    # Actividad física
    actividad_fisica = st.selectbox("Nivel de actividad física", [
        "0 - Sedentario", "1 - Moderado", "2 - Activo"
    ])
    actividad_fisica_valor = int(actividad_fisica[0])  # extraemos el número

    if st.button("Predecir"):
        input_df = pd.DataFrame({
            'edad': [edad],
            'ingresos_mensuales': [ingresos],
            'gastos_salud': [gastos],
            'glucosa': [glucosa],
            'colesterol': [colesterol],
            'creatinina': [creatinina],
            'leucocitos': [leucocitos],
            'actividad_fisica': [actividad_fisica_valor],
            'cancer': [1 if cancer == "Sí" else 0],
            'enfermedad_cardiaca': [1 if cardiaca == "Sí" else 0],
            'epoc': [1 if epoc == "Sí" else 0],
            'hipertension': [1 if hipertension == "Sí" else 0],
            'diabetes': [1 if diabetes == "Sí" else 0],
            'fumador': [1 if fumador == "Sí" else 0],
            'obesidad': [1 if obesidad == "Sí" else 0],
        })

        proba = predecir_supervivencia(input_df)
        st.metric("Probabilidad de Supervivencia", f"{proba*100:.1f} %")

        if proba < 0.4:
            st.error("Riesgo alto")
        elif proba < 0.7:
            st.warning("Riesgo medio")
        else:
            st.success("Riesgo bajo")