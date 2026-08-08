import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from pathlib import Path

RANDOM_SEED = 42
BATCH_SIZE = 1024
LR = 0.001
TRAIN_SIZE = 0.8
EPOCHS = 50

device = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(RANDOM_SEED)
torch.cuda.manual_seed(RANDOM_SEED)

california_housing = fetch_california_housing()
scaler = StandardScaler()

X = california_housing.data
y = california_housing.target

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE, random_state=RANDOM_SEED)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train, y_train = torch.from_numpy(X_train).type(torch.float32), torch.from_numpy(y_train).type(torch.float32)
X_test, y_test = torch.from_numpy(X_test).type(torch.float32), torch.from_numpy(y_test).type(torch.float32)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

class HousingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features=8, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1)
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.layers(X)

model = HousingModel()
model.to(device)
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    model.train()
    train_loss = 0
    for X_batch, y_batch in train_dataloader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        y_preds = model(X_batch)
        loss = loss_fn(y_preds.squeeze(), y_batch)
        train_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss /= len(train_dataloader)

    if epoch % 5 == 0:
        model.eval()
        test_loss = 0
        with torch.inference_mode():
            for X_batch, y_batch in test_dataloader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                y_test_preds = model(X_batch)
                loss = loss_fn(y_test_preds.squeeze(), y_batch)
                test_loss += loss.item()
            test_loss /= len(test_dataloader)
        print(f"Epoch: {epoch} | Train loss: {train_loss:.4f} | Test loss: {test_loss:.4f}")
        



