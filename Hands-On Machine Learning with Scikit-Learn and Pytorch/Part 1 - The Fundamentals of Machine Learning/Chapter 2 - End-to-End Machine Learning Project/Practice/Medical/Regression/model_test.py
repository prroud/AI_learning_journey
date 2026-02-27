import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error


data = pd.read_csv('archive/insurance.csv').dropna()

cat_features = ['sex', 'smoker', 'region']
num_features = ['age', 'children', 'bmi']

preprocess = ColumnTransformer(
    transformers = [
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

X_all = data[cat_features + num_features]
y = data['charges']

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)


# ---------- Model Testing ---------

models = {
    "Linear regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(),
    "KNR": KNeighborsRegressor(),
    "SVR": SVR()
}

results = []

for name, model in models.items():
    model = Pipeline([
        ('preprocess', preprocess),
        ('model', model)
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results.append({
        "Model": name,
        "RMSE": root_mean_squared_error(y_test, y_pred),
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred)
    })

print(results)

# Random forest is the best model for this task

rf_pipe = Pipeline([
    ('preprocess', preprocess),
    ('model', RandomForestRegressor(random_state=42))
])

rf_pipe.fit(X_train, y_train)
y_pred = rf_pipe.predict(X_test)

plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         'r--', lw=2)
plt.xlabel("Real charges")
plt.ylabel("Predicted charges")
plt.show()


