# 라이브러리 임포트
# Flask Framework
# view페이지 렌더링을 위한 render_template 메서드
# 요청 데이터에 접근 할 수 있는 flask.request 모듈
# dictionary를 json형식의 응답 데이터를 내보낼 수 있는 jsonify 메서드
from flask import Flask, render_template, request, jsonify,session
import time
wday = ['월', '화', '수', '목', '금', '토', '일']
app = Flask(__name__)

# MongoDB사용을 위한 pymongo와 certifi 임포트
# MongoDB(Atlas Cloud)를 사용하기 위한 pymongo 임포트
from pymongo import MongoClient
import certifi
# DB 커넥션 구성
ca = certifi.where()
client = MongoClient('mongodb+srv://ohnyong:test@cluster0.lu7mz8j.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)

# 조영익 MongoDB for listing test
#client = MongoClient('mongodb+srv://sparta:test@cluster0.fkikqje.mongodb.net/?retryWrites=true&w=majority')

db = client.gameinsight

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
   return render_template('index.html')

# ------------기능 구현 함수 부분----------------------------------------------------------------------------------------------------------------------

# ------평론가 평론 구현 (조영익) start----------------------------------------------------------------------------------------------------------------
@app.route("/critic_review", methods=["POST"]) # html에는 미적용
def game_post():
   url_receive = request.form['url_give']
   comment_receive=request.form['comment_give']
   star_receive=request.form['star_give']
   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_receive,headers=headers)
   soup = BeautifulSoup(data.text, 'html.parser')
   search_url=soup.select_one('meta[property="og:url"]').find('https://www.gamemeca.com/game.php?rts=gmview&')
   
   if search_url == -1:
      ogtitle=''
   else:
      ogtitle = soup.select_one('meta[property="og:title"]')['content'].split(" - ")[0]
      
   if ogtitle!='':
      ogimage=soup.select_one('meta[property="og:image"]')['content']
      tm = time.localtime()
      critic_review_list = list(db.critic_review.find({}, {'_id': False}))
      count = len(critic_review_list) + 1
      upload_time = f'{tm.tm_year}-{tm.tm_mon}-{tm.tm_mday} {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}({wday[tm.tm_wday]})'
      commenter = 'name' #'세션 호출을 통해서 받은 토큰이든 usernum이든을 통해서 name 호출(전문가버전이니 name 호출)'
      doc={
         'no': count,
         'title':ogtitle,
         'image':ogimage,                 
         'comment': comment_receive,
         'star':star_receive,
         'commenter':commenter,
         'upload_time': upload_time}
      db.critic_review.insert_one(doc)
      return jsonify({'code':200,'msg':'기록 완료!'})
   else :
      return jsonify({'code':404,'msg':'잘못된 링크입니다.'})

@app.route("/critic_review", methods=["GET"]) # POST 미적용 상태, 적용 전 확인은 db = client.dbsparta, client는 테스트용, games_data 값은 db.games로 변경 후 실행
def game_get():
   games_data = list(db.critic_review.find({},{'_id':False}))
   games_data.reverse()
   return jsonify({'result':games_data, 'msg':'successed'})

# ------평론가 평론 구현 (조영익) end----------------------------------------------------------------------------------------------------------------


# ------------기능 구현 함수 부분------------------------------------------------------------------------------------------------------------------------

# app이라는 메인 함수 
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
    
    
    
    
    

