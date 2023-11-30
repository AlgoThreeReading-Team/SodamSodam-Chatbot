from flask import Flask, request, jsonify, abort
from flask_restx import Api, Resource, fields

from recommend.recommend import (
    get_query_sim_top_k,
    get_product_info_by_id,
    get_product_reviews_by_id,
)
from chatbot.chatbot import (
    get_user_intent,
    get_recommendation_answer,
    get_description_answer,
    get_cart_intent,
)
from cart.cart import (
    plus_cart_item,
    get_all_cart_items,
    delete_cart_item,
)
import payment.payment
from payment.payment import payment_logic
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

                if payment.payment.is_payment == False:
                    # 사용자 의도 파악
                    intent = get_user_intent(query)
                    print(intent)
                    answer = ""

                    top_k = 3  # Top k recommendations
                    if intent == "payment":
                        answer = payment_logic(query)
                        payment.payment.is_payment = True
                    elif intent == "recommendation":
                        # 상품이 있으면 product_info에 상품을 담고, 없으면 None을 담음
                        product_info = get_query_sim_top_k(query, top_k)
                        if len(product_info) == 0:
                            answer = "해당 상품은 없습니다."
                        else:
                            product_info = product_info[0]
                            answer = get_recommendation_answer(product_info)

                    elif intent == "description":
                        product_id = api.payload["product_id"]
                        if product_id:
                            product_info = get_product_info_by_id(product_id)
                            if product_info:
                                answer = get_description_answer(product_info, query)
                            else:
                                answer = "해당 상품은 없습니다."
                        else:
                            answer = "어떤 상품을 원하세요?"

                    elif intent == "additional searches":
                        product_id = api.payload["product_id"]
                        if product_id:
                            product_info = get_product_info_by_id(product_id)
                            if product_info:
                                product_info = get_query_sim_top_k(
                                    product_info["title"], top_k
                                )
                                if len(product_info) == 0:
                                    answer = "해당 상품은 없습니다."
                                else:
                                    product_info = product_info[1]
                                    answer = get_recommendation_answer(product_info)
                            else:
                                answer = "해당 상품은 없습니다."
                        else:
                            product_info = None
                            answer = "어떤 상품을 원하세요?"
                    elif intent == "review":
                        product_id = api.payload["product_id"]
                        if product_id:
                            product_info = get_product_reviews_by_id(product_id)
                            if product_info:
                                # 3000자 이상 리뷰는 3000자로 자르기
                                product_info["review"] = (
                                    product_info["review"][:3000] + "..."
                                    if len(product_info["review"]) > 3000
                                    else product_info["review"]
                                )
                                print(product_info["review"])
                                answer = get_description_answer(product_info, query)
                            else:
                                answer = "해당 상품은 없습니다."
                        else:
                            answer = "어떤 상품을 원하세요?"

                    elif intent == "cart":
                        cart_intent = get_cart_intent(query)
                        if cart_intent == "show":
                            answer = (
                                get_all_cart_items()
                                + "\n만약 장바구니에 있는 상품을 삭제하고 싶다면 '장바구니 몇번 삭제'라고 말씀해주세요, 결제하고 싶다면 '결제 할래'라고 말씀해주세요."
                            )
                        elif cart_intent == "delete":
                            answer = delete_cart_item(query)
                        elif cart_intent == "add":
                            product_id = api.payload["product_id"]
                            if plus_cart_item(product_id):
                                answer = "장바구니에 담았습니다."
                            else:
                                answer = "이미 담긴 상품입니다."
                    elif intent == "unclassified":
                        answer = "죄송합니다. 다시 말씀해주세요"

                    # Create the response
                    response = {
                        "query": query,
                        "intent": intent,
                        "answer": answer,
                        "product_id": str(product_info["id"])
                        if (
                            intent == "recommendation"
                            or intent == "additional searches"
                        )
                        and product_info
                        else None,
                    }
                    print(response)

                else:
                    answer = payment_logic(query)

                    response = {
                        "query": query,
                        "intent": "payment",
                        "answer": answer,
                        "product_id": None,
                    }

                return jsonify(response)

            except Exception as ex:
                print(f"Error: {ex}")
                # Return a 500 Internal Server Error in case of an exception
                abort(500)

    return app
