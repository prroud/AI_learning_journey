import torch
from torch import nn
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader
from torchmetrics.classification import BinaryAccuracy
from pathlib import Path

SEED = 42

# 1. Pobieranie danych bezpośrednio do NumPy (usunięto Pandas)
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# 2. Podział na zbiory TRENINGOWY i TESTOWY
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=SEED)

# 3. SKALOWANIE DANYCH
scaler = StandardScaler()
# UWAGA: Uczymy skaler TYLKO na danych treningowych, aby uniknąć "wycieku danych" (data leakage)
X_train = scaler.fit_transform(X_train) 
# Na danych testowych robimy tylko transformację (używając średniej i odchylenia ze zbioru treningowego)
X_test = scaler.transform(X_test)

# 4. Konwersja do tensorów (zauważ, że NIE wysyłamy ich jeszcze na GPU)
X_train = torch.from_numpy(X_train).type(torch.float32)
y_train = torch.from_numpy(y_train).type(torch.float32)
X_test = torch.from_numpy(X_test).type(torch.float32)
y_test = torch.from_numpy(y_test).type(torch.float32)

# 5. Tworzenie DataLoaderów
BATCH_SIZE = 32
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# DataLoader sam podzieli dane na paczki (batches) po 32 elementy
train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

device = "cuda" if torch.cuda.is_available() else "cpu"

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

model = BCModel().to(device)

loss_fn = nn.BCEWithLogitsLoss()
# Zmniejszyłem learning rate. Po zastosowaniu StandardScaler optymalizatorowi
# łatwiej jest "zjeżdżać" po gradiencie, a 0.01 dla Adama to zazwyczaj za dużo.
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.001) 

accuracy = BinaryAccuracy().to(device)

# Zmniejszyłem liczbę epok. Po skalowaniu i z batchami model nauczy się znacznie szybciej.
epochs = 50 

for epoch in range(epochs):
    model.train()
    train_loss, train_acc = 0, 0
    
    # Trenujemy iterując po paczkach danych (batches) z DataLoadera
    for X_batch, y_batch in train_dataloader:
        # Przenosimy na GPU tylko obecną paczkę danych!
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        
        y_logits = model(X_batch).squeeze()
        y_preds = torch.round(torch.sigmoid(y_logits))
        
        loss = loss_fn(y_logits, y_batch)
        # Akumulujemy stratę i dokładność z poszczególnych batchy
        train_loss += loss.item() 
        train_acc += accuracy(y_preds, y_batch).item()
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Wyliczamy średnią z całej epoki
    train_loss /= len(train_dataloader)
    train_acc /= len(train_dataloader)

    # Ewaluacja co 10 epok
    if epoch % 10 == 0:
        model.eval()
        test_loss, test_acc = 0, 0
        with torch.inference_mode():
            for X_batch, y_batch in test_dataloader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                
                test_logits = model(X_batch).squeeze()
                test_preds = torch.round(torch.sigmoid(test_logits))
                
                test_loss += loss_fn(test_logits, y_batch).item()
                test_acc += accuracy(test_preds, y_batch).item()
            
            test_loss /= len(test_dataloader)
            test_acc /= len(test_dataloader)

        print(f"Epoch: {epoch:03d} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | Test Loss: {test_loss:.4f} | Test Acc: {test_acc*100:.2f}%")

# Zapis modelu
PATH = Path("models")
PATH.mkdir(parents=True, exist_ok=True)
MODEL_PATH = PATH / "bcmodel.pth"
torch.save(model.state_dict(), f=MODEL_PATH)