# 챗봇 로직 및 대화 관리
import openai
import pandas as pd
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch

# openai.api_key =
def chatbot(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # 모델 출력의 온도 계수, 출력의 무작위성을 조절합니다.
        stop=None
    )
    # OpenAI의 ChatCompletion 인터페이스를 호출합니다.
    return response.choices[0].message["content"]

def recommendataion(keywords):
    data = pd.read_csv('../product.csv', encoding='cp949')

    model = SentenceTransformer('jhgan/ko-sroberta-multitask') #사전 훈련된 모델을 로드합니다. 이 모델은 한국어 텍스트를 임베딩으로 변환하는데 사용될 것입니다.
    data['hf_embeddings'] = data['image_text'].apply(lambda x: model.encode(x))

    # 상품 추천
    query_encode = model.encode(keywords)
    # Numpy 배열로 변환
    query_encode = np.array(query_encode)
    data_embeddings = np.array(data['hf_embeddings'].tolist())  # data['hf_embeddings']를 Numpy 배열로 변환
    cos_scores = util.pytorch_cos_sim(torch.tensor(query_encode), torch.tensor(data_embeddings))[0]

    top_results = torch.topk(cos_scores, k=3)
    recommended_products = data.iloc[top_results.indices]
    recommended_titles = recommended_products['title']
    recommended_similarities = top_results.values

    # 제목과 코사인 유사도 함께 출력
    for i in range(len(recommended_titles)):
        print(f"{recommended_titles.iloc[i]}  {recommended_similarities[i]}")



word = "start"
while (word != "stop"):
    word = input()
    prompt = f""" 당신의 임무는 쇼핑을 도와주는 챗봇입니다. 사용자 텍스트는 삼중 역따옴표로 구분되어 있습니다. 응답은 "user_intent", "answer" 키를 가진 JSON 객체 형식으로 포맷팅하세요.
    user_intent는 "설명", "추천", "장바구니 담기", "결제", "미분류"로 구분되며, answer은 웹사이트에서 사용할 수 있는 HTML로 포맷팅하세요. 만약 user_intent가 "추천"으로 분류되면, "answer"키는 없애고 사용자 텍스트의 핵심 단어를 "keywords" 배열에 "keyword" 키를 가진 3개의 JSON 객체 형식도 추가해주세요.
    사용자: '''{word}'''
    """
    response = chatbot(prompt)
    print(response)
    response_json = json.loads(response)
    if response_json["user_intent"] == "추천":
        formatted_keywords = " ".join(keyword["keyword"] for keyword in response_json["keywords"])

        recommendataion(formatted_keywords)






