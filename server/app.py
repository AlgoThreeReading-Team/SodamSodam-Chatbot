from flask import Flask, request, jsonify, abort
from flask_restx import Api, Resource, fields
from recommend.recommend import get_query_sim_top_k, get_product_info_by_id
from chatbot.chatbot import (
    get_user_intent,
    get_recommendation_answer,
    get_description_answer,
)
from automation.automation import SeleniumService
from flask_cors import CORS
import json


def create_app():
    app = Flask(__name__)
    # cors 허용
    cors = CORS(app, resources={r"/query*": {"origins": "*"}})

    # Initialize the flask-restx API
    api = Api(
        app,
        version="1.0",
        title="Product Recommender API",
        description="API for recommending products",
    )

    # Define a namespace for your API
    ns = api.namespace("", description="Product recommendation operations")

    # Define a model for the response
    result_model = api.model(
        "RecommendationResult",
        {
            "query": fields.String(description="The query for product recommendation"),
            "results": fields.List(
                fields.String, description="List of recommended products"
            ),
        },
    )

    # Create a class-based resource for the recommendation endpoint
    @ns.route("/query")
    class QueryResource(Resource):
        @api.expect(
            api.model(
                "Query",
                {
                    "query": fields.String(
                        description="The query for product recommendation"
                    ),
                    "product_id": fields.String(description="The product information"),
                },
            )
        )
        @api.response(200, "Success", result_model)
        def post(self):
            try:
                # Get the query from the request
                query = api.payload["query"]
                # 사용자 의도 파악
                intent = get_user_intent(query)
                answer = ""

                top_k = 1  # Top k recommendations

                if intent == "결제":
                    try:
                        selenium_service = SeleniumService()
                        selenium_service.initialize()
                        selenium_service.login("", "")
                        selenium_service.goToCart()
                        selenium_service.selectAllItemsInCart()
                        selenium_service.clickBuyButton()
                        selenium_service.clickPayButton()
                        selenium_service.driver.close()
                        answer = "결제가 완료되었습니다."
                    except Exception as ex:
                        print(f"Error: {ex}")
                        answer = "결제에 실패하였습니다."

                elif intent == "추천":
                    product_info = get_query_sim_top_k(query, top_k)[0]
                    answer = get_recommendation_answer(product_info)

                elif intent == "설명":
                    product_id = api.payload["product_id"]
                    if product_id:
                        product_info = get_product_info_by_id(product_id)
                        if product_info:
                            answer = get_description_answer(product_info, query)
                        else:
                            answer = "해당 상품은 없습니다."
                        answer = get_description_answer(product_info, query)
                    else:
                        answer = "상품 ID를 입력해주세요."

                elif intent == "추가 검색":
                    answer = ""

                # Create the response
                response = {
                    "query": query,
                    "intent": intent,
                    "answer": answer,
                    "product_id": str(product_info["id"]) if intent == "추천" else None,
                }

                return jsonify(response)

            except Exception as ex:
                print(f"Error: {ex}")
                # Return a 500 Internal Server Error in case of an exception
                abort(500)

    return app
