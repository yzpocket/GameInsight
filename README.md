# Flask_project_Game_Insight
[Flask] Flask framework 프로젝트(project Game_Insight) 

## 🖥️ 프로젝트 소개 
게임인사이트는 간편한 게임 관련 정보를 제공하는 서비스 페이지입니다.

Flask Framework를 활용한 웹 서비스로 최근 게임 랭킹, <br>전문가(게임언론) 작가의 리뷰 페이지, 일반 사용자의 리뷰 페이지로 구성되어 있습니다.
<br>추가적으로 메인 페이지에서 각종 게임 뉴스, 신작, 공략, 이벤트 등 정보 페이지를 보여줍니다.

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
#### 시연 영상
https://www.youtube.com/watch?v=Szj9XZU_7gE

#### 팀 노션 페이지
https://ohnyong.notion.site/GameInsight-536ac8bfbd5445f19dff65eeddd385b4?pvs=4


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

### ⚙ 각자 기능 설명 부분

### ✅ 회원 가입 및 로그인 구현 - 김인용

- 회원 가입 양식
    - 회원 아이디
    - 비밀번호
    - 이메일 주소
    - 이름
    - 유저 타입( 전문가 / 일반 유저 / 관리자 )
    - 주소(Daum주소 API연동 자동입력)
- 로그인
    - 기본 정보
        - DB의 아이디
        - DB의 비밀번호
    - 유효성 체크
        - View 필드값 == DB 필드값 검증
            - #user_id == db.user의 user_id value
            - Hash sha256암호화된 비밀번호간의 검증
    - 로그인 진행 시 : JWT 토큰 발급(id+expired time, Seceret KEY, algorithm 포함)
    - 로그인 완료 시 : 토큰
    

### ✅ 전문가 리뷰 페이지 - 조영익

- 리뷰 작성
    - 입력 양식
        - 게임의 게임메카 url
        - 게임 평점(별점)
        - 게임 한줄평
    - 저장 정보
        - url 크롤링을 통한 og 정보
            - 게임 이름
            - 게임 이미지 링크
        - 게임 평점(별점)
        - 게임 한줄평
        - 등록 대상 id
    - 작성자 조건에 부합하는 대상에게만 작성 버튼 노출 필요
        - 로그인 시에 불러올 수 있는 정보가 필요
- 리뷰 목록 호출
    - 전문가 평점 버튼 입력 시 리뷰 목록 호출 (호출 순서는 최신순으로 정렬 필요)
    - 좌측에 이미지, 우측에는 위에서 순서대로 게임명, 평점, 한줄평, 작성자 id 노출

### ✅ 사용자 리뷰 페이지 - 정강용

- 리뷰 작성
- 리뷰 목록 호출

### ✅ 랭킹 데이터 페이지 - 김우응

- 게임메카에서 랭킹 TOP 10 정보 가져오기
    - 게임 사이트와 게임 회사 클릭시 사이트 연동해주기
