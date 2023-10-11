from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd

# 모델 로딩
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 데이터 로딩
df = pd.read_csv('recommend/product.csv', encoding='cp949')
df.fillna('null', inplace=True)
df['hf_embeddings'] = df['review'].apply(lambda x: model.encode(x))

def get_query_sim_top_k(query, top_k):
    # 쿼리를 임베딩
    query_encode = model.encode(query)
    cos_scores = util.pytorch_cos_sim(query_encode, df['hf_embeddings'])[0]
    top_results = torch.topk(cos_scores, k=top_k)

    top_indices = top_results.indices.tolist()  # 상위 상품 인덱스 리스트

    # 상위 상품들의 제목과 코사인 유사도 값을 가져옴
    result_list = []

    for index in top_indices:
        product_info = {
            "title": df.iloc[index]['title'],
            "product_url": df.iloc[index]['product_url'],
            "avg_star": df.iloc[index]['avg_star'],
            "cosine_similarity": cos_scores[index].item(),
            "count_star": df.iloc[index]['count_star'],
            "total_price": df.iloc[index]['total_price'],
            "shipping_fee": df.iloc[index]['shipping_fee'] + df.iloc[index]['shipping_fee_detail'],
            "original_price": df.iloc[index]['original_price'],
            "delivery_day": df.iloc[index]['delivery_day'],
            "essential_info": df.iloc[index]['essential_info'],
            "image_text": df.iloc[index]['image_text'],
            "text": df.iloc[index]['text'],
        }
        result_list.append(product_info)

    return result_list

