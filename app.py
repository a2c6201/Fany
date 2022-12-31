import json

import requests
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_parameter

import config

app = Flask(__name__)
app.secret_key = "range"

hot_key = config.HOT_PEPPER_API_KEY
geo_key = config.GEOCODING_API_KEY
hot_url = config.HOT_PEPPER_API_URL
geo_url = config.GEOCODING_API_URL

# 現在地近くの店舗をjson形式で抽出
def get_shops_json(range):
    # Geolocation APIを使って緯度・経度を取得
    data = requests.get(geo_url).json()
    lat = data['latitude']
    lng = data['longitude']

    # 検索クエリ
    query = {
            'key': hot_key, # APIキー
            'lat': lat, # 現在地の緯度
            'lng': lng, # 現在地の経度
            'range': range, # 2000m以内
            'count': 50, # 取得データ数
            'format': 'json' # データ形式json
            }

    # URLとクエリでリクエスト
    responce = requests.get(hot_url, query)

    # 戻り値をjson形式で読み出し、['results']['shop']を抽出
    shops = json.loads(responce.text)['results']['shop']
    return shops

# shop.idを使って店舗詳細情報を取得
def get_shop_detail(id):
    query = {
        'key': hot_key, # APIキー
        'id': id,
        'format': 'json' # データ形式json
            }
    # URLとクエリでリクエスト
    responce = requests.get(hot_url, query)
    # 戻り値をjson形式で読み出し、['results']['shop']を抽出
    result = json.loads(responce.text)['results']['shop']
    return result[0]


# 検索画面
@app.route('/')
def index():
    return render_template('index.html')

# 検索結果一覧
@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        session.permanent = True
        session['range'] = request.form.get('range')  # sessionを使って検索条件データを保持しページングに対応

    range = session['range']
    error = None
    if not range:
        error = '検索範囲を指定してください'
        return render_template('index.html', error=error)

    # メイン処理
    try:
        get_shops_json(range)
    except Exception:
        error = '現在地が特定できませんでした'
        return render_template('index.html', error=error)
    # お店が見つからなかった時
    shops = get_shops_json(range)
    if not shops:
        error = ('お店が見つかりませんでした 検索範囲を広げてみてください')
        return render_template('index.html', error=error)

    # クエリから表示しているページのページ番号を取得
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # ページング設定
    res = shops[(page - 1)*20: page*20]
    pagination = Pagination(page=page, total=len(shops),  per_page=20, css_framework='bootstrap4')
    return render_template('result.html', shops=res, pagination=pagination)

@app.route('/detail/<shop_id>')
def detail(shop_id):
    detail = get_shop_detail(shop_id)
    return render_template('detail.html', shop=detail)


if __name__ == "__main__":
    app.run(debug=True)
