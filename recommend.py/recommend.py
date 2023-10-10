# 상품 추천 모듈
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd

def get_query_sim_top_k(query, model, df, top_k):
    query_encode = model.encode(query)
    cos_scores = util.pytorch_cos_sim(query_encode, df['hf_embeddings'])[0]
    top_results = torch.topk(cos_scores, k=top_k)

    top_indices = top_results.indices.tolist()  # 상위 상품 인덱스 리스트

    # 상위 상품들의 제목과 코사인 유사도 값을 가져옴
    top_product_info = [(df.iloc[index]['title'], cos_scores[index].item()) for index in top_indices]

    return top_product_info

data = pd.read_csv('recommend.py/product.csv', encoding='cp949')
model = SentenceTransformer('jhgan/ko-sroberta-multitask')
data['hf_embeddings'] = data['review'].apply(lambda x: model.encode(x))


query = "청소기"
results = get_query_sim_top_k(query, model, data, 5)

# 보기 좋게 줄바꿈하여 제목과 코사인 유사도 출력
for idx, (title, similarity) in enumerate(results, start=1):
    print(f"{idx}. 제목: {title}, 코사인 유사도: {similarity:.4f}")
