import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Loan calculation function
def calculate_amortisation(loan_amount, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    months = years * 12
    payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)

    data = []
    balance = loan_amount

    for i in range(1, months + 1):
        interest = balance * monthly_rate
        principal = payment - interest
        balance -= principal
        data.append([i, round(payment, 2), round(principal, 2), round(interest, 2), round(balance, 2)])

    df = pd.DataFrame(data, columns=["Month", "Payment", "Principal", "Interest", "Balance"])
    return df

# Streamlit interface
st.title("Loan Amortisation Calculator")

loan_amount = st.number_input("Loan Amount", min_value=1000, value=100000)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=5.0)
loan_term = st.number_input("Loan Term (Years)", min_value=1, value=30)

if st.button("Calculate"):
    df = calculate_amortisation(loan_amount, interest_rate, loan_term)
    st.write("### Amortisation Table")
    st.dataframe(df)

    st.write("### Remaining Balance Over Time")
    plt.plot(df["Month"], df["Balance"])
    plt.xlabel("Month")
    plt.ylabel("Remaining Balance")
    plt.grid(True)
    st.pyplot(plt)
