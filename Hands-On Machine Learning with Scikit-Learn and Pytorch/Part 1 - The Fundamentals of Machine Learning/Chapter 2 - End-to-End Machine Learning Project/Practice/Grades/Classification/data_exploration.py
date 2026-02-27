import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv("archive/StudentsPerformance.csv")

print(data.shape)
print("-----")
print(data.info())
print("-----")
print(data.head())
print("-----")


plt.figure()
plt.hist(data["test preparation course"])
plt.title("Test preparation course")
plt.show()

gender_test = data.groupby(['gender', 'test preparation course']).size().unstack(fill_value=0)
sb.heatmap(gender_test, annot=True, fmt="d", cmap="Blues")
plt.title("Gender vs Test Preparation Course")
plt.show()

race_test = data.groupby(['race/ethnicity', 'test preparation course']).size().unstack(fill_value=0)
parent_test = data.groupby(['parental level of education', 'test preparation course']).size().unstack(fill_value=0)
math_test = data.groupby(['math score', 'test preparation course']).size().unstack(fill_value=0)
reading_test = data.groupby(['reading score', 'test preparation course']).size().unstack(fill_value=0)
writing_test = data.groupby(['writing score', 'test preparation course']).size().unstack(fill_value=0)

print(gender_test)
print(race_test)
print(parent_test)
print(math_test)
print(reading_test)
print(writing_test)

data['sum'] = (data['math score'] + data['writing score'] + data['reading score'])
sb.boxplot(x='test preparation course', y='sum', data=data)
plt.title("Sum of scores vs Test Preparation Course")
plt.show()


top_15 = data.sort_values(by = 'sum', ascending = False).head(15)
print(top_15)