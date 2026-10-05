# shiva-repository
This is my New GitHub Repository
# Loan Amortisation Calculator (Streamlit)

# Link to the application
https://loanamortisationwebpy-jzltmwlmoussnh946kbp8c.streamlit.app/

A small web app that calculates a loan repayment schedule and shows how extra repayments shorten the loan and reduce interest.

## What it does

Enter loan details and the app produces:

- A month-by-month schedule: minimum payment, extra payments, total payment, principal paid, interest paid and remaining balance.
- The number of months taken to pay off the loan.
- A CSV download of the schedule.
- Three charts: remaining balance vs total payment over time, payment distribution, and a monthly breakdown of principal and interest.

### Inputs

| Input | Description |
|---|---|
| Loan Amount | Amount borrowed (minimum 1,000) |
| Annual Interest Rate (%) | Nominal annual rate; 0% is supported |
| Extra Monthly Payment | Additional amount paid every month |
| Extra Annual Payment | Lump sum paid at the end of every 12th month |
| Loan Term (Years) | 1 to 30 years |

## How the calculation works

- Monthly rate = annual rate / 12 / 100.
- Minimum monthly payment uses the standard amortisation formula:
  `P × r × (1 + r)^n / ((1 + r)^n − 1)`, where P is the loan amount, r the monthly rate and n the number of months.
- Each month: interest = opening balance × monthly rate; principal = payment − interest; extra payments are then applied to principal.
- Payments are made at the end of each month (in arrears), and interest compounds monthly.
- The final payment is capped at the remaining balance.
- At 0% interest the loan is split into equal payments over the term.

### Sample check

Loan amount 500,000, rate 6%, term 30 years, no extras:

- Minimum monthly payment: **2,997.75** (matches Excel `=PMT(6%/12, 360, -500000)`)
- Paid off in 360 months, closing balance 0

## Setup and run

```bash
pip install -r requirements.txt
streamlit run LoanAmortisation_Web.py
```

The app opens in your browser (usually http://localhost:8501).

## How this was built

Built in Python with Streamlit, pandas and Plotly. The code was developed with AI coding assistance. I designed the requirements and reviewed and tested the logic, including a comparison of the minimum payment and schedule against standard amortisation calculations.

## Known limitations

- Extra annual payments are applied at months 12, 24, 36 and so on, not on a calendar date.
- Rates are assumed fixed for the whole term; no variable rates, offset accounts, fees or redraw.
- Results are illustrative and are not financial advice. Lenders' schedules may differ slightly (day-count conventions, payment frequency, rounding).
- Clicking "Download Schedule as CSV" refreshes the page in some Streamlit versions, which clears the displayed results. Click Calculate again.
