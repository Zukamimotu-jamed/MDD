
import pickle
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="💉")

# Load models
try:
    diabetes_model = pickle.load(open('diabetes.sav', 'rb'))
    heart_disease_model = pickle.load(open('heart.sav', 'rb'))
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# Input validation ranges
valid_ranges = {
    'Pregnancies': (0, 20),
    'Glucose': (50, 250),
    'BloodPressure': (40, 180),
    'SkinThickness': (7, 99),
    'Insulin': (10, 846),
    'BMI': (10.0, 67.0),
    'DiabetesPedigreeFunction': (0.0, 3.0),
    'Age': (0, 200),
    'age': (25, 90),
    'sex': (0, 1),
    'cp': (0, 3),
    'trestbps': (80, 200),
    'chol': (100, 600),
    'fbs': (0, 1),
    'restecg': (0, 2),
    'thalach': (60, 220),
    'exang': (0, 1),
    'oldpeak': (0.0, 6.2),
    'slope': (0, 2),
    'ca': (0, 3),
    'thal': (0, 2)
}

def validate_input(value, name):
    min_val, max_val = valid_ranges.get(name, (None, None))
    if min_val is not None and max_val is not None:
        if not (min_val <= value <= max_val):
            st.error(f"Invalid input for {name}: {value}. Must be between {min_val} and {max_val}.")
            return False
    return True

# Sidebar
with st.sidebar:
    selected = option_menu(
        'Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction'],
        menu_icon='hospital-fill',
        icons=['activity', 'heart'],
        default_index=0
    )

if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.text_input('Number of Pregnancies (enter 0 if male)')
    with col2: Glucose = st.text_input('Glucose Level')
    with col3: BloodPressure = st.text_input('Blood Pressure value')
    with col1: SkinThickness = st.text_input('Skin Thickness value')
    with col2: Insulin = st.text_input('Insulin Level')
    with col3: BMI = st.text_input('BMI value')
    with col1: DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2: Age = st.text_input('Age of the Person')

    if st.button('Diabetes Test Result'):
        try:
            inputs = {
                'Pregnancies': float(Pregnancies),
                'Glucose': float(Glucose),
                'BloodPressure': float(BloodPressure),
                'SkinThickness': float(SkinThickness),
                'Insulin': float(Insulin),
                'BMI': float(BMI),
                'DiabetesPedigreeFunction': float(DiabetesPedigreeFunction),
                'Age': float(Age)
            }
            if all(validate_input(v, k) for k, v in inputs.items()):
                user_input = np.array([[*inputs.values()]])
                prediction = diabetes_model.predict(user_input)
                if prediction[0] == 1:
                    st.error('The person is diabetic')
                    st.warning("⚠️ Untreated diabetes may lead to:\n"
                               "- Kidney Disease\n"
                               "- Heart Disease\n"
                               "- Vision Loss")

                    with st.expander("📘 Explore the many impacts of untreated diabetes"):
                        st.markdown("""
                ### 🩺 What Happens When Diabetes Goes Untreated?

                Diabetes silently damages organs and systems throughout the body. The elevated blood glucose acts like a corrosive agent over time.

                #### 🧠 Brain & Cognitive Function
                - Studies show increased risk of vascular dementia and cognitive decline.
                - Some researchers link long-term diabetes with a 50–100% increased risk of Alzheimer’s disease.

                #### 💓 Heart and Blood Vessels
                - Diabetics are 2–4x more likely to suffer heart attacks or strokes.
                - Chronic high blood sugar stiffens blood vessels, accelerating atherosclerosis.

                #### 🧍 Nerves
                - Diabetic neuropathy causes tingling, numbness, or burning sensations, often in the legs and feet.
                - More than 50% of diabetics experience some form of nerve damage.

                #### 👁️ Eyes
                - Retinopathy is caused by damage to the small blood vessels in the retina.
                - Diabetes is the leading cause of blindness in working-age adults.

                #### 🧪 Kidneys
                - Known as diabetic nephropathy, it begins with protein in urine and can end in kidney failure.
                - Diabetes accounts for nearly 44% of all new cases of kidney failure in the U.S.

                #### 📊 Global Snapshot
                - Over 537 million people live with diabetes (IDF, 2023).
                - 1 in 10 adults globally is affected.
                - Diabetes leads to 6.7 million deaths each year (that’s one every 5 seconds).

                """)

                else:
                    st.success('The person is not diabetic')
        except Exception as e:
            st.error(f"Prediction failed: {e}")

if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1: age = st.text_input('Age')
    with col2: sex = st.text_input('Sex')
    with col3: cp = st.text_input('Chest Pain types')
    with col1: trestbps = st.text_input('Resting Blood Pressure')
    with col2: chol = st.text_input('Serum Cholestoral in mg/dl')
    with col3: fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
    with col1: restecg = st.text_input('Resting Electrocardiographic results')
    with col2: thalach = st.text_input('Maximum Heart Rate achieved')
    with col3: exang = st.text_input('Exercise Induced Angina')
    with col1: oldpeak = st.text_input('ST depression induced by exercise')
    with col2: slope = st.text_input('Slope of the peak exercise ST segment')
    with col3: ca = st.text_input('Major vessels colored by flourosopy')
    with col1: thal = st.text_input('Thal (0=normal; 1=fixed; 2=reversible)')

    if st.button('Heart Disease Test Result'):
        try:
            inputs = {
                'age': float(age),
                'sex': float(sex),
                'cp': float(cp),
                'trestbps': float(trestbps),
                'chol': float(chol),
                'fbs': float(fbs),
                'restecg': float(restecg),
                'thalach': float(thalach),
                'exang': float(exang),
                'oldpeak': float(oldpeak),
                'slope': float(slope),
                'ca': float(ca),
                'thal': float(thal)
            }
            if all(validate_input(v, k) for k, v in inputs.items()):
                user_input = np.array([[*inputs.values()]])
                prediction = heart_disease_model.predict(user_input)
                if prediction[0] == 1:
                    st.error('The person has heart disease')
                    st.warning("⚠️ Untreated heart disease may lead to:\n"
                               "- Stroke\n"
                               "- Kidney Damage\n"
                               "- Heart Failure")

                    with st.expander("📘 What untreated heart disease can do"):
                        st.markdown("""
                    ### ❤️ Why You Should Never Ignore Heart Disease

                    Heart disease isn’t just about the heart. It’s about your entire circulatory system — and beyond.

                    #### 🧠 Stroke Risk
                    - Heart disease doubles the risk of stroke by promoting clots and blocking arteries to the brain.
                    - 1 in 4 stroke survivors has another stroke within 5 years.

                    #### 🫀 Heart Failure
                    - Over time, your heart struggles to keep up with the body's needs.
                    - Fluid may build up in the lungs, legs, and other areas — making daily life difficult.

                    #### 🧬 Kidney Breakdown
                    - Your kidneys rely on steady blood flow.
                    - When the heart fails, kidneys suffer too — increasing the chance of permanent damage.

                    #### 👣 Amputation Risk
                    - Reduced circulation and arterial blockage, especially in people with both heart disease and diabetes, can lead to limb loss.

                    #### 🪦 Sudden Cardiac Arrest
                    - 50% of people who die suddenly from heart issues had no prior symptoms.

                    #### 🌍 By the Numbers
                    - 17.9 million global deaths per year (WHO).
                    - Leading cause of death globally for over two decades.
                    - Costs the world economy $1 trillion annually in productivity loss and treatment.

                    """)

                else:
                    st.success('The person does not have heart disease')
        except Exception as e:
            st.error(f"Prediction failed: {e}")
