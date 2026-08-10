import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from torchmetrics import Accuracy

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

from helper_function import plot_decision_boundary

from pathlib import Path

device = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(42)
torch.cuda.manual_seed(42)

SEED = 42
EPOCHS = 50
LR = 0.001
BS = 256

X, y = make_moons(n_samples = 10000, noise = 0.1, random_state=SEED)


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=SEED)

X_train, X_test = torch.from_numpy(X_train).type(torch.float32), torch.from_numpy(X_test).type(torch.float32)
y_train, y_test = torch.from_numpy(y_train).type(torch.float32), torch.from_numpy(y_test).type(torch.float32)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(train_dataset, batch_size=BS, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BS, shuffle=False)

class MMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features=2, out_features=16),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=16),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=1)
        )
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.layers(X)

model = MMModel()
model.to(device)

accuracy = Accuracy(task="binary")
accuracy.to(device)
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    train_loss = 0
    train_acc = 0
    model.train()
    for X_batch, y_batch in train_dataloader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        y_logits = model(X_batch).squeeze()
        y_preds = torch.round(torch.sigmoid(y_logits))
        loss = loss_fn(y_logits, y_batch)
        acc = accuracy(y_preds, y_batch)
        train_loss += loss.item()
        train_acc += acc.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_loss /= len(train_dataloader)
    train_acc /= len(train_dataloader)

    if epoch % 5 == 0:
        test_loss = 0
        test_acc = 0
        model.eval()
        with torch.inference_mode():
            for X_batch, y_batch in test_dataloader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                y_test_logits = model(X_batch).squeeze()
                y_test_preds = torch.round(torch.sigmoid(y_test_logits))
                loss = loss_fn(y_test_logits, y_batch)
                acc = accuracy(y_test_preds, y_batch)
                test_loss += loss.item()
                test_acc += acc.item()

        test_loss /= len(test_dataloader)
        test_acc /= len(test_dataloader)

        print(f"Epoch: {epoch} | Train loss: {train_loss:.4f} | Train accuracy: {train_acc*100:.2f}% | Test loss: {test_loss:.4f} | Test accuracy: {test_acc*100:.2f}%")

MODEL_PATH = Path("models")
MODEL_PATH.mkdir(parents=False, exist_ok=True)
MODEL_NAME = "moons.pth"
SAVE_PATH = MODEL_PATH / MODEL_NAME
torch.save(model.state_dict(), f=SAVE_PATH)

plot_decision_boundary(model, X=X_test, y=y_test)
plt.show()



