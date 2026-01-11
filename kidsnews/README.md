# 하하 어린이 신문 (Haha Kids News) 🗞️

**하하 어린이 신문**은 AI 기술을 활용하여 7~9세 아이들을 위한 맞춤형 교육 신문을 자동으로 발행하는 시스템입니다. 매일 새로운 주제로 기사를 작성하고, 그에 어울리는 삽화와 교육 활동(퀴즈, 색칠놀이 등)을 생성하여 한 장의 신문으로 완성합니다.

---

## 🚀 주요 특징

- **AI 자동 기사 작성**: Google Gemini를 사용하여 아이들 눈높이에 맞는 흥미로운 기사를 매일 생성합니다.
- **맞춤형 삽화 생성**: Imagen 4.0을 통해 기사 내용과 찰떡궁합인 고품질 일러스트를 자동으로 그립니다.
- **다양한 교육 활동**: OX 퀴즈, 초성 퀴즈, 숨은그림 찾기, 색칠놀이, 4컷 만화 그리기 등 기사 내용과 연계된 창의 활동을 지원합니다.
- **통합 이미지 발행**: 생성된 HTML 페이지를 캡처하고 하나로 병합하여 출력 및 공유가 용이한 긴 이미지(`png`)로 제공합니다.

---

## 🛠️ 기술 스택 (Skill Sets)

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Language** | Python | 전체 시스템 로직 및 API 연동 |
| **Generative AI** | Google Gemini | 기사 텍스트 및 활동 데이터 생성 |
| **Image AI** | Imagen 4.0 | 기사 삽화 및 활동용 이미지 생성 |
| **Rendering** | Jinja2 | HTML 템플릿 엔진을 활용한 신문 레이아웃 구성 |
| **Screenshot** | Playwright | HTML을 고해상도 이미지로 캡처 |
| **Image Processing** | Pillow (PIL) | 캡처된 이미지 병합 및 후처리 |

---

## 📁 프로젝트 구조

```text
kidsnews/
├── make_news.py          # 신문 발행 메인 실행 스크립트
├── news_engine.py        # Gemini/Imagen API 및 활동 생성 엔진
├── templates/            # Jinja2 HTML 템플릿 및 CSS
│   ├── layout_p1.html    # 1페이지 (기사) 레이아웃
│   ├── layout_p2.html    # 2페이지 (활동) 레이아웃
│   ├── style.css         # 공통 스타일시트
│   └── activities/       # 활동별 상세 템플릿 (ox_quiz, coloring 등)
├── docs/                 # 최종 결과물 및 배포용 폴더
│   ├── [YYYY-MM-DD]/     # 매일 생성되는 결과물 (JSON, HTML, PNG)
│   └── index.html        # 오늘자 신문으로 리다이렉트되는 메인 페이지
└── USAGE.md              # 상세 실행 옵션 가이드
```

---

## ⚙️ 동작 방식 (Workflow)

신문 발행은 총 5단계의 스테이지를 거쳐 진행됩니다.

1.  **Stage 1: 기사 생성**: 요일별 주제 또는 사용자 입력 주제를 바탕으로 Gemini가 기사를 작성합니다.
2.  **Stage 2: 활동 데이터 생성**: 기사 내용에 적합한 활동(퀴즈 등)의 텍스트 데이터를 생성합니다.
3.  **Stage 3: AI 이미지 생성**: Imagen 4.0을 사용하여 기사 삽화와 활동에 필요한 이미지를 생성합니다.
4.  **Stage 4: HTML 렌더링**: 준비된 데이터를 Jinja2 템플릿에 주입하여 웹 페이지(`page1.html`, `page2.html`)를 만듭니다.
5.  **Stage 5: 캡처 및 병합**: Playwright로 HTML을 캡처한 뒤, 두 페이지를 세로로 이어 붙여 최종 신문 이미지(`full_newspaper_long.png`)를 완성합니다.

---

## 📝 사용 방법

기본적으로 파라메터 없이 실행하면 오늘 날짜의 신문을 발행합니다.

```bash
python make_news.py
```

더 자세한 옵션(주제 지정, 특정 활동 강제 등)은 [USAGE.md](file:///c:/Users/techz/kidsnews/USAGE.md) 파일을 참고하세요.
