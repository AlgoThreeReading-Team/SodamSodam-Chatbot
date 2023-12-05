# 결제해줘 -> 장바구니 보여주기 -> 모두 결제할 것인지, 번호 선택할 것인지 와 재확인 -> 비밀번호 확인 -> 결제 완료
import cart.cart
from cart.cart import (
    get_all_cart_items,
    korean_to_number,
)
from recommend.recommend import get_product_info_by_id

is_payment = False
method = ["show cart", "choose items and reconfirm", "check password", "finish"]
now_method = 0
choose_items = []
password = "12345"
password_count = 0
def payment_logic(query):
    global now_method
    global is_payment
    global choose_items
    global password
    global password_count

    if len(cart.cart.cart) == 0:
        return "장바구니에 담긴 상품이 없습니다. 쇼핑 로직으로 돌아갑니다."

    if password == "":
        return "비밀번호를 재설정 해주세요. 쇼핑 로직으로 돌아갑니다."

    if "결제 취소" in query:
        is_payment = False
        now_method = 0
        return "결제 취소 되셨습니다. 쇼핑 로직으로 돌아갑니다."
    else:
        # 장바구니 물건 보여주기
        if now_method == 0:
            print(method[now_method])
            now_method = now_method + 1
            return show_cart()
        # 모두 선택, 번호 선택 후 재확인
        elif now_method == 1:
            print(method[now_method])
            if "모두" in query:
                now_method = now_method + 1
                return all_choose()
            else:
                # 쿼리문의 숫자 배열로 변환
                choose_items = korean_to_number(query)

                if len(choose_items) == 0:
                    answer = "모두 결제하고 싶다면 '모두 결제'를 말하고, 원하는 상품들만 결제하고 싶다면 번호를 말해주세요."
                    return answer

                now_method = now_method + 1
                return part_choose(choose_items)
        # 비밀번호 확인
        elif now_method == 2:
            print(method[now_method])
            numbers = korean_to_number(query)
            # [1,2,3,4,5] 처럼 뽑혔으면 12345 만들어줌
            input_password = ''.join(map(str, numbers))

            if input_password == password:
                password_count = 0
                is_payment = False
                now_method = 0
                cart.cart.cart = []
                return "결제가 완료되었습니다."
            else:
                if 3-password_count == 0:
                    password = ""
                    is_payment = False
                    return "비밀번호를 재설정 해주세요. 쇼핑 로직으로 돌아갑니다."
                else:
                    answer = f"비밀번호가 틀렸습니다. {3-password_count}번 기회가 남았습니다."
                    password_count = password_count + 1
                    return answer


def show_cart():
    answer = "결제 로직이 진행될 예정입니다. 결제를 그만두고 싶다면 '결제 취소'라고 말씀해주세요.\n\n"
    answer = answer + get_all_cart_items() + "\n모두 결제하고 싶다면 '모두 결제'를 말하고, 원하는 상품들만 결제하고 싶다면 번호를 말해주세요."
    return answer

def all_choose():
    answer = f"장바구니에 총 {len(cart.cart.cart)}개의 상품이 있습니다.\n 구매할 상품 개수가 맞다면 비밀번호를 말해주세요"
    return answer

def part_choose(choose_items):
    answer = f"총 {len(choose_items)}개의 상품이 있습니다.\n"
    for item in choose_items:
        product_info = get_product_info_by_id(cart.cart.cart[item-1])
        answer = answer + f"{item}번 : {product_info['title']}\n"

    answer = answer + "\n 구매할 상품(들)이 맞으면 비밀번호를 말해주세요"
    return answer