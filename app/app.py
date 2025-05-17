import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente de Evaluación Clínica", layout="centered")

# ----------------------------
# Función de predicción manual (simulada)
# ----------------------------
def predecir_supervivencia_simulada(input_df):
    row = input_df.iloc[0]
    proba = 0.95
    if row['cancer'] == 1:
        proba -= 0.3
    if row['epoc'] == 1:
        proba -= 0.2
    if row['enfermedad_cardiaca'] == 1:
        proba -= 0.2
    if row['diabetes'] == 1 and row['creatinina'] > 1.5:
        proba -= 0.15
    if row['edad'] > 80:
        proba -= 0.1
    if row['fumador'] == 1:
        proba -= 0.05
    if row['actividad_fisica'] == 0:
        proba -= 0.05
    if row['gastos_salud'] > 3000:
        proba -= 0.05
    return max(0.0, min(1.0, proba))

# ----------------------------
# Interfaz Streamlit
# ----------------------------

st.sidebar.title("Asistente de Evaluación Clínica")
menu = st.sidebar.radio("Menú", ["Evaluación del Riesgo", "Base de Pacientes", "Red Neuronal Predictiva"])

# ----------------------------
# Sección 1: Evaluación individual
# ----------------------------
if menu == "Evaluación del Riesgo":
    st.title("Evaluación Clínica del Paciente")
    st.markdown("Complete los datos clínicos para obtener una evaluación automatizada del estado general del paciente.")

    edad = st.slider("Edad", 18, 100, 60)
    ingresos = st.number_input("Ingresos mensuales (€)", 0, 10000, 1500)
    gastos = st.number_input("Gastos en salud (€)", 0, 5000, 300)
    glucosa = st.number_input("Glucosa (mg/dL)", 50, 300, 100)
    colesterol = st.number_input("Colesterol (mg/dL)", 100, 400, 200)
    creatinina = st.number_input("Creatinina (mg/dL)", 0.1, 10.0, 1.2)
    leucocitos = st.number_input("Leucocitos", 3000, 20000, 7000)

    cancer = st.selectbox("¿Diagnóstico de cáncer?", ["No", "Sí"])
    cardiaca = st.selectbox("¿Enfermedad cardíaca diagnosticada?", ["No", "Sí"])
    epoc = st.selectbox("¿EPOC diagnosticado?", ["No", "Sí"])
    hipertension = st.selectbox("¿Hipertensión arterial?", ["No", "Sí"])
    diabetes = st.selectbox("¿Diabetes diagnosticada?", ["No", "Sí"])
    fumador = st.selectbox("¿Fumador activo?", ["No", "Sí"])
    obesidad = st.selectbox("¿Diagnóstico de obesidad?", ["No", "Sí"])

    actividad_fisica = st.selectbox("Nivel de actividad física", ["0 - Sedentario", "1 - Moderado", "2 - Activo"])
    actividad_fisica_valor = int(actividad_fisica[0])

    if st.button("Evaluar"):
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

        proba = predecir_supervivencia_simulada(input_df)

        # -------------------- Resumen Clínico --------------------
        st.subheader("Resumen del Perfil Clínico")
        resumen = []
        resumen.append("Paciente mayor" if edad > 80 else "Paciente joven" if edad < 40 else "Paciente adulto")
        if cancer == "Sí":
            resumen.append("con diagnóstico de cáncer")
        elif epoc == "Sí":
            resumen.append("con EPOC")
        elif cardiaca == "Sí":
            resumen.append("con enfermedad cardíaca")
        elif diabetes == "Sí":
            resumen.append("con diabetes")
        else:
            resumen.append("sin patologías críticas actuales")
        st.markdown("**" + ", ".join(resumen).capitalize() + ".**")

        # -------------------- Probabilidad --------------------
        st.subheader("Probabilidad de estabilidad clínica")
        if proba > 0.8:
            st.success(f"{proba*100:.1f}%")
        elif proba > 0.6:
            st.warning(f"{proba*100:.1f}%")
        else:
            st.error(f"{proba*100:.1f}%")

        # -------------------- Aspectos --------------------
        factores = []
        positivos = []

        if edad > 80:
            factores.append("Edad avanzada (>80 años)")
        elif edad < 40:
            positivos.append("Edad joven (<40 años)")
        if cancer == "Sí":
            factores.append("Diagnóstico de cáncer")
        if epoc == "Sí":
            factores.append("Antecedente de EPOC")
        if cardiaca == "Sí":
            factores.append("Enfermedad cardíaca")
        if diabetes == "Sí" and creatinina > 1.5:
            factores.append("Diabetes con deterioro renal")
        if fumador == "Sí":
            factores.append("Tabaquismo activo")
        if actividad_fisica_valor == 0:
            factores.append("Sedentarismo")
        if gastos > 3000:
            factores.append("Gastos elevados en salud")
        if actividad_fisica_valor == 2:
            positivos.append("Buena actividad física")
        if fumador == "No":
            positivos.append("No fumador")
        if cancer == "No" and cardiaca == "No" and epoc == "No":
            positivos.append("Sin patologías críticas actuales")

        st.subheader("Aspectos a considerar")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Factores de riesgo**")
            if factores:
                for f in factores:
                    st.markdown(f"- {f}")
            else:
                st.markdown("- Ninguno relevante")
        with col2:
            st.markdown("**Aspectos positivos**")
            if positivos:
                for p in positivos:
                    st.markdown(f"- {p}")
            else:
                st.markdown("- Ninguno destacado")

        # -------------------- Sugerencias --------------------
        st.subheader("Sugerencias para el paciente")
        sugerencias = []
        if cancer == "Sí":
            sugerencias.append("Derivar a oncología para seguimiento periódico.")
        if epoc == "Sí":
            sugerencias.append("Valoración por neumología y pruebas de función respiratoria.")
        if cardiaca == "Sí":
            sugerencias.append("Control cardiológico y seguimiento con ECG y ecocardiograma.")
        if diabetes == "Sí":
            sugerencias.append("Reducir consumo de azúcares y programar revisión endocrinológica.")
        if fumador == "Sí":
            sugerencias.append("Ofrecer programas de cesación tabáquica y evaluación respiratoria.")
        if actividad_fisica_valor == 0:
            sugerencias.append("Recomendar inicio progresivo de actividad física supervisada.")

        if sugerencias:
            for s in sugerencias:
                st.markdown(f"- {s}")
        else:
            st.markdown("No se requieren acciones inmediatas, mantener controles rutinarios.")

        with st.expander("Ver datos ingresados"):
            st.dataframe(input_df.T)

