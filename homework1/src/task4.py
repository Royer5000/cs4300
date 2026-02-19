def calculate_discount(price, discount):
    finalPrice = price - discount
    return finalPrice

price = 99.99
discount = 20.00
finalPrice = calculate_discount(price, discount)
print(finalPrice)
