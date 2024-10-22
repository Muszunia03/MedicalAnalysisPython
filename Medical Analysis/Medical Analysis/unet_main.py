import numpy as np
import cv2
import matplotlib.pyplot as plt
from unet_model import unet_model

#Wczytanie przetrenowanego modelu
model = unet_model()
model.load_weights('sciezka_do_przetrenowanego_modelu.h5')  # Za³aduj model

#Za³adowanie obrazu MRI do analizy
image_path = 'dane/MRI_images/sample_mri_image.png'  # Wska¿ œcie¿kê do obrazu MRI
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#Przetwarzanie obrazu i segmentacja
image_resized = cv2.resize(image, (128, 128))  # Dopasowanie obrazu do rozmiaru modelu
image_normalized = image_resized / 255.0  # Normalizacja
predicted_mask = model.predict(np.expand_dims(image_normalized, axis=0))[0]

#Przeskalowanie maski segmentacyjnej do oryginalnego rozmiaru
predicted_mask_resized = cv2.resize(predicted_mask, (image.shape[1], image.shape[0]))

#Generowanie mapy ciep³a
heatmap = cv2.applyColorMap((predicted_mask_resized * 255).astype(np.uint8), cv2.COLORMAP_JET)
overlayed_image = cv2.addWeighted(image, 0.6, heatmap, 0.4, 0)

#Sprawdzenie obecnoœci glejaka
threshold = 0.5
mask_area_percentage = np.sum(predicted_mask_resized > threshold) / np.prod(predicted_mask_resized.shape) * 100
presence_threshold = 1.0

if mask_area_percentage > presence_threshold:
    result = "TAK"
else:
    result = "NIE"

#Wizualizacja wyników
plt.figure(figsize=(10, 10))

plt.subplot(1, 4, 1)
plt.imshow(image, cmap='gray')
plt.title('Oryginalny obraz MRI')

plt.subplot(1, 4, 2)
plt.imshow(predicted_mask_resized, cmap='gray')
plt.title('Maska glejaka')

plt.subplot(1, 4, 3)
plt.imshow(overlayed_image)
plt.title('Mapa ciep³a')

plt.subplot(1, 4, 4)
plt.text(0.5, 0.5, result, fontsize=50, ha='center')
plt.title('Czy glejak jest obecny?')

plt.show()

#Wydrukowanie wyniku w konsoli
print(f'Czy glejak jest obecny? {result}')
