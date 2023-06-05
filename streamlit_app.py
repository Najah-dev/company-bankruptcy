from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://najahamrullah:{password}@tutorial.omdt7uf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.ml_uas
collections = test_db.list_collection_names()

import streamlit as st
import pandas as pd

# primaryColor="#F63366"
# backgroundColor="#FFFFFF"
# secondaryBackgroundColor="#F0F2F6"
# textColor="#262730"
# font="sans serif"

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠",
)

st.markdown("<h1 style='color: #22A7EC;'>Company Bankruptcy Prediction</h1>", unsafe_allow_html=True)
st.markdown("Aplikasi ini berguna untuk mengklasifikasi kebangkrutan sebuah perusahaan")
st.markdown("______")
# st.sidebar.success("pilih halaman")

from PIL import Image
image = Image.open('company.jpg')

st.image(image, caption='~')

st.write(
    """
    # Definisi

    Prediksi kebangkrutan perusahaan adalah proses menggunakan berbagai metode analisis
    untuk mengevaluasi kesehatan keuangan suatu perusahaan dan memprediksi apakah
    perusahaan tersebut berisiko menghadapi kebangkrutan di masa depan.

    Tujuan dari prediksi kebangkrutan perusahaan adalah memberikan informasi kepada
    pemangku kepentingan, seperti pemilik saham, kreditor, dan pemasok, agar mereka dapat
    mengambil langkah-langkah yang tepat untuk mengurangi risiko atau melindungi
    kepentingan mereka.
    """
)

# About us
# st.sidebar.header('About Us')
st.sidebar.markdown('Created by Kelompok 8')
