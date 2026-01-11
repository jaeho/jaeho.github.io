import os
import json
import datetime
import logging
from jinja2 import Template
from PIL import Image
from playwright.sync_api import sync_playwright
import argparse
import shutil

import news_engine

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# [Config] 설정 및 경로
# ---------------------------------------------------------
now = datetime.datetime.now()
days_ko = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

DATE_FOLDER = now.strftime("%Y-%m-%d")
DISPLAY_DATE = now.strftime("%Y년 %m월 %d일")
DISPLAY_DAY = days_ko[now.weekday()]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")
DOCS_DIR = os.path.join(CURRENT_DIR, "docs")
OUTPUT_DIR = os.path.join(DOCS_DIR, DATE_FOLDER)

# 출력 디렉토리 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 기수(Issue Number) 계산
def get_issue_label():
    import re
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not os.path.exists(DOCS_DIR):
        return "창간호"
    past_issues = [d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d)) and date_pattern.match(d)]
    issue_num = len(past_issues)
    if issue_num <= 1:
        return "창간호"
    else:
        return f"{issue_num}호"

ISSUE_LABEL = get_issue_label()


def load_or_generate_data(json_path, force_activity=None, manual_topic=None):
    """
    Stage 1 & 2: 기사 및 활동 데이터 로드 또는 생성
    """
    data = None
    if os.path.exists(json_path):
        logger.info("📂 기존 데이터 파일 발견, 로드합니다.")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    # 주제가 명시적으로 제공된 경우, 기존 데이터와 비교하여 다르면 재생성 유도
    if data and manual_topic:
        # 뉴스 제목(headline)에 주제 키워드가 포함되어 있는지 간단히 체크하거나, 
        # 그냥 주제가 제공되면 새로 생성하는 것이 안전할 수 있음.
        # 여기서는 사용자가 주제를 입력하면 기존 데이터를 무효화하고 새로 생성하도록 함.
        logger.info(f"📝 새로운 주제 지정됨: {manual_topic}. 기존 데이터를 무시하고 새로 생성합니다.")
        data = None

    # 강제 활동 타입 지정 시 처리 (data가 있는 경우)
    if data and force_activity:
        if data.get('activity_type') != force_activity:
            logger.info(f"🔄 활동 타입 변경 강제: {data.get('activity_type')} -> {force_activity}")
            data['activity_type'] = force_activity
            # 기존 활동 데이터 삭제하여 재생성 유도
            if 'activity_data' in data:
                del data['activity_data']

    if not data:
        # 1. 기사 발행 (Stage 1)
        logger.info("📰 Stage 1: 새 기사를 발행합니다...")
        data = news_engine.generate_article(DISPLAY_DAY, manual_topic=manual_topic)
        
        # 기사 생성 직후 강제 타입 적용
        if force_activity:
            logger.info(f"👉 활동 타입 강제 지정: {force_activity}")
            data['activity_type'] = force_activity
    
    # 2. 활동 상세 데이터 생성 (Stage 2)
    # 데이터가 없거나(새로 생성), 강제 변경으로 인해 삭제된 경우 재생성
    if 'activity_data' not in data:
        act_type = data.get('activity_type', 'basic')
        topic = data.get('page1', {}).get('headline', '제목 없음')
        body = " ".join(data.get('page1', {}).get('article_body', []))

        logger.info(f"🎮 Stage 2: '{act_type}' 활동 데이터 생성 중...")
        data['activity_data'] = news_engine.generate_activity_factory(act_type, topic, body)

        # 저장
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("💾 데이터 저장 완료.")
    
    return data


def render_html(data):
    """
    Stage 4: Jinja2 템플릿 렌더링
    """
    try:
        with open(os.path.join(TEMPLATE_DIR, "style.css"), "r", encoding="utf-8") as f:
            css_data = f.read()

        # 주제 클리닝 (괄호 제거)
        raw_topic = data.get('selected_topic', '오늘의 이야기')
        clean_topic = raw_topic.split('(')[0].strip()

        # Page 1 렌더링
        with open(os.path.join(TEMPLATE_DIR, "layout_p1.html"), "r", encoding="utf-8") as f:
            p1_html = Template(f.read()).render(
                css_content=css_data,
                today_date=DISPLAY_DATE,
                today_day=DISPLAY_DAY,
                image_url="article_image.png",
                clean_topic=clean_topic,
                issue_label=ISSUE_LABEL,
                **data['page1'],
                **data.get('word_info', {}),
                wisdom_window=data.get('wisdom_window', {"title": "미정", "meaning": "기사 내용을 확인해 보세요."}),
                hidden_word=data.get('hidden_word', {"word": "...", "mission": "본문에서 오늘의 핵심 단어를 찾아보세요!"})
            )
        with open(os.path.join(OUTPUT_DIR, "page1.html"), "w") as f:
            f.write(p1_html)

        # Page 2 렌더링
        act_type = data.get('activity_type', 'basic')
        p2_template_path = os.path.join(TEMPLATE_DIR, f"activities/{act_type}.html")
        
        # 템플릿이 없을 경우 basic으로 fallback
        if not os.path.exists(p2_template_path):
            logger.warning(f"⚠️ 템플릿 {act_type}.html이 없습니다. basic.html을 사용합니다.")
            p2_template_path = os.path.join(TEMPLATE_DIR, "activities/basic.html")

        with open(p2_template_path, "r", encoding="utf-8") as f:
            snippet = Template(f.read()).render(
                image_url="activity_image.png",
                **data.get('activity_data', {})
            )
        
        with open(os.path.join(TEMPLATE_DIR, "layout_p2.html"), "r", encoding="utf-8") as f:
            p2_html = Template(f.read()).render(
                css_content=css_data,
                activity_content=snippet,
                title=data.get('activity_data', {}).get('title', '오늘의 활동'),
                clean_topic=clean_topic,
                issue_label=ISSUE_LABEL,
                today_date=DISPLAY_DATE,
                wisdom_window=data.get('wisdom_window', {"title": "미정", "meaning": "기사 내용을 확인해 보세요."})
            )
        with open(os.path.join(OUTPUT_DIR, "page2.html"), "w") as f:
            f.write(p2_html)
            
        logger.info("HTML 렌더링 완료.")
        return True
    except Exception as e:
        logger.error(f"HTML 렌더링 실패: {e}")
        return False


