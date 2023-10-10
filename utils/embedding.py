import pandas as pd
from sentence_transformers import SentenceTransformer
import csv

data = pd.read_csv('utils/product.csv', encoding='cp949')

#data['combined_text'] = data['review_title'] + ' ' + data['review_content']
model = SentenceTransformer('jhgan/ko-sroberta-multitask')
data['hf_embeddings'] = data['review'].apply(lambda x: model.encode(x))

print(data.head(3))

data.to_csv('./embedded_product.csv', quoting=csv.QUOTE_ALL, index=False, encoding='utf-8-sig')