# ----------------------------
# Sección 2: Visualización de pacientes
# ----------------------------
elif menu == "Base de Pacientes":
    st.title("Base de Pacientes Clasificados")
    st.markdown("""
    Visualización de una muestra representativa de pacientes con su **probabilidad estimada de supervivencia**.

    Las filas están codificadas por colores para facilitar la revisión clínica diaria:

    - 🟥 **Rojo**: Paciente en estado crítico 
    - 🟨 **Amarillo**: Paciente preocupante 
    - 🟩 **Verde**: Paciente estable 

    """)

    try:
        df = pd.read_csv("pacientes_con_probabilidad.csv")
        df_sample = df.sample(n=15, random_state=42).reset_index(drop=True)

        # ---------------- Estilo de colores en la tabla ----------------
        def highlight_row(row):
            val = row['probabilidad_supervivencia']
            if val > 0.8:
                color = '#d4edda'  # verde
            elif val > 0.6:
                color = '#fff3cd'  # amarillo
            else:
                color = '#f8d7da'  # rojo
            return ['background-color: {}'.format(color)] * len(row)

        styled_df = df_sample.style.apply(highlight_row, axis=1).hide(axis='index')
        st.dataframe(styled_df, use_container_width=True)

        # ---------------- Clasificación y sugerencias ----------------
        def clasificar_paciente(row):
            if row['probabilidad_supervivencia'] < 0.6:
                return "Atención médica urgente"
            elif row['probabilidad_supervivencia'] < 0.8:
                return "Seguimiento sugerido"
            else:
                return "Estable"

        def sugerencia_medica(row):
            sugerencias = []
            if row.get('cancer', 0) == 1:
                sugerencias.append("Derivar a oncología")
            if row.get('epoc', 0) == 1:
                sugerencias.append("Consulta en neumología")
            if row.get('enfermedad_cardiaca', 0) == 1:
                sugerencias.append("Evaluación cardiológica")
            if row.get('colesterol', 0) > 240:
                sugerencias.append("Control de lípidos")
            if row.get('diabetes', 0) == 1:
                sugerencias.append("Consulta endocrina")
            return ", ".join(sugerencias) if sugerencias else "Sin acciones inmediatas"

        df_sample['nivel_atencion'] = df_sample.apply(clasificar_paciente, axis=1)
        df_sample['sugerencia'] = df_sample.apply(sugerencia_medica, axis=1)

        # ---------------- Resumen del día ----------------
        st.markdown("### Resumen de revisión clínica automática")
        urgentes = df_sample[df_sample['nivel_atencion'] == "Atención médica urgente"]
        seguimiento = df_sample[df_sample['nivel_atencion'] == "Seguimiento sugerido"]
        estables = df_sample[df_sample['nivel_atencion'] == "Estable"]

        st.markdown(f"- **Pacientes en estado crítico**: {len(urgentes)}")
        st.markdown(f"- **Pacientes en seguimiento**: {len(seguimiento)}")
        st.markdown(f"- **Pacientes estables**: {len(estables)}")
        st.markdown(f"- **Total de citas sugeridas**: {len(urgentes)}")

        # ---------------- Tabla pacientes urgentes ----------------
        st.markdown("###  Asignación de citas clínicas para pacientes críticos")

        if not urgentes.empty:
            # Crear tabla binaria de derivaciones por especialidad
            citas_data = []
            for idx, row in urgentes.iterrows():
                citas_data.append({
                    "ID": row['id'] if 'id' in row else idx + 1,
                    "Edad": row['edad'],
                    "Estabilidad (%)": f"{row['probabilidad_supervivencia']*100:.1f}",
                    "Oncología": "✅" if row['cancer'] == 1 else "",
                    "Cardiología": "✅" if row['enfermedad_cardiaca'] == 1 else "",
                    "Neumología": "✅" if row['epoc'] == 1 else "",
                    "Endocrinología": "✅" if row['diabetes'] == 1 else "",
                    "Control de lípidos": "✅" if row['colesterol'] > 240 else ""
                })

            citas_df = pd.DataFrame(citas_data)

            # Mostrar la tabla con estilo
            st.dataframe(citas_df.style.set_properties(**{
                'text-align': 'center'
            }), use_container_width=True)

            # Botón de descarga
            csv = citas_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=" Descargar listado de citas",
                data=csv,
                file_name='citas_pacientes_criticos.csv',
                mime='text/csv'
            ) 
        else:
            st.success("No hay pacientes que requieran atención médica urgente en esta muestra.")
    except FileNotFoundError:
        st.error("El archivo 'pacientes_con_probabilidad.csv' no se ha encontrado.")

