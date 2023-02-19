
import streamlit as st

speech_file='test_2023-02-19-06-40-28-929818.wav'
with io.open(speech_file,'rb') as f:
    content = f.read()

st.audio(content)










