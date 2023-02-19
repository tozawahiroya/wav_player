
import streamlit as st

uploaded_file = st.file_uploader("Choose a file")

st.audio(uploaded_file)










