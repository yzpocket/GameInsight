# 라이브러리 임포트
# Flask Framework
# view페이지 렌더링을 위한 render_template 메서드
# 요청 데이터에 접근 할 수 있는 flask.request 모듈
# dictionary를 json형식의 응답 데이터를 내보낼 수 있는 jsonify 메서드
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import time
wday = ['월', '화', '수', '목', '금', '토', '일']

app = Flask(__name__)
CORS(app)


# MongoDB사용을 위한 pymongo와 certifi 임포트
# MongoDB(Atlas Cloud)를 사용하기 위한 pymongo 임포트
from pymongo import MongoClient
import certifi
# DB 커넥션 구성
ca = certifi.where()

client = MongoClient('mongodb+srv://ohnyong:test@cluster0.lu7mz8j.mongodb.net/',tlsCAFile=ca)
db = client.gameinsight
collection = db['game_rank']
# 웹 크롤링을 위한 임포트
import requests
from bs4 import BeautifulSoup

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


# ------------크롤링 PATH 부분----------------------------------------------------------------------------------------------------------------------

# 웹 크롤링 URL 지정과 requests를통한 데이터 가져오기->bs를 통한 파싱

URL1 = "https://www.gamemeca.com/ranking.php"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data1 = requests.get(URL1, headers=headers)
soup1 = BeautifulSoup(data1.text, 'html.parser')
URL5 = "https://www.gamemeca.com/ranking.php" 
data = requests.get(URL5, headers=headers)

# URL = "https://kworb.net/spotify/country/us_daily.html"
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(URL, headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')


@app.route("/game_ranking", methods=["GET"])
def game_rank_get():
    all_game_ranks = list(db.game_rank.find({},{'_id':False}))
    return jsonify({'result':all_game_ranks})


# ------------크롤링 PATH 부분----------------------------------------------------------------------------------------------------------------------


# "localhost:5001/" URL요청에 메인 뷰 페이지 반환 응답
# app.py (Flask 애플리케이션)
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.user.find_one({"user_id": payload['user_id']})
            return render_template('index.html', user_id=user_info["user_id"], user_name=user_info["user_name"], user_type=user_info["user_type"])
        except jwt.ExpiredSignatureError:
            return render_template('index.html', user_id=None, user_name=None, user_type=None)
        except jwt.exceptions.DecodeError:
            return render_template('index.html', user_id=None, user_name=None, user_type=None)
    else:
        return render_template('index.html', user_id=None, user_name=None, user_type=None)
# @app.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.user.find_one({"user_id": payload['user_id']})
#         return render_template('index.html', user_id=user_info["user_id"], user_name=user_info["user_name"], user_type=user_info["user_type"])
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

# ------------기능 구현 함수 부분----------------------------------------------------------------------------------------------------------------------

# user_review 페이지 호출
@app.route('/user_review')
def ur():
   return render_template('user_review.html')

#################################
##  HTML을 주는 부분           ##
#################################


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API          ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    email_receive = request.form['email_give']
    name_receive = request.form['name_give']
    post_receive = request.form['post_give']
    addr1_receive = request.form['addr1_give']
    addr2_receive = request.form['addr2_give']
    type_receive = request.form['type_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print(id_receive)
    db.user.insert_one({'user_id': id_receive,
                        'user_password': pw_hash,
                        'user_email': email_receive,
                        'user_name': name_receive,
                        'user_postcode': post_receive,
                        'user_address1': addr1_receive,
                        'user_address2': addr2_receive,
                        'user_type': type_receive})

    return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'user_id': id_receive, 'user_password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'user_id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=200)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/logined', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'user_id': payload['user_id']}, {'_id': 0})
        return jsonify({'result': 'success', 'user_id': userinfo['user_id'], 'user_name': userinfo['user_name'],  'user_type': userinfo['user_type']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

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
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.user.find_one({"user_id": payload['user_id']})
            commenter = user_info["user_name"]
        except jwt.ExpiredSignatureError:
            return jsonify({'code':-1,'msg':'로그인 정보가 만료되었습니다. 로그아웃 후 다시 로그인 해 주세요'})
        except jwt.exceptions.DecodeError:
            return jsonify({'code':-1,'msg':'로그인 정보를 확인할 수 없습니다.'})
    
    if search_url == -1:
        return jsonify({'code':-1,'msg':'잘못된 링크입니다. 우측의 게임메타 링크를 통해 게임을 찾아보세요!'})
    if star_receive=='-- 선택하기 --':
        return jsonify({'code':-1,'msg':'별점을 선택해 주세요!'})
    if comment_receive.replace(" ", '').replace('','') == '':
        return jsonify({'code':-1,'msg':'리뷰를 작성해 주세요!'})
    
    ogtitle = soup.select_one('meta[property="og:title"]')['content'].split(" - ")[0]
    ogimage=soup.select_one('meta[property="og:image"]')['content']
    tm = time.localtime()
    critic_review_list = list(db.critic_review.find({}, {'_id': False}))
    count = len(critic_review_list) + 1
    upload_time = f'{tm.tm_year}-{tm.tm_mon}-{tm.tm_mday} {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}({wday[tm.tm_wday]})'
    

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


@app.route("/critic_review", methods=["GET"]) # POST 미적용 상태, 적용 전 확인은 db = client.dbsparta, client는 테스트용, games_data 값은 db.games로 변경 후 실행
def game_get():
   games_data = list(db.critic_review.find({},{'_id':False}))
   games_data.reverse()
   return jsonify({'result':games_data, 'msg':'successed'})

# ------평론가 평론 구현 (조영익) end----------------------------------------------------------------------------------------------------------------

#유저리뷰에 쓰일 top50 게임목록 db에 등록 및 가져오기
@app.route("/user_review_rank", methods=["GET"])
def user_review_get():

    games = soup1.select('#content > div.ranking_list > div.rank-list > div.content-left > table > tbody > tr')
    db.user_review_games.delete_many({})
    for a in games :
        num = a.select_one('td:nth-child(1)').text[0:4].strip()
        name = a.select_one('td:nth-child(4) > div.game-name > a').text
        link = a.select_one('td:nth-child(2) > img')['src']
        doc = {'num':num,'name':name,'link':link}
        db.user_review_games.insert_one(doc)
    
    all_games = list(db.user_review_games.find({},{'_id':False}))
    return jsonify({'result': all_games})

#유저리뷰 가져오기
@app.route("/user_review2", methods=["GET"])
def user_review_get2():

    all_user_reviews = list(db.user_review.find({},{'_id':False}))
    return jsonify({'result': all_user_reviews})

#유저리뷰 등록
@app.route("/user_review_save", methods=["POST"])
def save_user_review():
    
    gamename = request.form['gamename_give']    
    starnum = request.form['starnum_give']
    review = request.form['review_give']
    today = request.form['today_give']

    tmp = db.user_review_games.find_one({'name':gamename})
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
    
    
    
    
    

