import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

data = pd.read_csv('archive/amazon_sales_dataset.csv').dropna()

data['order_date'] = pd.to_datetime(data['order_date'])
data['year'] = data['order_date'].dt.year
data['year'] = data['year'].astype(int)

cat_features = ['product_category', 'customer_region']
num_features = ['year', 'price', 'discount_percent', 'quantity_sold', 'rating', 'review_count', 'discounted_price']

preprocess = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

X_all = data[cat_features + num_features]
y = data['payment_method']

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

print(y.value_counts())
print(y.value_counts(normalize=True))

models = {
    "LR": LogisticRegression(),
    "RFC": RandomForestClassifier(),
    "KNC": KNeighborsClassifier()
}
# In this case, I resigned from SVC to save time on training

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
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1 score": f1_score(y_test, y_pred, average='weighted'),
        "Precision": precision_score(y_test, y_pred, average='macro'),
        "Recall score": recall_score(y_test, y_pred, average='weighted')
    })

print(results)

# Dataset is bad for this problem, because the target is barely correlated with the features