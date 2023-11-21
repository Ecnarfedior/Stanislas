import streamlit as st
import pandas as pd
import numpy as np

st.title('Hello Wilders, welcome to my application!')

st.write("I enjoy to discover stremalit possibilities")

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(link)

# Here we use "magic commands":
df

options = ["US", "EUROPE", "JAPON"]
statut = st.selectbox("Choisissez une valeur :", options)

if st.button('US'):
    st.write('Vous avez cliqué sur le bouton.')

if st.button('EUROPE'):
    st.write('Vous avez cliqué sur le bouton.')

if st.button('JAPON'):
    st.write('Vous avez cliqué sur le bouton.')
