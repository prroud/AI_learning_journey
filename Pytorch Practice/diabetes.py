import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 42
EPOCHS = 50
BS = 128

scaler = StandardScaler()
device = "cuda" if torch.cuda.is_available() else "cpu"

if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
else:
    torch.manual_seed(SEED)

diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=SEED, train_size=0.75)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train, X_test = torch.from_numpy(X_train).type(torch.float), torch.from_numpy(X_test).type(torch.float)
y_train, y_test = torch.from_numpy(y_train).type(torch.float), torch.from_numpy(y_test).type(torch.float)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(train_dataset, batch_size=BS, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BS, shuffle=False)


class DBModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features=10, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=1),
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.layers(X)

model = DBModel()
model.to(device)

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.001)

for epoch in range(EPOCHS):
    train_mse = 0
    model.train()
    for X_batch, y_batch in train_dataloader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        y_preds = model(X_batch).squeeze(dim=1)
        loss = loss_fn(y_preds, y_batch)
        train_mse += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_mse /= len(train_dataloader)

    if epoch % 5 == 0:
        model.eval()
        with torch.inference_mode():
            test_mse = 0
            for X_batch, y_batch in test_dataloader:
                X_batch = X_batch.to(device)
                y_batch = y_batch.to(device)
                y_test_preds = model(X_batch).squeeze(dim=1)
                loss = loss_fn(y_test_preds, y_batch)
                test_mse += loss.item()
        test_mse /= len(test_dataloader)

        print(f"Epoch: {epoch} | Train loss: {train_mse} | Test loss: {test_mse}")




