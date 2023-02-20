from google.cloud import storage
import os
import io
import numpy as np
import pandas as pd
import audioop
import time
import datetime
import wave
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import speech
import streamlit as st


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tech0-step3-te-bd23bed77076.json'


def record_reader(bucket_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    binary_data = blob.download_as_string()

    return binary_data


def binary_wav_converter(binary_data):
    # ファイルの情報を指定
    nchannels = 1  # モノラル
    sampwidth = 2  # 16ビット
    framerate = 44100  # サンプリング周波数
    nframes = len(binary_data)  # 音声データの長さ（バイト数）

    # WAVファイルを作成し、ヘッダーを書き込む
    with wave.open("output.wav", "wb") as wavfile:
        wavfile.setnchannels(nchannels)
        wavfile.setsampwidth(sampwidth)
        wavfile.setframerate(framerate)
        wavfile.setnframes(nframes)
        wavfile.writeframes(binary_data)

    with open("output.wav", "rb") as f:
        contents = f.read()
    
    return contents


def data_reader():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイルをドライブにアップデートした際のパス
    json = 'tech0-step3-te-bd23bed77076.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
    gc = gspread.authorize(credentials)
    #書き込み先のスプレッドシートキーを追加
    SPREADSHEET_KEY = '1eXLTugi8tzy_L_keNkeu-Slyl6YbHlRJ7-WDXdNP7n4'
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    # スプレッドシートをDataFrameに取り込む
    df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
    
    return df



st.title('ケース面接Quest 採点者用ページ')

df = data_reader()

st.write(df.iloc[1:,:])

option = st.selectbox(
    '添削希望の回答（name列をKey）',
    df['name'][df['feedback_flag'] == '1'][df['feedback']=='']
    )

if option == df['name'][0]:
    st.stop()

question = str(df['question'][df['name']==option]).split()[1]
text = df['text'][df['name']==option]
file_name = "test_"+str(df['No'][df['name']==option]).split()[1]+".wav"

bucket_name = 'tech0-speachtotext'

binary_data = record_reader(bucket_name, file_name)
contents = binary_wav_converter(binary_data)

st.info('■設問　' + question)
st.audio(contents, format="audio/wav")
st.write(text)
# st.text_area('回答内容（Speech to text）', text)






