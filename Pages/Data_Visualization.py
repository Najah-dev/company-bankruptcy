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
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown("<h1 style='color: #22A7EC;'>Visualisasi Data</h1>", unsafe_allow_html=True)
st.write("#### Berikut adalah visualisasi data mengenai company bankruptcy prediction")
st.markdown("______")

#sidebar
st.sidebar.title('Visualisasi apakah perusahaan tersebut bangkrut atau tidak')

#data=pd.read_csv('resources/UAS.csv')
#checkbox to show data 
connection_string = f"mongodb+srv://najahamrullah:{password}@tutorial.omdt7uf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['ml_uas']
collection = db['ml_uas']

# Get data from MongoDB
data = collection.find()

# Create a DataFrame
df = pd.DataFrame(list(data))

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