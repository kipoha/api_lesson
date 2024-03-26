import requests
from config import *

url = URL
category = 'categories/'
product = 'products/'
review = 'reviews/'

data_category = {
    'name': 'hehe',
}

data_product = {
    'title': 'kika',
    'description': 'da',
    'price': 100,
    'category_id': 5,
    'tags': [1, 2]
}

data_review = {
    'text': 'testing...',
    'stars': 4,
    'product_id': 9
}

url += product

# url += '3/'

result = requests.post(url, data=data_product)

print("Status:", result.status_code)
# print("Content:", result.content)
# print("Text:", result.text)

try:
    print("JSON Response:", result.json())
except ValueError:
    print("Response is not in JSON format")
