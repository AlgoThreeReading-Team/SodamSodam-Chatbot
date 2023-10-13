import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")
print(openai.api_key)

# 사용자의 의도를 파악하는 모델
def get_user_intent(query):
  allowed_intents = ['설명', '추천', '결제']
  messages = [
      {"role": "system", "content": "You are a helpful assistant who understands the intent of the user's question."},
      {"role": "user", "content": f"Which category does the sentence below belong to: {' | '.join(allowed_intents)}? Be sure to answer with only one token. \n{query} \nA:"}
  ]

  response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
  chatbot_response = response['choices'][0]['message']['content']

  return chatbot_response if chatbot_response in allowed_intents else '미분류'

# TODO: 상품 추천 멘트
def get_recommendation_answer(product_info):
  messages = [
      {"role": "system", "content": "당신은 이제부터 시각장애인들에게 상품에 대한 정보를 제공해주는 점원입니다."},
      {"role": "assistant", "content": "다음 상품의 상품명, 가격, 평점을 두 줄이내로 딱딱 끊어서 말하지 말고 친절하게 설명해줘. 그 외에 정보들은 답변하지마."},
      {"role": "user", "content": f"{product_info}"}
  ]

  response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
  chatbot_response = response['choices'][0]['message']['content']
  return chatbot_response

# TODO: 상품 설명 멘트