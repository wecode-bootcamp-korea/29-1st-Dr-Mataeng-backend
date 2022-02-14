# Dr-Mataeng 1차 프로젝트🥾
- 닥터마틴은 샌들,슈즈,부츠 등을 취급하는 세계적인 의류기업이자 영국 60년 전통 패션 브랜드입니다.


- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인 / 기획 부분만 클론했습니다.


- 개발은 초기 세팅부터 전부 직접 구현 했으며, 아래 데모 영상에서 보이는 부분은 모두 프론트엔드와 백엔드가 통신하여 실제 서비스 수준으로 개발한 것입니다.
<br />

## 기간

- 개발기간: 2022.01.24 ~ 2022.02.11
<br />
<br />


## 팀원

- Frontend (3명) : 유재민, 오수민, 장예지
- Backend (2명)  : 강종범, 이혜린
<br />
<br />
<a href="https://github.com/wecode-bootcamp-korea/29-1st-Dr-Mataeng-frontend">프론트엔드 Github</a>
<br />
<a href="https://github.com/wecode-bootcamp-korea/29-1st-Dr-Mataeng-backend">  백엔드 Github</a>
<br />
<br />

## 사용된 기술
- Python
- Django
- MySQL
- Git
- AWS(RDS, EC2)
<br />
<br />


## 라이브러리
- bcrpyt
- jwt
- django-cors
<br />
<br />


## 협업

- Github
- Slack
- Notion
- Trello
- Agile Process (Scrum)
<br />
<br />



## 클론 영상


<iframe title="'jxngbxxm'에서 업로드한 동영상" width="640" height="360" src="https://play-tv.kakao.com/embed/player/cliplink/426313620?service=player_share" allowfullscreen frameborder="0" scrolling="no" allow="autoplay; fullscreen; encrypted-media"></iframe>


<br />
<br />


## ERD

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fdr0LPh%2Fbtrs7qddDjn%2FHDnX2KZlLDg6TNjjZsKuw0%2Fimg.png"/>

<br />
<br />


## 담당 구현 사항 및 구현 기능

#### 강종범 - 🤖  

#### 이혜린 - 🙂

<br />
<br />

- Project Modeling 🤖
- 로그인 🙂
- 회원가입 🤖
- 마이페이지 🙂
- 상품 리스트 (필터링 & 정렬) 🤖 
- 상품 디테일 🤖 
- 검색 🤖 
- 장바구니 🤖
- 주문 결제 🤖
<br />

---

## 🥾 User
<br />
회원가입 - 정규표현식을 활용한 유효성 검사, Bcrypt를 사용한 비밀번호 암호화
<br />
<br />
로그인 - bcrypt로 암호화한 비밀번호 다시 복호화하여 일치여부 확인, 일치하면 jwt 토큰 발급
<br />
<br />
인가 - Login Decorator를 작성하여 인가가 필요한 모든 API에 적용
<br />
<br />

## 🥾 Product
<br />
상품 리스트 (필터링 & 정렬) - 상품 리스트 조회, 필터링 기능 구현, 정렬 기능 구현
<br />
<br />
상품 디테일 - 상품 상세페이지 조회
<br />
<br />
검색 - 상품 검색 기능 구현
<br />
<br />

## 🥾 Cart
<br />
장바구니 - 장바구니에 상품 추가, 장바구니 수정, 장바구니 삭제, 장바구니 조회 기능 구현
<br />
<br />

## 🥾 Order
<br />
주문 결제 - 회원가입 성공시 받은 포인트로 결제 기능 구현, 주문 내역 조회 기능 구현

<br />
<br />

## API Documentstion

<a href="https://documenter.getpostman.com/view/19385058/UVeDt7zS#intro">Postman API</a>
<br />
<br />



### Reference
-----
- 이 프로젝트는 <a href="https://www.drmartens.co.kr/">닥터마틴</a> 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.