# Loan Amortisation Calculator
# ==========================================================
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Loan Amortisation Calculator")
st.markdown("Enter your loan details below to calculate the repayment schedule, including extra payments.")

# ---------------------------------------------------------
# Inputs
# ---------------------------------------------------------
principal = st.number_input("Loan Amount", min_value=1000, value=500000, step=500)
annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.0, step=0.1)
extra_monthly = st.number_input("Extra Monthly Payment", min_value=0.0, step=10.0)
extra_annual = st.number_input("Extra Annual Payment (paid every 12th month)", min_value=0.0, step=100.0)
loan_term_years = st.slider("Loan Term (Years)", min_value=1, max_value=30, value=30)

# ---------------------------------------------------------
# Calculation logic (handles 0% and positive interest rates)
# ---------------------------------------------------------
def build_schedule(principal, annual_rate, extra_monthly, extra_annual, loan_term_years):
    total_months = loan_term_years * 12
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        minimum_payment = principal / total_months
    else:
        growth = (1 + monthly_rate) ** total_months
        minimum_payment = principal * monthly_rate * growth / (growth - 1)

    rows = []
    balance = principal
    month = 1

    while balance > 0 and month <= total_months:
        interest = balance * monthly_rate
        scheduled_principal = min(minimum_payment - interest, balance)
        remaining = balance - scheduled_principal

        # Absorb tiny floating-point remainders so the loan closes cleanly
        if remaining < 0.005:
            scheduled_principal += remaining
            remaining = 0

        annual_extra = extra_annual if month % 12 == 0 else 0
        extra_total = min(extra_monthly + annual_extra, remaining)

        # Extra amounts actually applied (the last month may need less than planned)
        monthly_applied = min(extra_monthly, extra_total)
        annual_applied = extra_total - monthly_applied

        balance = remaining - extra_total
        if balance < 0.005:
            balance = 0

        total_payment = scheduled_principal + extra_total + interest

        rows.append([
            month,
            round(minimum_payment, 2),
            round(monthly_applied, 2),
            round(annual_applied, 2),
            round(total_payment, 2),
            round(scheduled_principal, 2),
            round(interest, 2),
            round(balance, 2),
        ])
        month += 1

    return pd.DataFrame(rows, columns=[
        "Month", "Minimum Payment", "Extra Monthly", "Extra Annual",
        "Total Payment", "Scheduled Principal", "Interest Paid", "Remaining Balance",
    ])


# ---------------------------------------------------------
# Calculate and keep results in session state
# (so the page does not clear when the CSV download is clicked)
# ---------------------------------------------------------
if st.button("Calculate"):
    st.session_state["df"] = build_schedule(
        principal, annual_rate, extra_monthly, extra_annual, loan_term_years
    )

df = st.session_state.get("df")

if df is not None:
    st.success(f"Loan paid off in {len(df)} months")
    st.dataframe(df)
    st.download_button(
        "Download Schedule as CSV", df.to_csv(index=False),
        "amortisation_schedule.csv", "text/csv",
    )

    # -----------------------------------------------------
    # Line chart: remaining balance and total payment
    # -----------------------------------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Month"], y=df["Remaining Balance"], mode="lines", name="Remaining Balance"))
    fig.add_trace(go.Scatter(x=df["Month"], y=df["Total Payment"], mode="lines", name="Total Payment"))
    fig.update_layout(title="Loan Amortisation Schedule", xaxis_title="Month", yaxis_title="Amount ($)")
    st.plotly_chart(fig)

    # -----------------------------------------------------
    # Pie chart: where the money goes (slices add up to total paid)
    # -----------------------------------------------------
    total_interest = df["Interest Paid"].sum()
    total_scheduled_principal = df["Scheduled Principal"].sum()
    total_extra = df["Extra Monthly"].sum() + df["Extra Annual"].sum()

    fig_pie = go.Figure(data=[go.Pie(
        labels=["Scheduled Principal", "Extra Payments (principal)", "Interest"],
        values=[total_scheduled_principal, total_extra, total_interest],
        textinfo="label+value", hoverinfo="label+percent", hole=0.3,
    )])
    fig_pie.update_layout(title="Payment Distribution (total paid over the loan)")
    st.plotly_chart(fig_pie)

    # -----------------------------------------------------
    # Stacked bar chart: monthly breakdown
    # -----------------------------------------------------
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df["Month"], y=df["Scheduled Principal"], name="Scheduled Principal", marker_color="blue"))
    fig_bar.add_trace(go.Bar(x=df["Month"], y=df["Interest Paid"], name="Interest Paid", marker_color="orange"))
    fig_bar.add_trace(go.Bar(x=df["Month"], y=df["Extra Monthly"], name="Extra Monthly", marker_color="green"))
    fig_bar.add_trace(go.Bar(x=df["Month"], y=df["Extra Annual"], name="Extra Annual", marker_color="red"))
    fig_bar.update_layout(title="Monthly Breakdown of Payments", xaxis_title="Month",
                          yaxis_title="Amount ($)", barmode="stack")
    st.plotly_chart(fig_bar)
