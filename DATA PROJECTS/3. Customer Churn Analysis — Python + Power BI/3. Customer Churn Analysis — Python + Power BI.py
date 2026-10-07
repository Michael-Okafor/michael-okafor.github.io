# ============================================================
# Customer Churn Analysis
# Author: Michael
# Tools: Python, Pandas, Matplotlib
#
# Objective:
# Analyse customer churn patterns across contract type,
# tenure, monthly charges, payment method and age.
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("customer_churn_dataset_10000_cleaned.csv")
print(df.shape)


# -------------------------------
# Data cleaning
# -------------------------------

df["Age"]=(df["Age"].astype(str).str.strip())
df["Customer ID"]=(df["Customer ID"].astype(str).str.strip())
df["Gender"]=(df["Gender"].astype(str).str.strip())
df["Contract type"]=(df["Contract type"].astype(str).str.strip())
df["Monthly charges"]=(df["Monthly charges"].astype(str).str.strip())
df["Total charges"]=(df["Total charges"].astype(str).str.strip())
df["Tenure"]=(df["Tenure"].astype(str).str.strip())
df["Payment method"]=(df["Payment method"].astype(str).str.strip())
df["Customer service calls"]=(df["Customer service calls"].astype(str).str.strip())
df["Churn"]=(df["Churn"].astype(str).str.strip())


df["Tenure"] = pd.to_numeric(df["Tenure"], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Monthly charges"] = pd.to_numeric(df["Monthly charges"], errors="coerce")
df["Total charges"] = pd.to_numeric(df["Total charges"], errors="coerce")
df["Customer service calls"] = pd.to_numeric(
    df["Customer service calls"], 
    errors="coerce"
)

# -------------------------------
# What percentage of customers have churned?
# -------------------------------

#churned = total churned/total users*100
print(df["Churn"].value_counts(dropna=False))

customers_lost = df[df["Churn"]=="Yes"]
customers_not_lost = df[df["Churn"]=="No"]
all_customers = (len(customers_not_lost)+len(customers_lost))

churned = (len(customers_lost)/len(customers_lost+customers_not_lost))*100
print(f"The percentage of customers that have churned is {churned}%")

# -------------------------------
# Which contract types have the highest churn?
# -------------------------------

churntract=(
    df.groupby("Contract type")["Churn"]
    .apply(lambda x:(x=="Yes").mean()*100))

print(churntract.map(lambda x:f"{x:.2f}%"))
highest_contract = churntract.idxmax()
highest_rate = churntract.max()

print(f"The contract with the highest churned customers is {highest_contract} customers at {highest_rate:.2f}% suggesting that customers without long lasting contracts were more prone to leave")

# -------------------------------
# Does churn increase for customers with short tenure?
# -------------------------------

df["Tenure Group"] = pd.cut(
    df["Tenure"],
    bins=[0, 12, 24, 48, float("inf")],
    labels=["0-12 months", "13-24 months", "25-48 months", "49+ months"]
)
tenure_churn = (
    df.groupby("Tenure Group", observed=True)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)
print(tenure_churn.map(lambda x:f"{x:.2f}%"))

print("Customers with shorter tenures have the highest churn rates, indicating that newer customers are more likely to leave.")

# -------------------------------
# Does monthly cost appear related to churn?
# -------------------------------

df["Monthly_pay Group"] = pd.cut(
    df["Monthly charges"],
    bins=[0,20,40,60,80,float("inf")],
    labels=["£0-20","£21-40","£41-60","£61-80","£81+"]
    )
monthly_churn = (
df.groupby("Monthly_pay Group",observed=True)["Churn"]
    .apply(lambda x:(x=="Yes").mean()*100)

    )
print(monthly_churn.map(lambda x:f"{x:.2f}%"))
print("Customers with the lowest monthly charges have the highest churn rate at 19.80%. However, the churn rate remains relatively stable across the higher monthly-charge groups, suggesting that monthly cost alone does not have a strong relationship with churn.")

# -------------------------------
# Which payment methods have the highest churn?
# -------------------------------

payment_to_churn=(
    df.groupby("Payment method")["Churn"]
    .apply(lambda x:(x=="Yes").mean()*100)
)
print(payment_to_churn.map(lambda x:f"{x:.2f}%"))
print(df["Payment method"].value_counts())

highest_churn_payment = payment_to_churn.idxmax()
highest_churn_payment_rate = payment_to_churn.max()
lowest_churn_payment = payment_to_churn.idxmin()
lowest_churn_payment_rate = payment_to_churn.min()

print(f"{highest_churn_payment} customers have the highest churn rate at {highest_churn_payment_rate:.2f}. Customers with an {lowest_churn_payment} payment method have a lower observed churn rate of {lowest_churn_payment_rate:.2f}, but this category should be treated cautiously because the actual payment method is unavailable.")


# -------------------------------
# Which customer groups have the highest churn
# -------------------------------

df["age_group"]=pd.cut(
    df["Age"],
    bins=[0,15,30,45,60,float("inf")],
    labels=["0-15","16-30","31-45","46-60","61+"]
    )

churn_by_age=(
    df.groupby("age_group",observed=True)["Churn"]
              .apply(lambda x:(x=="Yes").mean()*100)
)

print(churn_by_age.map(lambda x:f"{x:.2f}%"))

highest_churn_agegroup = churn_by_age.idxmax()
highest_churn_agegroup_rate = churn_by_age.max()
lowest_churn_agegroup = churn_by_age.idxmin()
lowest_churn_agegroup_rate = churn_by_age.min()

print(f"Customers aged {highest_churn_agegroup} years have the highest churn rate at {highest_churn_agegroup_rate:.2f}. Customers {lowest_churn_agegroup} have the lowest churn rate at {lowest_churn_agegroup_rate:.2f}. The relatively small difference between age groups suggests that age may not be a strong predictor of churn in this dataset")



