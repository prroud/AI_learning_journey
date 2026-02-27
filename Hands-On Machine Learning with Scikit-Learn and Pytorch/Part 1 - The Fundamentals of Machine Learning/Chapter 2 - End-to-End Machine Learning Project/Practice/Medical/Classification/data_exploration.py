import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv("archive/insurance.csv")

print(data.head())
print(data.info())
print(data.shape)

print('-------------------------')

charges_mean = data['charges'].mean()
charges_median = data['charges'].median()
charges_std = data['charges'].std()
charges_age = data.groupby('age')['charges'].mean().sort_values(ascending=False)
charges_gender = data.groupby('sex')['charges'].mean().sort_values(ascending=False)
charges_bmi = data.groupby('bmi')['charges'].mean().sort_values(ascending=False)
charges_children = data.groupby('children')['charges'].mean().sort_values(ascending=False)
charges_smoker = data.groupby('smoker')['charges'].mean().sort_values(ascending=False)
charges_region = data.groupby('region')['charges'].mean().sort_values(ascending=False)

print(charges_mean)
print(charges_median)
print(charges_std)
print(charges_age)
print(charges_gender)
print(charges_bmi)
print(charges_children)
print(charges_smoker)

print('-------------------------')

top_10 = data.sort_values(ascending=False, by='charges').head(10)
print(top_10)

print('-------------------------')

data_encoded = pd.get_dummies(data, drop_first=True)
corr_matrix = data_encoded.corr()
print(corr_matrix)

plt.figure(figsize=(10, 8))
sb.heatmap(corr_matrix, annot = True, cmap='coolwarm')
plt.show()