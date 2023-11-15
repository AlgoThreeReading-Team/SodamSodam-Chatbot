# 결제해줘 -> 장바구니 보여주기 -> 모두 결제할 것인지, 번호 선택할 것인지 와 재확인 -> 비밀번호 확인 -> 결제 완료
from cart.cart import (
    get_all_cart_items,
    korean_to_number,
    cart,
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

    if len(cart) == 0:
        return "장바구니에 담긴 상품이 없습니다. 쇼핑 로직으로 돌아갑니다."

    if password == "":
        return "비밀번호를 재설정 해주세요. 쇼핑 로직으로 돌아갑니다."

    if "결제 취소" in query:
        is_payment = False
        now_method = 0
        return "결제 취소 되셨습니다. 쇼핑 로직으로 돌아갑니다."
    else:
        if now_method == 0:
            print(method[now_method])
            answer = get_all_cart_items() + "\n모두 결제하고 싶다면 '모두 결제'를 말하고, 원하는 상품들만 결제하고 싶다면 번호를 말해주세요."
            now_method = now_method + 1
            return answer

        elif now_method == 1:
            print(method[now_method])
            if "모두" in query:
                choose_items = cart
                answer = f"장바구니에 총 {len(cart)}개의 상품이 있습니다.\n 구매하시는 상품 개수가 맞다면 비밀번호를 말해주세요"
                now_method = now_method + 1
                return answer
            else:
                choose_items = choose_cart_items(query)
                answer = buy_reconfirm(choose_items) + "\n 구매하실 상품(들)이 맞으면 비밀번호를 말해주세요"
                now_method = now_method + 1
                return answer
        elif now_method == 2:
            print(method[now_method])
            change_number = korean_to_number(query)
            numbers = [int(char) for char in change_number if char.isdigit()]
            input_password = ''.join(map(str, numbers))

            if input_password == password:
                return "결제가 완료되었습니다."
            else:
                if 3-password_count == 0:
                    password = ""
                    return "비밀번호를 재설정 해주세요"
                else:
                    answer = f"비밀번호가 틀렸습니다. {3-password_count}번 기회가 남았습니다."
                    password_count = password_count + 1
                    return answer

def choose_cart_items(query):
    change_number = korean_to_number(query)
    numbers = [int(char) for char in change_number if char.isdigit()]
    return numbers


def buy_reconfirm(choose_items):
    items = f"장바구니에 총 {len(choose_items)}개의 상품이 있습니다.\n"
    for i, item in enumerate(choose_items, 1):
        product_info = get_product_info_by_id(choose_items)
        items = items + f"{i}번 : {product_info['title']}\n"

    return items