import streamlit as st
import requests
from pymongo import MongoClient
import pandas as pd

# MongoDB setup
client = MongoClient('mongodb+srv://minwoo:alsdn980623@minwoo.gcloveg.mongodb.net/?retryWrites=true&w=majority&appName=Minwoo')
db = client['Advertisement']
collection = db['Advertisement']

st.title('광고 문구 서비스앱')
generate_ad_url = 'http://127.0.0.1:8000/create_ad'

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고 문구의 느낌', options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게'], default=['기본'])

if st.button("광고 문구 생성하기"):
    try:
        response = requests.post(
            generate_ad_url,
            json={"product_name": product_name,
                  "details": details,
                  "tone_and_manner": ", ".join(options)})
        ad = response.json()['ad']
        st.success(ad)

        # Save ad data to MongoDB
        ad_data = {
            'product_name': product_name,
            'details': details,
            'ad': ad
        }
        collection.insert_one(ad_data)
    except Exception as e:
        st.error(f"연결 실패! {e}")

st.write("저장된 광고 문구")

# Fetch
ads = list(collection.find())
if ads:
    df = pd.DataFrame(ads)
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    st.table(df)
else:
    st.write("No ads found in the database.")
