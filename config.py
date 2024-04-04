from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')
URL = config('URL')
ADM_TOKEN = config('ADM_TOKEN')
PASSWORD = config("PASSWORD")
EMAIL = config("EMAIL")
NAME = os.environ.get('NAME')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
DEBUG = os.environ.get('DEBUG')