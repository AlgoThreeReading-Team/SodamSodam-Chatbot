from flask import Flask, request, jsonify, abort
from flask_restx import Api, Resource, fields
from recommend.recommend import get_query_sim_top_k
from chatbot.chatbot import get_user_intent, get_recommendation_answer
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # cors 허용
    cors = CORS(app, resources={r"/query*": {"origins": "*"}})

    # Initialize the flask-restx API
    api = Api(app, version='1.0', title='Product Recommender API',
              description='API for recommending products')
    
    # Define a namespace for your API
    ns = api.namespace('', description='Product recommendation operations')

    # Define a model for the response
    result_model = api.model('RecommendationResult', {
        'query': fields.String(description='The query for product recommendation'),
        'results': fields.List(fields.String, description='List of recommended products')
    })

    # Create a class-based resource for the recommendation endpoint
    @ns.route('/query')
    class QueryResource(Resource):
        @api.expect(api.model('Query', {
            'query': fields.String(description='The query for product recommendation'),
            'product_info': fields.String(description='The product information')
        }))
        @api.response(200, 'Success', result_model)
        def post(self):
            try:
                # Get the query from the request
                query = api.payload['query']
                # 사용자 의도 파악
                intent = get_user_intent(query)
                answer = ""

                top_k = 1  # Top k recommendations

                if intent == '결제':
                    answer = ""
                elif intent == '추천':
                    product_info = get_query_sim_top_k(query, top_k)
                    answer = product_info
                elif intent == '설명':
                    answer = ""
                elif intent == '추가 검색':
                    answer = ""

                # Create the response
                response = {
                    'query': query,
                    'intent': intent,
                    'answer': answer,
                }

                return jsonify(response)

            except Exception as ex:
                print(f"Error: {ex}")
                # Return a 500 Internal Server Error in case of an exception
                abort(500)

    return app
