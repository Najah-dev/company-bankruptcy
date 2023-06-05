from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

#connection_string = f"mongodb+srv://najahamrullah:{password}@tutorial.omdt7uf.mongodb.net/?retryWrites=true&w=majority"

#client = MongoClient(connection_string)

#dbs = client.list_database_names()
#test_db = client.ml_uas
#collections = test_db.list_collection_names()

import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from sklearn.svm import SVC
import pickle
import joblib


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



st.markdown("<h1 style='color: #22A7EC;'>Company Bankruptcy Prediction</h1>", unsafe_allow_html=True)
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
    
    #st.experimental_rerun()
        #st.success("Data berhasil di update.")
        # # Unpickle classifier 
        # clf = joblib.load('model_saved/logistic_regression_model.pkl')
        
        # df = pd.DataFrame(get_data_from_db())
        # #st.dataframe(df)
        # # Store inputs into dataframe
        # X = df.drop(['Bankrupt?', '_id'], axis = 1)
        # Y = df['Bankrupt?']
        # # Get prediction
        # prediction = clf.predict(X)     
        
        #if prediction == 0:
            #st.write('The company is not likely to go bankrupt.')
        #else: 
            #st.write('The company is likely to go bankrupt.')


# Train an SVM model
#def user_input_features():
    #form = st.form(key='my_form')
    #x1 = form.number_input('masukkan variabel Current Ratio')
    #x2 = form.number_input('masukkan variabel Retained Earnings to Total Assets')
    #x3 = form.number_input('masukkan variabel ROA(C) before interest and depreciation before interest')
    #x4 = form.number_input('masukkan variabel Net worth/Assets')
    #orm.form_submit_button('prediksi')
    #data = {'Current Ratio': x1,
            #'Retained Earnings to Total Assets': x2,
            #'ROA(C) before interest and depreciation before interest': x3,
            #'Net worth/Assets': x4}
    #features = pd.DataFrame(data, index=[0])
    #return features
#input_df = user_input_features()

#UAS = pd.read_csv('Data_UAS.csv')
#penguins = UAS.drop(columns=['Bankrupt?'])
#df = input_df

# Reads in saved classification model
#load_clf = pickle.load(open('model_svm.pkl', 'rb'))


# Apply model to make predictions
#prediction = load_clf.predict(df)

#st.write("Hasil Prediksi:", prediction)


#st.subheader('Prediction')
#penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
#st.write(penguins_species[prediction])

#st.subheader('Prediction Probability')
#st.write(prediction_proba)

# Display dataframe with prediction column
#st.write('DataFrame with Prediction:')
#st.write(data_with_prediction)

# Display prediction result
#if prediction[0] == 0:
    #st.write('The company is not likely to go bankrupt.')
#else:
    #st.write('The company is likely to go bankrupt.')

# About us
# st.sidebar.header('About Us')
st.sidebar.markdown('Created by Kelompok 8')