import streamlit as st
import pandas as pd
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import pyqrcode
import numpy as np

# Function to verify if the email is in the list of participants
def verify_participant(email):
    if email:
        if email in participant_list:
            st.success(f"Email found in the list of participants: {email}.")
        else:
            st.warning("Email not found in the list of participants.")
    else:
        st.error("No QR code detected.")

# Function to read the QR code
def read_qr_code(image):
    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
        return data
    return None

# Function to generate the QR code with the affiliate's email
def generate_qr_code(email):
    qr_code = pyqrcode.create(email)
    qr_code.png("qr_code_affiliate.png", scale=8)

# Load the list of participants from the CSV file
def load_participant_list():
    try:
        df = pd.read_csv("participant_list.csv")  # Replace "participant_list.csv" with the path to your CSV file
        participant_list = df['mail'].tolist()
        return participant_list
    except FileNotFoundError:
        st.error("File 'participant_list.csv' not found.")

# Create the Streamlit app
st.title("Participant Verifier and QR Code Generator")

# Load the list of participants
participant_list = load_participant_list()

# Create a text input to enter the affiliate's email
affiliate_email = st.text_input("Enter the affiliate's email")

# Button to generate the QR code
if st.button("Generate QR Code"):
    if affiliate_email:
        generate_qr_code(affiliate_email)
        qr_image = Image.open("qr_code_affiliate.png")
        st.image(qr_image, caption='QR Code generated successfully!', use_column_width=True)
    else:
        st.error("Please enter a valid email.")

# Button to verify the participant
if st.button("Verify Participant"):
    qr_image = st.camera_input("Show QR code")
    email_from_qr = read_qr_code(qr_image)
    verify_participant(email_from_qr)





