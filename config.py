import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 認証に必要なキーとトークン
HOT_PEPPER_API_KEY = os.environ['HOT_PEPPER_API_KEY']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']

HOT_PEPPER_API_URL = os.environ['HOT_PEPPER_API_URL']
GOOGLE_MAPS_API_URL = os.environ['GOOGLE_MAPS_API_URL']
