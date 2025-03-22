import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'
    
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

# 소음 관련 컬럼 필터링 함수
def get_noise_columns(df):
    # 데시벨 관련 키워드 목록
    noise_keywords = ['데시벨', 'db', 'dB', 'DB']
    
    # 특정 장소 키워드 목록
    place_keywords = ['교실', '도서관', '복도', '운동장', '급식실', '화장실', '음악실']
    
    noise_columns = []
    
    for col in df.columns:
        # 데시벨 키워드가 포함된 컬럼 추가
        if any(keyword in col for keyword in noise_keywords):
            noise_columns.append(col)
        # 장소 키워드가 포함된 컬럼 중 숫자 데이터를 포함한 컬럼 추가
        elif any(keyword in col for keyword in place_keywords):
            try:
                # 숫자로 변환 가능한 데이터가 있는지 확인
                numeric_data = pd.to_numeric(df[col], errors='coerce')
                if not numeric_data.isna().all() and numeric_data.between(0, 120).any():
                    noise_columns.append(col)
            except:
                continue
    
    return noise_columns

# 페이지 설정
st.set_page_config(
    page_title="학교 소음 환경 분석",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
        }
        .main-header {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        hr {
            margin: 2rem 0;
            border: none;
            border-top: 1px solid #eee;
        }
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .dataframe {
            font-family: 'Malgun Gothic', sans-serif !important;
            font-size: 0.9rem !important;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
        .chart-container {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.title("분석 설정")
    
    uploaded_file = st.file_uploader(
        "설문조사 CSV 파일을 업로드하세요",
        type=['csv'],
        help="UTF-8 인코딩된 CSV 파일을 업로드해주세요."
    )

# 메인 페이지
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🔊 학교 소음 환경 분석 대시보드")
st.markdown("학교 환경의 소음이 학생들에게 미치는 영향을 분석합니다.")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        # 탭 생성
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 기본 통계", 
            "🎯 소음 분석", 
            "🔍 상관관계 분석",
            "📈 시계열 분석",
            "📑 원본 데이터",
            "💻 분석 방법론"
        ])

        # 기본 통계 탭
        with tab1:
            st.header("기본 응답 정보")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "총 응답자 수",
                    f"{len(df):,}명",
                    "전체"
                )
            
            with col2:
                if '학교에서 집중력 저하를 경험한 적이 있나요?' in df.columns:
                    concentration_rate = (df['학교에서 집중력 저하를 경험한 적이 있나요?'] == '네').mean() * 100
                    st.metric(
                        "집중력 저하 경험 비율",
                        f"{concentration_rate:.1f}%",
                        "응답자 중"
                    )
            
            with col3:
                if '현재 학교급' in df.columns:
                    school_counts = df['현재 학교급'].value_counts()
                    st.metric(
                        "가장 많은 학교급",
                        f"{school_counts.index[0]}",
                        f"{school_counts.iloc[0]}명"
                    )
            
            with col4:
                if '어느 지역에 거주하나요?' in df.columns:
                    region_counts = df['어느 지역에 거주하나요?'].value_counts()
                    st.metric(
                        "최다 응답 지역",
                        f"{region_counts.index[0]}",
                        f"{region_counts.iloc[0]}명"
                    )

            # 학교급별 분포
            st.subheader("학교급별 응답자 분포")
            if '현재 학교급' in df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.countplot(data=df, x='현재 학교급')
                plt.title('학교급별 응답자 수')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.close()
        # 소음 분석 탭
        with tab2:
            st.header("소음 분석")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("소음 경험 분포")
                if '학교 및 집 주변에서 소음이 심하다고 느낀 적이 있나요?' in df.columns:
                    noise_exp = df['학교 및 집 주변에서 소음이 심하다고 느낀 적이 있나요?'].value_counts()
                    fig, ax = plt.subplots()
                    noise_exp.plot(kind='bar')
                    plt.title('소음 경험 빈도')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close()
            
            with col2:
                st.subheader("장소별 소음 레벨")
                noise_columns = get_noise_columns(df)
                if noise_columns:
                    noise_data = df[noise_columns].apply(pd.to_numeric, errors='coerce')
                    fig, ax = plt.subplots()
                    sns.boxplot(data=noise_data)
                    plt.xticks(rotation=45)
                    plt.title('장소별 소음 분포')
                    st.pyplot(fig)
                    plt.close()

            # 주요 소음 유형 분석
            st.subheader("주요 소음 유형 분석")
            if '집중력을 방해하는 주된 소음 유형은 무엇인가요?' in df.columns:
                noise_types = df['집중력을 방해하는 주된 소음 유형은 무엇인가요?'].str.split(';').explode()
                noise_type_counts = noise_types.value_counts()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                noise_type_counts.plot(kind='barh')
                plt.title('방해되는 소음 유형')
                st.pyplot(fig)
                plt.close()

            # 시간대별 소음 분석
            st.subheader("시간대별 소음 분석")
            if '가장 소음이 심한 시간대는 언제인가요?' in df.columns:
                time_noise = df['가장 소음이 심한 시간대는 언제인가요?'].value_counts()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                time_noise.plot(kind='pie', autopct='%1.1f%%')
                plt.title('소음이 심한 시간대 분포')
                st.pyplot(fig)
                plt.close()

        # 상관관계 분석 탭
        with tab3:
            st.header("상관관계 분석")
            
            try:
                # 소음 관련 컬럼 필터링
                noise_columns = get_noise_columns(df)
                
                if noise_columns:
                    # 숫자형 데이터로 변환
                    noise_data = df[noise_columns].apply(pd.to_numeric, errors='coerce')
                    
                    # 결측치 처리
                    noise_data = noise_data.fillna(noise_data.mean())
                    
                    st.subheader("소음 레벨 간 상관관계")
                    
                    # 상관관계 행렬 계산
                    correlation_matrix = noise_data.corr()
                    
                    # 히트맵 생성
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(
                        correlation_matrix,
                        annot=True,
                        cmap='coolwarm',
                        vmin=-1,
                        vmax=1,
                        center=0,
                        fmt='.2f',
                        square=True,
                        ax=ax
                    )
                    plt.title('장소별 소음 레벨 상관관계')
                    st.pyplot(fig)
                    plt.close()

                    # 건강 영향 분석
                    if '소음이 심한 환경에서 다음과 같은 증상을 경험한 적이 있나요?' in df.columns:
                        st.subheader("건강 영향 분석")
                        
                        # 증상 데이터 전처리 수정
                        symptoms = df['소음이 심한 환경에서 다음과 같은 증상을 경험한 적이 있나요?'].fillna('')
                        # 세미콜론으로 분리된 증상들을 리스트로 변환
                        symptoms_list = symptoms.str.split(';')
                        
                        # 모든 고유 증상 추출
                        unique_symptoms = set()
                        for symptom_list in symptoms_list:
                            if isinstance(symptom_list, list):  # None이 아닌 경우만 처리
                                unique_symptoms.update(s.strip() for s in symptom_list if s.strip())
                        
                        # 각 증상에 대한 더미 변수 생성
                        symptoms_df = pd.DataFrame(index=df.index)
                        for symptom in unique_symptoms:
                            symptoms_df[symptom] = symptoms_list.apply(
                                lambda x: 1 if isinstance(x, list) and symptom in x else 0
                            )
                        
                        if not symptoms_df.empty:
                            # 증상 빈도 계산
                            symptom_counts = symptoms_df.sum()
                            
                            # 증상 빈도 시각화
                            fig, ax = plt.subplots(figsize=(10, 6))
                            symptom_counts.plot(kind='barh')
                            plt.title('소음으로 인한 건강 증상')
                            st.pyplot(fig)
                            plt.close()

                            # 소음 레벨과 증상의 상관관계 분석
                            st.subheader("소음 레벨과 증상의 관계")
                            
                            # 상관관계 계산
                            noise_symptom_corr = pd.DataFrame(index=noise_columns, columns=symptoms_df.columns)
                            
                            for noise_col in noise_columns:
                                noise_values = pd.to_numeric(df[noise_col], errors='coerce').fillna(0)
                                for symptom in symptoms_df.columns:
                                    correlation = np.corrcoef(noise_values, symptoms_df[symptom])[0,1]
                                    noise_symptom_corr.loc[noise_col, symptom] = correlation
                            
                            # 상관관계 히트맵
                            fig, ax = plt.subplots(figsize=(12, 6))
                            sns.heatmap(
                                noise_symptom_corr,
                                annot=True,
                                cmap='coolwarm',
                                center=0,
                                fmt='.2f',
                                ax=ax
                            )
                            plt.title('소음 레벨과 증상의 상관관계')
                            plt.xticks(rotation=45, ha='right')
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close()
                        else:
                            st.warning("건강 증상 데이터가 없거나 올바르지 않은 형식입니다.")
                    else:
                        st.warning("건강 증상 관련 데이터가 없습니다.")
                else:
                    st.warning("소음 측정 데이터를 찾을 수 없습니다.")
                    
            except Exception as e:
                st.error(f"상관관계 분석 중 오류가 발생했습니다: {str(e)}")
                st.write("데이터 형식을 확인해주세요.")

        # 시계열 분석 탭
        with tab4:
            st.header("시간대별 소음 패턴 분석")
            
            noise_columns = get_noise_columns(df)
            if '측정 시간' in df.columns:
                df['측정 시간'] = pd.to_datetime(df['측정 시간'])
                df['시간'] = df['측정 시간'].dt.hour
                
                for col in noise_columns:
                    hourly_noise = df.groupby('시간')[col].mean()
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    hourly_noise.plot(kind='line', marker='o')
                    plt.title(f'{col} 시간대별 평균')
                    plt.xlabel('시간')
                    plt.ylabel('데시벨 (dB)')
                    st.pyplot(fig)
                    plt.close()

        # 원본 데이터 탭
        with tab5:
            st.header("원본 데이터")
            
            # 필터링을 위한 변수 초기화
            selected_regions = []
            selected_schools = []
            date_range = None
            noise_threshold = (30, 80)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if '어느 지역에 거주하나요?' in df.columns:
                    selected_regions = st.multiselect(
                        "지역 선택",
                        options=df['어느 지역에 거주하나요?'].unique(),
                        default=[]
                    )
                
                if '측정 시간' in df.columns:
                    df['측정 시간'] = pd.to_datetime(df['측정 시간'])
                    date_range = st.date_input(
                        "날짜 범위 선택",
                        value=(df['측정 시간'].min(), df['측정 시간'].max())
                    )
            
            with col2:
                if '현재 학교급' in df.columns:
                    selected_schools = st.multiselect(
                        "학교급 선택",
                        options=df['현재 학교급'].unique(),
                        default=[]
                    )
                
                noise_columns = get_noise_columns(df)
                if noise_columns:
                    noise_threshold = st.slider(
                        "소음 레벨 필터 (dB)",
                        min_value=0,
                        max_value=100,
                        value=(30, 80)
                    )
            
            # 데이터 필터링
            filtered_df = df.copy()
            
            if selected_regions:
                filtered_df = filtered_df[filtered_df['어느 지역에 거주하나요?'].isin(selected_regions)]
            
            if selected_schools:
                filtered_df = filtered_df[filtered_df['현재 학교급'].isin(selected_schools)]
            
            if '측정 시간' in df.columns and date_range is not None:
                filtered_df = filtered_df[
                    (filtered_df['측정 시간'].dt.date >= date_range[0]) &
                    (filtered_df['측정 시간'].dt.date <= date_range[1])
                ]
            
            if noise_columns:
                for col in noise_columns:
                    try:
                        numeric_data = pd.to_numeric(filtered_df[col], errors='coerce')
                        filtered_df = filtered_df[
                            (numeric_data >= noise_threshold[0]) &
                            (numeric_data <= noise_threshold[1])
                        ]
                    except:
                        continue
            
            st.dataframe(filtered_df)
            
            csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 분석 데이터 다운로드",
                data=csv,
                file_name="noise_analysis_results.csv",
                mime="text/csv"
            )

        # 분석 방법론 탭
        with tab6:
            st.header("📊 데이터 분석 방법론")
            
            st.markdown("""
            ### 1. 데이터 전처리
            - CSV 파일 로딩 및 인코딩 처리
            - 결측치 처리
            - 데이터 타입 변환
            
            ### 2. 기술 통계 분석
            - 응답자 수 집계
            - 학교급별, 지역별 분포 분석
            - 집중력 저하 경험 비율 계산
            
            ### 3. 소음 분석
            - 장소별 소음 레벨 분포
            - 주요 소음 유형 분석
            - 시간대별 소음 패턴
            
            ### 4. 상관관계 분석
            - 장소별 소음 레벨 상관관계
            - 소음과 건강 증상의 관계
            - 통계적 유의성 검정
            
            ### 5. 시계열 분석
            - 시간대별 소음 패턴
            - 추세 분석
            """)

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {str(e)}")
        st.write("CSV 파일의 형식을 확인해주세요.")

else:
    st.info("👈 사이드바에서 CSV 파일을 업로드해주세요.")
    
    with st.expander("📝 필요한 데이터 형식 안내"):
        st.write("""
        CSV 파일은 다음과 같은 열을 포함해야 합니다:
        
        1. 기본 정보
           - 현재 학교급
           - 어느 지역에 거주하나요?
           
        2. 소음 경험
           - 학교에서 집중력 저하를 경험한 적이 있나요?
           - 학교 및 집 주변에서 소음이 심하다고 느낀 적이 있나요?
           - 집중력을 방해하는 주된 소음 유형은 무엇인가요?
           
        3. 소음 측정
           - [장소명] (예: 교실, 도서관 등)
           - 측정 시간
           
        4. 건강 영향
           - 소음이 심한 환경에서 다음과 같은 증상을 경험한 적이 있나요?
        """)
