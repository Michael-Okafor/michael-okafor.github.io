CREATE DATABASE retail_transactions_cleaned;
USE retail_transactions_cleaned;
DESCRIBE transactions;
alter table transactions 
rename column ï»¿OrderID to orderId;
#-------------------------
#1.) What is total revenue
SELECT SUM(revenue) as total_revenue
FROM transactions;
#-------------------------

#-------------------------
#2.)What is total profit?
SELECT SUM(profit) as total_profit
from transactions;
#-------------------------

#-------------------------
#3.)What is total profit?
SELECT COUNT(orderId) as total_orders
from transactions;
#-------------------------

#-------------------------
#4.)What is the average order value?
SELECT 
sum(revenue)/count(DISTINCT orderId) AS average_order
FROM transactions;
#-------------------------

#5.) Which product category generates the most revenue?
SELECT 
ProductCategory, count(*) AS highest_revenue
FROM transactions
group by ProductCategory
order by highest_revenue desc;
#-------------------------

#-------------------------
#-6.)Which location generates the most revenue?
select 
Location,round(sum(revenue),2) as total_revenue 
from transactions
group by Location
order by total_revenue desc
limit 1;
#-------------------------

#-7.)Which location generates the most profit?
select 
Location,round(sum(profit),2) as total_profit
from transactions
group by Location
order by total_profit desc
limit 1;
#-------------------------
select OrderDate
from transactions
limit 10;
describe transactions;

#-8.)Which month has the highest sales?
select 
DATE_FORMAT(STR_TO_DATE(OrderDate, '%c/%e/%Y'),'%Y-%M') as months,
round(sum(revenue),2) as total_sales
from transactions
GROUP BY DATE_FORMAT(STR_TO_DATE(OrderDate, '%c/%e/%Y'),'%Y-%M') 
order by total_sales desc
limit 1;
#-------------------------

#-------------------------
#-9.) What payment method is most commonly used?
select PaymentMethod,count(OrderID) as order_count
from transactions
group by PaymentMethod
order by order_count desc
limit 1;
#-------------------------

#-------------------------
#-10.)Which customer type generates the most revenue?
select CustomerType,round(sum(revenue),2) as most_revenue
from transactions
group by CustomerType
order by most_revenue desc
limit 1;
#-------------------------

#-------------------------
#-11.) What is the average order value by customer type?
select 
CustomerType,
sum(revenue)/count(distinct orderId) as average_order
from transactions
group by CustomerType
order by average_order desc;
#-------------------------

select ProductName,
round(sum(revenue),2) as total_revenue
from transactions
group by ProductName
order by total_revenue desc;

select ProductName,
round(avg(ProfitMargin)*100,2) as total_revenue
from transactions
group by ProductName
order by total_revenue asc;

#-------------------------
#-12.)which products have high revenue but low profit margins?
select ProductName,
round(sum(revenue),2) as total_revenue,
round(avg(ProfitMargin),2) as avg_profit_margin_percent
from transactions
group by ProductName
having total_revenue >= 5000 and avg_profit_margin_percent <= 10
order by total_revenue desc;
#-------------------------

#-------------------------
#-14.)Which locations have high sales but below-average profit?
select Location,
round(sum(revenue),2) as total_sales,
round(sum(profit),2) as total_profit,
round(avg(Profit),2) as average_profit
from transactions
group by Location
having sum(revenue) > 5000 and avg(Profit) > (
select avg(Profit)
from transactions)
order by total_sales desc;
#-------------------------

#-------------------------
#-15.)Are customers who receive larger discounts actually generating more revenue?
select 
	case
		when Discount < 0.1 then "under 10%"
		when Discount < 0.2 then "between 10% and 20%"
        else "20% or more"
	end as discount_brand,
    count(*) as transaction_count,
	round(avg(revenue),2) as average_revenue,
	round(sum(revenue),2) as total_revenue
from transactions
group by discount_brand
order by average_revenue desc
limit 10;
#-------------------------

#-------------------------
#-16.)Which customer age group spends the most?
select
	case
		when CustomerAge < 20 then "under 20"
		when CustomerAge < 30 then "20-29"
		when CustomerAge < 40 then "30-39"
		when CustomerAge < 60 then "40-59"
        else "60 and above"
	end as customer_age_group,
    count(*) as transaction_count,
    round(avg(revenue),2) as avg_spent,
    round(sum(revenue),2) as total_revenue
    from transactions
    group by customer_age_group
    order by total_revenue desc;
#-------------------------

#-------------------------
#-17.)Which product categories are growing or declining over time?
select ProductCategory,
DATE_FORMAT(STR_TO_DATE(OrderDate, '%c/%e/%Y'),'%Y-%m') as sales_month,
round(sum(revenue),2) as total_revenue,
round(sum(profit),2) as total_profit,
round(sum(profit) / nullif(sum(revenue),0)  * 100 ,2) as product_profit_margin
from transactions
group by ProductCategory,DATE_FORMAT(STR_TO_DATE(OrderDate, '%c/%e/%Y'),'%Y-%m')
order by ProductCategory,sales_month;
#-------------------------

#-------------------------
#-18.) What percentage of total revenue comes from the top 10 products?
SELECT
    ROUND(
        SUM(top_products.product_revenue) /
        (SELECT SUM(revenue) FROM transactions) * 100,
        2
    ) AS top_10_revenue_percentage
FROM (
    SELECT
        ProductName,
        SUM(revenue) AS product_revenue
    FROM transactions
    GROUP BY ProductName
    ORDER BY product_revenue DESC
    LIMIT 10
) AS top_products;


#-------------------------





