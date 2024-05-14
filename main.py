import streamlit as st
import pandas as pd
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import pyqrcode

# Função para verificar se o email está na lista de participantes
def verificar_participante():
    email_afiliado = ler_qr_code()
    if email_afiliado:
        if email_afiliado in lista_participantes:
            st.success(f"E-mail encontrado na lista de participantes: {email_afiliado}.")
        else:
            st.warning("E-mail não encontrado na lista de participantes.")
    else:
        st.error("Nenhum QR code detectado.")

# Função para ler o QR code
def ler_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)
        if decoded_objects is not None:  # Check if QR code is detected
            for obj in decoded_objects:
                email_afiliado = obj.data.decode("utf-8")
                cap.release()
                cv2.destroyAllWindows()
                return email_afiliado
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


import cv2
import numpy as np
import streamlit as st

image = st.camera_input("Show QR code")

if image is not None:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()

    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    st.write("Here!")
    st.write(data)







# Função para gerar o QR code com o email do afiliado
def gerar_qr_code(email_afiliado):
    qr_code = pyqrcode.create(email_afiliado)
    qr_code.png("qr_code_afiliado.png", scale=8)

# Carregar a lista de participantes do arquivo CSV
def carregar_lista_participantes():
    try:
        df = pd.read_csv("Melist.csv")  # Substitua "meelist.csv" pelo caminho do seu arquivo CSV
        lista_participantes = df['mail'].tolist()
        return lista_participantes
    except FileNotFoundError:
        st.error("Arquivo 'melist.csv' não encontrado.")

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

# Botão para verificar o participante
if st.button("Verificar Participante"):
    verificar_participante()





