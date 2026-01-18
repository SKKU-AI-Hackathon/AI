## 🏠 전세사기 피해자 지원 AI 모델

### 1. RAG 기반 지능형 상담 시스템
**기술 스택**
- Embedding: HuggingFace `all-MiniLM-L6-v2` (384 Dimensions)
- Vector DB: FAISS (Facebook AI Similarity Search)
- LLM: Google Gemini 1.5 Flash (High-speed & 1M+ Context support)
- Framework: LangChain (Expression Language, LCEL)

**주요 기능**
- 문서 분할 및 벡터화: 512자 단위 청킹 및 FAISS 인덱싱
- 시맨틱 검색: Cosine Similarity 기반 유사 문서 추출 (Top-K 검색)
- RAG 체인: 검색(Retriever) → 프롬프트 구성 → 답변 생성(Gemini) → 결과 파싱
- 대화 맥락 유지: `ConversationBufferWindowMemory`를 통한 이전 대화 흐름 반영 (최근 5개 메시지)

### 2. 부동산 위험도 분석 시스템
**기술 스택**
- Data Source: 서울시 부동산 실거래가 Open API (XML 방식)
- Parsing: `requests` + `xml.etree.ElementTree`
- Methodology: 논문 기반 가중치 적용 규칙 시스템 (Rule-based)

**핵심 알고리즘**
- 실거래 데이터 조회: `tbLnOpendataRtmsV` 등 관련 API 연동
- 전세가율 계산: LTV = (전세가 / 매매가) * 100 (최신 실거래가 기준)
- 종합 위험도 산정: 4가지 지표 가중 합산
  - 전세가율(40%) + 시장 지표(20%) + 건물 상태(30%) + 주변 환경(10%)
- 안전 등급 분류 (5단계): 
  - 80점 이상: 매우 위험
  - 20점 이하: 안전
