import streamlit as st
import pandas as pd
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import pyqrcode
import numpy as np

st.title("Verificador de Participantes e Gerador de QR Code")

def gerar_qr_code(email_afiliado):
    qr_code = pyqrcode.create(email_afiliado)
    qr_code.png("qr_code_afiliado.png", scale=8)


email_afiliado = st.text_input("Digite o e-mail do afiliado")

# Botão para gerar o QR code
if st.button("Gerar QR Codeeeee"):
    if email_afiliado:
        gerar_qr_code(email_afiliado)
        imagem_qr = Image.open("qr_code_afiliado.png")
        st.image(imagem_qr, caption='QR Code gerado com sucesso!', use_column_width=True)
    else:
        st.error("Por favor, insira um e-mail válido.")
# Função para verificar se o email está na lista de participantes
def verificar_participante():
    email_afiliado = data
    if email_afiliado:
        if email_afiliado in lista_participantes:
            st.success(f"Email found in the list of participants: {email_afiliado}.")
        else:
            st.warning("Email not found in the list of participants.")
    else:
        st.error("No QR code detected.")


# Função para ler o QR code

image = st.camera_input("Show QR code")

if image is not None:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
    st.write(data)



# Função para gerar o QR code com o email do afiliado


# Carregar a lista de participantes do arquivo CSV
def carregar_lista_participantes():
    try:
        df = pd.read_csv("Melist.csv")  # Substitua "meelist.csv" pelo caminho do seu arquivo CSV
        lista_participantes = df['mail'].tolist()
        return lista_participantes
    except FileNotFoundError:
        st.error("Arquivo 'melist.csv' não encontrado.")

# Criar a Streamlit app


# Carregar a lista de participantes
lista_participantes = carregar_lista_participantes()

# Criar um campo de texto para inserir o email do afiliado


# Botão para verificar o participante
if st.button("Verificar Participante"):
    if not email_afiliado:
        st.error("Nenhum email fornecido. Por favor escanea o QR-CODE para verificar.")
    else:
        verificar_participante(email_afiliado)






