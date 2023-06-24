import streamlit as st
import openai
import requests
from pprint import pprint

rapidapi_key = st.secrets["rapidapi_key"]
naver_client_id = st.secrets["naver_client_id"]
naver_client_secret = st.secrets["naver_client_secret"]

def summarize_and_translate(article_url, min_length=100, max_length=300):
    url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-url/"

    payload = {
        "url": article_url, # 주소
        "min_length": min_length, # 최소 길이
        "max_length": max_length, # 최대 길이
        "is_detailed": False # 한 문장으로 반환할 것인지 여부
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    summary = response.json()['summary'][0].strip()

    url = "https://openapi.naver.com/v1/papago/n2mt"

    payload = {
        "source": "en",
        "target": "ko",
        "text": summary,
    }

    headers = {
        "content-type": "application/json",
        "X-Naver-Client-Id": naver_client_id,
        "X-Naver-Client-Secret": naver_client_secret
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()['message']['result']['translatedText']

st.title("Summarize_and_Translate")

with st.form("form"):
    article_url = st.text_input("Article_URL")
    submit = st.form_submit_button("Submit")
    sumNtran = summarize_and_translate(article_url, 50, 100)
    with st.spinner("Waiting for Summation..."):
        if submit and article_url:
            st.write(sumNtran)
