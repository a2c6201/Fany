import json

import requests
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_parameter

import config

app = Flask(__name__)
app.secret_key = "range"

hot_key = config.HOT_PEPPER_API_KEY  # TODO省略しない
map_key = config.GOOGLE_MAPS_API_KEY
hot_url = config.HOT_PEPPER_API_URL
geo_url = config.GEOCODING_API_URL
map_base_url = config.GOOGLE_MAPS_API_URL


# Geolocation APIを使って現在地の緯度・経度を取得
def get_location():
    data = requests.get(geo_url).json()
    lat = data['latitude']
    lng = data['longitude']
    return lat, lng


# 現在地近くの店舗をjson形式で抽出
def shops_json(range):
    lat, lng = get_location()
    query = {
        'key': hot_key,  # APIキー　TODO揃える
        'lat': lat,      # 現在地の緯度
        'lng': lng,      # 現在地の経度
        'range': range,  # 2000m以内
        'count': 50,     # 取得データ数
        'format': 'json'  # データ形式json
    }

    responce = requests.get(hot_url, query)  # TODO
    shops = json.loads(responce.text)['results']['shop']
    return shops


# shop.idを使って店舗詳細情報を取得
def shop_json(id):
    query = {
        'key': hot_key,  # APIキー
        'id': id,
        'format': 'json'  # データ形式json
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
        session['range'] = request.form.get(
            'range')  # sessionを使って検索条件データを保持しページングに対応

    range = session['range']
    error = None
    # メイン処理
    try:
        shops_json(range)
    except Exception:
        error = '現在地が特定できませんでした' # TODO ローカル環境　キー削除でつまづく
        return render_template('index.html', error=error)
    shops = shops_json(range)
    if not shops:
        error = ('お店が見つかりませんでした 検索範囲を広げてみてください')  # TODO デプロイ環境ここでつまづく
        return render_template('index.html', error=error)

    # クエリから表示しているページのページ番号を取得
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # ページング設定
    res = shops[(page - 1) * 20: page * 20]
    pagination = Pagination(
        page=page,
        total=len(shops),
        per_page=20,
        css_framework='bootstrap4')
    return render_template('result.html', shops=res, pagination=pagination)


# 詳細画面
@app.route('/detail/<shop_id>')
def detail(shop_id):
    shop = shop_json(shop_id)
    lat, lng = get_location()
    map_url = '{}origin={},{}&destination={},{}'.format(
        map_base_url, lat, lng, shop['lat'], shop['lng']
    )
    return render_template('detail.html', shop=shop, map_url=map_url)


if __name__ == "__main__":
    app.run(debug=True)
