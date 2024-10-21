import torch
import torch.nn as nn
import torchvision.transforms as transforms
from monai.networks import nets
from monai.data import Dataset, DataLoader
from monai.transforms import Compose, LoadImage, ScaleIntensity, EnsureChannelFirst
from pathlib import Path


model = nets.UNet(
    dimensions=3,  # dla danych 3D
    in_channels=1,  # liczba kana³ów wejœciowych (np. 1 dla obrazów MRI)
    out_channels=1,  # liczba kana³ów wyjœciowych (np. 1 dla segmentacji binary)
    num_conv_per_stage=2,
    num_pooling=2,
    dropout=0.1,
).to(GPU)  # Upewnij siê, ¿e GPU jest odpowiednio ustawiony (CPU/GPU)

train_transforms = Compose([
    LoadImage(image_only=True),  # za³aduj obraz
    ScaleIntensity(),  # normalizacja
    EnsureChannelFirst(),  # dodaj kana³ (np. dla obrazów 2D)
    transforms.Resize((256, 256)),  # rozmiar obrazów wejœciowych
])

train_dataset = Dataset(data=Path("E:\GitHub\MedicalAnalysisPython\Task01_BrainTumour\imagesTr"), transform=train_transforms)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
def train_model(model, dataloader, num_epochs=25):
    criterion = nn.BCEWithLogitsLoss()  # u¿yj odpowiedniej funkcji straty
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()  # ustaw model w tryb treningowy
        for images, masks in dataloader:
            images = images.to(GPU)
            masks = masks.to(GPU)

            optimizer.zero_grad()  # zerowanie gradientów
            outputs = model(images)  # forward pass
            loss = criterion(outputs, masks)  # oblicz stratê
            loss.backward()  # backpropagation
            optimizer.step()  # aktualizacja wag

        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
model.eval()  # ustaw model w tryb ewaluacji
with torch.no_grad():
    for image in test_images:
        image = image.to(GPU)
        output = model(image.unsqueeze(0))  # dodaj wymiar batch
        prediction = torch.sigmoid(output)  # zastosuj funkcjê aktywacji
        # Mo¿esz teraz przetworzyæ prediction na obraz
import matplotlib.pyplot as plt

plt.imshow(prediction[0, 0].cpu().numpy(), cmap='gray')
plt.title('Segmented Image')
plt.show()


