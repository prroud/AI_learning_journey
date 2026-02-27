import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


data = pd.read_csv("archive/StudentsPerformance.csv")
data = data.dropna()

cat_features = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
num_features = ["reading score", "writing score"]

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
        ("num", StandardScaler(), num_features)
    ]
)

X_all = data[cat_features + num_features]
y = data["math score"]

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size = 0.2, random_state= 42)


# ----- Linear Regression -----
lr = Pipeline([
    ("preprocess", preprocess),
    ("model", LinearRegression())
])
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
rmse_lr = root_mean_squared_error(y_test, pred_lr)
r2_lr = r2_score(y_test, pred_lr)
mae_lr = mean_absolute_error(y_test, pred_lr)
print("Linear regression RMSE: ", rmse_lr)
print("Linear regression MAE: ", mae_lr)
print("Linear regression R2", r2_lr)


# ----- Random forest -----
rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestRegressor(random_state = 42))
])
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
rmse_rf = root_mean_squared_error(y_test, pred_rf)
print("Random forest RMSE: ", rmse_rf)


# ----- SVM -----
svm = Pipeline([
    ("preprocess", preprocess),
    ("model", SVR())
])
svm.fit(X_train, y_train)
pred_svm = svm.predict(X_test)
rmse_svm = root_mean_squared_error(y_test, pred_svm)
print("SVM RMSE: ", rmse_svm)


# ----- KNN -----
kn = Pipeline([
    ("preprocess", preprocess),
    ("model", KNeighborsRegressor())
])
kn.fit(X_train, y_train)
pred_kn = kn.predict(X_test)
rmse_kn = root_mean_squared_error(y_test, pred_kn)
print("KNN RMSE: ", rmse_kn)


# LR is the best model considering only RMSE

threshold = 50

pass_fail = ["pass" if x >= threshold else "fail" for x in pred_lr]

df_results = pd.DataFrame({
    "predicted_score" : pred_lr,
    "pass_fail": pass_fail
})
print(df_results.head())


# ----- Visualization -----


plt.figure(figsize=(6,6))
plt.scatter(y_test, pred_lr, alpha=0.7)
plt.plot([0, 100], [0, 100], 'r--')  
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Linear Regression: Predicted vs Actual")
plt.show()



# ----- Feature importance -----
feature_names_cat = lr.named_steps['preprocess'].named_transformers_['cat'].get_feature_names_out(cat_features)
feature_names_num = num_features
all_features = np.concatenate([feature_names_cat, feature_names_num])

coefs = lr.named_steps['model'].coef_

feat_imp_lr = pd.DataFrame({
    "feature": all_features,
    "coefficient": coefs
}).sort_values(by="coefficient", key=abs, ascending=False)

print(feat_imp_lr)


