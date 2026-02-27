import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

data = pd.read_csv("archive/StudentsPerformance.csv").dropna()

cat_features = ["gender", "race/ethnicity", "parental level of education", "lunch"]
num_features = ["math score" ,"reading score" ,"writing score"]

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown='ignore'), cat_features),
        ("num", StandardScaler(), num_features)
    ]
)

X_all = data[cat_features + num_features]
y = data['test preparation course'].map({"none": 0, "completed": 1})

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)


# ----- LR -----
lr = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression())
])
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)

acc_lr = accuracy_score(y_test, pred_lr)
pr_lr = precision_score(y_test, pred_lr)
f1_lr = f1_score(y_test, pred_lr)

print("LR accuracy: ", acc_lr)
print("LR precision: ", pr_lr)
print("LR f1 score: ", f1_lr)



# ----- RFC -----
rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(random_state=42))
])
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

acc_rf = accuracy_score(y_test, pred_rf)
pr_rf = precision_score(y_test, pred_rf)
f1_rf = f1_score(y_test, pred_rf)

print("RF accuracy: ", acc_rf)
print("RF precision: ", pr_rf)
print("RF f1 score: ", f1_rf)



# ----- KNN -----
kn = Pipeline([
    ("preprocess", preprocess),
    ("model", KNeighborsClassifier())
])
kn.fit(X_train, y_train)
pred_kn = kn.predict(X_test)

acc_kn = accuracy_score(y_test, pred_kn)
pr_kn = precision_score(y_test, pred_kn)
f1_kn = f1_score(y_test, pred_kn)

print("KN accuracy: ", acc_kn)
print("KN precision: ", pr_kn)
print("KN f1 score: ", f1_kn)



# ----- SVC -----
sv = Pipeline([
    ("preprocess", preprocess),
    ("model", SVC())
])
sv.fit(X_train, y_train)
pred_sv = sv.predict(X_test)

acc_sv = accuracy_score(y_test, pred_sv)
pr_sv = precision_score(y_test, pred_sv)
f1_sv = f1_score(y_test, pred_sv)

print("SV accuracy: ", acc_sv)
print("SV precision: ", pr_sv)
print("SV f1 score: ", f1_sv)




# LR is the best model for this problem



