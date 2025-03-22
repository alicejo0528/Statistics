import streamlit as st

st.set_page_config(
    page_title="학교 소음 환경 개선 프로젝트",
    page_icon="🏫",
    layout="wide"
)

# 향상된 커스텀 CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
            <style>
        /* 프로그레스 바 컨테이너 스타일 */
        .compact-progress {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* 프로그레스 항목 제목 */
        .progress-title {
            font-size: 0.9rem !important;
            color: #333;
            margin-bottom: 0.3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* 새로운 프로그레스 바 스타일 */
        .progress-bar-new {
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            overflow: hidden;
        }
        
        /* 프로그레스 바 채우기 애니메이션 */
        .progress-bar-fill-new {
            height: 100%;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            border-radius: 3px;
            transition: width 1.5s ease-in-out;
            animation: shimmer 2s infinite linear;
            background-size: 200% 100%;
        }
        
        /* 반짝이는 효과 애니메이션 */
        @keyframes shimmer {
            0% {
                background-position: 200% 0;
            }
            100% {
                background-position: -200% 0;
            }
        }
        
        /* 퍼센트 표시 */
        .progress-percent {
            font-size: 0.8rem;
            color: #666;
            font-weight: 500;
        }
        
        /* 프로그레스 섹션 전체 컨테이너 */
        .progress-container {
            max-width: 600px;
            margin: 0 auto;
        }

        * {
            font-family: 'Noto Sans KR', sans-serif;
        }
                h1 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
        }
        
        h2 {
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            font-size: 1.4rem !important;
            font-weight: 500 !important;
            margin-top: 1.5rem !important;
        }
        
        p {
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }
        
        .main-header {
            padding: 2.5rem;
        }
        
        .main-header h1 {
            font-size: 2.4rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .main-header h3 {
            font-size: 1.2rem !important;
            font-weight: 400 !important;
            opacity: 0.9;
        }
        
        .stat-card {
            padding: 1.2rem;
        }
        
        .stat-card h1 {
            font-size: 2rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stat-card p {
            font-size: 0.9rem !important;
            color: #666;
        }
        
        .progress-bar {
            height: 8px;
            margin: 0.5rem 0 1.5rem 0;
        }
        
        .section-content {
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            color: #333;
        }
        
        .team-card {
            padding: 1.2rem;
        }
        
        .team-card h3 {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .team-card p {
            font-size: 0.9rem !important;
            margin: 0.2rem 0 !important;
        }
        
        .button-primary {
            font-size: 0.9rem !important;
            padding: 0.6rem 1.2rem !important;
        }
        
        /* 탭 스타일링 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            font-size: 0.9rem !important;
        }
        
        /* 리스트 스타일링 */
        .section-content ul {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-left: 1.2rem;
        }
        
        .section-content li {
            font-size: 0.95rem !important;
            margin: 0.3rem 0;
            color: #444;
        }
        
        /* 컨텐츠 섹션 여백 조정 */
        .content-section {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* 구분선 추가 */
        .section-divider {
            height: 1px;
            background: #eee;
            margin: 2rem 0;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .content-section {
            background-color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .content-section:hover {
            transform: translateY(-5px);
        }
        
        .highlight {
            color: #4f46e5;
            font-weight: 600;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .team-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            margin: 0.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .progress-bar {
            height: 10px;
            background: #e2e8f0;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            border-radius: 5px;
            transition: width 0.5s ease;
        }
        
        .button-primary {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .button-primary:hover {
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🏫 학교 소음 환경 개선 프로젝트")
st.markdown("### 더 나은 학습 환경을 위한 종합적 연구")
st.markdown("""
<div style='display: flex; gap: 1rem; margin-top: 2rem;'>
    <button class='button-primary'>프로젝트 소개서 다운로드</button>
    <button class='button-primary'>연구 결과 보기</button>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 주요 통계
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h1 style='color: #4f46e5; font-size: 2.5rem;'>85%</h1>
        <p>학생들이 경험한<br>소음 스트레스</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h1 style='color: #4f46e5; font-size: 2.5rem;'>75dB</h1>
        <p>평균 교실<br>소음도</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h1 style='color: #4f46e5; font-size: 2.5rem;'>60%</h1>
        <p>집중력 저하<br>경험률</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h1 style='color: #4f46e5; font-size: 2.5rem;'>500+</h1>
        <p>설문 참여<br>학생 수</p>
    </div>
    """, unsafe_allow_html=True)

# 프로젝트 진행 현황
st.header("📈 프로젝트 진행 현황")

progress_items = {
    "데이터 수집": 100,
    "분석 단계": 80,
    "결과 도출": 60,
    "정책 제안": 30
}

for item, progress in progress_items.items():
    st.markdown(f"### {item}")
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-bar-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)

# 연구 방법론
st.header("🔬 연구 방법론")
method_col1, method_col2 = st.columns(2)

with method_col1:
    st.markdown("""
    ### 정량적 분석
    - 소음도 측정 및 분석
    - 통계적 데이터 처리
    - 설문 결과 분석
    """)

with method_col2:
    st.markdown("""
    ### 정성적 분석
    - 심층 인터뷰
    - 전문가 자문
    - 사례 연구
    """)
st.markdown('</div>', unsafe_allow_html=True)

# 연구 결과
st.header("📊 주요 연구 결과")
result_tabs = st.tabs(["소음 분포 분석", "건강 영향 평가", "학습 효과 분석"])

with result_tabs[0]:
    st.markdown("""
    ### 소음 분포 현황
    - 교실 내 평균 소음도: 75dB
    - 복도 평균 소음도: 80dB
    - 운동장 평균 소음도: 85dB
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with result_tabs[1]:
    st.markdown("""
    ### 건강 영향
    - 스트레스 증가: 85%
    - 청력 영향: 30%
    - 수면 장애: 25%
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with result_tabs[2]:
    st.markdown("""
    ### 학습 효과
    - 집중력 저하: 60%
    - 학업 성취도 영향: 45%
    - 수업 참여도 감소: 40%
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 프로젝트 팀
st.header("👥 자문 소개")
team_col1, team_col2, team_col3 = st.columns(3)

with team_col1:
    st.markdown("""
    <div class="team-card">
        <h3>소음 정책 교수</h3>
        <p>홍길동 교수</p>
        <p style='color: #666;'>환경공학 전문가</p>
    </div>
    """, unsafe_allow_html=True)

with team_col2:
    st.markdown("""
    <div class="team-card">
        <h3>Urban Planning</h3>
        <p>김철수 박사</p>
        <p style='color: #666;'>음향공학 전문가</p>
    </div>
    """, unsafe_allow_html=True)

with team_col3:
    st.markdown("""
    <div class="team-card">
        <h3>교육학 교수</h3>
        <p>이영희 연구원</p>
        <p style='color: #666;'>통계학 전문가</p>
    </div>
    """, unsafe_allow_html=True)

# 문의하기 섹션
st.header("📬 문의하기")
contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    st.markdown("""
    - 📧 이메일: research@school.edu
    - 📞 전화: 02-123-4567
    - 📍 주소: NLCS Jeju
    """)
st.markdown('</div>', unsafe_allow_html=True)