import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="코드 문서",
    page_icon="🖥️",
    layout="wide"
)

# CSS 스타일
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
        
        * {
            font-family: 'Noto Sans KR', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
            color: white;
            padding: 3rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
        
        .code-section {
            background-color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .feature-box {
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
        }
        
        .progress-bar {
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            margin: 0.5rem 0;
        }
        
        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6 0%, #1e40af 100%);
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        
        code {
            padding: 0.2em 0.4em;
            border-radius: 0.3em;
            background: #f1f5f9;
            font-size: 0.9em;
        }
        
        .reference-box {
            background: #f8fafc;
            padding: 2rem;
            border-radius: 1rem;
            margin-top: 2rem;
            border: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🖥️ 코드 문서")
st.markdown("### 📚 참고사항")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 사용된 라이브러리
    - **pandas**: 데이터 처리
    - **numpy**: 수치 연산
    - **matplotlib**: 시각화
    - **seaborn**: 통계 시각화
    - **scipy**: 통계 분석
    """)

with col2:
    st.markdown("""
    #### 분석 방법론
    - **데이터 전처리**: 결측치, 이상치 처리
    - **통계 분석**: 상관관계, 유의성 검정
    - **시각화**: 그래프, 차트 생성
    - **시계열 분석**: 추세, 주기성 분석
    """)

st.markdown('</div>', unsafe_allow_html=True)



# 코드 섹션 탭
tabs = st.tabs(["데이터 전처리", "기술 통계 분석", "소음 분석", "상관관계 분석", "시계열 분석"])

with tabs[0]:
    st.markdown("### 📊 데이터 전처리")
    st.markdown("""
    #### 주요 기능
    - CSV 파일 로딩 및 인코딩 처리
    - 결측치 처리
    - 데이터 타입 변환
    - 소음 관련 컬럼 필터링
    """)
    
    with st.expander("🔍 코드 보기", expanded=True):
        st.code("""
        # CSV 파일 로딩 및 인코딩 처리
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        # 결측치 처리
        noise_data = df[noise_columns].apply(pd.to_numeric, errors='coerce')
        noise_data = noise_data.fillna(noise_data.mean())
        
        # 데이터 타입 변환
        if '측정 시간' in df.columns:
            df['측정 시간'] = pd.to_datetime(df['측정 시간'])
            df['시간'] = df['측정 시간'].dt.hour
        """)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### 📈 기술 통계 분석")
    st.markdown("""
    #### 분석 항목
    - 전체 응답자 수 통계
    - 학교급별 분포도
    - 지역별 응답자 현황
    - 집중력 저하 경험 비율
    """)
    
    with st.expander("🔍 코드 보기", expanded=True):
        st.code("""
        # 응답자 수 집계
        total_respondents = len(df)
        
        # 학교급별 분포 분석
        if '현재 학교급' in df.columns:
            school_counts = df['현재 학교급'].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(data=df, x='현재 학교급')
            
        # 지역별 응답자 분석
        region_stats = df['지역'].value_counts()
        
        # 집중력 저하 경험 분석
        focus_impact = df['집중력_저하'].value_counts(normalize=True) * 100
        """)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 🔊 소음 분석")
    st.markdown("""
    #### 분석 방법
    - 장소별 소음 수준 비교
    - 소음 유형 분류 및 빈도 분석
    - 시간대별 소음 패턴
    - 소음 영향 평가
    """)
    
    with st.expander("🔍 코드 보기", expanded=True):
        st.code("""
        # 장소별 소음 레벨 분포
        noise_columns = get_noise_columns(df)
        if noise_columns:
            noise_data = df[noise_columns].apply(pd.to_numeric, errors='coerce')
            fig, ax = plt.subplots()
            sns.boxplot(data=noise_data)
            
        # 주요 소음 유형 분석
        if '주된_소음_유형' in df.columns:
            noise_types = df['주된_소음_유형'].str.split(';').explode()
            noise_type_counts = noise_types.value_counts()
            
        # 시간대별 소음 레벨
        hourly_noise = df.groupby('시간')['소음레벨'].mean()
        """)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 📊 상관관계 분석")
    st.markdown("""
    #### 분석 내용
    - 장소간 소음 상관관계
    - 건강 영향 연관성
    - 통계적 유의성 검정
    - 상관계수 시각화
    """)
    
    with st.expander("🔍 코드 보기", expanded=True):
        st.code("""
        # 장소별 소음 레벨 상관관계
        correlation_matrix = noise_data.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            vmin=-1,
            vmax=1,
            center=0
        )
        
        # 소음과 건강 증상의 관계 분석
        symptoms_df = pd.DataFrame(index=df.index)
        for symptom in unique_symptoms:
            symptoms_df[symptom] = symptoms_list.apply(
                lambda x: 1 if isinstance(x, list) and symptom in x else 0
            )
            
        # 통계적 유의성 검정
        from scipy import stats
        for symptom in symptoms_df.columns:
            t_stat, p_value = stats.ttest_ind(
                noise_data[noise_data.index.isin(symptoms_df[symptoms_df[symptom]==1].index)],
                noise_data[noise_data.index.isin(symptoms_df[symptoms_df[symptom]==0].index)]
            )
        """)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]:
    st.markdown("### ⏰ 시계열 분석")
    st.markdown("""
    #### 분석 기법
    - 시간대별 평균 소음도
    - 이동평균 계산
    - 선형 추세 분석
    - 주기성 패턴 탐지
    """)
    
    with st.expander("🔍 코드 보기", expanded=True):
        st.code("""
        # 시간대별 소음 패턴
        if '측정 시간' in df.columns:
            df['시간'] = df['측정 시간'].dt.hour
            
            for col in noise_columns:
                hourly_noise = df.groupby('시간')[col].mean()
                
                fig, ax = plt.subplots(figsize=(12, 6))
                hourly_noise.plot(kind='line', marker='o')
                
        # 추세 분석
        def analyze_trend(time_series):
            rolling_mean = time_series.rolling(window=3).mean()
            x = np.arange(len(time_series))
            z = np.polyfit(x, time_series, 1)
            p = np.poly1d(z)
            return rolling_mean, p(x)
            
        # 주기성 분석
        from scipy import signal
        def analyze_periodicity(time_series):
            f, Pxx = signal.periodogram(time_series)
            return f, Pxx
        """)
    st.markdown('</div>', unsafe_allow_html=True)
