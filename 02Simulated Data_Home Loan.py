# Simulated data for Home Loan Applications using Faker library

from faker import Faker
import random
import pandas as pd
import numpy as np
import os
import glob
from openpyxl import load_workbook

# Output files
fldr = os.path.join(os.path.expanduser("~"), "OneDrive", "Employment", "Self", "Coaching")
custinfo = os.path.join(fldr, 'Customer_info.xlsx')
clientgrpinfo = os.path.join(fldr, 'ClientGroup_info.xlsx')
applicationinfo = os.path.join(fldr, 'Application_info.xlsx')
homeloanproducts = os.path.join(fldr, 'HomeLoan_Products.xlsx')
applications = os.path.join(fldr, 'Applications.xlsx')

fake = Faker("")
# ==================================================
# Data 1: Customer Information
# ==================================================
num_records = 100
client_data = []

for i in range(num_records):
    customer_id = str(fake.unique.random_number(digits=6, fix_len=True))
    # Salutation is either Mr., Mrs., or Ms.
    salutation = random.choice(['Mr.', 'Mrs.', 'Ms.'])
    # Choose male/female names based on salutation
    if salutation == "Mr.":
        fname = fake.first_name_male()
        sex = "M"
    else:
        fname = fake.first_name_female()
        sex = "F"
    lname = fake.last_name()
    dob = fake.date_of_birth(minimum_age=21, maximum_age=65)
    # Email: last name + first 3 letters of first name
    email = f"{lname.lower()}.{fname[:3].lower()}@{fake.free_email_domain()}"
    employment_status = random.choice(['Employed', 'Self-Employed'])
    annual_income = round(random.uniform(30000, 150000), 2)
    # Residential Address in Australia
    residential_address = fake.street_address()
    residential_city = random.choice(['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'])
    # Append to list
    client_data.append({
        "CustomerID": customer_id,
        "Salutation": salutation,
        "FirstName": fname,
        "LastName": lname,
        "Sex": sex,
        "DOB": dob,
        "EmploymentStatus": employment_status,
        "AnnualIncome": annual_income,
        "ResidentialAddress": residential_address,
        "ResidentialCity": residential_city
    })

# Convert to DataFrame
df_customer_info = pd.DataFrame(client_data)

# ==================================================
# Date 2: Client Group Information
# Build Relationship: If Last Name is same then relationship can be Spouse, Siblings, Parent-Child etc. They share same Client Group ID
# If relationship == 'None' generate separate unique Client Group ID

# Reproducibility
random.seed(42)
fake = Faker()
Faker.seed(42)

def assign_client_groups(df_customer_info: pd.DataFrame) -> pd.DataFrame:
    client_group_rows = []
    # Optional: control relationship distribution
    rel_weights = {'Spouse': 0.50, 'Sibling': 0.50}

    # Helper to sample relationship by weights
    def sample_relationship(allow_spouse=True):
        choices = list(rel_weights.keys())
        weights = list(rel_weights.values())
        if not allow_spouse:
            # Normalize weights without Spouse
            idx = choices.index('Spouse')
            choices.pop(idx)
            weights.pop(idx)
            total = sum(weights)
            weights = [w/total for w in weights]
        return random.choices(choices, weights=weights, k=1)[0]

    # Process by last name groups
    for lastname, group in df_customer_info.groupby('LastName', sort=False):
        group_size = len(group)

        if group_size == 1:
            # Single occurrence → None relationship, unique group ID
            relationship = 'None'
            group_id = str(fake.unique.random_number(digits=5, fix_len=True))
            for _, row in group.iterrows():
                client_group_rows.append({
                    'Customer_ID': row['CustomerID'],
                    'Client_Group_ID': group_id,
                    'FirstName': row['FirstName'],
                    'LastName': row['LastName'],
                    'Relationship': relationship
                })
        else:
            # Multiple occurrences → choose relationship
            allow_spouse = (group_size % 2 == 0)  # spouse implies pairs
            relationship = sample_relationship(allow_spouse=allow_spouse)
            group_id = str(fake.unique.random_number(digits=5, fix_len=True))

            for _, row in group.iterrows():
                client_group_rows.append({
                    'Customer_ID': row['CustomerID'],
                    'Client_Group_ID': group_id,
                    'FirstName': row['FirstName'],
                    'LastName': row['LastName'],
                    'Relationship': relationship
                })

    return pd.DataFrame(client_group_rows)

# Create DataFrame for Client Group Information
df_client_group_info = assign_client_groups(df_customer_info)

# ===================================================
# Data 3: Home Loan Products
# Define Home Loan Products
home_loan_products = [
    {'ProductID': 'HL001', 'ProductName': 'Standard Variable Rate', 'InterestRate': 5.25},
    {'ProductID': 'HL002', 'ProductName': 'Fixed Rate 1 Year', 'InterestRate': 4.75},
    {'ProductID': 'HL003', 'ProductName': 'Fixed Rate 3 Years', 'InterestRate': 4.50},
    {'ProductID': 'HL004', 'ProductName': 'Interest Only Loan', 'InterestRate': 5.50},
    {'ProductID': 'HL005', 'ProductName': 'Re-Finance 5 Years', 'InterestRate': 6.00}
]
# Convert to DataFrame
df_home_loan_products = pd.DataFrame(home_loan_products)

# ===================================================
# Data 4: Application Forms
# Generate Application forms for each customer group. ie. one application form per Client Group ID
# Add Loan Amount and Loan Term to each application form
# Loan Amount has to be between 5000 to 500000. Loan Amount is related to annual income of customers in the group.
# Loan Amount has to be in 1000s (not like 12345.67). For e.g., 5000, 12,000, 250,000 etc.
# Loan Term: 15, 20, 25, 30 years
# Calculate total annual income from df_customer_info for each client group 
# Calculate total annual expense for each client group

