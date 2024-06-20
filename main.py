from def_imports import *
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'

# Define o caminho para a imagem capturada
image_path = 'captured_image.png'

# Função que captura a imagem pela webcam
capture_image(image_path)

# Faz a detecção facial na imagem capturada
print(detect_faces(image_path))