import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("student_performance_model.pkl", "rb") as file:
    model = pickle.load(file)


# Prediction function
def predict_performance(
    studytime,
    failures,
    absences,
    paid,
    activities,
    higher,
    internet,
    famrel,
    freetime,
    health
):

    # Study time mapping
    studytime_map = {
        "Less than 2 hours/week": 1,
        "2-5 hours/week": 2,
        "5-10 hours/week": 3,
        "More than 10 hours/week": 4
    }

    # Past failures mapping
    failures_map = {
        "No failures": 0,
        "1 failure": 1,
        "2 failures": 2,
        "3 failures": 3
    }

    studytime_val = studytime_map[studytime]
    failures_val = failures_map[failures]

    # IMPORTANT:
    # The trained model uses "yes"/"no", not 1/0
    paid_val = str(paid).lower()
    activities_val = str(activities).lower()
    higher_val = str(higher).lower()
    internet_val = str(internet).lower()

    # Create input dataframe
    student = pd.DataFrame({
        "studytime": [studytime_val],
        "failures": [failures_val],
        "absences": [absences],
        "paid": [paid_val],
        "activities": [activities_val],
        "higher": [higher_val],
        "internet": [internet_val],
        "famrel": [famrel],
        "freetime": [freetime],
        "health": [health]
    })

    # Prediction
    prediction = model.predict(student)[0]

    return prediction


# -----------------------------
# Streamlit App
# -----------------------------

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Performance Predictor")
st.write("Enter the student's details to predict their academic performance.")


# Study time
studytime = st.selectbox(
    "Study Time",
    [
        "Less than 2 hours/week",
        "2-5 hours/week",
        "5-10 hours/week",
        "More than 10 hours/week"
    ]
)


# Past failures
failures = st.selectbox(
    "Past Failures",
    [
        "No failures",
        "1 failure",
        "2 failures",
        "3 failures"
    ]
)


# Absences
absences = st.number_input(
    "Number of Absences",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)


# Paid classes
paid = st.selectbox(
    "Paid Extra Classes",
    ["Yes", "No"]
)


# Activities
activities = st.selectbox(
    "Participates in Extra-Curricular Activities",
    ["Yes", "No"]
)


# Higher education
higher = st.selectbox(
    "Wants to Pursue Higher Education",
    ["Yes", "No"]
)


# Internet
internet = st.selectbox(
    "Has Internet Access at Home",
    ["Yes", "No"]
)


# Family relationship
famrel = st.slider(
    "Family Relationship Quality",
    min_value=1,
    max_value=5,
    value=3
)


# Free time
freetime = st.slider(
    "Free Time After School",
    min_value=1,
    max_value=5,
    value=3
)


# Health
health = st.slider(
    "Current Health",
    min_value=1,
    max_value=5,
    value=3
)


# Prediction button
if st.button("Predict Performance"):
    result = predict_performance(
        studytime,
        failures,
        absences,
        paid,
        activities,
        higher,
        internet,
        famrel,
        freetime,
        health
    )

    st.subheader("Prediction Result")

    if result == "High Percentage":
        st.success("🎉 Predicted Performance: HIGH")
    elif result == "Average Percentage":
        st.info("📚 Predicted Performance: AVERAGE")
    elif result == "Low Percentage":
        st.warning("📖 Predicted Performance: LOW")
    else:
        st.write(f"Predicted Performance: {result}")
