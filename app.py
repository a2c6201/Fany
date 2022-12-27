import json

import requests
from flask import Flask, render_template, request, url_for

import config

hot_key = config.HOT_PEPPER_API_KEY
geo_key = config.GEOCODING_API_KEY
hot_url = config.HOT_PEPPER_API_URL
geo_url = config.GEOCODING_API_URL

# Geolocation APIを使って緯度・経度を取得
def current_location():
  data = requests.get(geo_url).json()
  return data['latitude'], data['longitude']

lat, lng = current_location()

# 検索クエリ
query = {
        'key': hot_key, # APIキー
        'lat': lat, # 現在地の緯度
        'lng': lng, # 現在地の経度
        'range': '4', # 2000m以内
        'count': 50, # 取得データ数
        'format': 'json' # データ形式json
        }

# URLとクエリでリクエスト
responce = requests.get(hot_url, query)

# 戻り値をjson形式で読み出し、['results']['shop']を抽出
result = json.loads(responce.text)['results']['shop']

# 店名、住所を表示
for i in result:
    print(i['name']+' : '+i['address'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