def capture_and_merge():
    """
    Stage 5: 이미지 캡처 및 병합
    """
    img_paths = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(device_scale_factor=2)
            
            for f in ["page1.html", "page2.html"]:
                p_path = os.path.join(OUTPUT_DIR, f)
                if os.path.exists(p_path):
                    img_out = p_path.replace(".html", ".png")
                    # A4 비율 (794x1123 px at 96 DPI)
                    page.set_viewport_size({"width": 794, "height": 1123})
                    # 배경이 흰색이므로 투명도 없이 깔끔하게 캡처
                    page.goto(f"file://{os.path.abspath(p_path)}", wait_until="networkidle")
                    page.screenshot(path=img_out, full_page=False) # full_page=False로 viewport 크기만큼만 캡쳐
                    img_paths.append(img_out)
            browser.close()

        if len(img_paths) == 2:
            imgs = [Image.open(x) for x in img_paths]
            # 세로로 연결
            merged = Image.new('RGB', (imgs[0].width, sum(i.height for i in imgs)))
            y = 0
            for im in imgs:
                merged.paste(im, (0, y))
                y += im.height
            merged.save(os.path.join(OUTPUT_DIR, "full_newspaper_long.png"))
            logger.info(f"✨ 전체 신문 발행 완료: {os.path.join(OUTPUT_DIR, 'full_newspaper_long.png')}")
        else:
            logger.warning("이미지 2장을 모두 생성하지 못해 병합을 건너뜁니다.")

    except Exception as e:
        logger.error(f"이미지 캡처 및 병합 실패: {e}")


def main():
    parser = argparse.ArgumentParser(description="하하 어린이 신문 발행 시스템")
    parser.add_argument("--activity", type=str, choices=['ox_quiz', 'hidden_objects', 'initial_quiz', 'emotion_guess', 'basic', 'coloring', 'cartoon'], help="강제로 생성할 활동 타입을 지정합니다.")
    parser.add_argument("--new", action="store_true", help="기존 데이터를 삭제하고 새로 발행합니다.")
    parser.add_argument("--topic", type=str, help="작성할 기사의 주제를 직접 입력합니다.")
    args = parser.parse_args()

    logger.info("🚀 하하 어린이 신문 발행 시스템 시작")
    
    # 강제 재생성 모드일 경우 기존 데이터 및 이미지 삭제
    if args.new:
        logger.warning(f"⚠️ --new 옵션이 활성화됨. {OUTPUT_DIR} 내부 파일을 모두 삭제합니다.")
        import shutil
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    json_path = os.path.join(OUTPUT_DIR, "data.json")
    
    # 1. 데이터 준비 (Stage 1 & 2)
    data = load_or_generate_data(json_path, force_activity=args.activity, manual_topic=args.topic)
    
    # 2. 이미지 생성 (Stage 3)
    if 'page1' in data and 'image_prompt' in data['page1']:
        news_engine.generate_img(data['page1']['image_prompt'], "article_image.png", OUTPUT_DIR)
    
    act_type = data.get('activity_type')
    activity_data = data.get('activity_data', {})
    if not isinstance(activity_data, dict):
        logger.warning(f"⚠️ activity_data가 dict가 아닙니다 ({type(activity_data)}). 빈 dict로 대체합니다.")
        activity_data = {}

    if act_type == 'emotion_guess':
        emotions = activity_data.get('emotions', [])
        news_engine.fetch_emotion_images(emotions, OUTPUT_DIR)
    elif act_type == 'hidden_objects':
        prompt = activity_data.get('image_prompt')
        if prompt:
            news_engine.generate_img(prompt, "activity_image.png", OUTPUT_DIR)
    elif act_type in ['coloring', 'cartoon']:
        prompt = activity_data.get('image_prompt')
        if prompt:
             # 색칠놀이나 만화는 단순 라인 아트여야 하므로 프롬프트가 중요 (news_engine에서 처리됨)
            news_engine.generate_img(prompt, "activity_image.png", OUTPUT_DIR)
            
    # 3. HTML 렌더링 (Stage 4)
    if render_html(data):
        # 4. 최종 결과물 생성 (Stage 5)
        capture_and_merge()

    # 5. 메인 페이지(index.html) 리다이렉트 업데이트
    try:
        index_dest = os.path.join(DOCS_DIR, "index.html")
        redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={DATE_FOLDER}/page1.html">
    <title>하루 한 장 어린이 신문 - 이동 중...</title>
</head>
<body>
    <p>신문으로 이동하고 있습니다. 이동하지 않으면 <a href="{DATE_FOLDER}/page1.html">여기</a>를 눌러주세요.</p>
</body>
</html>"""
        with open(index_dest, "w", encoding="utf-8") as f:
            f.write(redirect_html)
        logger.info("📍 메인 페이지(index.html)를 오늘자 신문으로 리다이렉트 설정했습니다.")
    except Exception as e:
        logger.error(f"메인 페이지 업데이트 실패: {e}")
        
    logger.info("✅ 모든 작업 완료.")

if __name__ == "__main__":
    main()