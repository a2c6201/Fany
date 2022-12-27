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
print(lat, lng)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
