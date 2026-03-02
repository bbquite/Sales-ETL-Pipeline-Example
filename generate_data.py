import csv
import random
from datetime import datetime, timedelta

num_rows = 1000
products = [
    "Apple",
    "Banana",
    "Orange",
    "Mango",
    "Grapes",
    "Pineapple",
    "Strawberry",
    "Blueberry",
    "Watermelon",
    "Peach",
    "Pear",
    "Plum",
    "Cherry",
    "Kiwi",
    "Lemon",
    "Lime",
    "Avocado",
    "Tomato",
    "Cucumber",
    "Carrot",
    "Potato",
    "Onion",
    "Garlic",
    "Broccoli",
    "Spinach",
    "Milk",
    "Cheese",
    "Yogurt",
    "Bread",
    "Eggs"
]
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 3, 31)

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

with open("orders.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Заголовок
    writer.writerow(["order_id", "product", "amount", "date"])
    
    # Данные
    for order_id in range(1, num_rows + 1):
        product = random.choice(products)
        amount = random.randint(10, 500)
        date = random_date(start_date, end_date)
        
        writer.writerow([order_id, product, amount, date])

print("Файл orders.csv успешно создан!")