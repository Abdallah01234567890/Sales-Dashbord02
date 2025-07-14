import pandas as pd

# Load directly from GitHub raw link
url = "https://raw.githubusercontent.com/sersun/supermarket-sales-analysis/main/supermarket_sales.csv"

# Read the CSV file
df = pd.read_csv(url)

# Show the first 5 rows
print(df.head())

# Basic info about the dataset
print(df.info())

df.to_csv("supermarket_sales.csv", index=False)
print("Dataset saved locally as 'supermarket_sales.csv'")

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract Month and Day of Week for analysis
df['Month'] = df['Date'].dt.month_name()
df['Day'] = df['Date'].dt.day_name()

# Optional: Check for missing values
print(df.isnull().sum())

product_sales = df.groupby('Product line')['Total'].sum().sort_values(ascending=False)
print(product_sales)

branch_sales = df.groupby('Branch')['Total'].sum()
print(branch_sales)

payment_counts = df['Payment'].value_counts()
print(payment_counts)

monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total'].sum()
print(monthly_sales)

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Total', y='Product line', estimator=sum, ci=None, palette='viridis')
plt.title('Total Sales by Product Line')
plt.xlabel('Total Sales')
plt.ylabel('Product Line')
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 5))
sns.barplot(data=df, x='Branch', y='Total', estimator=sum, ci=None, palette='magma')
plt.title('Total Sales by Branch')
plt.ylabel('Total Sales')
plt.xlabel('Branch')
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 4))
payment_counts = df['Payment'].value_counts()
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='Set2')
plt.title('Payment Method Distribution')
plt.ylabel('Number of Transactions')
plt.xlabel('Payment Method')
plt.tight_layout()
plt.show()

# Group by month (sorted correctly)
monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_sales, x='Date', y='Total', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


