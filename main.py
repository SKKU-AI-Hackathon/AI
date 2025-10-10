import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'classifier'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'rag_engine'))

from classifier.classifier_logic import start_initial_conversation, start_diagnosis_flow, analyze_user_query
from rag_engine.run_chain import get_rag_response


def main():
    """AI 담당 2 + AI 담당 1 통합 실행 - 대화형 챗봇"""
    
    print("="*70)
    print("🏠 전세사기 피해자 지원 통합 상담 시스템")
    print("="*70 + "\n")
    
    # ========================================
    # 1단계: 초기 상담 (팀원이 추가한 기능)
    # ========================================
    init_result = start_initial_conversation()
    
    # 위기 상황 감지 시 종료
    if init_result.get("status") == "crisis":
        print("\n상담을 종료합니다. 힘내세요. 🙏")
        return
    
    # ========================================
    # 2단계: AI 담당 2 - 요건 판별 (7개 질문)
    # ========================================
    user_situation = start_diagnosis_flow()
    
    # 제외 대상이나 미충족이면 종료
    if user_situation in ["지원 제외 대상", "지원 요건 미충족"]:
        print("\n⚠️ 추가 상담이 필요합니다. 가까운 지원센터에 문의해주세요.")
        return
    
    # ========================================
    # 3단계: 자치구 정보 수집
    # ========================================
    district = input("\n📍 [추가 정보] 거주하시는 자치구를 알려주세요 (예: 종로구, 강남구): ").strip()
    
    # ========================================
    # 4단계: 대화 루프 시작 (무한 반복)
    # ========================================
    print("\n💬 이제부터 궁금하신 점을 자유롭게 질문해주세요.")
    print("💡 언제든지 '종료', 'exit', '그만' 을 입력하시면 상담이 종료됩니다.\n")
    
    user_query = input("AI 붱: 질문: ").strip()
    
    # 위기 키워드 체크 (대화 중에도 체크)
    query_analysis = analyze_user_query(user_query)
    if query_analysis["status"] == "crisis":
        print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 지금 즉시 전화하세요
자살예방상담전화 ☎️ 1393 (24시간 무료)
정신건강 위기상담 ☎️ 1577-0199
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
혼자 감당하지 마시고 전문가와 상담하시길 간곡히 부탁드립니다.
        """)
        return
    
    conversation_count = 0
    
    while True:
        conversation_count += 1
        
        # 종료 명령어 체크
        if user_query.lower() in ['종료', 'exit', '그만', 'quit', 'q', '끝']:
            print("\n" + "="*70)
            print("✅ 상담을 종료합니다. 힘내세요! 🙏")
            print(f"총 {conversation_count-1}번의 질문에 답변해드렸습니다.")
            print("="*70)
            break
        
        # 빈 입력 처리
        if not user_query.strip():
            user_query = input("\n💬 다시 질문해주세요: ").strip()
            continue
        
        # AI 담당 1 - RAG 답변 생성
        print("\n💭 답변을 생성 중입니다...\n")
        
        # 첫 질문에만 자치구 정보 포함
        if conversation_count == 1:
            response = get_rag_response(user_situation, user_query, district)
        else:
            response = get_rag_response(user_situation, user_query)
        
        # 답변 출력
        print("="*70)
        print("📝 답변")
        print("="*70 + "\n")
        print(response)
        print("\n" + "="*70 + "\n")
        
        # 다음 질문 받기
        print("💬 추가로 궁금하신 점이 있으신가요?")
        print("   (종료하려면 '종료' 입력)")
        user_query = input("\nAI 붱: ").strip()
        
        # 대화 중 위기 키워드 재체크
        query_analysis = analyze_user_query(user_query)
        if query_analysis["status"] == "crisis":
            print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 자살예방상담전화: 1393 (24시간 무료)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """)
            break


if __name__ == "__main__":
    main()
