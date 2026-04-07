# Johanna Foston 22-SISN-2-036
# Modelo de deteccion de EPP usando Roboflow

from inference_sdk import InferenceHTTPClient
from PIL import Image

class ModeloEPP:
    def __init__(self):
        # Conecto con la API de Roboflow
        self.cliente = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key="KrpWYe6PaHxtCNdnpuvW"
        )

    def analizar(self, imagen):
        # Guardo la imagen temporalmente para Roboflow
        imagen.save("temp_imagen.jpg", format="JPEG")

        # Detecto casco y chaleco
        resultado_ppe = self.cliente.infer("temp_imagen.jpg", model_id="ppe-detection-vpw6m/1")
        etiquetas_ppe = [p["class"] for p in resultado_ppe["predictions"]]
        print("Etiquetas PPE:", etiquetas_ppe)

        # Detecto guantes
        resultado_guantes = self.cliente.infer("temp_imagen.jpg", model_id="gloves-f3gyu/1")
        etiquetas_guantes = [p["class"] for p in resultado_guantes["predictions"]]
        print("Etiquetas Guantes:", etiquetas_guantes)

        # Detecto mascarilla
        resultado_mascarilla = self.cliente.infer("temp_imagen.jpg", model_id="face-mask-detection-tmy8p/1")
        etiquetas_mascarilla = [p["class"] for p in resultado_mascarilla["predictions"]]
        print("Etiquetas Mascarilla:", etiquetas_mascarilla)

        # Armo el resultado final
        resultado_final = {
            "casco": any(c in etiquetas_ppe for c in ["helmet", "Casco"]),
            "chaleco": any(c in etiquetas_ppe for c in ["vest", "Chaleco"]),
            "guantes": len(etiquetas_guantes) > 0,
            "mascarilla": len(etiquetas_mascarilla) > 0,
        }

        return resultado_final