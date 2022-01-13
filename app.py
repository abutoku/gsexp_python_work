import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup
from pprint import pprint
import random

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/weather")
def index_weather():
    """天気画面を表示します."""
    return render_template("weather.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    #はてブのホットエントリーから記事を入手して、ランダムに1件返却
        #**** ここを実装します（基礎課題） ****

    #1. はてブのホットエントリーページのHTMLを取得する
    with urlopen("https://b.hatena.ne.jp/hotentry/all") as res:
        #res.read()でバイナリ型で受け取る,.decodeでutf-8に戻す
        html = res.read().decode("utf-8")
        
    #2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")
        
    #3. 記事一覧を取得する
    titles = soup.select(".entrylist-contents-title a")

    #4. ランダムに1件取得する
    contents = random.choice(titles)
    pprint(contents.string)
    #5. 以下の形式で返却する.
    return json.dumps({
        "content": contents.string,
        "link": contents["href"]
    })

    # ダミー
    # return json.dumps({
    #     "content" : "記事のタイトルだよー",
    #     "link" : "記事のURLだよー"
    # })

@app.route("/api/weather")
def api_weather():
    print('ok')
    
    with urlopen("https://weather.yahoo.co.jp/weather/jp/40/8210.html") as res:
        html = res.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")
        date = soup.select(".forecastCity td .date span")
        weater = soup.select(".forecastCity td img")

        date = [d.string for d in date]
        weater = [w["alt"] for w in weater]

        pprint('福岡の天気' + date[0] + date[1] + weater[0] + date[2] + date[3] + weater[1])
        
        result = [{
            "day": date[0],
            "week": date[1],
            "weather": weater[0]
        }, {
            "day": date[0],
            "week": date[1],
            "weather": weater[0]
        }]
        
        return json.dumps(result)
        

if __name__ == "__main__":
    app.run(debug=True, port=5004)
