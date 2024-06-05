from fastapi import FastAPI
from pydantic import BaseModel
import openai
from pymongo import MongoClient

openai.api_key = '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'

app = FastAPI()

# MongoDB 설정
client = MongoClient('mongodb+srv://minwoo:alsdn980623@minwoo.gcloveg.mongodb.net/?retryWrites=true&w=majority&appName=Minwoo')
db = client['Advertisement']
collection = db['Advertisement']


class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self, prompt):
        system_instruction = 'assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라'
        messages = [{'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': prompt}]
        response = openai.ChatCompletion.create(model=self.engine, messages=messages)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_engine(prompt=prompt)
        return result


class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str


@app.post('/create_ad')
async def create_ad(product: Product):
    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name=product.product_name,
                               details=product.details,
                               tone_and_manner=product.tone_and_manner)

    # MongoDB 저장
    ad_data = {
        'product_name': product.product_name,
        'details': product.details,
        'ad': ad
    }
    collection.insert_one(ad_data)

    return {'ad': ad}
