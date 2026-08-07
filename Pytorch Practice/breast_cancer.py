import torch
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from torchmetrics.classification import BinaryAccuracy
import pandas as pd
from pathlib import Path

SEED = 42

cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = pd.Series(cancer.target)

X = X.to_numpy()
y = y.to_numpy()

device = "cuda" if torch.cuda.is_available() else "cpu"

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=SEED)

X_train, X_test = torch.from_numpy(X_train).to(device).type(torch.float32), torch.from_numpy(X_test).to(device).type(torch.float32)
y_train, y_test = torch.from_numpy(y_train).to(device).type(torch.float32), torch.from_numpy(y_test).to(device).type(torch.float32)

class BCModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = nn.Sequential(
            nn.Linear(in_features=30, out_features=32),
            nn.Tanh(),
            nn.Linear(in_features=32, out_features=32),
            nn.Tanh(),
            nn.Linear(in_features=32, out_features=1)
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.structure(X)

model = BCModel()
model.to(device)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.01)

accuracy = BinaryAccuracy()

epochs = 300



for epoch in range(epochs):
    model.train()
    y_logits = model(X_train).squeeze()
    y_preds = torch.round(torch.sigmoid(y_logits))
    loss = loss_fn(y_logits, y_train)
    acc = accuracy(y_preds, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 25 == 0:
        model.eval()
        with torch.inference_mode():
            test_logits = model(X_test).squeeze()
            test_preds = torch.round(torch.sigmoid(test_logits))
            test_loss = loss_fn(test_logits, y_test)
            test_acc = accuracy(test_preds, y_test)

        print(f"Epoch: {epoch} | Loss: {loss:.4f} | Accuracy: {acc*100:.2f}% | Test loss: {test_loss:.4f} | Test accuracy: {test_acc*100:.2f}%")

PATH = Path("models")
PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "bcmodel.pth"
MODEL_PATH = PATH / MODEL_NAME
torch.save(model.state_dict(), f=MODEL_PATH)



