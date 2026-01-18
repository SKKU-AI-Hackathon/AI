## 🏠 전세사기 피해자 지원 AI 모델

</br>

> **"심리적 위로에서 실시간 데이터 기반 위험 분석까지, 당신을 위한 통합 가이드"**
> 
> 본 프로젝트는 전세사기 피해자들이 겪는 복잡한 법적/경제적 문제를 해결하고, 심리적 위기 상황에 즉각 대응하기 위해 개발된 인공지능 상담 솔루션입니다.
</br>

---

## 🚀 핵심 기능 및 기술적 구현 (Key Features & Technical Implementation)

### 1. Care-First 감정 분석 및 위기 대응 시스템
- **주요 기능**: 사용자 입력에서 위기 상황을 실시간 감지하여 심리적 안정과 긴급 상담을 우선 안내합니다.
- **기술적 구현**: 
    - 50개 이상의 도메인 특화 키워드를 활용한 **Emotion Filtering** 로직을 통해 3단계(Crisis, Shock, Confused) 감정 상태를 판별합니다.
    - **Crisis Detection**: '죽고 싶다' 등 고위험 키워드 매칭 시, RAG 답변에 앞서 자살예방상담전화(1393) 등의 정보를 즉각 노출하는 안전 가드레일을 구축했습니다.

</br>

### 2. 특별법 기반 피해자 요건 정밀 진단
- **주요 기능**: 복잡한 전세사기 특별법 지원 자격 유무를 7가지 문답을 통해 쉽고 정확하게 진단합니다.
- **기술적 구현**: 
    - **Boolean Matrix Diagnosis**: 특별법의 7개 핵심 요건을 불리언 매트릭스로 구성하여 지원 등급을 결정하는 **Rule-based Decision Tree** 알고리즘을 적용했습니다.
    - 진단 결과에 따라 4단계 지원 등급을 동적으로 할당하고, 이를 이후 RAG 체인의 `user_situation` 컨텍스트로 주입하여 개인화된 답변을 생성합니다.

</br>

### 3. 실거래가 기반 실시간 위험도 분석 엔진
- **주요 기능**: 서울시 실거래 데이터를 바탕으로 해당 매물의 전세사기 위험 점수를 산출합니다.
- **기술적 구현**: 
    - **Real-time API Pipeline**: 서울시 데이터광장 `tbLnOpendataRtmsV` API를 연동하여 실시간 XML 데이터를 수집 및 `ElementTree` 기반 파싱을 수행합니다.
    - **Weighted Sum Model (WSM)**: 아래 수식에 기반하여 종합 위험 점수($S$)를 산출합니다.
      $$S = (P_{LTV} \times 0.4) + (P_{Market} \times 0.2) + (P_{Building} \times 0.3) + (P_{Env} \times 0.1)$$
    - **Fall-back Heuristics**: API 장애 상황에서도 서비스 지속성을 유지하기 위해 유사 매물 추정 로직(`get_dummy_price_data`)을 포함한 예외 처리 시스템을 갖추었습니다.

</br>

### 4. 고도화된 RAG 상담 및 문맥 유지 시스템
- **주요 기능**: 법령과 지침을 기반으로 정확한 답변을 제공하며, 이전 대화 흐름을 기억해 상세 질문에 대응합니다.
- **기술적 구현**: 
    - **Document Engineering**: `RecursiveCharacterTextSplitter`를 활용해 **Chunk Size: 700 / Overlap: 100**으로 최적화된 지식 베이스를 구축했습니다.
    - **Vector Ops**: `FAISS`와 `all-MiniLM-L6-v2`를 이용한 시맨틱 검색(Top-K=5)을 수행합니다.
    - **Context-Aware Memory**: `ConversationMemory` 클래스를 구현하여 질문 내 특정 주제 집중(Focus) 지시문을 동적으로 프롬프트에 추가하는 **Enhanced Prompting** 기술을 적용했습니다.

</br>

---


## 🛠 기술 스택 (Tech Stack)

</br>

| 분류 | 기술 |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **LLM / Framework** | Google Gemini 1.5 Flash, LangChain (LCEL) |
| **Embedding** | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (384 dim) |
| **Vector DB** | FAISS (Facebook AI Similarity Search) |
| **Data API** | 서울시 부동산 실거래가 Open API (XML 방식) |
| **Libraries** | `requests`, `pypdf`, `python-dotenv`, `xml.etree.ElementTree` |


