import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

data = pd.read_csv('archive/amazon_sales_dataset.csv')

print(data.shape)
print(data.info)
print(data.head)

print(data['quantity_sold'].mean())
print(data['quantity_sold'].median())
print(data['quantity_sold'].std())


# I'm exploring only the features, I find useful, etc. order id is pointless to check, just as product_id
# I'm also giving up on discounted price, since we can calculate it from price and discount, so it's redundant. Same situation with total_revenue

# Features I'm left with: order_date, product_category, price, discount_percent, quantity_sold, customer_region, payment_method, rating, review_count

data['order_date'] = pd.to_datetime(data['order_date'])
data['month'] = data['order_date'].dt.month
data['month'] = data['month'].astype(int)

season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
}

data['season'] = data['month'].map(season_map)

user_product_counts = data.groupby(['season', 'quantity_sold'])['order_id'] \
                          .nunique() \
                          .reset_index(name='user_count')


season_order = ['Winter', 'Spring', 'Summer', 'Autumn']
user_product_counts['season'] = pd.Categorical(user_product_counts['season'], categories=season_order, ordered=True)
user_product_counts = user_product_counts.sort_values(['season', 'quantity_sold'])

print(user_product_counts)


plt.figure(figsize=(10,6))
sn.barplot(data=user_product_counts, x='quantity_sold', y='user_count', hue='season', hue_order=season_order)
plt.xlabel("Quantity sold")
plt.ylabel("Order count")
plt.legend(title='Season')
plt.show()

# Grupowanie po sezonie, kategorii produktu i liczbie kupionych sztuk
user_category_counts = data.groupby(['season', 'product_category', 'quantity_sold'])['order_id'] \
                          .nunique() \
                          .reset_index(name='user_count')


user_category_counts['season'] = pd.Categorical(user_category_counts['season'], categories=season_order, ordered=True)
user_category_counts = user_category_counts.sort_values(['season', 'product_category', 'quantity_sold'])

print(user_category_counts)

bins = [0, 100, 300, float('inf')]
labels = ['0-100', '100-300', '>300']
qs_price = data.groupby([pd.cut(data['price'], bins = bins, labels = labels), 'quantity_sold']).size()

print(qs_price)

qs_region = data.groupby(['customer_region', 'quantity_sold'])['order_id'] \
                       .nunique() \
                       .reset_index(name='user_count')
print(qs_region)


qs_rating = data.groupby(['rating', 'quantity_sold'])['order_id'] \
                       .nunique() \
                       .reset_index(name='user_count')
print(qs_rating)


qs_review = data.groupby(['review_count', 'quantity_sold'])['order_id'] \
                       .nunique() \
                       .reset_index(name='user_count')
print(qs_review)




