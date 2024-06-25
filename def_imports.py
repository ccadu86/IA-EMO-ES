# Importa as bibliotecas necessárias
import cv2  # Biblioteca para manipulação de imagens e vídeo
from google.cloud import vision  # Biblioteca do Google Cloud para detecção de faces
import numpy as np  # Biblioteca para manipulação de arrays
import RPi.GPIO as GPIO  # Biblioteca para controle de GPIO no Raspberry Pi

def detectorDeRosto(arquivoDeImagem):
    # Cria um cliente para o serviço de detecção de faces do Google Cloud
    client = vision.ImageAnnotatorClient()

    # Lê a imagem do arquivo
    with open(arquivoDeImagem, "rb") as image_file:
        content = image_file.read()

    # Cria um objeto de imagem a partir do conteúdo lido
    imagem = vision.Image(content=content)
    
    # Envia a imagem para o serviço de detecção de faces
    response = client.face_detection(image=imagem)
    faces = response.face_annotations

    # Verifica se houve algum erro na resposta
    if response.error.message:
        raise Exception(
            "{}\nPara informações ou erros, acesse: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # Retorna as anotações de faces detectadas
    return faces

def legendasDesenhosRosto(frame, faces):
    for face in faces:
        # Redimensiona as coordenadas dos vértices para a escala atual
        vertices = [(round(vertex.x * 1.5), round(vertex.y * 1.125)) for vertex in face.bounding_poly.vertices]
        pontos = np.array(vertices, np.int32)
        pontos = pontos.reshape((-1, 1, 2))

        # Desenha um polígono ao redor da face detectada
        cv2.polylines(frame, [pontos], True, (0, 255, 0), 2)

        # Obter a probabilidade dos sentimentos e a legenda correspondente
        probabilidades = {
            'FELICIDADE': face.joy_likelihood,
            'TRISTEZA': face.sorrow_likelihood,
            'RAIVA': face.anger_likelihood,
            'SURPRESA': face.surprise_likelihood
        }

        # Define um nível de comparação e o texto inicial
        comparacao = 2
        texto = "SENTIMENTO: NEUTRO"
        cores = (0, 0, 0)
        borda = (0,0,0)
        # Atualiza o texto com base na probabilidade dos sentimentos
        for chave, valor in probabilidades.items():
            if valor > comparacao:
                texto = f"SENTIMENTO: {chave}"
                match chave:
                    case "FELICIDADE":
                        cores = (0, 255, 255)  # Amarelo (BGR)
                        borda = (0,0,0)     # PRETO

                    case "TRISTEZA":
                        cores = (255, 0, 0)  # Azul (BGR)
                        borda = (0,0,0)     # PRETO

                    case "RAIVA":
                        cores = (0, 0, 255)  # Vermelho (BGR)
                        borda = (0,0,0)     # PRETO

                    case "SURPRESA":
                        cores = (128, 0, 128)  # Roxo escuro (BGR)
                        borda = (0,0,0)     # PRETO

                    case _:
                        cores = (0, 0, 0)


                

        # Define as posições iniciais e finais para exibir o texto
        Xinicial = vertices[0][0]
        Yinicial = vertices[0][1]
        Xfinal = vertices[3][0]
        Yfinal = vertices[3][1]
        text = texto

        # Exibe o texto no frame
        if Yinicial >= 45:
            # Desenha o contorno preto
            cv2.putText(frame, text, (Xinicial, Yinicial - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, borda, 6, cv2.LINE_AA)
            # Desenha o texto colorido
            cv2.putText(frame, text, (Xinicial, Yinicial - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, cores, 2, cv2.LINE_AA)
        else:
            # Desenha o contorno preto
            cv2.putText(frame, text, (Xfinal, Yfinal + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, borda, 6, cv2.LINE_AA)
            # Desenha o texto colorido
            cv2.putText(frame, text, (Xfinal, Yfinal + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, cores, 2, cv2.LINE_AA)

def capturaDeVideo():
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
    larguraDaTela = 1920
    alturaDaTela = 1080

    while True:
        estadoDoBotao = GPIO.input(BUTTON_PIN)

        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona o frame para preencher a tela
        frame_resized = cv2.resize(frame, (larguraDaTela, alturaDaTela), interpolation=cv2.INTER_LINEAR)

        if estadoDoBotao == 0:
            # Exibe o frame redimensionado na janela
            cv2.imshow('Webcam', frame_resized)

        # Sai do loop quando a tecla 'q' é pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        # Se o botão for pressionado, capture e exiba a imagem
        if estadoDoBotao == 1:
            # Define o caminho para salvar a imagem capturada
            arquivoDeImagem = 'captured_image.jpg'
            cv2.imwrite(arquivoDeImagem, frame)

            # Detecta as faces na imagem capturada
            faces = detectorDeRosto(arquivoDeImagem)
        
            # Exibe a imagem capturada
            capturarFrame = cv2.imread(arquivoDeImagem)
            frame_height, frame_width, _ = capturarFrame.shape

            # Redimensiona a imagem capturada
            imagem = cv2.resize(capturarFrame, (larguraDaTela, alturaDaTela), interpolation=cv2.INTER_LINEAR)
        
            # Desenha as legendas e os desenhos no frame capturado
            legendasDesenhosRosto(imagem, faces)
            
            cv2.imshow('Captura', imagem)
            cv2.waitKey(1)  # Atualiza a tela
            
            while estadoDoBotao == 1:
                estadoDoBotao = GPIO.input(BUTTON_PIN)
                cv2.imshow('Captura', imagem)
                cv2.waitKey(1)  # Atualiza a tela
        
            cv2.destroyWindow('Captura')  # Fecha a janela da captura

    # Libera a captura e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
