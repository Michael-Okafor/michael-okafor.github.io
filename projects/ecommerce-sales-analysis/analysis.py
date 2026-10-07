import pandas as pd
print(pd.__version__)

excelFile = pd.read_excel("sales_data.xlsx")
print(excelFile.head())

print(excelFile.info())
print(excelFile.describe())


print(f"Number of Orders: {excelFile.shape[0]}")


print(f"Number of customers: {excelFile["Customer"].nunique()}")

excelFile["Order_Date"] = pd.to_datetime(excelFile["Order_Date"])
print("Date Starts:",excelFile["Order_Date"].min())
print("Date Ends:",excelFile["Order_Date"].max())

print("Missing Columns:",excelFile.isnull().sum()[excelFile.isnull().sum()>0])


##########DATA CLEANING#################################################################

print("Duplicates:",excelFile.duplicated().sum())
print()
print()

print("Missing Columns:",excelFile.isnull().sum()[excelFile.isnull().sum()>0])

excelFile["Category"] = excelFile["Category"].fillna("unknown")
excelFile["Payment_Method"] = excelFile["Payment_Method"].fillna("unknown")


missinfgValues = excelFile.isnull().sum()
if missinfgValues.all() <= 0:
    print("###################################After Missing Has Been Handled")
    print()
    print(missinfgValues)
    print("Missing Columns = 0")
    print()
    print()


excelFile["Order_Date"] = pd.to_datetime(excelFile["Order_Date"])
print("Date DataType: ",excelFile["Order_Date"].dtype)
print()
print()


print(excelFile["Region"])
excelFile["Region"] = excelFile["Region"].str.strip().str.title()
print(excelFile["Region"])
print()
print()


print("##########Impossible Numbers###################################################")
print()
print()

print("Discount Numbers")
print(excelFile["Discount"].min())
print(excelFile["Discount"].max())
print()

print("Unit_Price Numbers")
print(excelFile[excelFile["Unit_Price"]<1])
print()
print()


print("##########Create a new Revenue column###########################################")
excelFile["Revenue"] = excelFile["Quantity"] * excelFile["Unit_Price"]* (1-excelFile["Discount"])
print(excelFile.head())
print()
print()


###################################DATA ANALYSIS########################################
print("SUM OF REVENUE:",excelFile["Revenue"].sum())
averageOrder = excelFile.groupby("Order_ID")["Revenue"].sum().mean()
print("Average order value:", averageOrder)
print()
print()


best_selling_product = excelFile.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
print(best_selling_product.head(10))

best_selling_category = excelFile.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
print(best_selling_category.head(10))

revenue_region = excelFile.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
print(revenue_region.head(10))

excelFile["Month"] = excelFile["Order_Date"].dt.to_period("M")
print(excelFile.head(2))
revenue_month = excelFile.groupby("Month")["Revenue"].sum().sort_values(ascending=False)
print(revenue_month.head(10))

top_customers  = excelFile.groupby("Customer")["Revenue"].sum().sort_values(ascending=False)
print(top_customers.head(10))


salesperson_performance = (excelFile.groupby("Salesperson").agg(Total_revenue=("Revenue","sum"),Orders=("Order_ID","count"),Average_order_value=("Revenue","mean")).sort_values("Total_revenue",ascending=False))
print(salesperson_performance)

average_discount = excelFile["Discount"].mean()
print("Average Discount is ",average_discount)


excelFile["Discount_Band"] = pd.cut(
    excelFile["Discount"],
    bins=[0,0.2,0.4,0.6],
    labels=["0-20%","20%-40%","40%-60%"]
    )
discount_analysis = (excelFile.groupby("Discount_Band",observed=True)
                    .agg(
                        average_discount=("Discount","mean"),
                        Total_revenue=("Revenue","sum"),
                        average_revenue=("Revenue","mean"),
                        Orders=("Order_ID","count")
                        )
                     )
print(discount_analysis)

excelFile.to_excel("cleaned_sales_data.xlsx",index=False)



###################################DA########################################


discount_revenue_analysis=excelFile.groupby("Revenue")["Discount"].agg(["count","mean","sum"]).reset_index()
print(discount_revenue_analysis)


import matplotlib.pyplot as plt

plt.scatter(excelFile["Discount"],excelFile["Revenue"])

plt.xlabel("Discount")
plt.ylabel("Revenue")
plt.title("Discount VS Revenue")

plt.show()


