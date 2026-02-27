import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from sklearn.linear_model import LinearRegression, PoissonRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
# from sklearn.svm import SVR      Due to the size of dataset, I resigned from SVR
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

data = pd.read_csv('archive/amazon_sales_dataset.csv')

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

cat_features = ['product_category', 'customer_region', 'season']
num_features = ['price', 'discount_percent', 'rating', 'review_count']

preprocess = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

X_all = data[cat_features + num_features]
y = data['quantity_sold']

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

models = {
    "LR": LinearRegression(),
    "RFR": RandomForestRegressor(),
    "KNR": KNeighborsRegressor(),
    "PR": PoissonRegressor()
}

results = []

for name, model in models.items():
    model = Pipeline([
        ('preprocess', preprocess),
        ('model', model)
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_int = np.round(y_pred).astype(int)
    results.append({
        "Model: ": name,
        "RMSE: ": root_mean_squared_error(y_test, y_pred_int),
        "MAE: ": mean_absolute_error(y_test, y_pred_int),
        "R2: ": r2_score(y_test, y_pred_int)
    })

print(results)

# Same as before, features are weakly correlated with target. This should be treated as classification problem, but I wanted to experiment with regression.