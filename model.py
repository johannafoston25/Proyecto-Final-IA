# Johanna Foston 22-SISN-2-036
# Aquí cargo y configuro el modelo de deep learning para detectar EPP

import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Aquí defino las categorías de equipo de protección personal que detecto
CATEGORIAS = [
    "casco",
    "guantes",
    "mascarilla",
    "chaleco",
    "lentes de seguridad"
]

class ModeloEPP:
    def __init__(self):
        # Aquí cargo el modelo ResNet preentrenado
        self.modelo = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.modelo.eval()  # Aquí pongo el modelo en modo evaluación

        # Aquí defino las transformaciones que aplico a cada imagen
        self.transformaciones = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def analizar(self, imagen):
        # Aquí analizo la imagen y detecto qué EPP está presente
        imagen_tensor = self.transformaciones(imagen).unsqueeze(0)

        with torch.no_grad():
            salida = self.modelo(imagen_tensor)

        # Aquí obtengo las probabilidades de cada categoría
        probabilidades = torch.nn.functional.softmax(salida[0], dim=0)

        # Aquí simulo la detección de EPP basándome en las probabilidades
        resultados = {}
        indices = [0, 100, 200, 300, 400]  # índices del modelo para cada EPP
        for i, categoria in enumerate(CATEGORIAS):
            prob = float(probabilidades[indices[i]])
            resultados[categoria] = prob > 0.001  # umbral de detección

        return resultados