##---------------------------------------------------------------------------
##MICHAEL OKAFOR - UK Supermarket Sales & Customer Analysis

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("retail_transactions_cleaned.csv")
dash=("-"*30)

print(f"{dash} MICHAEL OKAFOR {dash}")
print(f"{dash} UK Supermarket Sales & Customer Analysis {dash}")



df[df["Revenue"]>500]

df.groupby("ProductCategory")["Revenue"].sum().sort_values(ascending=False)

df.groupby("Location").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("OrderID", "nunique"))


##Revenue by month
print(f"{dash} revenue by month {dash}")
df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    format = "%m/%d/%Y"
    )

df["Month"] = df["OrderDate"].dt.month_name()
print(df.groupby("Month")["Revenue"].sum().sort_values(ascending=False))
##---------------------------------------------------------------------------
##Revenue by location
print(f"{dash} revenue by Location {dash}")
print(df.groupby("Location")["Revenue"].sum().sort_values(ascending=False))
##---------------------------------------------------------------------------
##Profit by category
print(f"{dash} Profit by category {dash}")
print(df.groupby("ProductCategory")["Profit"].sum().sort_values(ascending=False))
##---------------------------------------------------------------------------
##Customer spending distribution
print(f"{dash} Customer spending distribution {dash}")
customer_spending = df.groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False)
print(customer_spending.head(20))
customer_spending.plot(
    kind="hist",
    bins=20,
    edgecolor="black"
)

plt.title("Customer Spending Distribution")
plt.xlabel("Total Customer Spending (£)")
plt.ylabel("Number of Customers")
plt.show()
##---------------------------------------------------------------------------
##Discount vs profit
result = (df.groupby("ProductName").agg(
avg_Discount=("Discount","mean"),
Profit=("Profit","sum")
    ))
result["avg_Discount"] = result["avg_Discount"] * 100 
print(result)

##---------------------------------------------------------------------------
##Top 10 products
print(f"{dash} Top 10 products {dash}")
print(df.groupby("ProductName")["Revenue"].sum().sort_values(ascending=False).head(10))
##---------------------------------------------------------------------------

