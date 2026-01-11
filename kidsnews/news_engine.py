import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from google import genai
from google.genai import types
from PIL import Image

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# [Config] 초기 설정
# ---------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    logger.warning("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. API 호출 시 에러가 발생할 수 있습니다.")

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    logger.error(f"Gemini Client 초기화 실패: {e}")
    client = None

# ---------------------------------------------------------
# [Helpers] 공통 유틸리티
# ---------------------------------------------------------

def safe_parse_json(text):
    """
    Gemini 응답 텍스트를 파싱하여 Python 객체(Dict)로 변환합니다.
    응답이 리스트(List) 형태일 경우 첫 번째 요소를 반환하는 방어 로직을 포함합니다.
    반드시 딕셔너리(Dict) 형태를 반환하도록 보장합니다.
    """
    try:
        # Markdown 코드 블록 제거
        clean_text = text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        
        data = json.loads(clean_text)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        # 딕셔너리가 아닐 경우 빈 딕셔너리로 반환 (방어)
        if not isinstance(data, dict):
            logger.warning(f"JSON 파싱 결과가 Dict가 아님 ({type(data)}): {data}")
            return {}
            
        return data
    except Exception as e:
        logger.error(f"JSON 파싱 실패: {e} \nInput text: {text}")
        return {}

def generate_img(prompt, filename, output_dir):
    """
    Imagen 4.0을 사용하여 이미지를 생성하고 지정된 경로에 저장합니다.
    이미 파일이 존재하면 생성을 건너뛰어(캐싱) API 비용을 절약합니다.
    
    Args:
        prompt (str): 이미지 생성 프롬프트
        filename (str): 저장할 파일명 (확장자 포함)
        output_dir (str): 저장할 디렉토리 경로
        
    Returns:
        bool: 파일 존재 여부 (성공 시 True)
    """
    if not client:
        logger.error("Client가 초기화되지 않아 이미지를 생성할 수 없습니다.")
        return False

    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        try:
            logger.info(f"🎨 {filename} 생성 중 (Imagen 4.0)... Prompt: {prompt[:50]}...")
            img_resp = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="16:9")
            )
            if img_resp.generated_images:
                # PIL Image 객체 저장
                img_resp.generated_images[0].image.save(path)
                logger.info(f"✅ {filename} 생성 완료.")
                return True
        except Exception as e:
            logger.error(f"⚠️ 이미지 생성 실패 ({filename}): {e}")
            return False # 생성 실패
    else:
        logger.info(f"⏭️ {filename} 이미 존재함. 건너뜀.")
    
    return os.path.exists(path)

def fetch_emotion_images(emotions, output_dir):
    """
    감정 리스트에 대한 이미지를 3장 병렬로 생성합니다.
    
    Args:
        emotions (list): [{'prompt': '...'}, ...] 형태의 딕셔너리 리스트
        output_dir (str): 이미지를 저장할 디렉토리
    """
    def download(idx, item):
        # 캐릭터 일관성을 위한 프롬프트 프리픽스 추가
        full_prompt = f"Same character, cartoon style, {item.get('prompt', 'face')}"
        generate_img(full_prompt, f"emotion_{idx}.png", output_dir)

    # ThreadPoolExecutor를 사용하여 병렬 처리
    with ThreadPoolExecutor(max_workers=3) as exe:
        # enumerate를 사용하여 인덱스와 아이템을 함께 전달
        list(exe.map(lambda x: download(x[0], x[1]), enumerate(emotions)))

# ---------------------------------------------------------
# [Business Logic] 활동 생성 팩토리 (Dispatcher)
# ---------------------------------------------------------

