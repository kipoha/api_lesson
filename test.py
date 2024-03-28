import requests
from config import *
import random

url = URL
shop = 'shop/'
users = 'users/'

category = 'categories/'
product = 'products/'
review = 'reviews/'
registration = 'registration/'
login = 'login/'
confirm = 'confirm/'

data_category = {
    'name': 'hehe',
}

headers = {
    'Authorization': f'Token {ADM_TOKEN}'
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

data_users = {
    'username': 'kiki',
    'password': '123',
    'email': 'secret@gmail.com'
}

data_code = {
    'code': 584938
}

url += users

url += confirm


result = requests.post(url, data=data_code)

print("Status:", result.status_code)
# print("Content:", result.content)
# print("Text:", result.text)

try:
    print("JSON Response:", result.json())
except ValueError:
    print("Response is not in JSON format")

# code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

# print(code)