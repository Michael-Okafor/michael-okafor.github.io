CREATE DATABASE ecommerce_db;
USE ecommerce_db;
CREATE TABLE Customers(
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100)
);
INSERT INTO Customers 
(Customer_id, name, location)
VALUES
(1, 'John Smith', 'London'),
(2, 'Sarah Jones', 'Birmingham'),
(3, 'David Brown', 'Manchester'),
(4, 'Emma Wilson', 'London'),
(5, 'James Taylor', 'Leeds');

CREATE TABLE Products(
	product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
	price DECIMAL(10,2)
);
INSERT INTO Products
(product_id,product_name,category,price)
VALUES
(1, 'Laptop', 'Electronics', 899.99),
(2, 'Keyboard', 'Electronics', 49.99),
(3, 'Office Chair', 'Furniture', 199.99),
(4, 'Desk', 'Furniture', 299.99),
(5, 'Headphones', 'Electronics', 79.99),
(6, 'Notebook', 'Stationery', 9.99);

CREATE TABLE Orders(
	order_id INT PRIMARY KEY,
	customer_id INT,
    order_date DATE,
    total DECIMAL(10,2),
    
    FOREIGN KEY(Customer_id)
		REFERENCES Customers(Customer_id)
);
INSERT INTO Orders 
(order_id,customer_id,order_date,total)
VALUES
(1001, 1, '2026-01-05', 949.98),
(1002, 2, '2026-01-12', 299.99),
(1003, 1, '2026-02-03', 79.99),
(1004, 3, '2026-02-15', 499.98),
(1005, 4, '2026-03-01', 59.98),
(1006, 2, '2026-03-15', 899.99);

SELECT 
	Orders.order_id,
    Customers.name,
    Orders.order_date,
    Orders.total
FROM Orders
JOIN Customers
	ON Orders.customer_id = Customers.customer_id;

CREATE TABLE OrderItems(
	order_item_id INT PRIMARY KEY,
	order_id INT,
	product_id  INT,
    quantity  INT,
    unit_price  DECIMAL(10,2),
    
    FOREIGN KEY(order_id)
		REFERENCES Orders(order_id),
        
	FOREIGN KEY(product_id)
		REFERENCES Products(product_id)
);
INSERT INTO OrderItems 
(order_item_id,order_id,product_id,quantity,unit_price)
VALUES
(1, 1001, 1, 1, 899.99),
(2, 1001, 2, 1, 49.99),

(3, 1002, 4, 1, 299.99),

(4, 1003, 5, 1, 79.99),

(5, 1004, 3, 2, 199.99),

(6, 1005, 2, 1, 49.99),
(7, 1005, 6, 1, 9.99),

(8, 1006, 1, 1, 899.99);
SELECT
	o.order_id,
    c.name,
    p.product_name,
	oi.quantity,
    oi.unit_price
FROM Customers c
JOIN Orders o
	ON o.customer_id = c.customer_id
JOIN OrderItems oi
	ON o.order_id = oi.order_id
JOIN Products p
	ON p.product_id = oi.product_id;
    
CREATE TABLE Payments(
	payment_id INT PRIMARY KEY,
    order_id INT,
    payment_date  Date,
    payment_method  VARCHAR(100),
    amount DECIMAL(10,2),
    
    FOREIGN KEY(order_id)
		REFERENCES orders(order_id)
);
INSERT INTO Payments
(payment_id,order_id,payment_date,payment_method,amount)
VALUES
(1, 1001, '2026-01-05', 'Credit Card', 949.98),
(2, 1002, '2026-01-12', 'PayPal', 299.99),
(3, 1003, '2026-02-03', 'Debit Card', 79.99),
(4, 1004, '2026-02-15', 'Credit Card', 399.98),
(5, 1005, '2026-03-01', 'PayPal', 59.98),
(6, 1006, '2026-03-15', 'Credit Card', 899.99);

SELECT
    c.name AS customer,
    o.order_id,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    pay.payment_method,
    pay.amount
FROM Customers c
JOIN Orders o
    ON c.customer_id = o.customer_id
JOIN OrderItems oi
    ON o.order_id = oi.order_id
JOIN Products p
    ON oi.product_id = p.product_id
JOIN Payments pay
    ON o.order_id = pay.order_id;
    
 -- QUESTION 1: Which products generate the most revenue?   
SELECT 
	c.name,
	o.order_id,
	p.product_name,
    SUM(oi.quantity*oi.unit_price) AS Revenue
FROM OrderItems oi
JOIN Products p
	ON p.product_id = oi.product_id
JOIN orders o
	ON o.order_id = oi.order_id
JOIN customers c
	ON c.customer_id = o.customer_id
    
GROUP BY p.product_name,o.order_id,c.customer_id
ORDER BY Revenue DESC;

 -- QUESTION 2: Which customers have spent the most?  
 
SELECT 
	c.name,
	sum(o.total) AS total_spent
FROM customers c
JOIN orders o 
	ON c.customer_id = o.customer_id
GROUP BY c.customer_id,c.name
ORDER BY total_spent DESC;

 -- QUESTION 3: What are the monthly sales?
 
 SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(total) AS monthly_sales
FROM Orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

 -- QUESTION 4: What category is Performing the best?

SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS total_category
FROM OrderItems oi
JOIN Products p
	ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_category desc;

-- QUESTION 5: What percentage of orders come from repeat customers?
WITH customer_orders AS(
SELECT 
	c.name,o.customer_id,
    COUNT(o.order_id) AS order_count
FROM orders o
JOIN customers c
	ON c.customer_id = o.customer_id
GROUP BY c.name,o.customer_id
ORDER BY order_count desc)


SELECT
    ROUND(
        100.0 * SUM(
			CASE
                WHEN order_count > 1 THEN order_count
                ELSE 0
            END
        ) / (SELECT COUNT(*) FROM Orders),
        2
    ) AS repeat_order_percentage
FROM customer_orders;

 -- QUESTION 6: Which locations generate the most revenue?
 SELECT 
	c.location,   
    SUM(oi.quantity*oi.unit_price) AS most_revenue
FROM orders o
JOIN customers c
	ON c.customer_id = o.customer_id
JOIN orderitems oi
	ON o.order_id = oi.order_id
GROUP BY c.location
ORDER BY most_revenue desc














