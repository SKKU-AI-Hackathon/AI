"""
Contact Information by District

자치구별 연락처 정보 제공
"""

# 서울시 자치구별 연락처 DB
DISTRICT_CONTACTS = {
    "종로구": {
        "department": "부동산정보과",
        "phone": "02-2148-2893"
    },
    "중구": {
        "department": "부동산정보과",
        "phone": "02-3396-5114"
    },
    "용산구": {
        "department": "부동산정보과",
        "phone": "02-2199-7114"
    },
    "성동구": {
        "department": "부동산정보과",
        "phone": "02-2286-5114"
    },
    "광진구": {
        "department": "부동산정보과",
        "phone": "02-450-7114"
    },
    "동대문구": {
        "department": "부동산정보과",
        "phone": "02-2127-4114"
    },
    "중랑구": {
        "department": "부동산정보과",
        "phone": "02-2094-0114"
    },
    "성북구": {
        "department": "부동산정보과",
        "phone": "02-2241-2114"
    },
    "강북구": {
        "department": "부동산정보과",
        "phone": "02-901-6114"
    },
    "도봉구": {
        "department": "부동산정보과",
        "phone": "02-2091-2114"
    },
    "노원구": {
        "department": "부동산정보과",
        "phone": "02-2116-3114"
    },
    "은평구": {
        "department": "부동산정보과",
        "phone": "02-351-7114"
    },
    "서대문구": {
        "department": "부동산정보과",
        "phone": "02-330-1114"
    },
    "마포구": {
        "department": "부동산정보과",
        "phone": "02-3153-8114"
    },
    "양천구": {
        "department": "부동산정보과",
        "phone": "02-2620-3114"
    },
    "강서구": {
        "department": "부동산정보과",
        "phone": "02-2600-6114"
    },
    "구로구": {
        "department": "부동산정보과",
        "phone": "02-860-2114"
    },
    "금천구": {
        "department": "부동산정보과",
        "phone": "02-2627-1114"
    },
    "영등포구": {
        "department": "부동산정보과",
        "phone": "02-2670-3114"
    },
    "동작구": {
        "department": "부동산정보과",
        "phone": "02-820-1114"
    },
    "관악구": {
        "department": "부동산정보과",
        "phone": "02-879-5114"
    },
    "서초구": {
        "department": "부동산정보과",
        "phone": "02-2155-6114"
    },
    "강남구": {
        "department": "부동산정보과",
        "phone": "02-3423-6322"
    },
    "송파구": {
        "department": "부동산정보과",
        "phone": "02-2147-2114"
    },
    "강동구": {
        "department": "부동산정보과",
        "phone": "02-3425-5114"
    }
}

# 전국 통합 상담 연락처
NATIONAL_CONTACTS = """
🏢 전국 통합 상담
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HUG 통합콜센터: ☎ 1588-1663
전세피해지원센터: ☎ 02-6917-8119
경공매 지원센터: ☎ 1588-1663

💡 위 연락처로 전화하시면 담당자가 자세히 안내해드립니다.
"""


def get_contact_info(district: str) -> dict:
    """자치구별 연락처 정보 반환 (dict)"""
    return DISTRICT_CONTACTS.get(district)


def get_district_contact(district: str) -> str:
    """
    자치구별 연락처 정보를 텍스트 형태로 반환 (run_chain.py 호환)
    
    Args:
        district: 자치구 이름
    
    Returns:
        포맷팅된 연락처 문자열
    """
    return get_contact_info_text(district)


def get_contact_info_text(district: str) -> str:
    """
    자치구별 연락처 정보를 텍스트 형태로 반환
    
    Args:
        district: 자치구 이름 (예: "강남구")
    
    Returns:
        포맷팅된 연락처 문자열
    """
    contact = DISTRICT_CONTACTS.get(district)
    
    if not contact:
        return NATIONAL_CONTACTS
    
    district_info = f"""
{contact['department']}: ☎ {contact['phone']}
"""
    
    return district_info + NATIONAL_CONTACTS


def get_all_districts() -> list:
    """모든 자치구 목록 반환"""
    return list(DISTRICT_CONTACTS.keys())
