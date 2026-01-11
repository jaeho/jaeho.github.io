import os
import json
import datetime
from jinja2 import Template
from playwright.sync_api import sync_playwright
from google import genai
from google.genai import types
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 1. API 설정
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 2. 초기 설정 및 경로
now = datetime.datetime.now()
display_date = now.strftime("%Y년 %m월 %d일")
display_day = "목요일"

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, "templates")
test_output_dir = os.path.join(current_dir, "test_results_pro")
os.makedirs(test_output_dir, exist_ok=True)

# 3. MOCK 데이터 (Page 1 고정)
MOCK_BASE = {
    "page1": {
        "headline": "목요일은 '숲속 친구들의 요리 대회' 열리는 날!",
        "clean_topic": "숲속 요리 대회",
        "issue_label": "Vol. 12",
        "article_body": [
            "오늘은 숲속 마을에서 아주 특별한 요리 대회가 열렸어요.",
            "다람쥐 친구는 산에서 모은 도토리로 고소한 빵을 구웠대요.",
            "토끼 친구는 아삭아삭한 당근을 썰어 신선한 샐러드를 만들었죠.",
            "숲속 친구들은 서로의 음식을 나눠 먹으며 행복한 목요일을 보냈답니다.",
            "우리 친구들도 오늘 어떤 맛있는 음식을 먹었는지 가족들과 이야기해 볼까요?"
        ],
        "image_prompt": "A whimsical forest clearing storybook illustration style.",
        "hidden_word": {
            "mission": "기사 속에서 '요리'라는 단어를 찾아 동그라미를 쳐보세요!",
            "word": "요리"
        }
    },
    "word_info": { "word": "요리", "definition": "여러 가지 재료를 섞고 음식을 만드는 일이에요." },
    "wisdom_window": {
        "title": "백지장도 맞들면 낫다",
        "meaning": "아무리 쉬운 일이라도 서로 힘을 합치면 훨씬 더 쉬워진다는 뜻이에요."
    }
}

# ---------------------------------------------------------
# [Dispatcher] 활동별 실제 Gemini/Imagen 생성 함수 (원본 로직과 동일)
# ---------------------------------------------------------

def generate_img(prompt, filename, output_path):
    path = os.path.join(output_path, filename)
    try:
        print(f"🎨 {filename} 생성 중 (Imagen 4.0)...")
        img_resp = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="16:9")
        )
        if img_resp.generated_images:
            img_resp.generated_images[0].image.save(path)
            return True
    except Exception as e:
        print(f"⚠️ 이미지 실패: {e}")
    return False

def fetch_emotion_images(emotions, output_path):
    def download(idx, item):
        generate_img(f"Same character, cartoon style, {item['prompt']}", f"emotion_{idx}.png", output_path)
    with ThreadPoolExecutor(max_workers=3) as exe:
        list(exe.map(lambda x: download(x[0], x[1]), enumerate(emotions)))

def get_gemini_activity(act_type):
    print(f"🧠 Gemini가 '{act_type}' 데이터를 생성합니다...")
    topic = MOCK_BASE['page1']['headline']
    body = " ".join(MOCK_BASE['page1']['article_body'])

    # 프롬프트에 '최상위 객체는 반드시 {} 딕셔너리여야 함'을 강조
    prompts = {
        "ox_quiz": f"기사 '{body}' 기반 OX 퀴즈 3개. JSON: {{'instruction':'', 'items':[]}}",
        "spy_hunt": f"주제 '{topic}' 특사 찾기. JSON: {{'instruction':'', 'items':[], 'image_prompt':''}}",
        "initial_quiz": f"기사 '{body}' 초성 퀴즈 3개. JSON: {{'instruction':'', 'items':[{{'clue':'', 'initials':[]}}]}}",
        "emotion_guess": f"주제 '{topic}' 감정 유추 3가지 상황. JSON: {{'scenario':'', 'emotions':[{{'type':'', 'prompt':''}}]}}",
        "cartoon": f"주제 '{topic}' 4컷 만화 시작. JSON: {{'instruction':'', 'first_cut_dialogue':'', 'image_prompt':''}}",
        "coloring": f"주제 '{topic}' 색칠놀이. JSON: {{'instruction':'', 'image_prompt':''}}",
        "hidden_objects": f"주제 '{topic}' 숨은 그림 찾기. JSON: {{'instruction':'', 'items':[], 'image_prompt':''}}",
        "basic": f"주제 '{topic}' 느낀 점 가이드. JSON: {{'instruction':''}}"
    }

    resp = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompts[act_type],
        config=types.GenerateContentConfig(response_mime_type='application/json')
    )

    data = json.loads(resp.text)

    # --- 방어 코드 추가 (List일 경우 첫 번째 요소 추출) ---
    if isinstance(data, list):
        print("⚠️ Gemini가 리스트 형태로 응답했습니다. 첫 번째 요소를 사용합니다.")
        data = data[0]

    # --- 추가 가공: hidden_objects 아이템 개수 제한 (max 5) ---
    if act_type == "hidden_objects" and "items" in data and isinstance(data['items'], list):
        data['items'] = data['items'][:5]

    return data
