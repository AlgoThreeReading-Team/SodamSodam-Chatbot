from flask import Flask, request, jsonify, abort
from recommend.recommend import get_query_sim_top_k

def create_app():
    app = Flask(__name__)

    # 챗봇 엔진 query 전송 API
    @app.route('/query', methods=['POST'])
    def query():
        try:
            # 클라이언트가 전송한 데이터를 받음
            body = request.get_json()
            query = body['query']

            top_k = 3 # 상위 n개의 유사한 상품을 추천

            # 상품 추천 모듈
            results = get_query_sim_top_k(query, top_k)
            print(results)

            # 상품 추천 결과를 클라이언트에게 전송
            response = {
                'query': query,
                'results': results
            }

            return jsonify(response)
        except Exception as ex:
            print(f"오류 발생: {ex}")
            # 오류 발생 시 500 Error
            abort(500)
        
    return app