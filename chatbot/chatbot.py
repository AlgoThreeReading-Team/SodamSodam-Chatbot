from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# 사용자의 의도를 파악하는 모델
def get_user_intent(query):
    allowed_intents = [
        "description",
        "recommendation",
        "additional searches",
        "review",
        "cart",
        "payment",
        "unclassified",
    ]
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

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    chatbot_response = response.choices[0].message.content

    return chatbot_response if chatbot_response in allowed_intents else "unclassified"


def get_cart_intent(query):
    allowed_intents = ["show", "delete", "add"]
    messages = [
        {
            "role": "system",
            "content": "You are a system that adds products to your shopping cart, shows or confirm them, and deletes them.",
        },
        {
            "role": "user",
            "content": f"Which category does the sentence below belong to: {' | '.join(allowed_intents)}? Be sure to answer with only one token. \n{query} \nA:",
        },
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    chatbot_response = response.choices[0].message.content

    return chatbot_response if chatbot_response in allowed_intents else "장바구니 의도 파악 오류"


# TODO: 상품 추천 멘트
def get_recommendation_answer(product_info):
    return f"다음 상품은 어떠세요? 해당 상품은 {product_info['title']} 이며, 가격은 {product_info['total_price']}원 이며, 평점은 {product_info['avg_star']}, 평점 개수는 {product_info['count_star']}개 입니다. 배송료는 {product_info['shipping_fee']}원 입니다."


# TODO: 상품 설명 멘트
def get_description_answer(product_info, query):
    messages = [
        {
            "role": "system",
            "content": "당신은 사용자에게 상품에 대해서 설명해주는 점원입니다. 손님은 항상 바쁘기 때문에 답변을 간결하게 하려고 노력해주세요.",
        },
        {
            "role": "user",
            "content": f"질문: {query}\n상품 정보: {product_info}\n이 상품에 대해서 설명해주는 멘트만 짧게 작성해주세요. \nA:",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.5
    )
    chatbot_response = response.choices[0].message.content

    return chatbot_response
