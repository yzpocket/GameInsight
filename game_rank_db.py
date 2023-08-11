# 게임랭크를 DB에 추가하는 코드입니다.
from pymongo import MongoClient
import certifi
import requests
from bs4 import BeautifulSoup

# MongoDB Atlas Cloud에 연결하기 위한 정보
ca = certifi.where()
client = MongoClient('mongodb+srv://ohnyong:test@cluster0.lu7mz8j.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.gameinsight
collection = db['game_rank']

URL5 = "https://www.gamemeca.com/ranking.php"
response = requests.get(URL5)
soup = BeautifulSoup(response.content, "html.parser")

# 게임 정보 추출 및 저장
for row in soup.find_all("tr", class_="ranking-table-rows"):
    game_rank_span = row.find("span", class_=["rank", "rank red"])
    game_rank = game_rank_span.text if game_rank_span else None
    game_icon = row.find("img", class_="game-icon")["src"]
    game_name = row.find("div", class_="game-name").a.text.strip()
    game_info_spans = row.find("div", class_="game-info").find_all("span")
    game_company = game_info_spans[0].text.strip() if len(game_info_spans) > 0 else None
    game_genre = game_info_spans[1].text.strip() if len(game_info_spans) > 0 else None
    game_pay = game_info_spans[2].text.strip() if len(game_info_spans) > 1 else None
    
    game_data = {
        "rank": game_rank,
        "icon_url": game_icon,
        "name": game_name,
        "company":game_company,
        "genre": game_genre,
        "pay": game_pay
    }

        # MongoDB에 데이터 삽입
    collection.insert_one(game_data)
print("데이터 저장 완료")