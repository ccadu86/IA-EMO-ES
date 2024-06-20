from def_imports import *
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'

print(detect_faces('foto.jpeg'))
