import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv('archive/amazon_sales_dataset.csv')

print(data.shape)
print(data.info())
print(data.head())

plt.figure()
plt.hist(data['payment_method'])
plt.title("Payment methods")
plt.show()

data['order_date'] = pd.to_datetime(data['order_date'])
data['year'] = data['order_date'].dt.year

pm_year = data.groupby('year')['payment_method'].size()
pm_pcat = data.groupby(['product_category', 'payment_method']).size()

bins = [0, 100, 300, float('inf')]
labels = ['0-100', '100-300', '>300']
pm_price = data.groupby([pd.cut(data['price'], bins = bins, labels = labels), 'payment_method']).size()

bins_percent = [-0.1, 0, 30]
labels_percent = ['0', '1-30']
pm_discount = data.groupby([pd.cut(data['discount_percent'], bins = bins_percent, labels = labels_percent), 'payment_method']).size()

pm_region = data.groupby(['customer_region', 'payment_method']).size()

print(pm_year)
print(pm_pcat)
print(pm_price)
print(pm_discount)
print(pm_region)


