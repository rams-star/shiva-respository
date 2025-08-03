import streamlit as st
import pandas as pd

# Title and description
st.title("Loan Amortization Calculator")
st.markdown("Enter your loan details below to calculate the repayment schedule, including extra payments.")

# Input fields
principal = st.number_input("Loan Amount ($)", min_value=1000, step=500)
annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1)
extra_monthly = st.number_input("Extra Monthly Payment ($)", min_value=0.0, step=10.0)
extra_annual = st.number_input("Extra Annual Payment ($)", min_value=0.0, step=100.0)

# Calculation logic
def detailed_amortization_table(principal, annual_rate, extra_monthly, extra_annual):
    monthly_rate = annual_rate / 12 / 100
    minimum_monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** (30 * 12)) / ((1 + monthly_rate) ** (30 * 12) - 1)
    
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
    df = detailed_amortization_table(principal, annual_rate, extra_monthly, extra_annual)
    st.success(f"Loan Paid Off in {len(df)} Months")
    st.dataframe(df)

    # Offer download
    st.download_button("Download Schedule as CSV", df.to_csv(index=False), "amortization_schedule.csv", "text/csv")

# Note: This code is designed to run in a Streamlit environment.

# ==============================
# Adjustable Parameters
# ==============================
st.sidebar.header("Adjustable Parameters")
st.sidebar.markdown("You can adjust the parameters below to see how they affect the amortization schedule.")
st.sidebar.number_input("Loan Amount ($)", min_value=1000, step=500, value=principal)
st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1, value=annual_rate)
st.sidebar.number_input("Extra Monthly Payment ($)", min_value=0.0, step=10.0, value=extra_monthly)
st.sidebar.number_input("Extra Annual Payment ($)", min_value=0.0, step=100.0, value=extra_annual)


# ==============================
# Visualization
# ==============================
# Scatter plot of remaining balance and total payment over time
# if not df.empty:
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df['Month'], y=df['Remaining Balance'], mode='lines+markers', name='Remaining Balance'))
#     fig.add_trace(go.Scatter(x=df['Month'], y=df['Total Payment'], mode='lines+markers', name='Total Payment'))

#     fig.update_layout(title='Loan Amortization Schedule',
#                       xaxis_title='Month',
#                       yaxis_title='Amount ($)',
#                       legend=dict(x=0, y=1, traceorder='normal'))

#     st.plotly_chart(fig)

# # Scatter plot of principal paid and interest paid over time
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(x=df['Month'], y=df['Principal Paid'], mode='lines+markers', name='Principal Paid'))
#     fig2.add_trace(go.Scatter(x=df['Month'], y=df['Interest Paid'], mode='lines+markers', name='Interest Paid'))

#     fig2.update_layout(title='Principal and Interest Payments Over Time',
#                        xaxis_title='Month',
#                        yaxis_title='Amount ($)',
#                        hovermode='x unified',
#                        legend=dict(x=0, y=1, traceorder='normal'))

#     st.plotly_chart(fig2, use_container_width=True)

# # Pie chart proportions of principal and interest paid
#     total_principal_paid = df['Principal Paid'].sum()
#     total_interest_paid = df['Interest Paid'].sum()

#     fig3 = go.Figure(data=[go.Pie(labels=['Principal Paid', 'Interest Paid'],
#                                    values=[total_principal_paid, total_interest_paid],
#                                    hole=0.3)])

#     fig3.update_layout(title='Total Payments Breakdown',
#                        legend=dict(x=0, y=1, traceorder='normal'))

#     st.plotly_chart(fig3, use_container_width=True)
    
# ==============================
# Put it all together
# ==============================
# This code is designed to run in a Streamlit environment.
# Make sure to run this script using `streamlit run LoanAmortisation_Web.py`
# to see the interactive web application.
# ==============================
# End of code 
# ==============================

# Note: This code is designed to run in a Streamlit environment.
# Make sure to run this script using `streamlit run LoanAmortisation_Web.py`
# to see the interactive web application.
# ==============================

