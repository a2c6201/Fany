import base64
import json
from datetime import datetime

import pytz
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy

import config
import fetcher as fe

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photo.db'
db = SQLAlchemy(app)
app.secret_key = "range"  # sessionを暗号化

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HOT_PEPPER_API_KEY = config.HOT_PEPPER_API_KEY
HOT_PEPPER_URL = config.HOT_PEPPER_URL
GOOGLE_MAPS_API_URL = config.GOOGLE_MAPS_API_URL


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.Text(50), nullable=False)
    image = db.Column(db.Text(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


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


@app.route('/')
def index():
    # 検索画面
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    # 検索結果一覧
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


@app.route('/detail/<shop_id>')
def detail(shop_id):
    # 詳細画面
    shop = shop_json(shop_id)
    lat = session['lat']
    lng = session['lng']
    map_url = '{}origin={},{}&destination={},{}'.format(
        GOOGLE_MAPS_API_URL, lat, lng, shop['lat'], shop['lng']
    )
    shop_url = HOT_PEPPER_URL.format(shop_id)
    return render_template('detail.html', shop=shop, map_url=map_url, shop_url=shop_url)


@app.route('/create/<shop_id>', methods=['GET', 'POST'])
def create(shop_id):
    if request.method == "POST":
        #     title = request.form.get('title')
        #     image = request.files['image']
        #     photo = Photo(shop_id=shop_id, title=title, image=image)
        #     db.session.add(photo)
        #     db.session.commit()
        #     return redirect('/detail/{}'.format(shop_id))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            img_base64 = base64.b64encode(file.read())
            print(img_base64)
            return redirect(url_for('detail', shop_id=shop_id))
    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
