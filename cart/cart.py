import re
from recommend.recommend import get_product_info_by_id

cart = ["0","25","13","9"]
#장바구니 담기
def plus_cart_item(product_id):
    if product_id in cart:
        return False
    else:
        cart.append(product_id)
        return True
#장바구니 보기
def get_all_cart_items():
    if(len(cart) == 0):
        answer = "장바구니에 담긴 상품이 없습니다"
        return answer
    else:
        items = f"장바구니에 총 {len(cart)}개의 상품이 있습니다.\n"
        for i, item in enumerate(cart, 1):
            product_info = get_product_info_by_id(item)
            items = items + f"{i}번 : {product_info['title']}\n"

        return items

#장바구니 삭제
def delete_cart_item(query):
    numbers = korean_to_number(query)
    numbers_sorted = sorted(numbers, reverse=True)
    print(numbers_sorted)
    for number in numbers_sorted:
        del cart[number-1]

    answer = f"삭제되었습니다\n 장바구니에 총 {len(cart)}개의 상품이 있습니다."
    return answer

def korean_to_number(text):
    korean_number_map = {
        '이십': '20',
        '십일': '11',
        '십이': '12',
        '십삽': '13',
        '십사': '14',
        '십오': '15',
        '십육': '16',
        '십칠': '17',
        '십팔': '18',
        '십구': '19',
        '일': '1',
        '이': '2',
        '삼': '3',
        '사': '4',
        '오': '5',
        '육': '6',
        '칠': '7',
        '팔': '8',
        '구': '9',
        '십': '10',
    }

    for korean, number in korean_number_map.items():
        text = re.sub(korean , number , text)

    numbers = [int(char) for char in text if char.isdigit()]
    return numbers