# ---------------------------------------------------------
# 실행 엔진
# ---------------------------------------------------------

def run_pro_test():
    with open(os.path.join(template_dir, "style.css"), "r", encoding="utf-8") as f:
        css_data = f.read()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)

        test_types = ['ox_quiz', 'spy_hunt', 'initial_quiz', 'emotion_guess', 'cartoon', 'coloring', 'hidden_objects', 'basic']

        for act_type in test_types:
            print(f"\n🚀 [{act_type}] 테스트 시작")
            type_dir = os.path.join(test_output_dir, act_type)
            os.makedirs(type_dir, exist_ok=True)

            # 1. 실제 Gemini 데이터 생성
            act_data = get_gemini_activity(act_type)

            # 2. 실제 Imagen 이미지 생성
            if act_type == 'emotion_guess':
                fetch_emotion_images(act_data['emotions'], type_dir)
            elif act_type in ['spy_hunt', 'cartoon', 'coloring', 'hidden_objects']:
                generate_img(act_data['image_prompt'], "activity_image.png", type_dir)

            # 메인 기사 이미지는 공통 사용 (없으면 한 번 생성)
            generate_img(MOCK_BASE['page1']['image_prompt'], "article_image.png", type_dir)

            # 3. 렌더링
            # Page 1
            with open(os.path.join(template_dir, "layout_p1.html"), "r") as f:
                p1_html = Template(f.read()).render(css_content=css_data, today_date=display_date, today_day=display_day, image_url="article_image.png", **MOCK_BASE['page1'], **MOCK_BASE['word_info'])
            with open(os.path.join(type_dir, "page1.html"), "w") as f: f.write(p1_html)

            # Page 2
            with open(os.path.join(template_dir, f"activities/{act_type}.html"), "r") as f:
                snippet = Template(f.read()).render(image_url="activity_image.png", **act_data)
            with open(os.path.join(template_dir, "layout_p2.html"), "r") as f:
                p2_html = Template(f.read()).render(
                    css_content=css_data, 
                    activity_content=snippet, 
                    title=f"진짜 데이터 테스트: {act_type}", 
                    word_info=MOCK_BASE['word_info'],
                    wisdom_window=MOCK_BASE['wisdom_window'],
                    today_date=display_date,
                    today_day=display_day,
                    issue_label=MOCK_BASE['page1']['issue_label']
                )
            with open(os.path.join(type_dir, "page2.html"), "w") as f: f.write(p2_html)

            # 4. 캡처 및 병합
            img_paths = []
            for html_f in ["page1.html", "page2.html"]:
                f_path = os.path.join(type_dir, html_f)
                img_out = f_path.replace(".html", ".png")
                page.goto(f"file://{os.path.abspath(f_path)}", wait_until="networkidle")
                page.set_viewport_size({"width": 794, "height": 1123})
                page.screenshot(path=img_out, full_page=True)
                img_paths.append(img_out)

            imgs = [Image.open(x) for x in img_paths]
            merged = Image.new('RGB', (imgs[0].width, sum(i.height for i in imgs)))
            y = 0
            for im in imgs:
                merged.paste(im, (0, y))
                y += im.height
            merged.save(os.path.join(type_dir, f"pro_test_{act_type}.png"))
            print(f"✅ {act_type} 완료")

        browser.close()

if __name__ == "__main__":
    run_pro_test()