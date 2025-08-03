# Loan Amortization Calculator
# ==========================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Title and description
st.title("Loan Amortization Calculator")
st.markdown("Enter your loan details below to calculate the repayment schedule, including extra payments.")

# Input fields
principal = st.number_input("Loan Amount", min_value=1000, step=500)
annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1)
extra_monthly = st.number_input("Extra Monthly Payment", min_value=0.0, step=10.0)
extra_annual = st.number_input("Extra Annual Payment", min_value=0.0, step=100.0)

loan_term_years = st.slider('Loan Term (Years)', min_value=1, max_value=30, value=30)
total_months = loan_term_years * 12

# Calculation logic
def detailed_amortization_table(principal, annual_rate, extra_monthly, extra_annual):
    monthly_rate = annual_rate / 12 / 100
    minimum_monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** (loan_term_years * 12)) / ((1 + monthly_rate) ** (loan_term_years * 12) - 1)
    
    schedule = []
    balance = principal
    month = 1

    while balance > 0:
        interest = balance * monthly_rate
        principal_payment = minimum_monthly_payment - interest
        annual_extra = extra_annual if month % 12 == 0 else 0
        total_extra = extra_monthly + annual_extra

        total_principal = principal_payment + total_extra
        if balance <= total_principal:
            total_principal = balance
            total_payment = balance + interest
            balance = 0
        else:
            balance -= total_principal
            total_payment = total_principal + interest

        schedule.append([
            month, round(minimum_monthly_payment, 2), extra_monthly, annual_extra,
            round(total_payment, 2), round(total_principal, 2), round(interest, 2), round(balance, 2)
        ])
        month += 1

    return pd.DataFrame(schedule, columns=[
        "Month", "Minimum Payment", "Extra Monthly", "Extra Annual",
        "Total Payment", "Principal Paid", "Interest Paid", "Remaining Balance"
    ])

# Display results
if st.button("Calculate"):
    if principal <= 0:
        st.error("Please enter valid loan details: Loan amount must be greater than 0.")
    
    elif annual_rate < 0:
        st.error("Interest rate must be zero or positive.")
    
    elif annual_rate == 0:
        # Zero-interest logic: Equal payments, no interest
        base_payment = principal / total_months
        balance = principal
        schedule = []

        for month in range(1, total_months + 1):
            annual_extra = extra_annual if month % 12 == 0 else 0
            total_extra = extra_monthly + annual_extra
            payment = base_payment + total_extra

            if balance <= payment:
                payment = balance
                balance = 0
            else:
                balance -= payment

            schedule.append([
                month,
                round(base_payment, 2),
                extra_monthly,
                annual_extra,
                round(payment, 2),
                round(payment, 2),
                0.0,
                round(balance, 2)
            ])
        
        df = pd.DataFrame(schedule, columns=[
            "Month", "Base Payment", "Extra Monthly", "Extra Annual",
            "Total Payment", "Principal Paid", "Interest Paid", "Remaining Balance"
        ])
        st.success(f"Loan Paid Off in {len(df)} Months (0% Interest)")
        st.dataframe(df)

    else:
        df = detailed_amortization_table(principal, annual_rate, extra_monthly, extra_annual)
        st.success(f"Loan Paid Off in {len(df)} Months")
        st.dataframe(df)

    # Download button safely placed after df creation
    st.download_button("Download Schedule as CSV", df.to_csv(index=False), "amortization_schedule.csv", "text/csv")

# ===========================================================
# Visualization
# ===========================================================
if 'df' in locals():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Remaining Balance'], mode='lines+markers', name='Remaining Balance'))
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Total Payment'], mode='lines+markers', name='Total Payment'))
    fig.update_layout(title='Loan Amortization Schedule', xaxis_title='Month', yaxis_title='Amount ($)')
    st.plotly_chart(fig)

    # Bar chart for monthly payments
    fig2, ax2 = plt.subplots()
    df.plot(x='Month', y=['Minimum Payment', 'Extra Monthly', 'Extra Annual'], kind='bar', ax=ax2)
    ax2.set_title('Monthly Payments Breakdown')
    ax2.set_ylabel('Payment Amount ($)')
    st.pyplot(fig2)





