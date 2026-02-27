import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# ----- Data exploration -----

data = pd.read_csv("archive/StudentsPerformance.csv")

print(data.head())
print("----------------")
print(data.info())
print("----------------")
print(data.shape)

plt.figure()
plt.hist(data["math score"], bins=100)
plt.title("Math score")
plt.show()

math_mean = data["math score"].mean()
math_std = data["math score"].std()
math_median = data["math score"].median()
gender_grade = data.groupby("gender")["math score"].mean().sort_values(ascending=False)
race_grade = data.groupby("race/ethnicity")["math score"].mean().sort_values(ascending=False)
parent_grade = data.groupby("parental level of education")["math score"].mean().sort_values(ascending=False)
lunch_grade = data.groupby("lunch")["math score"].mean().sort_values(ascending=False)
preparation_grade = data.groupby("test preparation course")["math score"].mean().sort_values(ascending=False)
reading_grade = data.groupby("reading score")["math score"].mean().sort_values(ascending=False)
writing_grade = data.groupby("writing score")["math score"].mean().sort_values(ascending=False)

print(math_mean)
print(math_std)
print(math_median)
print(gender_grade)
print(race_grade)
print(parent_grade)
print(lunch_grade)
print(preparation_grade)
print(reading_grade)
print(writing_grade)

top_10 = data.sort_values(by="math score", ascending=False).head(10)
print(top_10)




