import torch
from torch import nn
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

torch.manual_seed(42)

start = 0
end = 1
step = 0.02

weight = 0.3
bias = 0.7

X = torch.arange(start=start, end=end, step=step).unsqueeze(dim=1)
y = weight * X + bias


proportion = 0.75
split = int(proportion * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


def plot_data(train_data, train_labels, test_data, test_labels, predictions=None):
    plt.figure(figsize=(10,7))
    plt.scatter(train_data, train_labels, s=4, c='b', label="Training data")
    plt.scatter(test_data, test_labels, s=4, c='g', label="Test data")

    if predictions is not None:
        plt.scatter(test_data, predictions, s=4, c='r', label="Predictions")

    plt.legend()
    plt.show()


class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer = nn.Linear(in_features=1, out_features=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)

model = LinearRegressionModel()

loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model.parameters(), lr=0.01)


epochs = 1000

epoch_count = []
loss_values = []
test_loss_values = []

for epoch in range(epochs):
    model.train()
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    model.eval()
    if epoch % 100 == 0:
        epoch_count.append(epoch)
        loss_values.append(loss)
        with torch.inference_mode():
            test_pred = model(X_test)
            test_loss = loss_fn(test_pred, y_test)
            test_loss_values.append(test_loss)

        print(f"Epoch: {epoch} | Loss: {loss} | Test loss: {test_loss}")
        print(model.state_dict())

model.eval()
with torch.inference_mode():
    y_final_pred = model(X_test)

plot_data(train_data=X_train, train_labels=y_train, test_data=X_test, test_labels=y_test, predictions=y_final_pred)

plt.plot(epoch_count, np.array(torch.tensor(loss_values).numpy()), label = "Train loss")
plt.plot(epoch_count, test_loss_values, label="Test loss")
plt.ylabel("Loss")
plt.xlabel("Epochs")
plt.legend()
plt.show()


MODEL_PATH = Path("models")
MODEL_PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "linear_model_practice.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

print(f"Saving model to: {MODEL_SAVE_PATH}")
torch.save(obj=model.state_dict(), f=MODEL_SAVE_PATH)


