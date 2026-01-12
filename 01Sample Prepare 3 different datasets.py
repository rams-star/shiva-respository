# Prepare 3 different datasets
# Dataset 1: Product information with product ID, name, category, and price
# Dataset 2: Customer information with customer ID, name, email, and location
# Dataset 3: Sales transactions with transaction ID, product ID, customer ID, date, and quantity

import pandas as pd
import numpy as np
import random
import faker
fake = faker.Faker()
# Set random seed for reproducibility
random.seed(42)
# Number of records for each dataset
num_products = 100
num_customers = 2000
num_transactions = 5000
# Dataset 1: Product information
product_ids = [f"P{str(i).zfill(4)}" for i in range(1, num_products + 1)]
product_names = [fake.word().capitalize() for _ in range(num_products)]
categories = [random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Toys']) for _ in range(num_products)]

prices = [round(random.uniform(5.0, 500.0), 2) for _ in range(num_products)]
products_df = pd.DataFrame({
    'product_id': product_ids,
    'product_name': product_names,
    'category': categories,
    'price': prices
})
# Dataset 2: Customer information
customer_ids = [f"C{str(i).zfill(5)}" for i in range(1, num_customers + 1)]
customer_names = [fake.name() for _ in range(num_customers)]
emails = [fake.email() for _ in range(num_customers)]
locations = [fake.city() for _ in range(num_customers)]
customers_df = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_name': customer_names,
    'email': emails,
    'location': locations
})
# Dataset 3: Sales transactions
transaction_ids = [f"T{str(i).zfill(6)}" for i in range(1, num_transactions + 1)]
transaction_product_ids = [random.choice(product_ids) for _ in range(num_transactions)]
transaction_customer_ids = [random.choice(customer_ids) for _ in range(num_transactions)]
dates = [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_transactions)]
quantities = [random.randint(1, 10) for _ in range(num_transactions)]
transactions_df = pd.DataFrame({
    'transaction_id': transaction_ids,
    'product_id': transaction_product_ids,
    'customer_id': transaction_customer_ids,
    'date': dates,
    'quantity': quantities
})

# Want to understand which product categories are least popular among customers in different locations.
# Total sales by category and location
product_transactions_df = transactions_df.merge(products_df, on='product_id').merge(customers_df, on='customer_id')
sales_by_category_location = product_transactions_df.groupby(['category', 'location']).agg(total_sales=('quantity', 'sum')).reset_index()
sales_by_location = product_transactions_df.groupby(['location']).agg(total_sales=('quantity', 'sum')).reset_index()

sales_by_category_location_bottom5 = sales_by_category_location.nsmallest(5, 'total_sales')

# From each category, get the location with the least sales
least_popular_by_category = sales_by_category_location.loc[sales_by_category_location.groupby(['category'])['total_sales'].idxmin()].reset_index(drop=True)

# Plot heat map of sales by category and location
import seaborn as sns
import matplotlib.pyplot as plt
heatmap_data = sales_by_category_location.pivot(index='category', columns='location', values='total_sales').fillna(0)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title('Total Sales by Product Category and Location')
plt.xlabel('Location')
plt.ylabel('Product Category')
plt.show()

# View the total sales by location data on world map
import geopandas as gpd
import geodatasets

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
location_sales_map = sales_by_location.merge(world, left_on='location', right_on='name', how='left')
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax, linewidth=1)
location_sales_map.plot(column='total_sales', ax=ax, legend=True,
                        legend_kwds={'label': "Total Sales by Location",
                                     'orientation': "horizontal"},
                        cmap='OrRd', missing_kwds={"color": "lightgrey"})
plt.title('Total Sales by Location on World Map')
plt.show()