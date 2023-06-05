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
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from sklearn.svm import SVC
import pickle
import joblib
import matplotlib.pyplot as plt
import plotly.express as px

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


# Connect to MongoDB
connection_string = f"mongodb+srv://najahamrullah:{password}@tutorial.omdt7uf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['ml_uas']
collection = db['ml_uas']

# Get data from MongoDB
data = collection.find()

# Create a DataFrame
df = pd.DataFrame(list(data))

# Sort by timestamp
#df.sort_values(by='timestamp', ascending=False, inplace=True)
def model():
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix, classification_report
        
    dataset = pd.DataFrame(df)
        
    # Hapus baris yang mengandung nilai NaN
    dataset.dropna()
        
    # Pisahkan fitur dan label
    X = dataset.drop(['Bankrupt?', '_id'], axis = 1)
    y = dataset['Bankrupt?']

    # Split data menjadi data latih dan data uji
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inisialisasi dan latih model Regresi Logistik
    logreg_model = LogisticRegression()
    logreg_model.fit(X_train, y_train)

    # Evaluasi model menggunakan data uji
    y_pred = logreg_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    #print("Akurasi model:", accuracy)
    # Simpan model dalam file .pkl
    joblib.dump(logreg_model, '../model_saved/logistic_regression_model.pkl')

    return logreg_model



st.markdown("<h1 style='color: #22A7EC;'>Input Data</h3>", unsafe_allow_html=True)
st.write("#### Masukkan Data Variabel yang Diperlukan")

x1 = st.number_input('Current Ratio', format="%.5f")
x2 = st.number_input('Retained Earnings to Total Assets', format="%.5f")
x3 = st.number_input('ROA(C) before interest and depreciation before interest', format="%.5f")
x4 = st.number_input('Net worth/Assets', format="%.5f")

# If button is pressed
if st.button("Submit"):
    logreg_model = joblib.load("model_saved/logistic_regression_model.pkl")
        
    X = pd.DataFrame([[x1, x2, x3, x4]], 
                     columns = ["Current Ratio", "Retained Earnings to Total Assets", "masukkan variabel ROA(C) before interest and depreciation before interest", "Net worth/Assets"])
        
    # Get prediction
    prediction = logreg_model.predict(X)[0]
    
    new_data = {
        'Bankrupt?': int(prediction),  # mengubah tipe data ke int agar sesuai dengan tipe data di MongoDB
        'Current Ratio': x1, 
        'Retained Earnings to Total Assets': x2, 
        'ROA(C) before interest and depreciation before interest': x3, 
        'Net worth/Assets': x4
    }
    
    # Memasukkan data baru ke dalam koleksi
    collection.insert_one(new_data)
    
    if prediction == 0:
        st.write('The company is not bankrupt.')
    else:
        st.write('The company is bankrupt.')



st.markdown("<h1 style='color: #22A7EC;'>Visualisasi Data</h3>", unsafe_allow_html=True)
st.write("#### Berikut adalah visualisasi data mengenai company bankruptcy prediction")
st.markdown("______")

#sidebar
#st.sidebar.title('Visualisasi apakah perusahaan tersebut bangkrut atau tidak')

if st.checkbox("Show Data"):
    st.write(df.head(10))

#selectbox + visualisation

# Multiple widgets of the same type may not share the same key.
select=st.sidebar.selectbox('pilih jenis grafik',['Histogram','Pie Chart'],key=0)
bankruptcy=df['Bankrupt?'].value_counts()
bankruptcy=pd.DataFrame({'bankruptcy':bankruptcy.index,'Jumlah':bankruptcy.values})

st.markdown("###  company bankruptcy count")
if select == "Histogram":
        fig = px.bar(bankruptcy, x='bankruptcy', y='Jumlah', color = 'bankruptcy', height= 500)
        st.plotly_chart(fig)
else:
        fig = px.pie(bankruptcy, values='Jumlah', names='bankruptcy')
        st.plotly_chart(fig)



# About us
# st.sidebar.header('About Us')
st.sidebar.markdown('Created by Kelompok 8')
