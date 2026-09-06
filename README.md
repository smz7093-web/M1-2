# M1-2

# 🏚️ 빈집 인사이트 AI 비서 (Vacant House AI Assistant)

> **"전국 빈집 13만 4천 호 시계열 데이터를 기억하고 맞춤형 정책·투자 인사이트를 제공하는 컨텍스트 기반 AI 웹 서비스"**

---

## 📖 1. 서비스 소개

일반적인 ChatGPT는 사용자의 특정 내부 데이터나 최신 로컬 현황을 알지 못합니다. "현재 빈집 문제가 어느 정도로 심각해?"라고 물으면 교과서적인 원론적 답변만 내놓습니다.

**빈집 인사이트 AI 비서**는 2015년부터 2024년까지의 **전국 17개 시도별 방치 빈집 시계열 데이터(총 170개 포인트, 2024년 13만 4,009호 확정치)**를 Firestore에 저장하고, 실시간으로 데이터 요약 통계(최근 추세, 수도권 vs 비수도권 누적 비중, 이상치 지역 등)를 산출하여 **AI 시스템 프롬프트에 컨텍스트로 자동 주입(Context Injection)**합니다. 

사용자는 자연어 대화만으로 내 데이터 기반의 정밀한 정책 제언 및 시계열 트렌드 답변을 즉시 얻을 수 있으며, 웹 인터페이스를 통해 데이터를 직접 CRUD 관리하고 과거 대화 이력을 언제든 불러올 수 있습니다.

---

## 🛠️ 2. 기술 스택 (Tech Stack)

### Backend & AI
* **Framework**: FastAPI (Python 3.10+)
* **ASGI Server**: Uvicorn
* **Database**: Google Cloud Firebase (Firestore Database)
* **LLM Engine**: OpenAI API (`gpt-4o-mini` 또는 `gpt-3.5-turbo`)
* **Validation**: Pydantic v2
* **Deployment**: Render (Web Service)

### Frontend
* **Core**: Vanilla HTML5, CSS3, Modern JavaScript (ES6+) — *프레임워크 없이 순수 웹 표준 구현*
* **Visualization (보너스)**: Chart.js (CDN)
* **Deployment**: Vercel

---

## 🌐 3. 배포 URL 및 API 문서

* **웹 프론트엔드 (Vercel)**: `https://vacant-house-ai.vercel.app`
* **백엔드 API 서버 (Render)**: `https://vacant-house-api.onrender.com`
* **인터랙티브 API 문서 (Swagger UI)**: `https://vacant-house-api.onrender.com/docs`

> 💡 **콜드 스타트(Cold Start) 안내**:
> Render 무료 티어 정책상 약 15분 이상 요청이 없을 경우 서버가 슬립 모드로 전환됩니다. 첫 접속 시 최초 응답까지 약 30~50초의 지연이 발생할 수 있습니다. 프론트엔드 UI에 로딩 스피너 및 슬립 해제 대기 안내 문구가 표시됩니다.

---

## 📂 4. 프로젝트 디렉터리 구조

```text
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── data.py          # 데이터 CRUD 및 요약(/api/data, /summary) 엔드포인트
│   │   │   ├── chat.py          # AI 컨텍스트 주입 챗봇(/api/chat) 엔드포인트
│   │   │   └── conversation.py  # 대화 기록 관리(/api/conversations) 엔드포인트
│   │   ├── core/
│   │   │   ├── config.py        # 환경변수 로드 및 설정
│   │   │   └── firebase.py      # Firestore 클라이언트 초기화
│   │   ├── schemas/
│   │   │   ├── data.py          # Pydantic 데이터 검증 모델 (DataCreate, DataResponse 등)
│   │   │   └── chat.py          # 대화 및 메시지 입출력 모델
│   │   ├── services/
│   │   │   ├── data_service.py  # 시계열 요약 알고리즘 및 Firestore 연동 로직
│   │   │   └── chat_service.py  # OpenAI 프롬프트 주입 및 대화 자동 저장 로직
│   │   └── main.py              # FastAPI 인스턴스, CORS 미들웨어 및 라우터 등록
│   ├── seed_data.py             # 10개년 빈집 데이터(170건) Firestore 초기 적재 스크립트
│   ├── requirements.txt         # 백엔드 의존성 목록
│   └── serviceAccountKey.json   # Firebase 서비스 계정 키 (로컬용, .gitignore 등록)
│
├── frontend/
│   ├── index.html               # 단일 페이지 바닐라 웹 애플리케이션
│   ├── style.css                # 반응형 디자인, 다크모드 지원 CSS
│   ├── app.js                   # REST API 통신, DOM 조작, 차트 렌더링
│   └── vercel.json              # Vercel 배포 및 환경 설정
│
├── .gitignore
└── README.md                    # 프로젝트 문서 (본 파일)

```

## ⚙️ 5. 환경 변수 설정 
(.env)서비스 구동을 위해 필요한 환경 변수 목록입니다. 보안을 위해 API 키와 서비스 계정 정보는 절대 Git 저장소에 커밋하지 않습니다.백엔드 (backend/.env 및 Render 환경 변수)Ini, TOML# OpenAI API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

** Firebase / Firestore 설정
FIREBASE_PROJECT_ID=vacant-house-ai-prod
FIREBASE_PRIVATE_KEY_ID=xxxxxxxxxxxx
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@vacant-house-ai-prod.iam.gserviceaccount.com
# ※ Render 등 배포 환경에서는 줄바꿈(\n)을 포함한 비공개 키 문자열을 환경 변수에 직접 등록
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC..."

