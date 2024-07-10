import streamlit as st
import os

# doesnt work yet
# # Function to read the visitor count
# def read_counter():
#     if not os.path.exists("counter.txt"):
#         with open("counter.txt", "w", encoding='utf-8') as f:
#             f.write("0")
#     with open("counter.txt", "r", encoding='utf-8') as f:
#         count = int(f.read().strip())
#     return count

# # Function to update the visitor count
# def update_counter():
#     count = read_counter() + 1
#     with open("counter.txt", "w", encoding='utf-8') as f:
#         f.write(str(count))
#     return count

# # Update the visitor counter
# visitor_count = update_counter()

# Updated tax brackets and rates from YA 2024 onwards
tax_brackets = [
    (20000, 0.02, 0),
    (30000, 0.035, 200),
    (40000, 0.07, 550),
    (80000, 0.115, 3350),
    (120000, 0.15, 7950),
    (160000, 0.18, 13950),
    (200000, 0.19, 21150),
    (240000, 0.195, 28750),
    (280000, 0.20, 36550),
    (320000, 0.22, 44550),
    (500000, 0.23, 84150),
    (1000000, 0.24, 199150)
]

# Placeholder personal reliefs and deductions
personal_reliefs = {
    "Earned Income Relief": 1000,
    "Spouse/handicapped spouse relief": 2000,
    "Qualifying/handicapped child relief": 4000,
    "Working mother's child relief": 15000,
    "Parent/handicapped parent relief": 9000,
    "Grandparent caregiver relief": 3000,
    "Handicapped brother/sister relief": 5500,
    "CPF/provident Fund relief": 17000,
    "Life Insurance relief": 5000,
    "Course fees relief": 5500,
    "Foreign domestic worker levy relief": 3000,
    "CPF cash top-up relief": 7000,
    "Supplementary Retirement Scheme (SRS) relief": 15000,
    "NSman (Self/wife/parent) relief": 3000
}

# Function to calculate personal income tax
def calculate_income_tax(chargeable_income):
    tax = 0
    previous_bracket_limit = 0

    for bracket_limit, rate, base_tax in tax_brackets:
        if chargeable_income > bracket_limit:
            continue
        else:
            tax = base_tax + (chargeable_income - previous_bracket_limit) * rate
            break
    return tax

# Streamlit app
st.title("myTaxAppSG")

st.header("Income Details")
employment_income = st.number_input("Enter your employment income (SGD):", min_value=0)
employment_expenses = st.number_input("Enter your employment expenses (SGD):", min_value=0)
net_employment_income = employment_income - employment_expenses

trade_income = st.number_input("Enter your trade, business, profession or vocation income (SGD):", min_value=0)

st.subheader("Other Income")
dividends = st.number_input("Enter your dividends income (SGD):", min_value=0)
interest = st.number_input("Enter your interest income (SGD):", min_value=0)
rent = st.number_input("Enter your rent from property income (SGD):", min_value=0)
royalty = st.number_input("Enter your royalty income (SGD):", min_value=0)
gains = st.number_input("Enter your gains or profits of an income nature (SGD):", min_value=0)

other_income = dividends + interest + rent + royalty + gains

total_income = net_employment_income + trade_income + other_income

st.header("Deductions and Reliefs")
approved_donations = st.number_input("Enter your approved donations (SGD):", min_value=0)
assessable_income = total_income - approved_donations

st.subheader("Personal Reliefs")
relief_selection = st.multiselect("Select applicable reliefs:", list(personal_reliefs.keys()))
selected_reliefs = {relief: personal_reliefs[relief] for relief in relief_selection}
total_reliefs = sum(selected_reliefs.values())

# Cap total personal reliefs at $80,000
total_reliefs = min(total_reliefs, 80000)

chargeable_income = assessable_income - total_reliefs

st.header("Tax Calculation")
parenthood_tax_rebate = st.number_input("Enter your parenthood tax rebate (SGD):", min_value=0)

if st.button("Calculate Tax"):
    tax_payable = calculate_income_tax(chargeable_income)
    net_tax_payable = tax_payable - parenthood_tax_rebate
    st.write(f"Total Income: SGD {total_income}")
    st.write(f"Approved Donations: SGD {approved_donations}")
    st.write(f"Assessable Income: SGD {assessable_income}")
    st.write(f"Total Reliefs: SGD {total_reliefs}")
    st.write(f"Chargeable Income: SGD {chargeable_income}")
    st.write(f"Tax Payable: SGD {tax_payable}")
    st.write(f"Parenthood Tax Rebate: SGD {parenthood_tax_rebate}")
    st.write(f"Net Tax Payable: SGD {net_tax_payable}")

st.sidebar.header("Developed by:")
linkedin_url = "https://www.linkedin.com/in/ng-johnson-35245a2a4/"
st.sidebar.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Ng Johnson`</a>', unsafe_allow_html=True)

st.sidebar.header("Tax Brackets")
st.sidebar.table(tax_brackets)

st.sidebar.header("Available Reliefs")
st.sidebar.table(personal_reliefs)