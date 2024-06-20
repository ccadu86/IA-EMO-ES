import cv2
from google.cloud import vision
import numpy as np
import RPi.GPIO as GPIO

def detectorDeRosto(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return faces

def legendasDsenhosRosto(frame, faces):
    for face in faces:
        vertices = [(vertex.x*3, round(vertex.y*2.25)) for vertex in face.bounding_poly.vertices]
        pts = np.array(vertices, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        # Obter a probabilidade mais provável e sua legenda correspondente
        likelihoods = {
            'Alegria': face.joy_likelihood,
            'Tristeza': face.sorrow_likelihood,
            'Raiva': face.anger_likelihood,
            'Surpresa': face.surprise_likelihood
        }

        # Converter likelihood para porcentagem
        # likelihood_name = {
        #     0: "Desconhecido",
        #     1: "Muito Improvável",
        #     2: "Improvável",
        #     3: "Possível",
        #     4: "Provável",
        #     5: "Muito Provável"
        # }

        likelihood_name = (
             "Desconhecido",
             "Muito Improvável",
             "Improvável",
             "Possível",
             "Provável",
             "Muito Provável"
        )

        valor =2
        texto = "SENTIMENTO NEUTRO"
        if (likelihoods['Alegria']>valor): 
            valor=likelihoods['Alegria']
            texto = "SENTIMENTO: FELICIDADE"
        if (likelihoods['Tristeza']>valor): 
            valor=likelihoods['Tristeza']
            texto = "SENTIMENTO: TRISTEZA"
        if (likelihoods['Raiva']>valor): 
            valor=likelihoods['Raiva']
            texto = "SENTIMENTO: RAIVA"
        if (likelihoods['Surpresa']>valor): 
            valor=likelihoods['Surpresa']
            texto = "SENTIMENTO: SURPRESO"


        
        # print("Oir carlão", likelihoods['Alegria'])

        # most_likely_emotion = max(likelihoods, key=likelihoods.get)
        # most_likely_value = likelihoods[most_likely_emotion]
        # most_likely_percent = (most_likely_value / 5) * 100

        # # Desenhar as legendas de todas as emoções
        text_y_offset = 20

        # for emotion, value in likelihoods.items():
        #     percent = (value / 5) * 100
        #     color = (0, 255, 0) if emotion == most_likely_emotion else (0, 0, 255)
        #     text = f"{emotion}: {percent:.2f}% ({likelihood_name[value]})"
        #     vertice1 = vertices[0][0]
        #     vertice2 = int(round(vertices[0][1]))

        vertice1 = vertices[0][0]
        vertice2 = int(round(vertices[0][1]))
        text = texto
        color = (255,0, 0)

        cv2.putText(frame, text, (vertice1, vertice2 - text_y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        text_y_offset += 20

def capture_video():
    # Inicializa a captura de vídeo da webcam
    cap = cv2.VideoCapture(0)
    GPIO.setmode(GPIO.BCM)
    BUTTON_PIN = 17
    GPIO.setup(BUTTON_PIN, GPIO.IN)

    # Define a resolução desejada (1920x1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Cria uma janela e define-a para fullscreen
    cv2.namedWindow('Webcam', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Webcam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Define a resolução da tela
    screen_width = 1920
    screen_height = 1080

    while True:
        button_state = GPIO.input(BUTTON_PIN)

        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona o frame para preencher a tela
        frame_resized = cv2.resize(frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)

        if button_state == 0:
            # Exibe o frame redimensionado na janela
            cv2.imshow('Webcam', frame_resized)

        # Sai do loop quando a tecla 'q' é pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        # Se o botão for pressionado, capture e exiba a imagem
        if button_state == 1:
            # Define o caminho para salvar a imagem capturada
            image_path = 'captured_image.jpg'
            cv2.imwrite(image_path, frame)

            faces = detectorDeRosto(image_path)
            print(faces)
            # Exibe a imagem capturada
            captured_frame = cv2.imread(image_path)
            captured_frame_resized = cv2.resize(captured_frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)
            
            image = captured_frame_resized.astype(np.uint8)

            # Desenha as legendas e os desenhos no frame capturado
            legendasDsenhosRosto(image, faces)
            
            cv2.imshow('Captura', image)
            cv2.waitKey(1)  # Atualiza a tela
            
            while button_state == 1:
                button_state = GPIO.input(BUTTON_PIN)
                cv2.imshow('Captura', image)
                cv2.waitKey(1)  # Atualiza a tela
        
            cv2.destroyWindow('Captura')  # Fecha a janela da captura

    # Libera a captura e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()


