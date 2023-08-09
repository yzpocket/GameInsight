# 라이브러리 임포트
# Flask Framework
# view페이지 렌더링을 위한 render_template 메서드
# 요청 데이터에 접근 할 수 있는 flask.request 모듈
# dictionary를 json형식의 응답 데이터를 내보낼 수 있는 jsonify 메서드
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# MongoDB사용을 위한 pymongo와 certifi 임포트
# MongoDB(Atlas Cloud)를 사용하기 위한 pymongo 임포트
from pymongo import MongoClient
import certifi
# DB 커넥션 구성
ca = certifi.where()
# client = MongoClient('mongodb+srv://ohnyong:test@cluster0.lu7mz8j.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
# 내꺼로 임시
client = MongoClient('mongodb+srv://sparta:test@cluster0.hkkz3cj.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# 웹 크롤링을 위한 임포트
import requests
from bs4 import BeautifulSoup

# ------------크롤링 PATH 부분----------------------------------------------------------------------------------------------------------------------

# 웹 크롤링 URL 지정과 requests를통한 데이터 가져오기->bs를 통한 파싱
# URL = "https://kworb.net/spotify/country/us_daily.html"
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(URL, headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')



# ------------크롤링 PATH 부분----------------------------------------------------------------------------------------------------------------------

# "localhost:5001/" URL요청에 메인 뷰 페이지 반환 응답
@app.route('/')
def home():
   return render_template('user_review.html')

# ------------기능 구현 함수 부분----------------------------------------------------------------------------------------------------------------------

@app.route("/user_review", methods=["GET"])
def index_get():
    all_games = list(db.game.find({},{'_id':False}))
    return jsonify({'result': all_games})

@app.route("/user_review2", methods=["GET"])
def index_get2():
    all_user_reviews = list(db.user_review.find({},{'_id':False}))
    return jsonify({'result': all_user_reviews})

@app.route("/user_review", methods=["POST"])
def save_user_review():
    
    gamename = request.form['gamename_give']    
    starnum = request.form['starnum_give']
    review = request.form['review_give']
    today = request.form['today_give']

    tmp = db.game.find_one({'name':gamename})
    imgurl = tmp['link'] 
   
    doc = {'gamename':gamename,
           'starnum':starnum,
           'review':review,
           'today':today,
           'imgurl':imgurl}
    db.user_review.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})



# ------------기능 구현 함수 부분------------------------------------------------------------------------------------------------------------------------

# app이라는 메인 함수 
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)