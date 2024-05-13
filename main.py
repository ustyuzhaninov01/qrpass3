import streamlit as st
import pandas as pd
from PIL import Image
import cv2
import pyqrcode
import numpy as np

# Função para verificar se o email está na lista de participantes
def verificar_participante(email_afiliado):
    if email_afiliado in lista_participantes:
        st.success(f"E-mail encontrado na lista de participantes: {email_afiliado}.")
    else:
        st.warning("E-mail não encontrado na lista de participantes.")

# Função para ler o QR code
def ler_qr_code(frame):
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecodeMulti(frame)
    if bbox is not None:
        for i in range(len(bbox)):
            cv2.polylines(frame, [np.int32(bbox[i])], True, (255, 0, 0), 2)
            email_afiliado = data[i]
            verificar_participante(email_afiliado)
    return frame

# Função para gerar o QR code com o email do afiliado
def gerar_qr_code(email_afiliado):
    qr_code = pyqrcode.create(email_afiliado)
    qr_code.png("qr_code_afiliado.png", scale=8)

# Carregar a lista de participantes do arquivo CSV
def carregar_lista_participantes():
    try:
        df = pd.read_csv("melist.csv")  # Substitua "meelist.csv" pelo caminho do seu arquivo CSV
        lista_participantes = df['mail'].tolist()
        return lista_participantes
    except FileNotFoundError:
        st.error("Arquivo 'meelist.csv' não encontrado.")

# Criar a Streamlit app
st.title("Verificador de Participantes e Gerador de QR Code")

# Carregar a lista de participantes
lista_participantes = carregar_lista_participantes()

# Criar um campo de texto para inserir o email do afiliado
email_afiliado = st.text_input("Digite o e-mail do afiliado")

# Botão para gerar o QR code
if st.button("Gerar QR Code"):
    if email_afiliado:
        gerar_qr_code(email_afiliado)
        imagem_qr = Image.open("qr_code_afiliado.png")
        st.image(imagem_qr, caption='QR Code gerado com sucesso!', use_column_width=True)
    else:
        st.error("Por favor, insira um e-mail válido.")

# Botão para iniciar a câmera e verificar o participante
if st.button("Verificar Participante"):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Erro ao capturar vídeo.")
            break
        frame = ler_qr_code(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, channels="RGB", caption="Pressione 'Esc' para encerrar.")
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()




