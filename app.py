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
client = MongoClient('mongodb+srv://ohnyong:test@cluster0.lu7mz8j.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.gameinsight

# 웹 크롤링을 위한 임포트
import requests
from bs4 import BeautifulSoup

# 로그인 및 회원가입 부분을 위한 라이브러리 임포트 추가
from flask import session, redirect, url_for;
# 비밀번호 암호화를 위한 Hashlib 사용
# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt
# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime
# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib
# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'inyongkim'

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
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"user_id": payload['user_id']})
      return render_template('index.html', nickname=user_info["name"])
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

# ------------기능 구현 함수 부분----------------------------------------------------------------------------------------------------------------------

# 회원가입 양식을 보여주는 부분
@app.route('/joinForm')
def user_Join():
   return render_template('joinForm.html')

# 로그인 페이지를 보여주는 부분
@app.route('/loginForm')
def login():
    msg = request.args.get("msg")
    return render_template('loginForm.html', msg=msg)

# 회원가입 기능 API
@app.route("/api/join", methods=["POST"])
def join():
    user_name_receive = request.form['user_name_give']
    user_id_receive = request.form['user_id_give']
    user_password1_receive = request.form['user_password1_give']
    user_postcode_receive = request.form['user_postcode_give']
    user_address1_receive = request.form['user_address1_give']
    user_address2_receive = request.form['user_address2_give']
    user_email_receive = request.form['user_email_give']
    user_type_receive = request.form['user_type_give']

   # PW 암호화
    pw_hash = hashlib.sha256(user_password1_receive.encode('utf-8')).hexdigest()

   # user_num 고유번호 추출 방법
    user_list = list(db.user.find({}, {'_id': False}))
    user_num = len(user_list) + 1

    doc = {
        'user_num':user_num, # 추후 특정 유저를 찾기 위해 'num' 이라는 고유 값 부여
        'user_name' : user_name_receive, # 이름
        'user_id' : user_id_receive, # 아이디
        'user_password1' : pw_hash, # -------- 암호화된 비밀번호(Hashlib)
        'user_postcode' : user_postcode_receive, # 우편번호
        'user_address1' : user_address1_receive, # 주소1(시군구)
        'user_address2' : user_address2_receive, # 주소2(상세주소)
        'user_email' : user_email_receive, # 이메일
        'user_type' : user_type_receive, # 일반사용자 or 전문가
    }
    db.user.insert_one(doc)
    # [POST-7] insert가 완료되었으니 완료 메시지를 반환한다.
    return jsonify({'msg': 'POST 연결 완료!'+'회원가입 완료!'})
    

# 로그인 기능 API
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def login():
    user_id_receive = request.form['user_id_give']
    user_password1_receive = request.form['user_password1_give']

   # PW 암호화
    pw_hash = hashlib.sha256(user_password1_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': user_id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'user_id': user_id_receive,
            'expiry_time': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
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
# 
@app.route('/api/userinfo', methods=['GET'])
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
        return jsonify({'result': 'success', 'user_name': userinfo['user_name']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

# ------------기능 구현 함수 부분------------------------------------------------------------------------------------------------------------------------

# app이라는 메인 함수 
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)