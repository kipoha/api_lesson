import requests
from config import *

url = URL
category = 'categories'
product = 'products'
review = 'reviews'

data_category = {
    'name': 'hehe',
}

data_product = {
    'title': 'kika',
    'description': 'da',
    'price': 100,
    'category_id': 4,
}

data_review = {
    'text': 'testing...',
    'stars': 4,
    'product_id': 3
}

url += review

url += '/6'

result = requests.delete(url)

print(result.status_code)