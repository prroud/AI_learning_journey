import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, confusion_matrix, ConfusionMatrixDisplay


data = pd.read_csv('archive/insurance.csv').dropna()

cat_features = ['sex' ,'smoker' ,'region']
num_features = ['age', 'bmi', 'children']

preprocess = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

threshold = data['charges'].quantile(0.75)
data['high_charge'] = (data['charges'] >= threshold).astype(int)

X_all = data[cat_features + num_features]
y = data['high_charge']

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

models = {
    "LR": LogisticRegression(),
    "KNC": KNeighborsClassifier(),
    "RFC": RandomForestClassifier(),
    "SVC": SVC()
}

result = []

for name, model in models.items():
    model = Pipeline([
        ('preprocess', preprocess),
        ('model', model)
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    result.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1 score": f1_score(y_test, y_pred),
        "Precission": precision_score(y_test, y_pred)
    })

print(result)


# LR is the best model for this problem

lr_pipeline = Pipeline([
    ('preprocess', preprocess),
    ('model', LogisticRegression())
])
lr_pipeline.fit(X_train, y_train)
y_pred = lr_pipeline.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0,1])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Logistic Regression")
plt.show()
