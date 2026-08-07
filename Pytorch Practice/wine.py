from sklearn.datasets import load_wine
import torch
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
from torchmetrics import Accuracy
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from pathlib import Path

BATCH_SIZE = 32
RANDOM_SEED = 42
EPOCHS = 50
LR = 0.001

torch.manual_seed(RANDOM_SEED)
torch.cuda.manual_seed(RANDOM_SEED)

data = load_wine()

X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=RANDOM_SEED, stratify=y)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train, y_train = torch.from_numpy(X_train).type(torch.float32), torch.from_numpy(y_train).type(torch.long)
X_test, y_test = torch.from_numpy(X_test).type(torch.float32), torch.from_numpy(y_test).type(torch.long)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=False)

device = "cuda" if torch.cuda.is_available() else "cpu"

class WineModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = nn.Sequential(
            nn.Linear(in_features=13, out_features=32),
            nn.Tanh(),
            nn.Linear(in_features=32, out_features=32),
            nn.Tanh(),
            nn.Linear(in_features=32, out_features=3),
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.structure(X)

model = WineModel().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LR)
accuracy = Accuracy(task="multiclass", num_classes=3).to(device)

for epoch in range(EPOCHS):
    model.train()
    train_loss, train_acc = 0, 0

    for X_batch, y_batch in train_dataloader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        y_logits = model(X_batch)
        y_preds = torch.softmax(y_logits, dim=1).argmax(dim=1)
        loss = loss_fn(y_logits, y_batch)
        train_loss += loss.item()
        train_acc += accuracy(y_preds, y_batch).item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss /= len(train_dataloader)
    train_acc /= len(train_dataloader)

    if epoch % 5 == 0:
        model.eval()
        test_loss, test_acc = 0, 0
        with torch.inference_mode():
            for X_batch, y_batch in test_dataloader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                y_test_logits = model(X_batch)
                y_test_preds = torch.softmax(y_test_logits, dim=1).argmax(dim=1)
                loss = loss_fn(y_test_logits, y_batch)
                test_loss += loss.item()
                test_acc += accuracy(y_test_preds, y_batch).item()

        test_loss /= len(test_dataloader)
        test_acc /= len(test_dataloader)

        print(f"Epoch: {epoch} | Train loss: {train_loss:.4f} | Train accuracy: {train_acc*100:.2f}% | Test loss: {test_loss:.4f} | Test accuracy: {test_acc*100:.2f}%")

PATH = Path("models")
PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "wine_model.pth"
MODEL_PATH = PATH / MODEL_NAME

torch.save(model.state_dict(), f=MODEL_PATH)



