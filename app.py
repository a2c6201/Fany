import json

from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_parameter

import config
import fetcher as fe

app = Flask(__name__)
app.secret_key = "range"

HOT_PEPPER_API_KEY = config.HOT_PEPPER_API_KEY
GOOGLE_MAPS_API_URL = config.GOOGLE_MAPS_API_URL


def shops_json(range, lat, lng):
    # 現在地近くの店舗をjson形式で抽出
    query = {
        'key': HOT_PEPPER_API_KEY,   # APIキー
        'lat': lat,                  # 現在地の緯度
        'lng': lng,                  # 現在地の経度
        'range': range,              # 検索範囲
        'count': 50,                 # 取得データ数
        'format': 'json'             # データ形式json
    }

    responce = fe.search(query)
    shops = json.loads(responce.text)['results']['shop']
    return shops


def shop_json(id):
    # shop.idを使って店舗詳細情報を取得
    query = {
        'key': HOT_PEPPER_API_KEY,
        'id': id,
        'format': 'json'
    }

    responce = fe.search(query)
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
        if (request.headers['Content-Type'] == 'application/json'):
            session.permanent = True
            session['lat'] = request.json['lat']
            session['lng'] = request.json['lng']
            session['range'] = request.json['range']

    range = session['range']
    lat = session['lat']
    lng = session['lng']
    error = None

    # メイン処理
    try:
        shops_json(range, lat, lng)
    except Exception:
        error = '現在地が特定できませんでした'
        return render_template('index.html', error=error)

    shops = shops_json(range, lat, lng)
    if not shops:
        error = ('お店が見つかりませんでした 検索範囲を広げてみてください')
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
    lat = session['lat']
    lng = session['lng']
    map_url = '{}origin={},{}&destination={},{}'.format(
        GOOGLE_MAPS_API_URL, lat, lng, shop['lat'], shop['lng']
    )
    return render_template('detail.html', shop=shop, map_url=map_url)


if __name__ == "__main__":
    app.run(debug=True)
