# Flask_project_Game_Insight
[Flask] Flask framework 프로젝트(project Game_Insight) 

## 🖥️ 프로젝트 소개 
게임 관련 랭킹, 전문가 리뷰 및 유저 리뷰를 확인 할 수 있는 웹 페이지 서비스

## 🕰️ 개발 기간
* 23.08.09일 - 23.08.11일

### 🧑‍🤝‍🧑 맴버구성 
 - (팀장) 김인용 - 로그인 및 회원 가입, 수정 및 삭제
 - (팀원) 조영익 - 전문가 리뷰 부분
 - (팀원) 정강용 - 유저 리뷰
 - (팀원) 김우응 - 랭킹 정보

### ⚙️ 개발 환경 
- **MainLanguage** : `PYTHON`
- **IDE** : VisualStudio Code 1.79.2 (Universal)
- **Framework** : Flask Framework
- **Database** : MongoDB(5.0.11)
- **SERVER** : AWS EB

## 📌 주요 기능
#### View 구성
* Header부분 :<br>
    - 웹 페이지 타이틀(title)
    - 네비게이션(메뉴)
    -- 전문가 리뷰
    -- 사용자 리뷰
* Content부분 : (작업중)<br>
    1. (예시)응원댓글 기록 : <br>
    - div(#mypost)내 input(#name)의 입력필드 생성 placeholder로 입력 내용 가이드 "닉네임"
* Footer부분 :<br>
    - 기본 내용 입력

#### 각자 기능 설명 부분 (예시)
#### 서울시 실시간 날씨 OpenAPI 사용
- URL로부터 OpenAPI 요청, 기온 부분을 받아와서 출력

#### 웹 크롤링
- URL로부터 Super Shy의 데일리 랭킹 크롤링(soup.select_one)

#### 응원 댓글 기록 진행
- input,textarea에 값 입력
- '댓글남기기' 버튼으로 입력값 DB로 전송 및 저장 (insert)

#### 응원 댓글 목록 확인
- DB에 저장된 기록된 응원 댓글 데이터 받기(find(==read))
- 받은 데이터를 content 부분에 한줄씩 출력