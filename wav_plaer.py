
import streamlit as st
#import io

#speech_file='test_2023-02-19-06-40-28-929818.wav'
#with io.open(speech_file,'rb') as f:
#    content = f.read()

content = st.file_uploader('label')
    
st.audio(content, format = "audio/wav")










