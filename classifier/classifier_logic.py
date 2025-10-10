from langchain_core.prompts import ChatPromptTemplate

# ==============================================================================
# 0. 설정 및 상수
# ==============================================================================
CRISIS_KEYWORDS = ["죽고 싶", "자살", "극단적", "끝내고 싶", "살기 싫"]

SYSTEM_PROMPT_PATH = "classifier/system_prompt.txt"  # system prompt 파일 경로

# ==============================================================================
# 1. 감정 및 위기 감지
# ==============================================================================
def analyze_user_query(text: str) -> dict:
    """사용자의 입력에서 위기 상황을 감지합니다."""
    processed_text = text.replace(" ", "")
    for keyword in CRISIS_KEYWORDS:
        if keyword in processed_text:
            return {"status": "crisis", "keyword": keyword}
    return {"status": "normal"}


# ==============================================================================
# 2. 초기 상담 단계 (공감 + 위기 분기)
# ==============================================================================
def start_initial_conversation() -> dict:
    """초기 상담: 인사 → 위기 감지 → 공감 또는 상담 안내"""
    print("AI 청월 🌙: 안녕하세요, 청월입니다.")
    print("찾아주신 분께서는 어떤 상황이신가요?\n")

    user_first = input("사용자: ").strip()
    emotion = analyze_user_query(user_first)

    # 🚨 위기 상황 감지
    if emotion["status"] == "crisis":
        print("""
AI 청월 🌙:
말씀해주셔서 감사해요.

지금 당장 할 일은 전세사기 문제가 아니라 님의 마음을 돌보는 거예요.

━━━━━━━━━━━━━━━━━━
🚨 지금 즉시 전화하세요
자살예방상담전화 ☎️ 1393
• 24시간 운영
• 무료
• 익명 가능
━━━━━━━━━━━━━━━━━━

전화하시기 어려우시면
카카오톡 '마음터' 채팅상담 (24시간 운영)

전세사기 문제는 님의 마음이 안정된 다음에 천천히 해결하면 돼요.
제가 여기 있을게요. 언제든 다시 오세요.
        """)
        return {"status": "crisis"}

    # 😊 정상 상황일 경우 공감 멘트 후 진단 단계로 진입
    print("""
AI 청월 🌙:
전세 사기를 당하셨군요. 많이 놀라셨겠어요.
일단 숨 한번 깊게 쉬시고, 천천히 말씀해주세요.
몇 가지만 여쭤볼게요.
    """)
    return {"status": "normal", "text": user_first}


# ==============================================================================
# 3. 피해자 요건 진단
# ==============================================================================
def determine_victim_status(user_data: dict) -> str:
    """[공식 기준] 피해자 지원 등급을 판별"""
    req1 = user_data.get("요건1_대항력", False)
    req2 = user_data.get("요건2_보증금액", False)
    req3 = user_data.get("요건3_다수피해", False)
    req4 = user_data.get("요건4_사기의도", False)
    exc1 = user_data.get("제외_보증보험", False)
    exc2 = user_data.get("제외_최우선변제", False)
    exc3 = user_data.get("제외_자력회수", False)

    if exc1 or exc2 or exc3:
        return "지원 제외 대상"
    if req1 and req2 and req3 and req4:
        return "피해자 결정 (모든 지원 가능)"
    if not req1 and req2 and req4:
        return "피해자 결정 (금융지원 및 긴급복지 가능)"
    if req1 and not req2 and req3 and req4:
        return "피해자 결정 (조세채권 안분 지원 가능)"
    return "지원 요건 미충족"


def start_diagnosis_flow() -> str:
    """피해자 지원 요건 진단 절차"""
    questions = [
        ("주택 인도, 전입신고, 확정일자를 모두 갖추셨나요? (임차권 등기 포함)", "요건1_대항력"),
        ("임대차 보증금이 5억 원 이하인가요?", "요건2_보증금액"),
        ("집주인의 파산, 경매 등으로 2인 이상 임차인에게 피해가 발생했나요?", "요건3_다수피해"),
        ("임대인이 보증금을 돌려줄 의사나 능력이 없었다고 의심되나요?", "요건4_사기의도"),
        ("전세보증금 반환 보증보험에 가입되어 있나요?", "제외_보증보험"),
        ("소액임차인 최우선변제 제도로 보증금 '전액'을 돌려받을 수 있나요?", "제외_최우선변제"),
        ("대항력(경매 신청 등)을 통해 보증금 '전액'을 직접 회수할 수 있나요?", "제외_자력회수")
    ]

    user_data = {}
    print("AI 청월 🌙: 아래 질문에 예/아니오로 답변해주세요.\n")

    def ask(question, key):
        while True:
            answer = input(f"❓ {question} (예/아니오): ").strip().lower()
            if answer in ["예", "y", "yes"]:
                user_data[key] = True
                break
            elif answer in ["아니오", "아니요", "n", "no"]:
                user_data[key] = False
                break
            else:
                print("⚠️ '예' 또는 '아니오'로만 답변해주세요.")

    for q_text, q_key in questions:
        ask(q_text, q_key)

    result = determine_victim_status(user_data)
    print(f"\n📊 [진단 결과] 청월 판단: {result}")
    return result


# ==============================================================================
# 4. 프롬프트 생성
# ==============================================================================
def create_prompt(user_situation: str, user_query: str):
    """LangChain ChatPromptTemplate 기반 프롬프트 생성"""
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        system_text = f.read()

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_text),
        ("human", "{user_query}")
    ])

    formatted = prompt.format_messages(
        user_situation=user_situation,
        user_query=user_query
    )
    return formatted


# ==============================================================================
# 5. 통합 실행 (AI-2 전체 흐름)
# ==============================================================================
def run_ai2_pipeline():
    """초기 상담 → 위기 감지 → 진단 → 프롬프트 생성"""
    # 초기 상담
    init_result = start_initial_conversation()
    if init_result["status"] == "crisis":
        return None  # 위기 종료

    # 진단 단계
    user_situation = start_diagnosis_flow()

    # 사용자 마지막 질문
    user_query = input("\n청월 🌙: 마지막으로, 가장 궁금하신 점을 말씀해주세요.\n사용자: ")

    # 프롬프트 생성
    final_prompt = create_prompt(user_situation, user_query)

    print("\n--------------------------------------")
    print("📤 [AI-1 전달용 프롬프트]")
    for msg in final_prompt:
        print(f"**{msg.type.upper()}:**\n{msg.content}\n")
    print("--------------------------------------")

    return final_prompt


# ==============================================================================
# 6. 실행
# ==============================================================================
if __name__ == "__main__":
    run_ai2_pipeline()
