import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")


# 사용자의 의도를 파악하는 모델
def get_user_intent(query):
    allowed_intents = ["설명", "추천", "장바구니", "결제"]
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who understands the intent of the user's question.",
        },
        {
            "role": "user",
            "content": f"Which category does the sentence below belong to: {' | '.join(allowed_intents)}? Be sure to answer with only one token. \n{query} \nA:",
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    chatbot_response = response["choices"][0]["message"]["content"]

    return chatbot_response if chatbot_response in allowed_intents else "미분류"


# TODO: 상품 추천 멘트
def get_recommendation_answer(product_info):
    return f"다음 상품은 어떠세요? 해당 상품은 {product_info['title']} 이며, 가격은 {product_info['total_price']}원 이며, 평점은 {product_info['avg_star']}, 평점 개수는 {product_info['count_star']}개 입니다. 배송료는 {product_info['shipping_fee']}원 입니다."


# TODO: 상품 설명 멘트
def get_description_answer(product_info, query):
    print(product_info, query)
    messages = [
        {"role": "system", "content": "당신은 사용자에게 상품에 대해서 설명해주는 점원입니다."},
        {"role": "assistant", "content": f"{product_info}"},
        {"role": "user", "content": f"{query}"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    chatbot_response = response["choices"][0]["message"]["content"]

    return chatbot_response