def _generate_content_safe(prompt, model="gemini-3-flash-preview"):
    """Gemini API 호출 및 안전한 JSON 파싱을 수행하는 내부 헬퍼 함수"""
    if not client:
        return {}
    try:
        resp = client.models.generate_content(
            model=model, 
            contents=prompt, 
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        return safe_parse_json(resp.text)
    except Exception as e:
        logger.error(f"Gemini API 호출 실패: {e}")
        return {}

def generate_emotion_activity(topic):
    logger.info(f"🧠 [Emotion] 주제 '{topic}' 관련 감정 데이터 생성...")
    prompt = f"{{'scenario': '상황', 'emotions': [{{'type': '감정', 'prompt': '이미지프롬프트'}}]}} 형식으로 주제 '{topic}' 관련 감정 유추 퀴즈 데이터 생성해줘."
    return _generate_content_safe(prompt)

def generate_hidden_objects_activity(topic):
    logger.info(f"🧠 [HiddenObjects] 주제 '{topic}' 관련 숨은그림 찾기 생성...")
    prompt = f"""
    주제 '{topic}'와 어울리는 배경에 숨길 사물 5개를 정해줘. 이미지에 숨겨진 사물은 하나씩만 그려져야해!
    응답 JSON: {{'instruction': '가이드', 'items': ['사물1', '사물2'...], 'image_prompt': 'Black and white line art style for searching objects'}}
    """
    data = _generate_content_safe(prompt)
    if 'items' in data and isinstance(data['items'], list):
        data['items'] = data['items'][:5]
    return data

def generate_initial_quiz_activity(topic, body):
    logger.info(f"🧠 [Initial] 기사 내용을 바탕으로 초성 퀴즈 생성...")
    prompt = f"기사 '{body}' 관련 초성 퀴즈 3개 생성해줘. JSON: {{'instruction': '', 'items': [{{'clue': '', 'initials': []}}]}}"
    return _generate_content_safe(prompt)

def generate_ox_quiz_activity(topic, body):
    logger.info(f"🧠 [OX Quiz] 기사 내용을 바탕으로 OX 퀴즈 생성...")
    prompt = f"기사 '{body}' 기반 OX 퀴즈 3개. JSON: {{'instruction': '', 'items': ['질문1', '질문2', '질문3']}} (질문은 반드시 단순 문자열 리스트여야 함)"
    data = _generate_content_safe(prompt)
    
    # 데이터 노멀라이제이션 (객체로 올 경우 대비)
    if 'items' in data:
        normalized_items = []
        for i in data['items']:
            if isinstance(i, dict) and 'question' in i:
                normalized_items.append(i['question'])
            elif isinstance(i, str):
                normalized_items.append(i)
            else:
                # Fallback for unexpected types
                normalized_items.append(str(i))
        data['items'] = normalized_items
        
    return data

def generate_basic_activity(topic):
    logger.info(f"🧠 [Basic] 자유 활동 생성...")
    prompt = f"주제 '{topic}' 와 관련해서 그림 그리기 또는 느낀 점을 쓰는 곳의 적절한 제목 생성해줘. JSON: {{'instruction': ''}}"
    return _generate_content_safe(prompt)

def generate_coloring_activity(topic):
    logger.info(f"🧠 [Coloring] 주제 '{topic}' 관련 색칠놀이 생성...")
    prompt = f"""
    주제 '{topic}'와 관련된 아이들이 색칠할 수 있는 그림을 위한 프롬프트를 생성해줘.
    복잡하지 않고 단순한 선으로 이루어진 그림이어야 해.
    이미지에 색깔이 들어가면 안 돼. 반드시 흑백 선화(Line Art)여야 해.
    응답 JSON: {{'instruction': '색칠놀이 가이드 (예: 알록달록 색칠해보아요)', 'image_prompt': 'Black and white simple line art for kids coloring book, {topic}, white background, thick lines, no shading'}}
    """
    return _generate_content_safe(prompt)

def generate_cartoon_activity(topic, body):
    logger.info(f"🧠 [Cartoon] 주제 '{topic}' 관련 4컷 만화 생성...")
    prompt = f"""
    기사 주제 '{topic}'와 본문 '{body}'를 바탕으로 4컷 만화의 첫 번째 칸을 위한 설정을 만들어줘.
    어린이가 뒤의 세 칸을 상상해서 그릴 수 있도록 이야기의 시작이 되는 흥미로운 장면이어야 해.
    응답 JSON: {{
        "instruction": "첫 번째 칸을 보고 나머지 이야기를 상상해서 그려보세요!",
        "first_cut_dialogue": "첫 번째 칸에 들어갈 짧고 재미있는 대사",
        "image_prompt": "Black and white simple line art for kids, {topic} theme, the first scene of a story, a cute character doing something related to the article, white background, thick lines, no shading"
    }}
    """
    return _generate_content_safe(prompt)

def generate_activity_factory(act_type, topic, body):
    """
    활동 타입에 따라 적절한 생성 함수를 호출하는 팩토리 함수.
    
    Args:
        act_type (str): 활동 타입 ('emotion_guess', 'hidden_objects', 'initial_quiz', 'ox_quiz')
        topic (str): 기사 주제 (헤드라인)
        body (str): 기사 본문
        
    Returns:
        dict: 생성된 활동 데이터
    """
    try:
        if act_type == 'emotion_guess':
            return generate_emotion_activity(topic)
        elif act_type == 'hidden_objects':
            return generate_hidden_objects_activity(topic)
        elif act_type == 'initial_quiz':
            return generate_initial_quiz_activity(topic, body)
        elif act_type == 'ox_quiz':
            return generate_ox_quiz_activity(topic, body)
        elif act_type == 'coloring':
            return generate_coloring_activity(topic)
        elif act_type == 'cartoon':
            return generate_cartoon_activity(topic, body)
        else:
            logger.warning(f"알 수 없는 활동 타입 '{act_type}'. 기본(Basic) 활동으로 전환합니다.")
            return generate_basic_activity(topic)
    except Exception as e:
        logger.error(f"활동 생성 중 치명적 오류 발생: {e}. 기본(Basic) 활동으로 Fallback 합니다.")
        return generate_basic_activity(topic)

def generate_article(day_str, manual_topic=None):
    """
    1단계: 기사 및 활동 타입 결정.
    요일에 따른 주제를 미리 선정하여 Gemini에게 전달합니다.
    사용자가 직접 주제를 입력(manual_topic)한 경우 이를 우선 사용합니다.
    """
    if manual_topic:
        selected_topic = manual_topic
        logger.info(f"📰 Stage 1: 기사 발행 요청 (사용자 지정 주제: {selected_topic})...")
    else:
        # 요일별 주제 매칭 맵
        topic_map = {
            "월요일": "동물과 자연 (예: 멸종 위기 동물, 신기한 생물)",
            "화요일": "과학과 기술 (예: 나노 기술, 미래 발명품)",
            "수요일": "역사와 인물 (예: 용기를 낸 인물, 역사적 지혜)",
            "목요일": "마음 돌봄 (예: 친구 관계, 감정 표현, 거절의 기술)",
            "금요일": "꿈과 성장 (예: 이미지 트레이닝, 목표 달성)",
            "토요일": "경제와 생활 (예: 올바른 용돈 쓰기, 물건이 만들어지는 과정)",
            "일요일": "세상 뉴스 (예: 사회 변화, 미래 사회 예측)"
        }
        # 해당 요일의 주제 가져오기 (기본값 설정)
        selected_topic = topic_map.get(day_str, "자유 주제 (아이들이 흥미로워할 만한 이야기)")
        logger.info(f"📰 Stage 1: 기사 발행 요청 (주제: {selected_topic})...")
    
    prompt = f"""
    [시스템 역할] 
    너는 7세 아이들을 위한 일간 신문인 **'하하 어린이 신문(하루 한 장 어린이 신문)'**의 전문 편집장이야. 
    이 신문은 아이들이 하루 10분 투자를 통해 문해력의 기본기를 다지고 세상에 대한 호기심을 키우는 '병아리들의 놀이터' 같은 역할을 해.

    [오늘의 미션]
    아래의 [주제]를 바탕으로 7~9세 아이들이 흥미를 느낄만한 기사를 작성해줘.

    [작성 가이드라인]
    1. 대상: 7~9세 아이가 이해할 수 있는 쉬운 단어와 짧은 문장을 사용해줘.
    2. 톤앤매너: 친절하고 다정한 말투를 사용하며, 아이들의 상상력을 자극하도록 구성해줘.
    3. 주제: {selected_topic}
    4. 활동 타입 선택: 기사 내용과 가장 잘 어울리는 활동 타입('ox_quiz', 'hidden_objects', 'initial_quiz', 'emotion_guess', 'coloring', 'cartoon') 중 하나를 골라줘.

    [응답 포맷]
    반드시 아래 JSON 형식을 지켜줘:
    {{
      "page1": {{
        "headline": "아이들 눈높이의 제목",
        "article_body": ["문단1", "문단2", "문단3 (3~4문장 권장)"],
        "image_prompt": "기사 내용을 잘 보여주는 밝고 따뜻한 삽화 스타일 프롬프트"
      }},
      "activity_type": "선택한 활동 타입",
      "word_info": {{
        "word": "기사 속 어려운 단어 하나",
        "definition": "아이들 눈높이의 쉬운 풀이"
      }},
      "wisdom_window": {{
        "title": "속담 또는 사자성어",
        "meaning": "아이들 눈높이의 쉬운 풀이"
      }},
      "hidden_word": {{
        "word": "본문에 포함된 단어 중 하나 (찾아야 할 단어)",
        "mission": "해당 단어에 대한 설명과 함께 '기사에서 찾아 동그라미를 쳐보세요!'라는 미션 문구"
      }}
    }}
    """
    data = _generate_content_safe(prompt)
    if data:
        data['selected_topic'] = selected_topic
    return data
