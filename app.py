import streamlit as st
import requests

API_URL = "http://98.80.188.42:8000" 

st.title("Customer Churn Prediction")
st.write("Enter customer details to predict churn probability.")


with st.form("churn_form"):
    age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
    credit_score = st.number_input("Credit Score", min_value=300, max_value=1000, value=600, step=1)
    geography = st.selectbox("Geography", options=["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", options=["Male", "Female"])    
    tenure = st.number_input("Tenure (years)", min_value=0, max_value=10, value=3, step=1)
    balance = st.number_input("Balance", min_value=0.0, value=1000.0, format="%.2f")
    num_of_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1, step=1)
    has_cr_card = st.selectbox("Has Credit Card", options=["Yes", "No"])
    is_active_member = st.selectbox("Is Active Member", options=["Yes", "No"])
    estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0, format="%.2f")

    submitted = st.form_submit_button("Predict")

    if submitted:
        payload = {
            "credit_score": credit_score,
            "geography": geography,
            "gender": gender,
            "age": age,
            "tenure": tenure,
            "balance": balance,
            "num_of_products": num_of_products,
            "has_cr_card": 1 if has_cr_card == "Yes" else 0,
            "is_active_member": 1 if is_active_member == "Yes" else 0,
            "estimated_salary": estimated_salary
        }

        try:
            with st.spinner("Predicting..."):
                response = requests.post(
                    f"{API_URL}/predict",
                    json=payload,
                    timeout=5
                )
        except requests.exceptions.RequestException:
            st.error("Backend not reachable. Please contact with Bikram")
            st.stop()

        if response.status_code != 200:
            st.error("Prediction failed. Please try again later.")
            st.stop()

        try:
            result = response.json()
        except ValueError:
            st.error("Invalid response from backend")
            st.stop()

        churn_pred = result["churn_prediction"]
        proba = result["churn_probability"]

        st.subheader("Churn Probability ⬇️")
        col1, col2 = st.columns(2)
        col1.metric("Stay Probability", f"{proba['no_churn']*100:.2f}%")
        col2.metric("Churn Probability", f"{proba['churn']*100:.2f}%")


        st.subheader("Prediction ⬇️")
        if proba["churn"] > 0.6:
            st.error("🚨 The customer is likely to leave.")
        elif proba["churn"] > 0.35:
            st.warning("⚠️ The customer has a moderate chance of leaving.")
        else:
            st.success("✅ The customer is likely to stay.")
            st.balloons()