** 서버 환경 및 CORS
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=[https://vacant-house-ai.vercel.app](https://vacant-house-ai.vercel.app),http://localhost:3000,[http://127.0.0.1:5500](http://127.0.0.1:5500)
프론트엔드 (frontend/vercel.json 또는 app.js 상수)JavaScript// app.js 상단 또는 빌드 시 주입
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : '[https://vacant-house-api.onrender.com](https://vacant-house-api.onrender.com)';

---
    
## 💻 6. 로컬 개발 환경 실행 방법1) 사전 준비Python 3.10 이상 설치Firebase Console에서 Firestore Database 생성 및 서비스 계정 키(JSON) 발급OpenAI API Key 발급2) 백엔드 실행Bash# 1. 백엔드 디렉터리 이동 및 가상환경 생성
cd backend
python -m venv venv

# 가상환경 활성화 (Windows: venv\Scripts\activate / macOS, Linux: source venv/bin/activate)
source venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일 내 OPENAI_API_KEY 및 FIREBASE 관련 키 입력

# 4. 초기 시계열 데이터(170건) DB 적재 (최초 1회 실행)
python seed_data.py

# 5. FastAPI 서버 구동
uvicorn app.main:app --reload --port 8000
로컬 Swagger UI 접속: http://localhost:8000/docs3) 프론트엔드 실행프레임워크 빌드가 필요 없는 순수 HTML/CSS/JS이므로 브라우저에서 바로 열거나 간이 웹서버를 이용합니다.Bashcd ../frontend

# VS Code의 'Live Server' 확장 사용 또는 Python 내장 웹서버 실행
python -m http.server 3000
브라우저에서 http://localhost:3000 접속

---

## 📡 7. API 엔드포인트 명세1) 데이터 관리 API (/api/data)MethodEndpoint설명POST/api/data새 빈집 관측 데이터 추가 (date, value, memo)GET/api/data전체 데이터 목록 조회 (정렬 및 필터 지원)PUT/api/data/{id}특정 ID의 데이터 수정DELETE/api/data/{id}특정 ID의 데이터 삭제GET/api/data/summary[핵심] LLM 프롬프트 주입용 시계열 통계 요약 반환/api/data/summary 응답 예시:JSON{
  "total_count": 170,
  "period": "2015 ~ 2024",
  "latest_total_value": 134009,
  "growth_10yr_pct": 57.6,
  "top_regions": ["전남 (19,850호)", "경북 (18,920호)", "전북 (15,400호)"],
  "capital_share_pct": 10.3,
  "non_capital_share_pct": 89.7,
  "trend_status": "지속적 가속 증가세 (3개년 이동평균 우상향)"
}
2) 대화 기록 API (/api/conversations)MethodEndpoint설명POST/api/conversations새 대화 세션 생성 및 저장GET/api/conversations전체 대화 목록 조회 (세션 ID, 제목, 일시)GET/api/conversations/{id}특정 대화 세션의 전체 메시지(messages) 불러오기DELETE/api/conversations/{id}특정 대화 세션 삭제3) AI 챗봇 API (/api/chat)MethodEndpoint설명POST/api/chat자연어 질의 전송 ➡️ 요약 컨텍스트 주입 ➡️ GPT 응답 생성 ➡️ DB 자동 저장

---

## 🧠 8. 핵심 아키텍처: 컨텍스트 주입(Context Injection) 원리Plaintext[사용자 질문] "현재 지방 빈집 비중이 얼마나 되고 왜 계속 늘어나?"
      │
      ▼
[FastAPI 백엔드]
  1. Firestore로부터 시계열 데이터 요약(/api/data/summary) 자동 계산
  2. 시스템 프롬프트 템플릿에 통계 수치를 동적으로 주입
      │
      ▼
┌────────────────────────────────────────────────────────────────────────┐
│ [동적 생성된 System Prompt]                                             │
│ 너는 대한민국 빈집 전문 정책 분석관이야. 반드시 아래 데이터를 근거로 답변해:   │
│ - 분석 기간: 2015~2024년 (총 170개 관측치)                               │
│ - 2024년 전국 합계: 134,009호 (10년간 57.6% 급증)                         │
│ - 지역 집중도: 비수도권이 89.7%(12만 호), 전남·경북·전북이 전체의 40.4%       │
│ - 이동평균 추세: 최근 5년 증가폭이 과거 5년 대비 1.45배 가속화됨          │
└────────────────────────────────────────────────────────────────────────┘
      │
      ▼
[OpenAI GPT API 호출]
      │
      ▼
[결과 반환 및 Firestore conversations 컬렉션에 자동 저장]

---

## 📸 9. 서비스 화면 및 제출 증빙 스크린샷1. 데이터 요약 & AI 질의응답 화면2. 데이터 관리 (CRUD) 동작 화면3. 대화 기록 저장 및 불러오기 화면상단 요약 카드와 프롬프트 주입 기반 AI 답변신규 데이터 등록 및 삭제 후 목록 즉시 갱신사이드바의 이전 대화 클릭 시 본문 메시지 복원

---

## 🌟 10. 보너스 과제 구현 사항시각화 대시보드 연동: 바닐라 프론트엔드 내 Chart.js를 연동하여 연도별 전국 빈집 추세선(MA-3 포함)을 상단 위젯으로 렌더링.데이터 내보내기 (Export): 등록된 시계열 데이터셋 전체를 브라우저에서 .csv 파일로 즉시 다운로드하는 기능 탑재.다크 모드(Dark Mode) 지원: localStorage에 사용자 테마 상태를 보존하는 원클릭 다크/라이트 모드 토글 구현.AI 도구 호출 (Function Calling): 사용자가 특정 시도(예: "전남 통계만 따로 보여줘")를 물어볼 경우, GPT가 get_regional_stats(region="전남") 도구를 스스로 호출하도록 백엔드 함수 스키마 정의 및 연동.
