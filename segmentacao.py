"""
Exercicio: fruta fora da especificação

Objetivo
- Esse algoritmo é um sistema simples de Visão Computacional 
  utilizando uma Raspberry Pi com câmera (PiCamera) 
- A partir de uma região da imagem selecionada manualmente 
  pelo usuário (ROI), o sistema identifica a faixa de cor (em HSV)
  e gera uma máscara que destaca todas as áreas da imagem com 
  tonalidade semelhante, permitindo a visualização da presença 
  da cor ao longo do vídeo em tempo real.

Resumo
- Captura vídeo da webcam em tempo real
- Solicita que o usuário selecione uma região da imagem 
  com a cor desejada (ROI)
- Extrai automaticamente a faixa de cor (HSV) dessa região
- Gera e exibe uma máscara binária que destaca todas as áreas da 
  imagem que possuem a mesma faixa de cor
- Atualiza a máscara continuamente a cada novo quadro

Aplicações
- Rastreamento básico de cores em sistemas embarcados
- Detecção de presença ou ausência de objetos coloridos 
  em linhas de montagem industrial
- Sistemas de segurança, identificando mudanças de cor 
  em ambientes monitorados
- Monitoramento agrícola para detectar o amadurecimento 
  de frutas com base na cor
- Dispositivos IoT para alertas visuais baseados em 
  detecção de cores específicas
- Análise ambiental, como identificação de manchas de 
  poluição ou variação de cores em corpos d'água
"""

import cv2
import numpy as np


def extrairCor(imagem, r):
    imagemHSV = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    imagemNova = imagemHSV[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
    H, S, V = imagemNova[:, :, 0], imagemNova[:, :, 1], imagemNova[:, :, 2]
    hMin, hMax = np.min(H), np.max(H)
    sMin, sMax = np.min(S), np.max(S)
    vMin, vMax = np.min(V), np.max(V)

    limiteBaixo = np.array([hMin, sMin, vMin], np.uint8)
    limiteAlto = np.array([hMax, sMax, vMax], np.uint8)
    return limiteBaixo, limiteAlto


def testaCor(imagem, limiteBaixo, limiteAlto):
    imagem2 = imagem.copy()
    imagemHSV = cv2.cvtColor(imagem2, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(imagemHSV, limiteBaixo, limiteAlto)
    return imagem2, mascara


resolucao = (640, 480)
camera = cv2.VideoCapture(0)
camera.set(3, resolucao[0])
camera.set(4, resolucao[1])

contagem = 0
while True:
    sucesso, imagem = camera.read()
    if not sucesso:
        break

    if contagem == 10:
        roi = cv2.selectROI(
            "imagem", imagem, fromCenter=False, showCrosshair=True)
        roi = tuple(map(int, roi))
        limiteBaixo, limiteAlto = extrairCor(imagem, roi)
    elif contagem > 10:
        _, mascara = testaCor(imagem, limiteBaixo, limiteAlto)
        cv2.imshow("imagem", mascara)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    contagem += 1

camera.release()
cv2.destroyAllWindows()