elif menu == "Red Neuronal Predictiva":
    st.title(" Modelo de Red Neuronal para Evaluación Clínica")

    st.markdown("""
    Hemos desarrollado y entrenado una red neuronal para estimar la **probabilidad de estabilidad clínica** de un paciente
    en función de variables clínicas, sociodemográficas y de estilo de vida.
    """)
    st.markdown("""
    La arquitectura del modelo base se compone de una red neuronal sencilla pero eficaz, entrenada con datos clínicos reales de pacientes.  
    Este modelo toma como entrada  variables clínicas, demográficas y de estilo de vida del paciente y está diseñado con:

    - Una **capa** de 16 neuronas con función de activación *ReLU*, que permite modelar relaciones no lineales complejas entre las variables.
    - Una **capa de Dropout** con probabilidad del 40 % para prevenir el *overfitting*, desactivando aleatoriamente algunas neuronas durante el entrenamiento.
    - Una **capa de salida** con una única neurona y activación *sigmoid*, que devuelve un valor entre 0 y 1, interpretado como la **probabilidad estimada de supervivencia** del paciente.
                
    Esta salida binaria permite clasificar a los pacientes como  **alto riesgo (0)** o **estables(1)**.
    """)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("img/baseline_model.png", caption="Arquitectura red")
    

    # ---------------------------
    st.subheader(" Curva de aprendizaje")
    st.markdown("""
    La evolución de la pérdida (*loss*) en el entrenamiento y validación muestra una tendencia estable y descendente,
    lo que indica que el modelo **aprende correctamente sin sobreajustarse**.
    """)
    st.image("img/loss_fuc.png", caption="Curva de pérdida en entrenamiento y validación")

    # ---------------------------
    st.subheader(" Matriz de confusión")
    st.markdown("""
    El modelo ha sido ajustado para priorizar la **minimización de errores en pacientes de alto riesgo clínico** (clase 0), 
    es decir, aquellos con baja probabilidad de supervivencia. El objetivo principal ha sido **maximizar el *Recall*** sobre estos casos 
    críticos para **reducir los falsos negativos**, es decir, evitar clasificar erróneamente como supervivientess a pacientes que fallecerán.

    Durante el proceso de entrenamiento, se probaron técnicas específicas para abordar el fuerte desbalance en las clases:

    - **Undersampling** de la clase mayoritaria.
    - **Class weights** para penalizar más los errores sobre la clase minoritaria.
    - **Focal Loss**, una función de pérdida adaptada a escenarios con desbalance extremo.

    A pesar de estos esfuerzos, **no se lograron mejoras significativas en el rendimiento predictivo sobre la clase minoritaria**. Se concluye que, para avanzar, es necesario **contar con más muestras de pacientes con desenlace adverso (clase 0)**, 
    ya que el desbalance actual **limita la capacidad del modelo para aprender patrones representativos** en esos casos.
    """)
    st.image("img/cfm.png", caption="Matriz de confusión en el conjunto de validación")

    # ---------------------------
    
    st.subheader("Aplicaciones futuras")
    st.markdown("""
    Este modelo puede ser integrado como un **sistema de apoyo a la decisión médica**, permitiendo:

    - **Monitorizar automáticamente** la estabilidad clínica de los pacientes tras cada consulta.
    - **Asignar citas periódicas o derivaciones** a especialistas en función del perfil clínico del paciente.
    - **Enviar recordatorios automáticos** (vía email o sistema interno) a pacientes clasificados como preocupantes, sin necesidad de intervención directa del médico.
    - **Visualizar diariamente los pacientes atendidos**, clasificados por niveles de riesgo, para priorizar actuaciones.

    Con este sistema, el profesional sanitario podría identificar rápidamente:
    - Qué pacientes requieren atención urgente o seguimiento estrecho.
    - Qué pacientes pueden mantenerse en control rutinario.
    - Qué especialidades médicas deben intervenir en cada caso (oncología, neumología, etc.).


    """)
    