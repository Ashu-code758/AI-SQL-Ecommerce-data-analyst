DATABASE_SCHEMA = """
Database: ecommerce_analysis

Table: ecommerce_sales

Columns:
- Order_Id
- Order_Date
- Customer_Name
- Customer_Segment
- Country
- Product_Category
- Product_Name
- Quantity
- Unit_Price
- Discount_Percent
- Total_Sales
- Sipping_Cost
- Profit
- Payment_Method

Important:
- Total_Sales is the actual sales amount.
- Use Total_Sales for sales calculations.
- Use Profit for profit calculations.
- Use Shipping_Cost for shipping cost questions.
"""