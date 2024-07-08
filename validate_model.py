import torch
import torchvision.transforms as transforms
from PIL import Image
import os
from ultralytics import YOLO

# Definir las transformaciones de la imagen
transform = transforms.Compose([
    transforms.Resize((640, 640)),  # Cambiado a 640x640 para coincidir con el tamaño esperado por YOLO
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"El archivo del modelo {model_path} no existe.")
    
    model = YOLO(model_path)
    model.eval()
    return model

def validate_image(image_path, model):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen {image_path} no existe.")
    
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        results = model(image)
    
    # Asume que el modelo produce una lista de resultados
    predictions = []
    for result in results:
        predictions.append(result)
    
    return predictions

if __name__ == "__main__":
    model_path = 'best.pt'  # Sustituye esto con la ruta real a tu modelo
    image_path = os.path.join('images', 'frisona.jpg')  # Ruta a la imagen frisona.jpg
    
    try:
        model = load_model(model_path)
        predictions = validate_image(image_path, model)
        print(f'Predicciones: {predictions}')
    except Exception as e:
        print(f"Error: {e}")