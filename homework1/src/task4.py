def calculate_discount(price, discount):
    final_price = price - price * (discount * 0.01)
    final_price = (int)(final_price * 100) / 100
    return final_price

price = 100
discount = 20
final_price = calculate_discount(price, discount)
print(final_price)
