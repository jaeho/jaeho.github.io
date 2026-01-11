import os
import json
import logging
import datetime
from jinja2 import Template
import news_engine

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# [Config] 설정 및 경로
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "test_results_pro")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Page 1 Mock Data (고정)
MOCK_PAGE1 = {
    "headline": "하하 어린이 신문 테스트 발행",
    "article_body": [
        "오늘은 하하 어린이 신문의 새로운 시스템을 테스트하는 날이에요.",
        "멋진 활동지들이 잘 만들어지는지 확인해볼까요?",
        "모두 함께 즐겁게 문제를 풀어보아요."
    ],
    "image_prompt": "Cute cartoon robot fixing a newspaper printing machine, bright colors"
}
MOCK_WORD_INFO = {
    "word": "시스템",
    "definition": "필요한 기능을 실현하기 위하여 관련 요소를 체계적으로 결합한 집합체예요."
}

def render_page2(act_type, activity_data, output_filename):
    """
    Page 2 렌더링 (CSS 포함)
    """
    try:
        with open(os.path.join(TEMPLATE_DIR, "style.css"), "r") as f:
            css_data = f.read()

        # Activity 템플릿 로드
        tpl_path = os.path.join(TEMPLATE_DIR, f"activities/{act_type}.html")
        if not os.path.exists(tpl_path):
            tpl_path = os.path.join(TEMPLATE_DIR, "activities/basic.html")
        
        with open(tpl_path, "r") as f:
            snippet = Template(f.read()).render(
                image_url="test_activity_image.png",
                **activity_data
            )

        with open(os.path.join(TEMPLATE_DIR, "layout_p2.html"), "r") as f:
            p2_html = Template(f.read()).render(
                css_content=css_data,
                activity_content=snippet,
                title=activity_data.get('title', f'{act_type} 활동'),
                word_info=MOCK_WORD_INFO
            )
        
        out_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(out_path, "w") as f:
            f.write(p2_html)
        logger.info(f"✅ {output_filename} 생성 완료")
    
    except Exception as e:
        logger.error(f"❌ 렌더링 실패 ({act_type}): {e}")

def run_test():
    logger.info("🧪 Layout Pro 테스트 시작...")

    # 1. Page 1 생성 (Mock)
    logger.info("📄 Page 1 (Mock) 생성 중...")
    try:
        with open(os.path.join(TEMPLATE_DIR, "style.css"), "r") as f:
            css_data = f.read()
        
        with open(os.path.join(TEMPLATE_DIR, "layout_p1.html"), "r") as f:
            p1_html = Template(f.read()).render(
                css_content=css_data,
                today_date="2024년 1월 1일",
                today_day="월요일",
                image_url="test_article_image.png",
                **MOCK_PAGE1,
                **MOCK_WORD_INFO
            )
        with open(os.path.join(OUTPUT_DIR, "page1_mock.html"), "w") as f:
            f.write(p1_html)
        
        # 이미지 생성 테스트 (Page 1)
        news_engine.generate_img(MOCK_PAGE1['image_prompt'], "test_article_image.png", OUTPUT_DIR)
        
    except Exception as e:
        logger.error(f"Page 1 생성 실패: {e}")

    # 2. Page 2 Loop Test
    activity_types = ['ox_quiz', 'hidden_objects', 'initial_quiz', 'emotion_guess', 'basic', 'coloring']
    
    for act_type in activity_types:
        logger.info(f"🔄 Testing Activity: {act_type}")
        try:
            # 실시간 API 호출로 데이터 생성 Verification
            # topic과 body는 Mock 데이터를 사용
            act_data = news_engine.generate_activity_factory(
                act_type, 
                MOCK_PAGE1['headline'], 
                " ".join(MOCK_PAGE1['article_body'])
            )
            
            # 이미지 생성 테스트 (Activity)
            if act_type == 'emotion_guess':
                emotions = act_data.get('emotions', [])
                if emotions:
                    news_engine.fetch_emotion_images(emotions, OUTPUT_DIR)
            elif act_type == 'hidden_objects' or act_type == 'coloring':
                prompt = act_data.get('image_prompt')
                if prompt:
                    news_engine.generate_img(prompt, "test_activity_image.png", OUTPUT_DIR)
            
            # HTML 렌더링
            render_page2(act_type, act_data, f"page2_{act_type}.html")
            
        except Exception as e:
            logger.error(f"❌ Test Failed for {act_type}: {e}")

    logger.info("✨ 모든 테스트가 완료되었습니다. 'test_results_pro' 폴더를 확인하세요.")

if __name__ == "__main__":
    run_test()