client_group_income = {}
for client_group_id, group in df_client_group_info.groupby('Client_Group_ID', sort=False):
    customer_ids = group['Customer_ID'].tolist()
    income_sum = df_customer_info[df_customer_info['CustomerID'].isin(customer_ids)]['AnnualIncome'].sum()
    client_group_income[client_group_id] = income_sum

# Total expense is between 50% to 80% of total income (randomly)
client_group_expense = {}
for client_group_id, income in client_group_income.items():
    expense = round(income * random.uniform(0.5, 0.8), 2)
    client_group_expense[client_group_id] = expense
# Add channel of application: Online, Branch, Broker

# Generate application forms
application_forms = []
for client_group_id, group in df_client_group_info.groupby('Client_Group_ID', sort=False):

    customer_ids = group['Customer_ID'].tolist()
    # Add Total Income and Expense from client_group_income and client_group_expense dicts
    total_income = client_group_income[client_group_id]
    total_expense = client_group_expense[client_group_id]

    # Generate Fake Application ID
    application_id = str(fake.unique.random_number(digits=7, fix_len=True))
    # Add home loan details
    home_loan_product = random.choice(home_loan_products)

    # Loan Amount between 50000 to 1000000
    loan_amount = random.randrange(5000, 500000, 1000)

    loan_term_years = random.choice([15, 20, 25, 30])
    application_channel = random.choice(['Online', 'Branch'])

    application_forms.append({
        'Customer_IDs': customer_ids,
        'Client_Group_ID': client_group_id,
        'Total_Annual_Income': total_income,
        'Total_Annual_Expense': total_expense,
        'ApplicationID': application_id,
        'ProductID': home_loan_product['ProductID'],
        'LoanAmount': loan_amount,
        'LoanTermYears': loan_term_years,
        'ApplicationChannel': application_channel
    })

# Dataframe for Application Forms
df_application_forms = pd.DataFrame(application_forms)

# ===================================================
# Data 4B: Applicattion Status 
# Statuses: Submitted, Under Review, Approved, Disbursed, Rejected, Closed
# Note: An application can have multiple statuses over time. Once approved it can be disbursed or rejected etc.
# Two Types of Rejection: Initial Rejection (Under Review -> Rejected), Post Approval Rejection (Approved -> Rejected)
# Approval Rule: If total expense < 70% of total income then higher chance of approval.
# Reason for Rejected: High Expense to Income Ratio, Incomplete Documents, Client History, Client Refusal etc

# Calculate Timestamp for each status change
from datetime import timedelta

def get_base_date():
    # Start date for application — random within the year
    return fake.date_time_this_year()

def build_status_sequence(expense_income_ratio: float) -> list[dict]:
    """
    Returns a list of status dicts in the correct logical order.
    """
    seq = [
        {'Status': 'Submitted'},
        {'Status': 'Under Review'}
    ]

    if expense_income_ratio < 0.7:
        if random.random() < 0.8:
            seq.append({'Status': 'Approved'})
            seq.append({'Status': 'Disbursed'})
        else:
            seq.append({'Status': 'Approved'})
            seq.append({'Status': 'Rejected', 'Reason': 'Client Refusal'})
    else:
        if random.random() < 0.7:
            seq.append({'Status': 'Rejected', 'Reason': 'High Expense to Income Ratio'})
        else:
            seq.append({'Status': 'Approved'})
            seq.append({'Status': 'Disbursed'})
    return seq

def assign_daywise_timestamps(seq: list[dict]) -> list[dict]:
    """
    Assigns timestamps with realistic day gaps between stages.
    """
    current_ts = get_base_date()
    seq_with_ts = []

    for i, item in enumerate(seq):
        if i > 0:
            # Random day gap between stages: 1 to 5 days
            day_gap = random.randint(1, 5)
            current_ts += timedelta(days=day_gap)
        seq_with_ts.append({**item, 'Timestamp': current_ts})

    return seq_with_ts

# ===================================================
# Data 4B: Application Status (daywise timestamps)
# ===================================================
application_status_data = []

for _, app in df_application_forms.iterrows():
    client_group_id = app['Client_Group_ID']
    application_id = app['ApplicationID']

    income = client_group_income[client_group_id]
    expense = client_group_expense[client_group_id]
    expense_income_ratio = expense / income

    # Build logical status sequence
    seq = build_status_sequence(expense_income_ratio)
    # Assign timestamps with realistic day gaps
    seq = assign_daywise_timestamps(seq)

    for row in seq:
        application_status_data.append({
            'ApplicationID': application_id,
            'Status': row['Status'],
            'Timestamp': row['Timestamp'],
            'Reason': row.get('Reason', '')
        })

# Dataframe for Application Status
df_application_status = pd.DataFrame(application_status_data)

# ===================================================
# Output to Excel files
# ===================================================
df_home_loan_products.to_excel(homeloanproducts, index=False)

with pd.ExcelWriter(custinfo, engine='openpyxl') as writer:
    df_customer_info.to_excel(writer, sheet_name='CustomerInfo', index=False)
    df_client_group_info.to_excel(writer, sheet_name='ClientGroupInfo', index=False)

with pd.ExcelWriter(applicationinfo, engine='openpyxl') as writer:
    df_application_forms.to_excel(writer, sheet_name='ApplicationForms', index=False)
    df_application_status.to_excel(writer, sheet_name='ApplicationStatus', index=False)