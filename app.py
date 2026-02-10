import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import requests
import io

# =============================================================================
# 0. 페이지 설정 & 보안
# =============================================================================
st.set_page_config(page_title="범우켐 통합분석", layout="wide")

# ★★★ 다크모드 강제 적용 CSS ★★★
st.markdown("""
<style>
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    /* ★★★ 전체 다크모드 강제 적용 ★★★ */
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    
    /* 전체 배경 다크모드 */
    .stApp {
        background-color: #0e1117 !important;
        color: #fafafa !important;
    }
    
    /* 사이드바 다크모드 */
    [data-testid="stSidebar"] {
        background-color: #262730 !important;
    }
    [data-testid="stSidebar"] * {
        color: #fafafa !important;
    }
    
    /* 메인 컨텐츠 다크모드 */
    .main .block-container {
        background-color: #0e1117 !important;
    }
    
    /* 텍스트 색상 */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #fafafa !important;
    }
    
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    /* ★★★ 입력 필드: 흰배경 + 검정글씨 + 빨간테두리 (통합검색처럼) ★★★ */
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    
    /* ★★★ 셀렉트박스 (연도, 월 선택 등) - 선택값 보이게 ★★★ */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #ff4b4b !important;
        border-radius: 5px !important;
    }
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stSelectbox [data-baseweb="select"] span {
        color: #000000 !important;
    }
    .stSelectbox [data-baseweb="select"] div[data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }
    /* 선택된 값 텍스트 */
    .stSelectbox [data-baseweb="select"] [data-testid="stWidgetLabel"] {
        color: #000000 !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        color: #000000 !important;
    }
    .stSelectbox div[data-baseweb="select"] > div > div {
        color: #000000 !important;
    }
    .stSelectbox svg {
        fill: #000000 !important;
        color: #000000 !important;
    }
    /* 셀렉트박스 내부 모든 텍스트 검정색 */
    .stSelectbox * {
        color: #000000 !important;
    }
    .stSelectbox > label {
        color: #fafafa !important;
    }
    
    /* ★★★ 멀티셀렉트 (거래처, 품목, 담당자 검색) ★★★ */
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        border: 2px solid #ff4b4b !important;
        border-radius: 5px !important;
    }
    .stMultiSelect > div > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stMultiSelect > div > div > div > div {
        color: #000000 !important;
    }
    .stMultiSelect svg {
        fill: #000000 !important;
        color: #000000 !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
    }
    .stMultiSelect input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .stMultiSelect [data-baseweb="icon"] {
        color: #000000 !important;
    }
    .stMultiSelect span {
        color: #000000 !important;
    }
    .stMultiSelect > label {
        color: #fafafa !important;
    }
    
    /* ★★★ 드롭다운 목록 (팝업 메뉴) ★★★ */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    [data-baseweb="popover"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-baseweb="popover"] li:hover {
        background-color: #ffe0e0 !important;
    }
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    [data-baseweb="menu"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-baseweb="menu"] li:hover {
        background-color: #ffe0e0 !important;
    }
    [role="listbox"] {
        background-color: #ffffff !important;
    }
    [role="listbox"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [role="option"]:hover {
        background-color: #ffe0e0 !important;
    }
    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* ★★★ 일반 입력 필드 ★★★ */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ff4b4b !important;
        border-radius: 5px !important;
    }
    
    /* ★★★ 다운로드 버튼 - 파란색으로 눈에 띄게 ★★★ */
    .stDownloadButton > button {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
        border: 2px solid #1f77b4 !important;
        font-weight: bold !important;
    }
    .stDownloadButton > button:hover {
        background-color: #1565c0 !important;
        border: 2px solid #1565c0 !important;
    }
    
    /* ★★★ 일반 버튼 ★★★ */
    .stButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #4a4a4a !important;
    }
    
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    /* ★★★ 탭/표/필터 - 다크모드 강제 ★★★ */
    /* ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ */
    
    /* 탭 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #fafafa !important;
        background-color: #262730 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #0e1117 !important;
    }
    
    /* ★★★ 표/데이터프레임은 Streamlit 기본 테마 사용 ★★★ */
    /* (다크모드 → 다크표, 라이트모드 → 라이트표) */
    
    /* ★★★ 정보/경고/성공 박스 - 다크모드 강제 ★★★ */
    .stAlert {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    [data-testid="stAlert"] {
        background-color: #262730 !important;
    }
    .stAlert > div {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    /* info 박스 */
    .stAlert[data-baseweb="notification"] {
        background-color: #262730 !important;
    }
    div[data-testid="stNotification"] {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    
    /* ★★★ 메트릭 카드 - 다크모드 강제 ★★★ */
    [data-testid="metric-container"] {
        background-color: #262730 !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
    [data-testid="metric-container"] * {
        color: #fafafa !important;
    }
    [data-testid="stMetricValue"] {
        color: #fafafa !important;
    }
    [data-testid="stMetricDelta"] {
        color: #fafafa !important;
    }
    
    /* 라디오 버튼 */
    .stRadio > div {
        background-color: transparent !important;
    }
    
    /* 익스팬더 */
    .streamlit-expanderHeader {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    [data-testid="stExpander"] {
        background-color: #262730 !important;
        border: 1px solid #4a4a4a !important;
    }
    [data-testid="stExpander"] > div {
        background-color: #262730 !important;
    }
    
    /* ★★★ 컬럼/컨테이너 배경 - 검정줄 방지 ★★★ */
    [data-testid="column"] {
        background-color: transparent !important;
    }
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }
    [data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
    }
    
    /* 구분선 - 검정줄 방지 */
    hr {
        border: none !important;
        border-top: 1px solid #4a4a4a !important;
        background-color: transparent !important;
        height: 1px !important;
    }
    
    /* ★★★ 링크 색상 - 항상 보이게 ★★★ */
    a {
        color: #4da6ff !important;
    }
    a:hover {
        color: #80bdff !important;
    }
    
    /* ★★★ 마크다운 텍스트 ★★★ */
    .stMarkdown {
        color: #fafafa !important;
    }
    .stMarkdown * {
        color: #fafafa !important;
    }
    
    /* ★★★ 캡션 ★★★ */
    .stCaption {
        color: #fafafa !important;
    }
    
    /* ★★★ 인쇄/PDF 전용 CSS ★★★ */
    @media print {
        /* 전체 배경 흰색 */
        .stApp, .main, .block-container, [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"], .element-container {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        body, html {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* ★★★ 검정줄 방지 - 컨테이너 배경 ★★★ */
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="column"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* ★★★ 구분선 검정줄 방지 ★★★ */
        hr {
            border: none !important;
            border-top: 1px solid #cccccc !important;
            background-color: transparent !important;
            background: transparent !important;
            height: 1px !important;
        }
        
        /* 모든 텍스트 검정색 */
        h1, h2, h3, h4, h5, h6, p, span, label, div, td, th, li, a, strong, b {
            color: #000000 !important;
        }
        
        /* ★★★ Streamlit 컬러 문법 PDF 출력 지원 ★★★ */
        span[style*="color: red"], span[style*="color:red"] {
            color: red !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        span[style*="color: blue"], span[style*="color:blue"] {
            color: blue !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* 사이드바 숨김 */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* 섹션별 페이지 나눔 */
        .print-page-break {
            page-break-before: always !important;
            break-before: page !important;
        }
        
        /* 데이터프레임/테이블 */
        .stDataFrame, [data-testid="stDataFrame"], 
        [data-testid="stTable"], table {
            background-color: #ffffff !important;
            border: 1px solid #333333 !important;
        }
        
        table td, table th, .stDataFrame td, .stDataFrame th,
        [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
            padding: 8px !important;
        }
        
        table thead th, .stDataFrame thead th {
            background-color: #f0f0f0 !important;
            color: #000000 !important;
            font-weight: bold !important;
        }
        
        /* 메트릭 컨테이너 */
        [data-testid="metric-container"] {
            background-color: #f8f9fa !important;
            border: 1px solid #dee2e6 !important;
        }
        [data-testid="metric-container"] * {
            color: #000000 !important;
        }
        
        /* 알림/정보 박스 */
        .stAlert, [data-testid="stAlert"] {
            background-color: #f8f9fa !important;
            border: 1px solid #dee2e6 !important;
            color: #000000 !important;
        }
        
        /* Plotly 차트 */
        .js-plotly-plot, .plot-container, .plotly,
        [data-testid="stPlotlyChart"] {
            background-color: #ffffff !important;
        }
        
        .js-plotly-plot text, .plotly text,
        .legend text, .gtitle, .xtitle, .ytitle,
        .xtick text, .ytick text {
            fill: #000000 !important;
            color: #000000 !important;
        }
        
        svg text, svg tspan {
            fill: #000000 !important;
        }
        
        .legend, .legendtext {
            fill: #000000 !important;
        }
        
        /* 탭 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f0f0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: #ffffff !important;
        }
        
        /* 버튼 */
        .stButton > button, .stDownloadButton > button {
            background-color: #f0f0f0 !important;
            color: #000000 !important;
            border: 1px solid #333333 !important;
        }
        
        .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        
        .streamlit-expanderHeader {
            background-color: #f0f0f0 !important;
            color: #000000 !important;
        }
        
        .stMarkdown, .stMarkdown p, .stMarkdown span,
        .stMarkdown div, .stMarkdown li {
            color: #000000 !important;
        }
        
        .gridlayer line, .zerolinelayer line {
            stroke: #cccccc !important;
        }
        
        .bars text, .bar text {
            fill: #000000 !important;
        }
        
        /* Tab B 배너 색상 보존 */
        div[style*="background-color: #2D3748"] {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    
    st.warning("🔒 관계자 외 접속을 제한합니다.")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    # secrets에서 비밀번호 읽기
    correct_password = st.secrets["password"]
    
    if password == correct_password:
        st.session_state["password_correct"] = True
        st.rerun()
    elif password:
        st.error("비밀번호가 틀렸습니다.")
    return False

if not check_password():
    st.stop()

# =============================================================================
# ★★★ Google Drive에서 CSV 파일 로드 ★★★
# =============================================================================
@st.cache_data(ttl=300, show_spinner=False)  # 5분 캐시
def load_csv_from_gdrive(file_id):
    """Google Drive에서 CSV 파일 다운로드"""
    if not file_id:
        return None
    try:
        url = f"https://drive.google.com/uc?id={file_id}&export=download"
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"파일 로드 실패 (ID: {file_id}): {e}")
        return None

# =============================================================================
# 1. 데이터 로드 함수 (캐시 적용)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_erp_data(uploaded_file_content, filename):
    """ERP 마감 데이터 로드 (2025년, 2024년 마감.csv) - 캐시 적용"""
    if uploaded_file_content is None:
        return pd.DataFrame()
    
    try:
        import io
        # 인코딩 시도
        try:
            df = pd.read_csv(io.BytesIO(uploaded_file_content), header=1, encoding='utf-8', thousands=',')
        except:
            df = pd.read_csv(io.BytesIO(uploaded_file_content), header=1, encoding='cp949', thousands=',')
        
        # 빈 값 처리
        df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
        
        # 일자 파싱
        if '일자' in df.columns:
            df['일자'] = df['일자'].astype(str).str.strip()
            df['일자_dt'] = pd.to_datetime(df['일자'], errors='coerce', dayfirst=False)
            df.dropna(subset=['일자_dt'], inplace=True)
            df['연도'] = df['일자_dt'].dt.year
            df['월'] = df['일자_dt'].dt.month.astype(int)
        
        # 숫자 컬럼 처리
        numeric_cols = ['수량', '공급가액', '입고단가', '단가']
        for col in numeric_cols:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace(',', ''), 
                        errors='coerce'
                    ).fillna(0)
                else:
                    df[col] = df[col].fillna(0)
        
        # 문자열 컬럼 정리
        str_cols = ['거래처명', '품목명', '담당자명', '구분', '단위', '매입처']
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # 단위 표준화
        if '단위' in df.columns:
            df['단위'] = df['단위'].fillna("").str.upper().str.replace(" ", "")
            df['단위'] = df['단위'].replace("NAN", "")
        
        # 드럼 환산 수량 계산
        def calc_drum_qty(row):
            unit = str(row.get('단위', ''))
            qty = row.get('수량', 0)
            
            # D/C 항목은 수량에서 제외 (금액만 반영)
            item_name = str(row.get('품목명', ''))
            if 'D/C' in item_name or 'd/c' in item_name.lower():
                return 0.0
            
            if 'D/M' in unit or 'DRUM' in unit or 'DM' in unit:
                return qty * 1.0
            elif 'P/L' in unit or 'PAIL' in unit or 'PL' in unit:
                return qty * 0.1
            else:
                return 0.0  # E/A 등은 드럼 환산에서 제외
        
        df['수량_드럼'] = df.apply(calc_drum_qty, axis=1)
        
        # 매입금액 계산 (입고단가 × 수량)
        if '입고단가' in df.columns and '수량' in df.columns:
            df['매입금액'] = df['입고단가'] * df['수량']
        else:
            df['매입금액'] = 0
        
        return df
    
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return pd.DataFrame()


def load_plan_data(file_content):
    """사업계획서 데이터 로드 (content 기반)"""
    if file_content is None:
        return pd.DataFrame()
    
    try:
        try:
            df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8', thousands=',')
        except:
            df = pd.read_csv(io.BytesIO(file_content), encoding='cp949', thousands=',')
        
        df.columns = df.columns.str.strip()
        
        # 컬럼명 공백 제거 및 표준화
        df.columns = [col.strip() for col in df.columns]
        
        # 숫자 컬럼 처리
        for col in df.columns:
            if '수량' in col or '매출' in col or '매입' in col:
                if df[col].dtype == object:
                    # '-' 값을 0으로 처리
                    df[col] = df[col].astype(str).str.replace(',', '').str.replace('-', '0').str.strip()
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = df[col].fillna(0)
        
        # 단위 표준화
        if '단위' in df.columns:
            df['단위'] = df['단위'].fillna("").astype(str).str.strip().str.upper()
        
        # 문자열 컬럼 정리
        str_cols = ['거래처명', '품목명', '담당자명', '구분', '매입처']
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    except Exception as e:
        st.error(f"계획 데이터 로드 오류: {e}")
        return pd.DataFrame()


# =============================================================================
# 2. 사이드바 설정
# =============================================================================

# 타이틀과 PDF 다운로드 버튼을 같은 행에 배치
title_col, pdf_col = st.columns([4, 1])
with title_col:
    st.title("범우켐 통합분석")
with pdf_col:
    # PDF 다운로드 placeholder (데이터 로드 후 채움)
    pdf_placeholder = st.empty()

# ★★★ 메인 탭 구조: A (KPI 대시보드) / B (확장 분석) ★★★
main_tab_a, main_tab_b = st.tabs(["📊 A. KPI 대시보드 (계획/금년/전년)", "📈 B. 시계열 확장분석"])

with st.sidebar:
    st.header("⚙️ 조회 설정")
    
    # 1. 통합 조회 기간 설정
    st.subheader("1. 통합 조회 기간 설정")
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # 연도 선택 - 좌측: 비교년도(전년), 우측: 금년도
    col_year1, col_year2 = st.columns(2)
    with col_year1:
        # 비교년도
        prev_year = st.selectbox(
            "비교년도", 
            range(2019, 2070), 
            index=5,  # 2024년 기본
            key="prev_year"
        )
    with col_year2:
        # 금년도
        base_year = st.selectbox(
            "금년도", 
            range(2020, 2071), 
            index=5,  # 2025년 기본
            key="base_year"
        )
    
    # 월 범위 선택
    col_start, col_end = st.columns(2)
    with col_start:
        start_month = st.selectbox("시작 월", range(1, 13), index=0, key="start_month")
    with col_end:
        end_month = st.selectbox("종료 월", range(1, 13), index=11, key="end_month")
    
    # 연도 설정 (내부적으로 사용)
    start_year = base_year
    end_year = base_year
    
    # 기간 유효성 검사
    if start_month > end_month:
        st.error("⚠️ 시작 월이 종료 월보다 늦습니다!")
    
    st.markdown("---")
    
    # 2. 통합 검색 (다중 선택)
    st.subheader("2. 통합 검색")
    
    # 세션 상태 초기화
    if 'all_clients' not in st.session_state:
        st.session_state['all_clients'] = []
    if 'all_items' not in st.session_state:
        st.session_state['all_items'] = []
    if 'all_managers' not in st.session_state:
        st.session_state['all_managers'] = []
    
    # 거래처 다중 선택
    client_options = st.session_state.get('all_clients', [])
    search_clients = st.multiselect(
        "거래처명 검색 (다중 선택)",
        options=client_options,
        default=[],
        placeholder="전체 (거래처 선택...)",
        key="search_clients"
    )
    
    # 품목 다중 선택
    item_options = st.session_state.get('all_items', [])
    search_items = st.multiselect(
        "품목명 검색 (다중 선택)", 
        options=item_options,
        default=[],
        placeholder="전체 (품목 선택...)",
        key="search_items"
    )
    
    # 담당자 다중 선택
    manager_options = st.session_state.get('all_managers', [])
    search_managers = st.multiselect(
        "담당자 선택 (다중 선택)",
        options=manager_options,
        default=[],
        placeholder="전체 (담당자 선택...)",
        key="search_managers"
    )
    
    st.markdown("---")
    
    # 3. 판매 채널 구분
    st.subheader("3. 판매 채널 구분")
    channel_option = st.radio(
        "채널 선택",
        ["전체 보기", "직접 판매", "간접 판매"],
        index=0
    )
    
    st.markdown("---")
    
    # ★★★ Google Drive 연동 (Secrets에서 자동 로드) ★★★
    st.subheader("📂 Google Drive 연동")
    
    # Secrets에서 파일 ID 가져오기
    gdrive_config = st.secrets.get("gdrive", {})
    
    file_id_plan = gdrive_config.get("plan_2026", "")
    file_id_current = gdrive_config.get("sales_2026", "")
    file_id_previous = gdrive_config.get("sales_2025", "")
    file_id_year_2 = gdrive_config.get("sales_2024", "")
    file_id_year_3 = gdrive_config.get("sales_2023", "")
    file_id_year_4 = gdrive_config.get("sales_2022", "")
    file_id_year_5 = gdrive_config.get("sales_2021", "")
    file_id_year_6 = gdrive_config.get("sales_2020", "")
    
    if file_id_plan and file_id_current and file_id_previous:
        st.success("✅ Secrets에서 파일 ID 로드 완료")
    else:
        st.warning("⚠️ Secrets에 파일 ID가 없습니다. 수동 입력하세요.")
        file_id_plan = st.text_input("사업계획서 ID", value="", key="manual_plan")
        file_id_current = st.text_input("금년 실적 ID", value="", key="manual_current")
        file_id_previous = st.text_input("전년 실적 ID", value="", key="manual_previous")
        
        with st.expander("📁 과거 시계열 데이터 ID", expanded=False):
            file_id_year_2 = st.text_input("2년전 ID", value="", key="manual_y2")
            file_id_year_3 = st.text_input("3년전 ID", value="", key="manual_y3")
            file_id_year_4 = st.text_input("4년전 ID", value="", key="manual_y4")
            file_id_year_5 = st.text_input("5년전 ID", value="", key="manual_y5")
            file_id_year_6 = st.text_input("6년전 ID", value="", key="manual_y6")


# =============================================================================
# 3. 메인 대시보드
# =============================================================================
has_required_ids = file_id_plan and file_id_current and file_id_previous

if has_required_ids:
    # Google Drive에서 데이터 로드
    with st.spinner("📊 Google Drive에서 데이터 로드 중..."):
        content_plan = load_csv_from_gdrive(file_id_plan)
        content_current = load_csv_from_gdrive(file_id_current)
        content_previous = load_csv_from_gdrive(file_id_previous)
        content_year_2 = load_csv_from_gdrive(file_id_year_2) if file_id_year_2 else None
        content_year_3 = load_csv_from_gdrive(file_id_year_3) if file_id_year_3 else None
        content_year_4 = load_csv_from_gdrive(file_id_year_4) if file_id_year_4 else None
        content_year_5 = load_csv_from_gdrive(file_id_year_5) if file_id_year_5 else None
        content_year_6 = load_csv_from_gdrive(file_id_year_6) if file_id_year_6 else None
    
    # 데이터 로드 확인
    if not content_plan or not content_current or not content_previous:
        st.error("❌ 필수 데이터 로드 실패. 파일 ID와 공유 설정을 확인해주세요.")
        st.stop()
    
    # 데이터 로드 (Google Drive content에서)
    df_plan = load_plan_data(content_plan)
    df_current = load_erp_data(content_current, "current.csv")
    df_previous = load_erp_data(content_previous, "previous.csv")
    
    # 과거 시계열 데이터 로드
    df_year_2 = load_erp_data(content_year_2, "year_2.csv") if content_year_2 else pd.DataFrame()
    df_year_3 = load_erp_data(content_year_3, "year_3.csv") if content_year_3 else pd.DataFrame()
    df_year_4 = load_erp_data(content_year_4, "year_4.csv") if content_year_4 else pd.DataFrame()
    df_year_5 = load_erp_data(content_year_5, "year_5.csv") if content_year_5 else pd.DataFrame()
    df_year_6 = load_erp_data(content_year_6, "year_6.csv") if content_year_6 else pd.DataFrame()
    df_year_7 = pd.DataFrame()  # 7년전 데이터는 없음
    
    # 거래처/품목/담당자 목록 업데이트 (자동완성용) - 과거 시계열 데이터 포함
    all_clients = set()
    all_items = set()
    all_managers = set()
    
    # 기본 데이터 + 과거 시계열 데이터 모두 포함
    all_dfs_for_search = [df_current, df_previous, df_plan, df_year_2, df_year_3, df_year_4, df_year_5, df_year_6, df_year_7]
    
    for df in all_dfs_for_search:
        if df is not None and not df.empty:
            if '거래처명' in df.columns:
                all_clients.update(df['거래처명'].dropna().unique())
            if '품목명' in df.columns:
                all_items.update(df['품목명'].dropna().unique())
            if '담당자명' in df.columns:
                all_managers.update(df['담당자명'].dropna().unique())
    
    # 새 목록 생성
    new_clients = sorted([c for c in all_clients if c and c != 'nan'])
    new_items = sorted([i for i in all_items if i and i != 'nan'])
    new_managers = sorted([m for m in all_managers if m and m != 'nan'])
    
    # 목록이 변경되었는지 확인 후 업데이트
    needs_rerun = False
    if st.session_state.get('all_clients', []) != new_clients:
        st.session_state['all_clients'] = new_clients
        needs_rerun = True
    if st.session_state.get('all_items', []) != new_items:
        st.session_state['all_items'] = new_items
        needs_rerun = True
    if st.session_state.get('all_managers', []) != new_managers:
        st.session_state['all_managers'] = new_managers
        needs_rerun = True
    
    # 처음 로드 시 rerun하여 필터 옵션 업데이트
    if needs_rerun and 'data_loaded' not in st.session_state:
        st.session_state['data_loaded'] = True
        st.rerun()
    
    # 필터링 함수
    def apply_filters(df):
        """공통 필터 적용"""
        filtered = df.copy()
        
        # 채널 필터
        if channel_option == "직접 판매" and '구분' in filtered.columns:
            filtered = filtered[filtered['구분'] == '직접']
        elif channel_option == "간접 판매" and '구분' in filtered.columns:
            filtered = filtered[filtered['구분'] == '간접']
        
        # 거래처 검색 (다중 선택 - 리스트가 비어있지 않을 때만 필터)
        if search_clients and len(search_clients) > 0 and '거래처명' in filtered.columns:
            filtered = filtered[filtered['거래처명'].isin(search_clients)]
        
        # 품목 검색 (다중 선택)
        if search_items and len(search_items) > 0 and '품목명' in filtered.columns:
            filtered = filtered[filtered['품목명'].isin(search_items)]
        
        # 담당자 검색 (다중 선택)
        if search_managers and len(search_managers) > 0 and '담당자명' in filtered.columns:
            filtered = filtered[filtered['담당자명'].isin(search_managers)]
        
        return filtered
    
    # 필터 적용
    df_current_filtered = apply_filters(df_current)
    df_previous_filtered = apply_filters(df_previous)
    df_plan_filtered = apply_filters(df_plan)
    
    # 기간 필터링 함수
    def filter_by_period(df, start_y, start_m, end_y, end_m):
        """지정 기간으로 필터링"""
        if df.empty or '연도' not in df.columns:
            return df
        
        mask = (
            (df['연도'] * 100 + df['월']) >= (start_y * 100 + start_m)
        ) & (
            (df['연도'] * 100 + df['월']) <= (end_y * 100 + end_m)
        )
        return df[mask]
    
    # 선택 기간 데이터
    df_period = filter_by_period(df_current_filtered, start_year, start_month, end_year, end_month)
    df_period_prev = filter_by_period(df_previous_filtered, start_year - 1, start_month, start_year - 1, end_month)
    
    # ★★★ 금년 데이터의 실제 최대 월 확인 ★★★
    if not df_current_filtered.empty and '월' in df_current_filtered.columns:
        max_month_in_current = int(df_current_filtered['월'].max())
    else:
        max_month_in_current = end_month
    
    # 연간 누적 데이터 (금년: 1월 ~ 금년 데이터의 최대 월)
    df_ytd = filter_by_period(df_current_filtered, base_year, 1, base_year, max_month_in_current)
    df_ytd_prev = filter_by_period(df_previous_filtered, prev_year, 1, prev_year, max_month_in_current)
    
    # 금년 데이터의 실제 가용 월 확인
    if not df_current_filtered.empty and '월' in df_current_filtered.columns:
        available_months_current = sorted(df_current_filtered['월'].unique())
        max_available_month = max(available_months_current) if available_months_current else 0
        
        # 경고는 상단에서 표시하므로 여기서는 생략
    
    # 전년 데이터의 실제 가용 월 확인
    if not df_previous_filtered.empty and '월' in df_previous_filtered.columns:
        available_months_prev = sorted(df_previous_filtered['월'].unique())
        max_available_month_prev = max(available_months_prev) if available_months_prev else 0
    
    # 계획 데이터 집계 함수
    def get_plan_for_months(df_plan, months, data_type='sales'):
        """특정 월들의 계획 합계"""
        if df_plan.empty:
            return 0
        
        total = 0
        for m in months:
            if data_type == 'sales':
                # 컬럼명 변형 체크 (공백 포함 가능)
                possible_cols = [f'{m}월 매출', f'{m}월매출']
                for col in df_plan.columns:
                    col_clean = col.strip()
                    if col_clean == f'{m}월 매출' or col_clean == f'{m}월매출':
                        val = pd.to_numeric(df_plan[col].astype(str).str.replace(',', '').str.replace('-', '0'), errors='coerce').fillna(0).sum()
                        total += val
                        break
            else:  # qty - 드럼 환산 수량
                # 수량(d) 컬럼 우선 사용
                found = False
                for col in df_plan.columns:
                    col_clean = col.strip()
                    if col_clean == f'{m}월 수량(d)':
                        val = pd.to_numeric(df_plan[col].astype(str).str.replace(',', '').str.replace('-', '0'), errors='coerce').fillna(0).sum()
                        total += val
                        found = True
                        break
                
                # 수량(d)가 없으면 일반 수량 컬럼 사용
                if not found:
                    for col in df_plan.columns:
                        col_clean = col.strip()
                        if col_clean == f'{m}월 수량':
                            val = pd.to_numeric(df_plan[col].astype(str).str.replace(',', '').str.replace('-', '0'), errors='coerce').fillna(0).sum()
                            total += val
                            break
        
        return total
    
    # 선택 기간 월 리스트
    period_months = []
    for y in range(start_year, end_year + 1):
        for m in range(1, 13):
            if y == start_year and m < start_month:
                continue
            if y == end_year and m > end_month:
                continue
            if y == start_year or y == end_year:
                period_months.append(m)
    
    # ★★★ 금년 누적 월 리스트 (금년 데이터의 최대 월까지) ★★★
    ytd_months = list(range(1, max_month_in_current + 1))
    
    # ★★★ 메인 탭 A 컨텐츠 시작 ★★★
    with main_tab_a:
    
        # ★★★ 경고문구 상단 표시 ★★★
        if not df_current_filtered.empty and '월' in df_current_filtered.columns:
            available_months_current_check = sorted(df_current_filtered['월'].unique())
            max_available_month_check = max(available_months_current_check) if available_months_current_check else 0
            if end_month > max_available_month_check and max_available_month_check > 0:
                st.warning(f"⚠️ 금년({base_year}년) 실적 데이터에서 선택한 항목은 **{max_available_month_check}월**까지만 있습니다. 선택한 기간({start_month}~{end_month}월) 중 가용 데이터만 표시됩니다.")
        
        # ★★★ 조회기간 안내 문구 ★★★
        st.info(f"🔍 **조회기간 안내:** KPI 대시보드는 계획/금년/전년 데이터만 비교분석합니다. 좌측 사이드바에서 조회기간을 먼저 확인해주세요.")
    
        # =========================================================================
        # SECTION A: KPI 전사 요약 (Executive Summary)
        # =========================================================================
        st.markdown("---")
        st.subheader("📊 SECTION A : KPI 전사 요약 (Executive Summary)")
        
        # 현재 조회 기준 표시 - 사용자 선택 기간 기준
        # 전년 시작 ~ 금년 종료월 기준
        period_text = f"전년: {prev_year}/{start_month:02d}/01 ~ 금년: {base_year}/{end_month:02d}/{'28' if end_month == 2 else '30' if end_month in [4,6,9,11] else '31'}"
        
        # 필터 정보 구성
        filter_parts = []
        if search_clients and len(search_clients) > 0:
            if len(search_clients) <= 3:
                filter_parts.append(f"거래처: {', '.join(search_clients)}")
            else:
                filter_parts.append(f"거래처: {', '.join(search_clients[:3])} 외 {len(search_clients)-3}개")
        
        if search_items and len(search_items) > 0:
            if len(search_items) <= 2:
                filter_parts.append(f"품목: {', '.join(search_items)}")
            else:
                filter_parts.append(f"품목: {', '.join(search_items[:2])} 외 {len(search_items)-2}개")
        
        if search_managers and len(search_managers) > 0:
            filter_parts.append(f"담당자: {', '.join(search_managers)}")
    
        if channel_option != "전체 보기":
            filter_parts.append(f"채널: {channel_option}")
    
        # 필터 텍스트 생성 - 파란색 글씨
        if filter_parts:
            filter_text = " | ".join(filter_parts)
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span>', unsafe_allow_html=True)
            st.markdown(f"📌 **적용 필터:** {filter_text}")
        else:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span> (전체 데이터)', unsafe_allow_html=True)
    
        # KPI 계산
        # 선택 기간
        period_sales = df_period['공급가액'].sum() if not df_period.empty else 0
        period_qty = df_period['수량_드럼'].sum() if not df_period.empty else 0
        period_sales_prev = df_period_prev['공급가액'].sum() if not df_period_prev.empty else 0
        period_qty_prev = df_period_prev['수량_드럼'].sum() if not df_period_prev.empty else 0
    
        # 선택 기간 계획
        period_plan_sales = get_plan_for_months(df_plan_filtered, period_months, 'sales')
        period_plan_qty = get_plan_for_months(df_plan_filtered, period_months, 'qty')
    
        # 연간 누적
        ytd_sales = df_ytd['공급가액'].sum() if not df_ytd.empty else 0
        ytd_qty = df_ytd['수량_드럼'].sum() if not df_ytd.empty else 0
        ytd_sales_prev = df_ytd_prev['공급가액'].sum() if not df_ytd_prev.empty else 0
        ytd_qty_prev = df_ytd_prev['수량_드럼'].sum() if not df_ytd_prev.empty else 0
    
        # 연간 누적 계획
        ytd_plan_sales = get_plan_for_months(df_plan_filtered, ytd_months, 'sales')
        ytd_plan_qty = get_plan_for_months(df_plan_filtered, ytd_months, 'qty')
    
        # 달성률/동기비 계산 함수
        def calc_rate(actual, target):
            if target and target != 0:
                return (actual / target) * 100
            return 0
    
        # 금액 포맷 함수
        def format_currency(value):
            """억 단위로 포맷 (백만단위까지 정확하게)"""
            if abs(value) >= 100000000:  # 1억 이상
                return f"{value/100000000:,.2f}억 원"
            elif abs(value) >= 10000000:  # 1천만 이상
                return f"{value/100000000:,.2f}억 원"
            elif abs(value) >= 10000:  # 1만 이상
                return f"{value/10000:,.0f}만 원"
            else:
                return f"{value:,.0f}원"
    
        # 레이아웃: 좌측(선택기간) / 우측(연간누적)
        col_left, col_right = st.columns(2)
    
        with col_left:
            st.markdown(f"### 📅 선택 기간 ({start_month}~{end_month}월) 성적표")
        
            # 매출액
            ach_rate_sales = calc_rate(period_sales, period_plan_sales)  # 달성률
            yoy_rate_sales = calc_rate(period_sales, period_sales_prev)  # 동기비 = 실적/전년*100
        
            # 달성률 화살표 (100% 기준)
            ach_diff_sales = ach_rate_sales - 100
            ach_arrow_sales = '▲' if ach_diff_sales >= 0 else '▼'
            ach_color_sales = 'red' if ach_diff_sales >= 0 else 'blue'
        
            # 동기비 화살표 (100% 기준)
            yoy_diff_sales = yoy_rate_sales - 100
            yoy_arrow_sales = '▲' if yoy_diff_sales >= 0 else '▼'
            yoy_color_sales = 'red' if yoy_diff_sales >= 0 else 'blue'
        
            st.markdown(f"### ● 매출액: {format_currency(period_sales)}")
            st.markdown(f'<h4 style="margin:0; padding:0;">&nbsp;&nbsp;&nbsp;달성률 <strong>{ach_rate_sales:.1f}%</strong> <span style="color: {ach_color_sales}; font-weight: bold;">{ach_arrow_sales}{abs(ach_diff_sales):.1f}%</span> / 동기비 <strong>{yoy_rate_sales:.1f}%</strong> <span style="color: {yoy_color_sales}; font-weight: bold;">{yoy_arrow_sales}{abs(yoy_diff_sales):.1f}%</span></h4>', unsafe_allow_html=True)
            st.markdown(f"### &nbsp;&nbsp;&nbsp;└ 계획: {format_currency(period_plan_sales)} / 전년: {format_currency(period_sales_prev)}")
        
            st.markdown("")
        
            # 판매수량
            ach_rate_qty = calc_rate(period_qty, period_plan_qty)
            yoy_rate_qty = calc_rate(period_qty, period_qty_prev)
        
            ach_diff_qty = ach_rate_qty - 100
            ach_arrow_qty = '▲' if ach_diff_qty >= 0 else '▼'
            ach_color_qty = 'red' if ach_diff_qty >= 0 else 'blue'
        
            yoy_diff_qty = yoy_rate_qty - 100
            yoy_arrow_qty = '▲' if yoy_diff_qty >= 0 else '▼'
            yoy_color_qty = 'red' if yoy_diff_qty >= 0 else 'blue'
        
            st.markdown(f"### ● 판매수량: {period_qty:,.1f} D/M")
            st.markdown(f'<h4 style="margin:0; padding:0;">&nbsp;&nbsp;&nbsp;달성률 <strong>{ach_rate_qty:.1f}%</strong> <span style="color: {ach_color_qty}; font-weight: bold;">{ach_arrow_qty}{abs(ach_diff_qty):.1f}%</span> / 동기비 <strong>{yoy_rate_qty:.1f}%</strong> <span style="color: {yoy_color_qty}; font-weight: bold;">{yoy_arrow_qty}{abs(yoy_diff_qty):.1f}%</span></h4>', unsafe_allow_html=True)
            st.markdown(f"### &nbsp;&nbsp;&nbsp;└ 계획: {period_plan_qty:,.1f} D/M / 전년: {period_qty_prev:,.1f} D/M")
    
        with col_right:
            st.markdown(f"### 📊 선택 기간 ({start_month}~{end_month}월) 채널별")
        
            # ★★★ 직접/간접 판매 데이터 계산 ★★★
            # 직접 판매 (금년)
            direct_qty = df_period[df_period['구분'] == '직접']['수량_드럼'].sum() if not df_period.empty and '구분' in df_period.columns else 0
            # 직접 판매 (전년)
            direct_qty_prev = df_period_prev[df_period_prev['구분'] == '직접']['수량_드럼'].sum() if not df_period_prev.empty and '구분' in df_period_prev.columns else 0
            # 직접 판매 (계획)
            direct_plan_qty = get_plan_for_months(df_plan_filtered[df_plan_filtered['구분'] == '직접'] if '구분' in df_plan_filtered.columns else df_plan_filtered, period_months, 'qty') if not df_plan_filtered.empty else 0
            
            # 간접 판매 (금년)
            indirect_qty = df_period[df_period['구분'] == '간접']['수량_드럼'].sum() if not df_period.empty and '구분' in df_period.columns else 0
            # 간접 판매 (전년)
            indirect_qty_prev = df_period_prev[df_period_prev['구분'] == '간접']['수량_드럼'].sum() if not df_period_prev.empty and '구분' in df_period_prev.columns else 0
            # 간접 판매 (계획)
            indirect_plan_qty = get_plan_for_months(df_plan_filtered[df_plan_filtered['구분'] == '간접'] if '구분' in df_plan_filtered.columns else df_plan_filtered, period_months, 'qty') if not df_plan_filtered.empty else 0
            
            # 직접 판매 달성률/동기비
            direct_ach = calc_rate(direct_qty, direct_plan_qty)
            direct_yoy = calc_rate(direct_qty, direct_qty_prev)
            
            direct_ach_diff = direct_ach - 100
            direct_ach_arrow = '▲' if direct_ach_diff >= 0 else '▼'
            direct_ach_color = 'red' if direct_ach_diff >= 0 else 'blue'
            
            direct_yoy_diff = direct_yoy - 100
            direct_yoy_arrow = '▲' if direct_yoy_diff >= 0 else '▼'
            direct_yoy_color = 'red' if direct_yoy_diff >= 0 else 'blue'
        
            st.markdown(f"### ● 직접 판매수량: {direct_qty:,.1f} D/M")
            st.markdown(f'<h4 style="margin:0; padding:0;">&nbsp;&nbsp;&nbsp;달성률 <strong>{direct_ach:.1f}%</strong> <span style="color: {direct_ach_color}; font-weight: bold;">{direct_ach_arrow}{abs(direct_ach_diff):.1f}%</span> / 동기비 <strong>{direct_yoy:.1f}%</strong> <span style="color: {direct_yoy_color}; font-weight: bold;">{direct_yoy_arrow}{abs(direct_yoy_diff):.1f}%</span></h4>', unsafe_allow_html=True)
            st.markdown(f"### &nbsp;&nbsp;&nbsp;└ 계획: {direct_plan_qty:,.1f} D/M / 전년: {direct_qty_prev:,.1f} D/M")
        
            st.markdown("")
        
            # 간접 판매 달성률/동기비
            indirect_ach = calc_rate(indirect_qty, indirect_plan_qty)
            indirect_yoy = calc_rate(indirect_qty, indirect_qty_prev)
            
            indirect_ach_diff = indirect_ach - 100
            indirect_ach_arrow = '▲' if indirect_ach_diff >= 0 else '▼'
            indirect_ach_color = 'red' if indirect_ach_diff >= 0 else 'blue'
            
            indirect_yoy_diff = indirect_yoy - 100
            indirect_yoy_arrow = '▲' if indirect_yoy_diff >= 0 else '▼'
            indirect_yoy_color = 'red' if indirect_yoy_diff >= 0 else 'blue'
        
            st.markdown(f"### ● 간접 판매수량: {indirect_qty:,.1f} D/M")
            st.markdown(f'<h4 style="margin:0; padding:0;">&nbsp;&nbsp;&nbsp;달성률 <strong>{indirect_ach:.1f}%</strong> <span style="color: {indirect_ach_color}; font-weight: bold;">{indirect_ach_arrow}{abs(indirect_ach_diff):.1f}%</span> / 동기비 <strong>{indirect_yoy:.1f}%</strong> <span style="color: {indirect_yoy_color}; font-weight: bold;">{indirect_yoy_arrow}{abs(indirect_yoy_diff):.1f}%</span></h4>', unsafe_allow_html=True)
            st.markdown(f"### &nbsp;&nbsp;&nbsp;└ 계획: {indirect_plan_qty:,.1f} D/M / 전년: {indirect_qty_prev:,.1f} D/M")
    
        st.markdown("---")
    
        # =========================================================================
        # SECTION B: KPI 영업 성과 추세 (Sales Performance - Trend)
        # =========================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.subheader("📈 SECTION B : KPI 영업 성과 (Sales Performance - Trend)")
    
        # 현재 필터 정보 표시 (SECTION A와 동일)
        if filter_parts:
            filter_text = " | ".join(filter_parts)
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span>', unsafe_allow_html=True)
            st.markdown(f"📌 **적용 필터:** {filter_text}")
        else:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span> (전체 데이터)', unsafe_allow_html=True)
    
        # 월별 데이터 집계
        def get_monthly_trend():
            trend_list = []
        
            for m in range(1, 13):
                # 금년 실적
                curr_sales = df_current_filtered[df_current_filtered['월'] == m]['공급가액'].sum() if not df_current_filtered.empty and '월' in df_current_filtered.columns else 0
                curr_qty = df_current_filtered[df_current_filtered['월'] == m]['수량_드럼'].sum() if not df_current_filtered.empty and '월' in df_current_filtered.columns else 0
            
                # 전년 실적
                prev_sales = df_previous_filtered[df_previous_filtered['월'] == m]['공급가액'].sum() if not df_previous_filtered.empty and '월' in df_previous_filtered.columns else 0
                prev_qty = df_previous_filtered[df_previous_filtered['월'] == m]['수량_드럼'].sum() if not df_previous_filtered.empty and '월' in df_previous_filtered.columns else 0
            
                # 계획
                plan_sales = get_plan_for_months(df_plan_filtered, [m], 'sales')
                plan_qty = get_plan_for_months(df_plan_filtered, [m], 'qty')
            
                trend_list.append({
                    '월': f'{m}월',
                    '월_num': m,
                    '실적_매출': curr_sales,
                    '계획_매출': plan_sales,
                    '전년_매출': prev_sales,
                    '실적_수량': curr_qty,
                    '계획_수량': plan_qty,
                    '전년_수량': prev_qty
                })
        
            return pd.DataFrame(trend_list)
    
        trend_df = get_monthly_trend()
    
        # Y축 스케일 자동 결정 함수
        def get_y_axis_config(max_value):
            """매출 규모에 따라 Y축 설정 자동 조정"""
            if max_value <= 10000000:  # 1천만 이하 → 1M 단위
                step = 1000000
            elif max_value <= 100000000:  # 1억 이하 → 10M 단위
                step = 10000000
            elif max_value <= 500000000:  # 5억 이하 → 50M 단위
                step = 50000000
            else:  # 5억 초과 → 100M 단위
                step = 100000000
        
            divider = 1000000
            num_ticks = int(max_value / step) + 2
            tickvals = [i * step for i in range(num_ticks)]
            ticktext = [f'{int(v/divider)}M' for v in tickvals]
        
            return tickvals, ticktext
    
        # 탭: 매출 / 수량
        trend_tab1, trend_tab2 = st.tabs(["💰 매출 추세", "📦 수량 추세"])
    
        with trend_tab1:
            st.markdown(f"**{start_year}년 월별 매출 추세** (단위: 백만원)")
        
            # 최대값 계산
            max_sales = max(
                trend_df['실적_매출'].max(),
                trend_df['계획_매출'].max(),
                trend_df['전년_매출'].max()
            ) * 1.15  # 15% 여유 (텍스트 공간)
        
            tickvals, ticktext = get_y_axis_config(max_sales)
        
            fig_sales = go.Figure()
        
            # 실적 (파란 막대 - 두껍게)
            fig_sales.add_trace(go.Bar(
                x=trend_df['월'],
                y=trend_df['실적_매출'],
                name='실적',
                marker_color='#2E86AB',
                width=0.7,
                text=[f'{v/1000000:.0f}M' for v in trend_df['실적_매출']],
                textposition='outside',
                textfont=dict(size=14, color='white', family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>실적: %{y:,.0f}원<extra></extra>'
            ))
        
            # 계획 (진한 빨간 점선)
            fig_sales.add_trace(go.Scatter(
                x=trend_df['월'],
                y=trend_df['계획_매출'],
                name='계획',
                line=dict(color='#C41E3A', width=4, dash='dot'),
                mode='lines+markers',
                marker=dict(size=10, symbol='circle'),
                hovertemplate='<b>%{x}</b><br>계획: %{y:,.0f}원<extra></extra>'
            ))
        
            # 전년 (진한 회색 실선)
            fig_sales.add_trace(go.Scatter(
                x=trend_df['월'],
                y=trend_df['전년_매출'],
                name='전년',
                line=dict(color='#4A4A4A', width=3),
                mode='lines+markers',
                marker=dict(size=8, symbol='diamond'),
                hovertemplate='<b>%{x}</b><br>전년: %{y:,.0f}원<extra></extra>'
            ))
        
            fig_sales.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text='월', font=dict(size=16, color='white', family='Arial Black')),
                    tickmode='array',
                    tickvals=trend_df['월'],
                    ticktext=[f'{i}월' for i in range(1, 13)],
                    tickfont=dict(size=16, color='white', family='Arial Black'),
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.3)',
                    linecolor='white'
                ),
                yaxis=dict(
                    title=dict(text='매출액', font=dict(size=16, color='white', family='Arial Black')),
                    tickvals=tickvals,
                    ticktext=ticktext,
                    tickfont=dict(size=14, color='white', family='Arial Black'),
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.3)',
                    linecolor='white'
                ),
                legend=dict(
                    orientation='h', 
                    yanchor='bottom', 
                    y=1.02, 
                    xanchor='center', 
                    x=0.5,
                    font=dict(size=20, color='white', family='Arial Black')
                ),
                bargap=0.2,
                hoverlabel=dict(
                    bgcolor='rgba(30,30,30,0.95)',
                    font_size=16,
                    font_family='Arial Black',
                    font_color='white'
                )
            )
        
            st.plotly_chart(fig_sales, use_container_width=True, key='trend_sales_chart')
    
        with trend_tab2:
            st.markdown(f"**{start_year}년 월별 수량 추세** (단위: D/M 환산)")
        
            # 최대값 계산
            max_qty = max(
                trend_df['실적_수량'].max(),
                trend_df['계획_수량'].max(),
                trend_df['전년_수량'].max()
            ) * 1.15
        
            fig_qty = go.Figure()
        
            # 실적 (파란 막대 - 두껍게)
            fig_qty.add_trace(go.Bar(
                x=trend_df['월'],
                y=trend_df['실적_수량'],
                name='실적',
                marker_color='#2E86AB',
                width=0.7,
                text=[f'{v:.0f}' for v in trend_df['실적_수량']],
                textposition='outside',
                textfont=dict(size=14, color='white', family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>실적: %{y:,.1f} D/M<extra></extra>'
            ))
        
            # 계획 (진한 빨간 점선)
            fig_qty.add_trace(go.Scatter(
                x=trend_df['월'],
                y=trend_df['계획_수량'],
                name='계획',
                line=dict(color='#C41E3A', width=4, dash='dot'),
                mode='lines+markers',
                marker=dict(size=10, symbol='circle'),
                hovertemplate='<b>%{x}</b><br>계획: %{y:,.1f} D/M<extra></extra>'
            ))
        
            # 전년 (진한 회색 실선)
            fig_qty.add_trace(go.Scatter(
                x=trend_df['월'],
                y=trend_df['전년_수량'],
                name='전년',
                line=dict(color='#4A4A4A', width=3),
                mode='lines+markers',
                marker=dict(size=8, symbol='diamond'),
                hovertemplate='<b>%{x}</b><br>전년: %{y:,.1f} D/M<extra></extra>'
            ))
        
            fig_qty.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text='월', font=dict(size=16, color='white', family='Arial Black')),
                    tickmode='array',
                    tickvals=trend_df['월'],
                    ticktext=[f'{i}월' for i in range(1, 13)],
                    tickfont=dict(size=16, color='white', family='Arial Black'),
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.3)',
                    linecolor='white'
                ),
                yaxis=dict(
                    title=dict(text='수량 (D/M)', font=dict(size=16, color='white', family='Arial Black')),
                    tickformat=',.0f',
                    tickfont=dict(size=14, color='white', family='Arial Black'),
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.3)',
                    linecolor='white'
                ),
                legend=dict(
                    orientation='h', 
                    yanchor='bottom', 
                    y=1.02, 
                    xanchor='center', 
                    x=0.5,
                    font=dict(size=20, color='white', family='Arial Black')
                ),
                bargap=0.2,
                hoverlabel=dict(
                    bgcolor='rgba(30,30,30,0.95)',
                    font_size=16,
                    font_family='Arial Black',
                    font_color='white'
                )
            )
        
            st.plotly_chart(fig_qty, use_container_width=True, key='trend_qty_chart')
    
        st.markdown("---")
    
        # =========================================================================
        # SECTION B-2: KPI 거래처별 성과지표 (Key Account Status)
        # =========================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.subheader("📊 SECTION B-2 : KPI 거래처별 성과지표 (Key Account Status)")
    
        # 현재 필터 정보 표시
        if filter_parts:
            filter_text = " | ".join(filter_parts)
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span>', unsafe_allow_html=True)
            st.markdown(f"📌 **적용 필터:** {filter_text}")
        else:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span> (전체 데이터)', unsafe_allow_html=True)
    
        # 선택월 데이터 표시
    
        def create_account_analysis_v2(df_act, df_prev, df_plan_data, months_list, is_ytd=False):
            """거래처별 성과 분석 데이터 생성 (연간 기준 포함)"""
        
            # 실적 집계
            if not df_act.empty and '거래처명' in df_act.columns:
                act_by_client = df_act.groupby('거래처명').agg({
                    '공급가액': 'sum',
                    '수량_드럼': 'sum'
                }).reset_index()
                act_by_client.columns = ['거래처명', '실적_금액', '실적_수량']
            else:
                act_by_client = pd.DataFrame(columns=['거래처명', '실적_금액', '실적_수량'])
        
            # 전년 집계 (연간 기준: 1~12월 전체)
            if not df_prev.empty and '거래처명' in df_prev.columns:
                if is_ytd:
                    # 연간누적일 때는 전년 전체 데이터 사용
                    prev_by_client = df_prev.groupby('거래처명').agg({
                        '공급가액': 'sum',
                        '수량_드럼': 'sum'
                    }).reset_index()
                else:
                    prev_by_client = df_prev.groupby('거래처명').agg({
                        '공급가액': 'sum',
                        '수량_드럼': 'sum'
                    }).reset_index()
                prev_by_client.columns = ['거래처명', '전년_금액', '전년_수량']
            else:
                prev_by_client = pd.DataFrame(columns=['거래처명', '전년_금액', '전년_수량'])
        
            # 전년 연간 누적 (미계획 신규 판단용 - 1~12월 전체)
            if not df_previous_filtered.empty and '거래처명' in df_previous_filtered.columns:
                prev_annual = df_previous_filtered.groupby('거래처명').agg({
                    '공급가액': 'sum'
                }).reset_index()
                prev_annual.columns = ['거래처명', '전년_연간']
            else:
                prev_annual = pd.DataFrame(columns=['거래처명', '전년_연간'])
        
            # 계획 집계 (연간 기준: 1~12월 전체)
            plan_annual_by_client = pd.DataFrame(columns=['거래처명', '계획_연간'])
            if not df_plan_data.empty and '거래처명' in df_plan_data.columns:
                plan_annual_list = []
                for _, row in df_plan_data.iterrows():
                    plan_row = {'거래처명': row['거래처명']}
                    # 연간 계획 (1~12월)
                    plan_row['계획_연간'] = sum([
                        float(str(row.get(f'{m}월 매출', 0)).replace(',','').replace('-','0') or 0)
                        for m in range(1, 13) if f'{m}월 매출' in df_plan_data.columns
                    ])
                    plan_annual_list.append(plan_row)
                plan_annual_by_client = pd.DataFrame(plan_annual_list)
                plan_annual_by_client = plan_annual_by_client.groupby('거래처명', as_index=False)['계획_연간'].sum()
        
            # 선택 기간 계획
            if not df_plan_data.empty and '거래처명' in df_plan_data.columns:
                plan_list = []
                for _, row in df_plan_data.iterrows():
                    plan_row = {'거래처명': row['거래처명']}
                    plan_row['계획_금액'] = sum([
                        float(str(row.get(f'{m}월 매출', 0)).replace(',','').replace('-','0') or 0)
                        for m in months_list if f'{m}월 매출' in df_plan_data.columns
                    ])
                    plan_list.append(plan_row)
                plan_by_client = pd.DataFrame(plan_list)
                plan_by_client = plan_by_client.groupby('거래처명', as_index=False)['계획_금액'].sum()
            else:
                plan_by_client = pd.DataFrame(columns=['거래처명', '계획_금액'])
        
            # 병합
            merged = act_by_client.merge(prev_by_client, on='거래처명', how='outer')
            merged = merged.merge(plan_by_client, on='거래처명', how='outer')
            merged = merged.merge(prev_annual, on='거래처명', how='outer')
            merged = merged.merge(plan_annual_by_client, on='거래처명', how='outer')
            merged = merged.fillna(0)
        
            # 차이 계산
            merged['계획대비_금액'] = merged['실적_금액'] - merged['계획_금액']
            merged['전년대비_금액'] = merged['실적_금액'] - merged['전년_금액']
            merged['달성률'] = merged.apply(lambda x: (x['실적_금액']/x['계획_금액']*100) if x['계획_금액'] > 0 else 0, axis=1)
        
            return merged
    
        def draw_b2_charts_v2(data, tab_key):
            """B-2 차트 그리기 (굵은 버전)"""
        
            if data.empty:
                st.warning("데이터가 없습니다.")
                return
        
            col1, col2 = st.columns(2)
        
            # 1. 계획 대비 초과 (Best 10)
            with col1:
                st.markdown("#### 1. 계획 대비 초과 (Best 10)")
                best_plan = data[data['계획대비_금액'] > 0].nlargest(10, '계획대비_금액')
            
                if not best_plan.empty:
                    fig1 = go.Figure(go.Bar(
                        x=best_plan['계획대비_금액'],
                        y=best_plan['거래처명'],
                        orientation='h',
                        marker_color='#2ECC71',
                        width=0.7,
                        text=[f"+{v/10000:,.0f}만 ({r:.0f}%)" for v, r in zip(best_plan['계획대비_금액'], best_plan['달성률'])],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>초과: +%{x:,.0f}원<extra></extra>'
                    ))
                    fig1.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig1, use_container_width=True, key=f'best_plan_{tab_key}')
                else:
                    st.info("계획 초과 달성 거래처가 없습니다.")
        
            # 2. 전년 동기 대비 초과 (Growth 10)
            with col2:
                st.markdown("#### 2. 전년 대비 성장 (Growth 10)")
                best_yoy = data[data['전년대비_금액'] > 0].nlargest(10, '전년대비_금액')
            
                if not best_yoy.empty:
                    fig2 = go.Figure(go.Bar(
                        x=best_yoy['전년대비_금액'],
                        y=best_yoy['거래처명'],
                        orientation='h',
                        marker_color='#3498DB',
                        width=0.7,
                        text=[f"+{v/10000:,.0f}만" for v in best_yoy['전년대비_금액']],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>성장: +%{x:,.0f}원<extra></extra>'
                    ))
                    fig2.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig2, use_container_width=True, key=f'best_yoy_{tab_key}')
                else:
                    st.info("전년 대비 성장 거래처가 없습니다.")
        
            col3, col4 = st.columns(2)
        
            # 3. 계획 대비 미달 (Worst 10)
            with col3:
                st.markdown("#### 3. 계획 대비 미달 (Worst 10)")
                worst_plan = data[data['계획대비_금액'] < 0].nsmallest(10, '계획대비_금액')
            
                if not worst_plan.empty:
                    fig3 = go.Figure(go.Bar(
                        x=worst_plan['계획대비_금액'].abs(),
                        y=worst_plan['거래처명'],
                        orientation='h',
                        marker_color='#E74C3C',
                        width=0.7,
                        text=[f"-{abs(v)/10000:,.0f}만 ({r:.0f}%)" for v, r in zip(worst_plan['계획대비_금액'], worst_plan['달성률'])],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>미달: -%{x:,.0f}원<extra></extra>'
                    ))
                    fig3.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig3, use_container_width=True, key=f'worst_plan_{tab_key}')
                else:
                    st.info("계획 미달 거래처가 없습니다.")
        
            # 4. 전년 동기 대비 하락 (Decline 10)
            with col4:
                st.markdown("#### 4. 전년 대비 하락 (Decline 10)")
                worst_yoy = data[data['전년대비_금액'] < 0].nsmallest(10, '전년대비_금액')
            
                if not worst_yoy.empty:
                    fig4 = go.Figure(go.Bar(
                        x=worst_yoy['전년대비_금액'].abs(),
                        y=worst_yoy['거래처명'],
                        orientation='h',
                        marker_color='#E67E22',
                        width=0.7,
                        text=[f"-{abs(v)/10000:,.0f}만" for v in worst_yoy['전년대비_금액']],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>하락: -%{x:,.0f}원<extra></extra>'
                    ))
                    fig4.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig4, use_container_width=True, key=f'worst_yoy_{tab_key}')
                else:
                    st.info("전년 대비 하락 거래처가 없습니다.")
        
            # 5번과 6번을 나란히 배치
            col5, col6 = st.columns(2)
        
            # 5. 미계획 신규 (Best 10)
            with col5:
                st.markdown("#### 5. 미계획 신규 (Best 10)")
                st.caption("📌 계획 및 전년 실적 없음 / 금년 실적 있음")
            
                # 미계획 신규: 계획=0 AND 전년실적=0 AND 금년 실적 > 0
                new_clients = data[
                    (data['계획_금액'] == 0) & 
                    (data['전년_금액'] == 0) & 
                    (data['실적_금액'] > 0)
                ]
                new_clients = new_clients.nlargest(10, '실적_금액')
            
                if not new_clients.empty:
                    fig5 = go.Figure(go.Bar(
                        x=new_clients['실적_금액'],
                        y=new_clients['거래처명'],
                        orientation='h',
                        marker_color='#9B59B6',
                        width=0.7,
                        text=[f"{v/10000:,.0f}만" for v in new_clients['실적_금액']],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>신규 매출: %{x:,.0f}원<extra></extra>'
                    ))
                    fig5.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig5, use_container_width=True, key=f'new_clients_{tab_key}')
                else:
                    st.info("미계획 신규 거래처가 없습니다.")
        
            # 6. 주의 및 확인 업체 (Worst 10)
            with col6:
                st.markdown("#### 6. 주의 및 확인 업체 (Worst 10)")
                st.caption("📌 계획 AND 전년 실적 있음 / 금년 실적 없음")
            
                # 주의 업체: 계획 > 0 AND 전년실적 > 0 AND 금년 실적 = 0
                caution_clients = data[
                    (data['계획_금액'] > 0) & 
                    (data['전년_금액'] > 0) & 
                    (data['실적_금액'] == 0)
                ].copy()
            
                # 전년 실적 또는 계획 중 큰 값 기준 정렬
                caution_clients['기준_금액'] = caution_clients[['계획_금액', '전년_금액']].max(axis=1)
                caution_clients = caution_clients.nlargest(10, '기준_금액')
            
                if not caution_clients.empty:
                    fig6 = go.Figure(go.Bar(
                        x=caution_clients['기준_금액'],
                        y=caution_clients['거래처명'],
                        orientation='h',
                        marker_color='#E74C3C',
                        width=0.7,
                        text=[f"{v/10000:,.0f}만 (계획/전년)" for v in caution_clients['기준_금액']],
                        textposition='inside',
                        textfont=dict(size=14, color='white', family='Arial Black'),
                        hovertemplate='<b>%{y}</b><br>계획/전년 기준: %{x:,.0f}원<br>⚠️ 금년 실적: 0원<extra></extra>'
                    ))
                    fig6.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(tickfont=dict(size=12, color='white'), showgrid=True, gridcolor='rgba(128,128,128,0.3)'),
                        yaxis=dict(tickfont=dict(size=12, color='white', family='Arial Black'), autorange='reversed'),
                        hoverlabel=dict(bgcolor='rgba(30,30,30,0.95)', font_size=14, font_color='white')
                    )
                    st.plotly_chart(fig6, use_container_width=True, key=f'caution_clients_{tab_key}')
                else:
                    st.info("주의 및 확인 업체가 없습니다.")
    
        # 선택월 데이터만 표시 (금년누적 제거)
        data_monthly = create_account_analysis_v2(df_period, df_period_prev, df_plan_filtered, period_months, is_ytd=False)
        draw_b2_charts_v2(data_monthly, 'monthly')
    
        st.markdown("---")
    
        # =========================================================================
        # SECTION C: KPI 매출분석 (Sales Analysis)
        # =========================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.subheader("📋 SECTION C : KPI 매출분석 (Sales Analysis)")
    
        # 현재 필터 정보 표시 (통합정밀검색 TRACING)
        if filter_parts:
            filter_text = " | ".join(filter_parts)
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span>', unsafe_allow_html=True)
            st.markdown(f"📌 **적용 필터:** {filter_text}")
        else:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span> (전체 데이터)', unsafe_allow_html=True)
    
        # 뷰 모드 - 선택월만 사용 (금년누적 제거)
        is_monthly_view = True
    
        # 단일월 여부 확인
        is_single_month = (start_month == end_month and start_year == end_year)
    
        # ★★★ 메인 탭: KPI / RAW DATA ★★★
        kpi_main_tab, raw_main_tab = st.tabs(["📊 KPI", "📋 RAW DATA"])
    
        # 전월 데이터 준비 (단일월일 때만)
        if is_single_month:
            if start_month == 1:
                prev_month = 12
                prev_month_year = start_year - 1
                df_prev_month = filter_by_period(df_previous_filtered, prev_month_year, prev_month, prev_month_year, prev_month)
            else:
                prev_month = start_month - 1
                prev_month_year = start_year
                df_prev_month = filter_by_period(df_current_filtered, prev_month_year, prev_month, prev_month_year, prev_month)
        else:
            prev_month = None
            prev_month_year = None
            df_prev_month = pd.DataFrame()
    
        def create_analysis_simple(df_act, df_prev, df_prev_month_data, df_plan_data, months_list, group_cols, data_type='qty', include_prev_month=False):
            """
            간결화된 분석 데이터 생성
        
            ★★★ 로직 ★★★
            - qty: 수량_드럼 사용 (P/L*0.1 + D/M*1), 기타 단위 제외
            - sales: 공급가액 사용, 모든 단위 포함 (기타 포함)
            """
        
            df_act_copy = df_act.copy() if not df_act.empty else pd.DataFrame()
            df_prev_copy = df_prev.copy() if not df_prev.empty else pd.DataFrame()
            df_prev_month_copy = df_prev_month_data.copy() if not df_prev_month_data.empty else pd.DataFrame()
            df_plan_copy = df_plan_data.copy() if not df_plan_data.empty else pd.DataFrame()
        
            # 집계 컬럼 결정
            if data_type == 'sales':
                agg_col = '공급가액'
                plan_col_suffix = '매출'
            else:
                # 수량: P/L, D/M만 (기타 제외)
                agg_col = '수량_드럼'
                plan_col_suffix = '수량(d)'
            
                def is_drum_unit(unit_str):
                    if pd.isna(unit_str): return False
                    u = str(unit_str).upper()
                    return 'D' in u or 'M' in u or 'P' in u or 'L' in u
            
                for df in [df_act_copy, df_prev_copy, df_prev_month_copy]:
                    if not df.empty and '단위' in df.columns:
                        df.drop(df[~df['단위'].apply(is_drum_unit)].index, inplace=True)
        
            # 그룹 컬럼 설정
            extended_group_cols = []
            for col in ['거래처명', '구분', '담당자명', '품목명']:
                if col in group_cols or (col == '구분' and '거래처명' in group_cols):
                    if (not df_act_copy.empty and col in df_act_copy.columns) or \
                       (not df_plan_copy.empty and col in df_plan_copy.columns) or col in group_cols:
                        extended_group_cols.append(col)
        
            # D/C는 수량에서 제외
            if data_type == 'qty':
                for df in [df_act_copy, df_prev_copy, df_prev_month_copy]:
                    if not df.empty and '품목명' in df.columns and agg_col in df.columns:
                        df.loc[df['품목명'].str.contains('D/C', case=False, na=False), agg_col] = 0
        
            # 실적 집계
            act_grp = pd.DataFrame()
            if not df_act_copy.empty and agg_col in df_act_copy.columns:
                valid_cols = [c for c in extended_group_cols if c in df_act_copy.columns]
                if valid_cols:
                    act_grp = df_act_copy.groupby(valid_cols, as_index=False)[agg_col].sum()
                    act_grp = act_grp.rename(columns={agg_col: '실적'})
        
            # 전년 집계
            prev_grp = pd.DataFrame()
            if not df_prev_copy.empty and agg_col in df_prev_copy.columns:
                valid_cols = [c for c in extended_group_cols if c in df_prev_copy.columns]
                if valid_cols:
                    prev_grp = df_prev_copy.groupby(valid_cols, as_index=False)[agg_col].sum()
                    prev_grp = prev_grp.rename(columns={agg_col: '전년'})
        
            # 전월 집계
            prev_month_grp = pd.DataFrame()
            if include_prev_month and not df_prev_month_copy.empty and agg_col in df_prev_month_copy.columns:
                valid_cols = [c for c in extended_group_cols if c in df_prev_month_copy.columns]
                if valid_cols:
                    prev_month_grp = df_prev_month_copy.groupby(valid_cols, as_index=False)[agg_col].sum()
                    prev_month_grp = prev_month_grp.rename(columns={agg_col: '전월'})
        
            # 계획 집계
            plan_grp = pd.DataFrame()
            if not df_plan_copy.empty and '거래처명' in df_plan_copy.columns:
                plan_list = []
                for _, row in df_plan_copy.iterrows():
                    plan_row = {col: row.get(col, '-') for col in extended_group_cols if col in df_plan_copy.columns}
                
                    total_value = 0
                    for m in months_list:
                        for col in df_plan_copy.columns:
                            col_clean = col.strip()
                            target_col = f'{m}월 {plan_col_suffix}' if plan_col_suffix != '매출' else f'{m}월 매출'
                            if col_clean == target_col or col_clean == f'{m}월매출':
                                val_str = str(row.get(col, 0)).replace(',', '').replace('-', '0').strip()
                                try:
                                    total_value += float(val_str) if val_str else 0
                                except:
                                    pass
                                break
                
                    plan_row['계획'] = total_value
                    plan_list.append(plan_row)
            
                if plan_list:
                    plan_grp = pd.DataFrame(plan_list)
                    plan_group_cols = [c for c in extended_group_cols if c in plan_grp.columns]
                    if plan_group_cols:
                        plan_grp = plan_grp.groupby(plan_group_cols, as_index=False)['계획'].sum()
        
            # 병합
            if act_grp.empty and prev_grp.empty and plan_grp.empty:
                return pd.DataFrame()
        
            all_data = []
        
            if not act_grp.empty:
                for _, row in act_grp.iterrows():
                    all_data.append(dict(row))
        
            if not prev_grp.empty:
                for _, row in prev_grp.iterrows():
                    key_cols = [c for c in extended_group_cols if c in row.index]
                    key = tuple(row[c] for c in key_cols)
                    exists = False
                    for existing in all_data:
                        if tuple(existing.get(c, '') for c in key_cols) == key:
                            existing['전년'] = row['전년']
                            exists = True
                            break
                    if not exists:
                        new_row = dict(row)
                        new_row['실적'] = 0
                        all_data.append(new_row)
        
            if include_prev_month and not prev_month_grp.empty:
                for _, row in prev_month_grp.iterrows():
                    key_cols = [c for c in extended_group_cols if c in row.index]
                    key = tuple(row[c] for c in key_cols)
                    exists = False
                    for existing in all_data:
                        if tuple(existing.get(c, '') for c in key_cols) == key:
                            existing['전월'] = row['전월']
                            exists = True
                            break
                    # 전월에만 있는 데이터도 추가
                    if not exists:
                        new_row = dict(row)
                        new_row['실적'] = 0
                        new_row['전년'] = 0
                        all_data.append(new_row)
        
            if not plan_grp.empty:
                for _, row in plan_grp.iterrows():
                    key_cols = [c for c in extended_group_cols if c in row.index]
                    key = tuple(row[c] for c in key_cols)
                    exists = False
                    for existing in all_data:
                        if tuple(existing.get(c, '') for c in key_cols) == key:
                            existing['계획'] = row['계획']
                            exists = True
                            break
                    if not exists:
                        new_row = dict(row)
                        new_row['실적'] = 0
                        new_row['전년'] = 0
                        if include_prev_month:
                            new_row['전월'] = 0
                        all_data.append(new_row)
        
            if not all_data:
                return pd.DataFrame()
        
            merged = pd.DataFrame(all_data)
        
            for col in ['실적', '전년', '계획']:
                if col not in merged.columns:
                    merged[col] = 0
            if include_prev_month and '전월' not in merged.columns:
                merged['전월'] = 0
        
            merged = merged.fillna(0)
        
            # 계산
            merged['가감'] = merged['실적'] - merged['계획']
            merged['동기'] = merged['실적'] - merged['전년']
            merged['달성률(%)'] = merged.apply(lambda x: round((x['실적']/x['계획'])*100, 1) if x['계획'] > 0 else 0, axis=1)
            merged['동기비(%)'] = merged.apply(lambda x: round((x['실적']/x['전년'])*100, 1) if x['전년'] > 0 else 0, axis=1)
        
            if include_prev_month:
                merged['전월차'] = merged['실적'] - merged['전월']
                merged['전월비(%)'] = merged.apply(lambda x: round((x['실적']/x['전월'])*100, 1) if x['전월'] > 0 else 0, axis=1)
        
            merged = merged.sort_values('실적', ascending=False)
        
            # 컬럼 순서
            final_cols = [c for c in ['거래처명', '구분', '담당자명', '품목명'] if c in merged.columns]
            if include_prev_month:
                final_cols += ['계획', '실적', '전년', '전월', '가감', '동기', '전월차', '달성률(%)', '동기비(%)', '전월비(%)']
            else:
                final_cols += ['계획', '실적', '전년', '가감', '동기', '달성률(%)', '동기비(%)']
        
            final_cols = [c for c in final_cols if c in merged.columns]
            return merged[final_cols]
    
        def display_analysis_simple(data, data_type, tab_key, kpi_plan, kpi_actual, kpi_prev, kpi_prev_month=0, include_prev_month=False):
            """간결화된 테이블 표시"""
        
            if data.empty:
                st.warning("데이터가 없습니다.")
                return
        
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 CSV 다운로드", data=csv, file_name=f"매출분석_{tab_key}.csv", mime="text/csv", key=f"dl_{tab_key}")
        
            fmt = {'계획': '{:,.1f}', '실적': '{:,.1f}', '전년': '{:,.1f}', '전월': '{:,.1f}', '가감': '{:,.1f}', '동기': '{:,.1f}', '전월차': '{:,.1f}', '달성률(%)': '{:.1f}', '동기비(%)': '{:.1f}', '전월비(%)': '{:.1f}'} if data_type == 'qty' else {'계획': '{:,.0f}', '실적': '{:,.0f}', '전년': '{:,.0f}', '전월': '{:,.0f}', '가감': '{:,.0f}', '동기': '{:,.0f}', '전월차': '{:,.0f}', '달성률(%)': '{:.1f}', '동기비(%)': '{:.1f}', '전월비(%)': '{:.1f}'}
        
            st.dataframe(data.style.format(fmt, na_rep="-"), use_container_width=True, hide_index=True, height=450)
        
            # 합계 - 데이터 테이블과 동일한 컬럼 구조
            total_gap = kpi_actual - kpi_plan
            total_yoy = kpi_actual - kpi_prev
            total_ach = round((kpi_actual / kpi_plan) * 100, 1) if kpi_plan > 0 else 0
            total_yoy_rate = round((kpi_actual / kpi_prev) * 100, 1) if kpi_prev > 0 else 0
        
            st.markdown("##### ℹ️ 합계 (Total)")
        
            # 데이터 테이블과 동일한 컬럼 구조로 합계 생성
            sum_row = {}
            for col in data.columns:
                if col == '거래처명':
                    sum_row[col] = '합계'
                elif col in ['구분', '담당자명', '품목명']:
                    sum_row[col] = ''
                elif col == '계획':
                    sum_row[col] = kpi_plan
                elif col == '실적':
                    sum_row[col] = kpi_actual
                elif col == '전년':
                    sum_row[col] = kpi_prev
                elif col == '전월':
                    sum_row[col] = kpi_prev_month
                elif col == '가감':
                    sum_row[col] = total_gap
                elif col == '동기':
                    sum_row[col] = total_yoy
                elif col == '전월차':
                    sum_row[col] = kpi_actual - kpi_prev_month if include_prev_month else 0
                elif col == '달성률(%)':
                    sum_row[col] = total_ach
                elif col == '동기비(%)':
                    sum_row[col] = total_yoy_rate
                elif col == '전월비(%)':
                    sum_row[col] = round((kpi_actual / kpi_prev_month) * 100, 1) if include_prev_month and kpi_prev_month > 0 else 0
                else:
                    sum_row[col] = ''
        
            sum_df = pd.DataFrame([sum_row])
            st.dataframe(sum_df.style.format(fmt, na_rep=""), use_container_width=True, hide_index=True, height=60)
    
        # 데이터 선택
        if is_monthly_view:
            df_c_act = df_period
            df_c_prev = df_period_prev
            c_months = period_months
            kpi_plan_sales = period_plan_sales
            kpi_plan_qty = period_plan_qty
            kpi_actual_sales = period_sales
            kpi_actual_qty = period_qty
            kpi_prev_sales = period_sales_prev
            kpi_prev_qty = period_qty_prev
            if is_single_month and not df_prev_month.empty:
                kpi_prev_month_sales = df_prev_month['공급가액'].sum()
                kpi_prev_month_qty = df_prev_month['수량_드럼'].sum()
            else:
                kpi_prev_month_sales = 0
                kpi_prev_month_qty = 0
        else:
            df_c_act = df_ytd
            df_c_prev = df_ytd_prev
            c_months = ytd_months
            kpi_plan_sales = ytd_plan_sales
            kpi_plan_qty = ytd_plan_qty
            kpi_actual_sales = ytd_sales
            kpi_actual_qty = ytd_qty
            kpi_prev_sales = ytd_sales_prev
            kpi_prev_qty = ytd_qty_prev
            kpi_prev_month_sales = 0
            kpi_prev_month_qty = 0
    
        include_prev_month_flag = is_single_month and is_monthly_view
    
        # =========================================================================
        # KPI TAB - 기존 4개 서브탭
        # =========================================================================
        with kpi_main_tab:
            c_tab1, c_tab2, c_tab3, c_tab4 = st.tabs([
                "📦 업체별 수량(D/M 환산)", 
                "💰 업체별 금액",
                "📦 업체 및 품목별 수량(D/M 환산)", 
                "💰 업체 및 품목별 금액"
            ])
        
            with c_tab1:
                # 업체별 수량(D/M 환산) - P/L*0.1 + D/M, 기타 제외
                data = create_analysis_simple(df_c_act, df_c_prev, df_prev_month, df_plan_filtered, c_months, ['거래처명'], 'qty', include_prev_month_flag)
                display_analysis_simple(data, 'qty', 'c_tab1_qty', kpi_plan_qty, kpi_actual_qty, kpi_prev_qty, kpi_prev_month_qty, include_prev_month_flag)
        
            with c_tab2:
                # 업체별 금액 - 모든 단위 포함
                data = create_analysis_simple(df_c_act, df_c_prev, df_prev_month, df_plan_filtered, c_months, ['거래처명'], 'sales', include_prev_month_flag)
                display_analysis_simple(data, 'sales', 'c_tab2_sales', kpi_plan_sales, kpi_actual_sales, kpi_prev_sales, kpi_prev_month_sales, include_prev_month_flag)
        
            with c_tab3:
                # 업체 및 품목별 수량(D/M 환산) - P/L*0.1 + D/M, 기타 제외
                data = create_analysis_simple(df_c_act, df_c_prev, df_prev_month, df_plan_filtered, c_months, ['거래처명', '품목명'], 'qty', include_prev_month_flag)
                display_analysis_simple(data, 'qty', 'c_tab3_qty_item', kpi_plan_qty, kpi_actual_qty, kpi_prev_qty, kpi_prev_month_qty, include_prev_month_flag)
        
            with c_tab4:
                # 업체 및 품목별 금액 - 모든 단위 포함 (P/L, D/M 동일 품목 합산)
                data = create_analysis_simple(df_c_act, df_c_prev, df_prev_month, df_plan_filtered, c_months, ['거래처명', '품목명'], 'sales', include_prev_month_flag)
                display_analysis_simple(data, 'sales', 'c_tab4_sales_item', kpi_plan_sales, kpi_actual_sales, kpi_prev_sales, kpi_prev_month_sales, include_prev_month_flag)
    
        # =========================================================================
        # RAW DATA TAB - 단위별 원본 데이터
        # =========================================================================
        with raw_main_tab:
            st.caption("📌 P/L, D/M, 기타 단위별 원본 수량 및 금액 데이터")
        
            def create_raw_data(df_act, df_prev, group_cols):
                """RAW DATA 생성 - 단위별 원본 수량/금액 (전월 제외)"""
            
                df_act_copy = df_act.copy() if not df_act.empty else pd.DataFrame()
                df_prev_copy = df_prev.copy() if not df_prev.empty else pd.DataFrame()
            
                # 단위구분 컬럼 생성
                def get_unit_type(unit_str):
                    if pd.isna(unit_str) or str(unit_str).strip() == '':
                        return '기타'
                    u = str(unit_str).upper()
                    if 'P' in u or 'L' in u:
                        return 'P/L'
                    elif 'D' in u or 'M' in u:
                        return 'D/M'
                    return '기타'
            
                for df in [df_act_copy, df_prev_copy]:
                    if not df.empty and '단위' in df.columns:
                        df['단위'] = df['단위'].apply(get_unit_type)
            
                # 그룹 컬럼 설정 (단위 포함)
                extended_group_cols = []
                for col in ['거래처명', '구분', '담당자명', '품목명']:
                    if col in group_cols or (col == '구분' and '거래처명' in group_cols):
                        if (not df_act_copy.empty and col in df_act_copy.columns) or col in group_cols:
                            extended_group_cols.append(col)
            
                # 품목명 다음에 단위 추가
                group_cols_with_unit = extended_group_cols.copy()
                if '품목명' in group_cols_with_unit:
                    idx = group_cols_with_unit.index('품목명') + 1
                    group_cols_with_unit.insert(idx, '단위')
                else:
                    group_cols_with_unit.append('단위')
            
                # 실적 집계
                act_grp = pd.DataFrame()
                if not df_act_copy.empty:
                    valid_cols = [c for c in group_cols_with_unit if c in df_act_copy.columns]
                    if valid_cols:
                        agg_dict = {}
                        if '수량' in df_act_copy.columns:
                            agg_dict['수량'] = 'sum'
                        if '공급가액' in df_act_copy.columns:
                            agg_dict['공급가액'] = 'sum'
                        if agg_dict:
                            act_grp = df_act_copy.groupby(valid_cols, as_index=False).agg(agg_dict)
                            act_grp = act_grp.rename(columns={'수량': '실적(수량)', '공급가액': '실적(금액)'})
            
                # 전년 집계
                prev_grp = pd.DataFrame()
                if not df_prev_copy.empty:
                    valid_cols = [c for c in group_cols_with_unit if c in df_prev_copy.columns]
                    if valid_cols:
                        agg_dict = {}
                        if '수량' in df_prev_copy.columns:
                            agg_dict['수량'] = 'sum'
                        if '공급가액' in df_prev_copy.columns:
                            agg_dict['공급가액'] = 'sum'
                        if agg_dict:
                            prev_grp = df_prev_copy.groupby(valid_cols, as_index=False).agg(agg_dict)
                            prev_grp = prev_grp.rename(columns={'수량': '전년(수량)', '공급가액': '전년(금액)'})
            
                # 병합
                if act_grp.empty and prev_grp.empty:
                    return pd.DataFrame()
            
                all_data = []
            
                if not act_grp.empty:
                    for _, row in act_grp.iterrows():
                        all_data.append(dict(row))
            
                if not prev_grp.empty:
                    for _, row in prev_grp.iterrows():
                        key_cols = [c for c in group_cols_with_unit if c in row.index]
                        key = tuple(row[c] for c in key_cols)
                        exists = False
                        for existing in all_data:
                            if tuple(existing.get(c, '') for c in key_cols) == key:
                                existing['전년(수량)'] = row.get('전년(수량)', 0)
                                existing['전년(금액)'] = row.get('전년(금액)', 0)
                                exists = True
                                break
                        if not exists:
                            new_row = dict(row)
                            new_row['실적(수량)'] = 0
                            new_row['실적(금액)'] = 0
                            all_data.append(new_row)
            
                if not all_data:
                    return pd.DataFrame()
            
                merged = pd.DataFrame(all_data)
            
                # 누락 컬럼 채우기
                for col in ['실적(수량)', '실적(금액)', '전년(수량)', '전년(금액)']:
                    if col not in merged.columns:
                        merged[col] = 0
            
                merged = merged.fillna(0)
            
                # 증감 계산
                merged['동기(수량)'] = merged['실적(수량)'] - merged['전년(수량)']
                merged['동기(금액)'] = merged['실적(금액)'] - merged['전년(금액)']
            
                merged = merged.sort_values('실적(금액)', ascending=False)
            
                # 컬럼 순서 - 품목명 우측에 단위
                final_cols = [c for c in ['거래처명', '구분', '담당자명', '품목명', '단위'] if c in merged.columns]
                final_cols += ['실적(수량)', '실적(금액)', '전년(수량)', '전년(금액)', '동기(수량)', '동기(금액)']
            
                final_cols = [c for c in final_cols if c in merged.columns]
                return merged[final_cols]
        
            def display_raw_data(data, tab_key):
                """RAW DATA 테이블 표시"""
                if data.empty:
                    st.warning("데이터가 없습니다.")
                    return
            
                csv = data.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="📥 CSV 다운로드", data=csv, file_name=f"raw_data_{tab_key}.csv", mime="text/csv", key=f"dl_raw_{tab_key}")
            
                fmt = {
                    '실적(수량)': '{:,.0f}', '실적(금액)': '{:,.0f}',
                    '전년(수량)': '{:,.0f}', '전년(금액)': '{:,.0f}',
                    '동기(수량)': '{:,.0f}', '동기(금액)': '{:,.0f}'
                }
                st.dataframe(data.style.format(fmt, na_rep="-"), use_container_width=True, hide_index=True, height=450)
            
                # 합계 - 데이터 테이블과 동일한 컬럼 구조
                st.markdown("##### ℹ️ 합계 (Total)")
            
                sum_row = {}
                for col in data.columns:
                    if col == '거래처명':
                        sum_row[col] = '합계'
                    elif col in ['구분', '담당자명', '품목명', '단위']:
                        sum_row[col] = ''
                    elif col in ['실적(수량)', '실적(금액)', '전년(수량)', '전년(금액)', '동기(수량)', '동기(금액)']:
                        sum_row[col] = data[col].sum()
                    else:
                        sum_row[col] = ''
            
                sum_df = pd.DataFrame([sum_row])
                st.dataframe(sum_df.style.format(fmt, na_rep=""), use_container_width=True, hide_index=True, height=60)
        
            raw_tab1, raw_tab2 = st.tabs(["📦 업체별 RAW", "📦 업체 및 품목별 RAW"])
        
            with raw_tab1:
                raw_data = create_raw_data(df_c_act, df_c_prev, ['거래처명'])
                display_raw_data(raw_data, 'raw_client')
        
            with raw_tab2:
                raw_data = create_raw_data(df_c_act, df_c_prev, ['거래처명', '품목명'])
                display_raw_data(raw_data, 'raw_client_item')
    
        # =========================================================================
        # SECTION C-2: 2개년 시계열 매출 분석 (KPI TAB 추종 - 품목/거래처 선택 시 표시)
        # =========================================================================
        with kpi_main_tab:
            if (search_items and len(search_items) > 0) or (search_clients and len(search_clients) > 0):
                st.markdown("---")
                st.subheader("📈 SECTION C-2 : KPI 2개년 시계열 매출분석")
                st.caption(f"📅 분석 기간: {prev_year}년 1월 ~ {base_year}년 12월 (24개월)")
            
                # 2개년 시계열 데이터 준비
                df_c2_current = df_current_filtered.copy()
                df_c2_prev = df_previous_filtered.copy()
            
                # 연도 라벨 추가
                if not df_c2_current.empty:
                    df_c2_current['연도'] = base_year
                if not df_c2_prev.empty:
                    df_c2_prev['연도'] = prev_year
            
                # 2개년 데이터 합치기
                df_c2_combined = pd.concat([df_c2_prev, df_c2_current], ignore_index=True)
            
                if not df_c2_combined.empty and '월' in df_c2_combined.columns:
                    # 품목 선택 시 → 거래처별 2개년 시계열 (X축 24개월)
                    if search_items and len(search_items) > 0:
                        st.markdown(f"##### 📊 선택 품목별 거래처 매출 추세 (2개년)")
                        st.caption(f"선택된 품목: {', '.join(search_items[:5])}{'...' if len(search_items) > 5 else ''}")
                    
                        # 품목별 → 거래처별 연도/월별 매출 집계
                        c2_data = df_c2_combined.groupby(['연도', '월', '거래처명']).agg({
                            '공급가액': 'sum',
                            '수량_드럼': 'sum'
                        }).reset_index()
                    
                        # X축 라벨 생성 (24개월: 24년1월 ~ 25년12월)
                        c2_data['연월'] = c2_data.apply(lambda x: f"{str(x['연도'])[2:]}년{x['월']}월", axis=1)
                        c2_data['연월순서'] = c2_data['연도'] * 100 + c2_data['월']
                        c2_data = c2_data.sort_values('연월순서')
                    
                        if not c2_data.empty:
                            # TOP 5 거래처 선정 (금년 매출 기준)
                            current_year_data = c2_data[c2_data['연도'] == base_year]
                            if not current_year_data.empty:
                                top_clients = current_year_data.groupby('거래처명')['공급가액'].sum().nlargest(5).index.tolist()
                            else:
                                top_clients = c2_data.groupby('거래처명')['공급가액'].sum().nlargest(5).index.tolist()
                        
                            # 24개월 X축 라벨
                            x_labels = []
                            for y in [prev_year, base_year]:
                                for m in range(1, 13):
                                    x_labels.append(f"{str(y)[2:]}년{m}월")
                        
                            # 시계열 차트 생성
                            fig_c2 = go.Figure()
                        
                            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                        
                            for idx, client in enumerate(top_clients):
                                client_data = c2_data[c2_data['거래처명'] == client].sort_values('연월순서')
                                client_short = client[:15] + '..' if len(client) > 15 else client
                            
                                fig_c2.add_trace(go.Scatter(
                                    x=client_data['연월'],
                                    y=client_data['공급가액'] / 10000,
                                    name=client_short,
                                    mode='lines+markers',
                                    line=dict(color=colors[idx % len(colors)], width=3),
                                    marker=dict(size=8),
                                    hovertemplate=f'<b>{client}</b><br>%{{x}}<br>매출: %{{y:,.0f}}만원<extra></extra>'
                                ))
                        
                            fig_c2.update_layout(
                                title=dict(text=f'TOP 5 거래처 2개년 월별 매출 추세', font=dict(size=16, family='Arial Black', color='#FFFFFF')),
                                xaxis=dict(
                                    title='',
                                    tickangle=45,
                                    tickfont=dict(size=10, family='Arial Black', color='#FFFFFF'),
                                    categoryorder='array',
                                    categoryarray=x_labels
                                ),
                                yaxis=dict(
                                    title='매출액 (만원)',
                                title_font=dict(size=14, family='Arial Black', color='#FFFFFF'),
                                tickfont=dict(size=12, family='Arial Black', color='#FFFFFF'),
                                tickformat=',.0f'
                            ),
                            height=500,
                            legend=dict(
                                orientation='v',
                                yanchor='top',
                                y=0.99,
                                xanchor='left',
                                x=1.02,
                                font=dict(size=13, family='Arial Black', color='#FFFFFF'),
                                bgcolor='rgba(0,0,0,0.5)',
                                traceorder='normal'  # TOP1부터 순서대로 (이미 정렬됨)
                            ),
                            hovermode='x unified',
                            hoverlabel=dict(font_size=14, font_family='Arial Black'),
                            margin=dict(r=180, b=100),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#FFFFFF')
                        )
                    
                        st.plotly_chart(fig_c2, use_container_width=True)
                    
                        # TOP 5 집계 테이블
                        st.markdown("##### 📋 TOP 5 거래처 집계 (금년 기준)")
                        top5_curr = c2_data[(c2_data['거래처명'].isin(top_clients)) & (c2_data['연도'] == base_year)].groupby('거래처명').agg({
                            '공급가액': 'sum',
                            '수량_드럼': 'sum'
                        }).reset_index()
                        top5_curr = top5_curr.sort_values('공급가액', ascending=False)
                        top5_curr.columns = ['거래처명', '매출액', '드럼환산수량']
                    
                        st.dataframe(
                            top5_curr.style.format({
                                '매출액': '{:,.0f}',
                                '드럼환산수량': '{:,.1f}'
                            }),
                            use_container_width=True,
                            hide_index=True,
                            height=220
                        )
            
                # 거래처 선택 시 → 품목별 2개년 시계열 (X축 24개월)
                if search_clients and len(search_clients) > 0:
                    st.markdown(f"##### 📊 선택 거래처별 품목 매출 추세 (2개년)")
                    st.caption(f"선택된 거래처: {', '.join(search_clients[:5])}{'...' if len(search_clients) > 5 else ''}")
                
                    # 거래처별 → 품목별 연도/월별 매출 집계
                    c2_item_data = df_c2_combined.groupby(['연도', '월', '품목명']).agg({
                        '공급가액': 'sum',
                        '수량_드럼': 'sum'
                    }).reset_index()
                
                    # X축 라벨 생성 (24개월)
                    c2_item_data['연월'] = c2_item_data.apply(lambda x: f"{str(x['연도'])[2:]}년{x['월']}월", axis=1)
                    c2_item_data['연월순서'] = c2_item_data['연도'] * 100 + c2_item_data['월']
                    c2_item_data = c2_item_data.sort_values('연월순서')
                
                    if not c2_item_data.empty:
                        # TOP 5 품목 선정 (금년 매출 기준)
                        current_year_item = c2_item_data[c2_item_data['연도'] == base_year]
                        if not current_year_item.empty:
                            top_items = current_year_item.groupby('품목명')['공급가액'].sum().nlargest(5).index.tolist()
                        else:
                            top_items = c2_item_data.groupby('품목명')['공급가액'].sum().nlargest(5).index.tolist()
                    
                        # 24개월 X축 라벨
                        x_labels_item = []
                        for y in [prev_year, base_year]:
                            for m in range(1, 13):
                                x_labels_item.append(f"{str(y)[2:]}년{m}월")
                    
                        # 시계열 차트 생성
                        fig_c2_item = go.Figure()
                    
                        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                    
                        for idx, item in enumerate(top_items):
                            item_data = c2_item_data[c2_item_data['품목명'] == item].sort_values('연월순서')
                            item_short = item[:18] + '..' if len(item) > 18 else item
                        
                            fig_c2_item.add_trace(go.Scatter(
                                x=item_data['연월'],
                                y=item_data['공급가액'] / 10000,
                                name=item_short,
                                mode='lines+markers',
                                line=dict(color=colors[idx % len(colors)], width=3),
                                marker=dict(size=8),
                                hovertemplate=f'<b>{item}</b><br>%{{x}}<br>매출: %{{y:,.0f}}만원<extra></extra>'
                            ))
                    
                        fig_c2_item.update_layout(
                            title=dict(text=f'TOP 5 품목 2개년 월별 매출 추세', font=dict(size=16, family='Arial Black', color='#FFFFFF')),
                            xaxis=dict(
                                title='',
                                tickangle=45,
                                tickfont=dict(size=10, family='Arial Black', color='#FFFFFF'),
                                categoryorder='array',
                                categoryarray=x_labels_item
                            ),
                            yaxis=dict(
                                title='매출액 (만원)',
                                title_font=dict(size=14, family='Arial Black', color='#FFFFFF'),
                                tickfont=dict(size=12, family='Arial Black', color='#FFFFFF'),
                                tickformat=',.0f'
                            ),
                            height=500,
                            legend=dict(
                                orientation='v',
                                yanchor='top',
                                y=0.99,
                                xanchor='left',
                                x=1.02,
                                font=dict(size=12, family='Arial Black', color='#FFFFFF'),
                                bgcolor='rgba(0,0,0,0.5)',
                                traceorder='normal'
                            ),
                            hovermode='x unified',
                            hoverlabel=dict(font_size=14, font_family='Arial Black'),
                            margin=dict(r=200, b=100),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#FFFFFF')
                        )
                    
                        st.plotly_chart(fig_c2_item, use_container_width=True)
                    
                        # TOP 5 집계 테이블
                        st.markdown("##### 📋 TOP 5 품목 집계 (금년 기준)")
                        top5_item_curr = c2_item_data[(c2_item_data['품목명'].isin(top_items)) & (c2_item_data['연도'] == base_year)].groupby('품목명').agg({
                            '공급가액': 'sum',
                            '수량_드럼': 'sum'
                        }).reset_index()
                        top5_item_curr = top5_item_curr.sort_values('공급가액', ascending=False)
                        top5_item_curr.columns = ['품목명', '매출액', '드럼환산수량']
                    
                        st.dataframe(
                            top5_item_curr.style.format({
                                '매출액': '{:,.0f}',
                                '드럼환산수량': '{:,.1f}'
                            }),
                            use_container_width=True,
                            hide_index=True,
                            height=220
                        )
    
        st.markdown("---")
    
        # =========================================================================
        # SECTION D: KPI 수익성 분석 (Profitability Analysis)
        # =========================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.subheader("💹 SECTION D : KPI 수익성 분석 (Profitability Analysis)")
    
        # 현재 필터 정보 표시
        if filter_parts:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span>', unsafe_allow_html=True)
            st.markdown(f"📌 **적용 필터:** {' | '.join(filter_parts)}")
        else:
            st.markdown(f'🔍 **현재 조회 기준:** <span style="color: #1E90FF;">{period_text}</span> (전체 데이터)', unsafe_allow_html=True)
    
        # 뷰 모드 - 선택월만 사용 (금년누적 제거)
        df_d_curr, df_d_prev = df_period, df_period_prev
        d_period_text = f"{start_month}~{end_month}월" if start_month != end_month else f"{start_month}월"
    
        # 검색 여부 확인
        has_item_search = search_items and len(search_items) > 0
        has_any_search = has_item_search or (search_clients and len(search_clients) > 0)
    
        st.markdown(f"##### 📊 거래처별 수익성 분석 ({d_period_text})")
    
        # ★★★ 검색 시에만 테이블 표시 ★★★
        if has_any_search:
            # 수익성 데이터 생성 함수 (인라인)
            def make_profit_data(df):
                if df.empty:
                    return pd.DataFrame(), 0
                cols = ['거래처명', '구분', '담당자명', '품목명', '단위', '수량', '수량_드럼', '공급가액', '입고단가', '단가', '출고단가', '매입금액']
                d = df[[c for c in cols if c in df.columns]].copy()
                d['수량'] = d.get('수량', d.get('수량_드럼', 0))
                d['단위'] = d.get('단위', pd.Series(['-']*len(d))).fillna('-')
                d['매입단가'] = pd.to_numeric(d.get('입고단가', 0), errors='coerce').fillna(0)
                d['매출단가'] = pd.to_numeric(d.get('출고단가', d.get('단가', 0)), errors='coerce').fillna(0)
                d['매입금액'] = pd.to_numeric(d.get('매입금액', d['수량']*d['매입단가']), errors='coerce').fillna(0)
                for c in ['거래처명','구분','담당자명','품목명']:
                    if c not in d.columns: d[c] = '-'
                d['매출이익'] = d['매출단가'] - d['매입단가']
                g = d.groupby(['거래처명','구분','담당자명','품목명','단위','매입단가','매출단가','매출이익'], as_index=False).agg({'수량':'sum','공급가액':'sum','매입금액':'sum'})
                g = g.rename(columns={'수량':'실제수량','공급가액':'총 매출','매입금액':'총 매입'})
                g['총 매출이익'] = g['총 매출'] - g['총 매입']
                g['매출이익률(%)'] = np.where(g['총 매출']>0, np.round((g['총 매출이익']/g['총 매출'])*100,1), 0)
                g['비고'] = ''
                # 정렬
                def sk(u): 
                    u=str(u).upper()
                    return 0 if 'P' in u or 'L' in u else 1 if 'D' in u or 'M' in u else 2
                g['_sk'] = g['단위'].apply(sk)
                g = g.sort_values(['_sk','매출이익률(%)'], ascending=[True,False]).drop(columns=['_sk'])
                ts, tp = g['총 매출'].sum(), g['총 매출이익'].sum()
                return g[['거래처명','구분','담당자명','품목명','단위','실제수량','매입단가','매출단가','매출이익','총 매입','총 매출','총 매출이익','매출이익률(%)','비고']], round((tp/ts)*100,1) if ts>0 else 0
        
            p_curr, r_curr = make_profit_data(df_d_curr)
            p_prev, r_prev = make_profit_data(df_d_prev)
        
            # 테이블 표시 함수
            def show_table(data, rate, key):
                if data.empty:
                    st.warning("데이터가 없습니다.")
                    return
                st.download_button("📥 CSV 다운로드", data.to_csv(index=False).encode('utf-8-sig'), f"수익성_{key}.csv", "text/csv", key=f"dl_{key}")
                fmt = {'실제수량':'{:,.1f}','매입단가':'{:,.0f}','매출단가':'{:,.0f}','매출이익':'{:,.0f}','총 매입':'{:,.0f}','총 매출':'{:,.0f}','총 매출이익':'{:,.0f}','매출이익률(%)':'{:.1f}'}
                st.dataframe(data.style.format(fmt, na_rep="-"), use_container_width=True, hide_index=True, height=400)
                # 합계
                st.markdown("##### ℹ️ 합계")
                s = pd.DataFrame([{'거래처명':'합계','구분':'','담당자명':'','품목명':'','단위':'','실제수량':data['실제수량'].sum(),'매입단가':'','매출단가':'','매출이익':'','총 매입':data['총 매입'].sum(),'총 매출':data['총 매출'].sum(),'총 매출이익':data['총 매출이익'].sum(),'매출이익률(%)':rate,'비고':''}])
                st.dataframe(s.style.format({'실제수량':'{:,.1f}','총 매입':'{:,.0f}','총 매출':'{:,.0f}','총 매출이익':'{:,.0f}','매출이익률(%)':'{:.1f}'}, na_rep=""), use_container_width=True, hide_index=True, height=60)
        
            tab1, tab2 = st.tabs([f"📅 {base_year}년 (금년)", f"📅 {prev_year}년 (전년)"])
            with tab1: show_table(p_curr, r_curr, f's3_curr_{base_year}')
            with tab2: show_table(p_prev, r_prev, f's3_prev_{prev_year}')
        
            # ★★★ 버블차트는 품목 검색 시에만 ★★★
            if has_item_search and (not p_curr.empty or not p_prev.empty):
                st.markdown(f"##### 📈 선택 품목 수익성 버블차트 ({prev_year}년+{base_year}년 합계)")
                st.caption(f"선택된 품목: {', '.join(search_items)}")
            
                # 합계 데이터
                combined = pd.concat([p_curr, p_prev], ignore_index=True) if not p_prev.empty else p_curr.copy()
                if combined.empty:
                    st.info("버블차트 데이터가 없습니다.")
                else:
                    # P/L, D/M 수량 계산 (벡터화)
                    combined['_u'] = combined['단위'].astype(str).str.upper()
                    combined['PL'] = np.where(combined['_u'].str.contains('P|L', regex=True), combined['실제수량'], 0)
                    combined['DM'] = np.where(combined['_u'].str.contains('D|M', regex=True) & ~combined['_u'].str.contains('P|L', regex=True), combined['실제수량'], 0)
                
                    # 집계
                    b = combined.groupby(['거래처명','품목명']).agg({'총 매출이익':'sum','총 매출':'sum','PL':'sum','DM':'sum'}).reset_index()
                    b['이익률'] = np.where(b['총 매출']>0, np.round((b['총 매출이익']/b['총 매출'])*100,1), 0)
                
                    # ★★★ 품목별 TOP 5 선정 (다중 품목 지원) ★★★
                    b_top5_list = []
                    for item in search_items:
                        item_data = b[b['품목명'] == item].copy()
                        if not item_data.empty:
                            item_data = item_data.sort_values('총 매출이익', ascending=False)
                            item_data['품목내순위'] = range(1, len(item_data)+1)
                            top5_item = item_data[item_data['품목내순위'] <= 5]
                            b_top5_list.append(top5_item)
                
                    if not b_top5_list:
                        st.info("버블차트 데이터가 없습니다.")
                    else:
                        b_top5 = pd.concat(b_top5_list, ignore_index=True)
                    
                        if b_top5.empty:
                            st.info("버블차트 데이터가 없습니다.")
                        else:
                            mx = max(b_top5['총 매출이익'].abs().max(), 1)
                            b_top5['크기'] = (b_top5['총 매출이익'].abs()/mx)*60+30
                        
                            # 평균 이익률 (전체 기준)
                            avg_r = round((b['총 매출이익'].sum()/b['총 매출'].sum())*100,1) if b['총 매출'].sum()>0 else 0
                        
                            # 차트
                            fig = go.Figure()
                            colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
                        
                            for i, item in enumerate(b_top5['품목명'].unique()):
                                d = b_top5[b_top5['품목명']==item]
                                # 라벨을 아래로 (bottom center)
                                lbls = [f"<b>{r['거래처명']}</b><br>{item}<br>{r['총 매출이익']/10000:,.0f}만원<br>{r['PL']:.0f}P/L+{r['DM']:.0f}D/M" for _,r in d.iterrows()]
                                fig.add_trace(go.Scatter(
                                    x=d['이익률'], y=d['총 매출이익']/10000, mode='markers+text', name=item,
                                    marker=dict(size=d['크기'], color=colors[i%10], opacity=0.8, line=dict(width=2,color='white')),
                                    text=lbls, textposition='bottom center', textfont=dict(size=11, color='white'),
                                    hovertemplate='<b>%{customdata[0]}</b><br>품목: '+item+'<br>이익률: %{x:.1f}%<br>이익: %{y:,.0f}만원<br>P/L: %{customdata[1]:.0f}<br>D/M: %{customdata[2]:.0f}<extra></extra>',
                                    customdata=d[['거래처명','PL','DM']].values
                                ))
                        
                            # 선택 품목 수에 따른 타이틀
                            num_items = len(search_items)
                            title_text = f'품목별 TOP 5 수익성 버블차트 ({num_items}개 품목 × 5 = 최대 {num_items*5}개)'
                        
                            fig.add_vline(x=avg_r, line=dict(color='red',width=3,dash='dash'), annotation_text=f'평균 {avg_r:.1f}%', annotation_position='top', annotation_font=dict(size=14,color='red',family='Arial Black'))
                            fig.update_layout(
                                title=dict(text=title_text, font=dict(size=18,family='Arial Black',color='white')),
                                xaxis=dict(title=dict(text='매출이익률 (%)',font=dict(size=16,family='Arial Black',color='white')), tickfont=dict(size=14,family='Arial Black',color='white'), gridcolor='rgba(128,128,128,0.3)', linecolor='white'),
                                yaxis=dict(title=dict(text='매출이익 (만원)',font=dict(size=16,family='Arial Black',color='white')), tickfont=dict(size=14,family='Arial Black',color='white'), tickformat=',', gridcolor='rgba(128,128,128,0.3)', linecolor='white'),
                                height=750, showlegend=True,
                                legend=dict(orientation='h',yanchor='bottom',y=-0.15,xanchor='center',x=0.5,font=dict(size=12,family='Arial Black',color='white')),
                                hovermode='closest', margin=dict(b=100,t=80,l=80,r=40),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📌 **통합검색에서 거래처 또는 품목을 선택하면 상세 분석이 표시됩니다.**")
    
        st.markdown("---")
        st.success("✅ 대시보드 완료!")
    
        # === TAB A 리포트 다운로드 기능 (엑셀 기반) ===
        try:
            import io
            
            # 수익성 관련 변수 안전하게 가져오기
            try:
                report_avg_rate = r_curr if 'r_curr' in dir() else 0
                report_profit_data = p_curr if 'p_curr' in dir() else pd.DataFrame()
            except:
                report_avg_rate = 0
                report_profit_data = pd.DataFrame()
            
            # 요약 데이터 생성
            summary_data = pd.DataFrame({
                '구분': ['선택기간', '선택기간', '선택기간', '선택기간', '연간누적', '연간누적', '연간누적', '연간누적'],
                '항목': ['매출액(억)', '판매수량(D/M)', '계획달성률(%)', '전년대비(%)', '매출액(억)', '판매수량(D/M)', '계획달성률(%)', '전년대비(%)'],
                '값': [
                    round(period_sales/100000000, 1),
                    round(period_qty, 0),
                    round(calc_rate(period_sales, period_plan_sales), 1),
                    round(calc_rate(period_sales, period_prev_sales), 1),
                    round(ytd_sales/100000000, 1),
                    round(ytd_qty, 0),
                    round(calc_rate(ytd_sales, ytd_plan_sales), 1),
                    round(calc_rate(ytd_sales, ytd_prev_sales), 1)
                ]
            })
            
            # 엑셀 파일 생성
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 시트 1: KPI 요약
                summary_data.to_excel(writer, sheet_name='KPI요약', index=False)
                
                # 시트 2: 수익성 분석 (데이터 있을 때만)
                if not report_profit_data.empty:
                    report_profit_data.to_excel(writer, sheet_name='수익성분석', index=False)
            
            excel_buffer.seek(0)
            
            # 다운로드 버튼
            with pdf_placeholder:
                st.download_button(
                    label="📥 Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"KPI_{base_year}_{start_month}_{end_month}월.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="excel_download_main",
                    use_container_width=True
                )
        except Exception as e:
            with pdf_placeholder:
                st.warning("📥")






    # =========================================================================
    # 메인 탭 B: 시계열 확장분석
    # =========================================================================
    with main_tab_b:
        # ★★★ 경고문구 상단 표시 ★★★
        if not df_current_filtered.empty and '월' in df_current_filtered.columns:
            available_months_current_b = sorted(df_current_filtered['월'].unique())
            max_available_month_b = max(available_months_current_b) if available_months_current_b else 0
            if end_month > max_available_month_b and max_available_month_b > 0:
                st.warning(f"⚠️ 금년({base_year}년) 실적 데이터에서 선택한 항목은 **{max_available_month_b}월**까지만 있습니다. 선택한 기간({start_month}~{end_month}월) 중 가용 데이터만 표시됩니다.")
        
        st.markdown("---")
        
        # =====================================================================
        # 데이터 수집 함수
        # =====================================================================
        def get_year_from_df(df):
            """DataFrame에서 연도 추출"""
            if df is None or df.empty:
                return None
            if '연도' in df.columns:
                try:
                    return int(df['연도'].dropna().mode().iloc[0])
                except:
                    pass
            if '일자_dt' in df.columns:
                try:
                    return int(df['일자_dt'].dt.year.mode().iloc[0])
                except:
                    pass
            return None
        
        def apply_tab_b_filters(df):
            """TAB B용 필터 적용 (조회기간 + 통합검색)"""
            if df is None or df.empty:
                return pd.DataFrame()
            
            df_f = df.copy()
            
            # 월 컬럼 확인 및 생성
            if '월' not in df_f.columns and '일자_dt' in df_f.columns:
                df_f['월'] = df_f['일자_dt'].dt.month
            
            # 조회기간 필터 (월)
            if '월' in df_f.columns:
                df_f['월'] = pd.to_numeric(df_f['월'], errors='coerce')
                df_f = df_f[(df_f['월'] >= start_month) & (df_f['월'] <= end_month)]
            
            # 거래처 필터
            if search_clients and len(search_clients) > 0 and '거래처명' in df_f.columns:
                df_f = df_f[df_f['거래처명'].isin(search_clients)]
            
            # 품목 필터
            if search_items and len(search_items) > 0 and '품목명' in df_f.columns:
                df_f = df_f[df_f['품목명'].isin(search_items)]
            
            # 담당자 필터
            if search_managers and len(search_managers) > 0 and '담당자명' in df_f.columns:
                df_f = df_f[df_f['담당자명'].isin(search_managers)]
            
            # 채널 필터
            if channel_option == "직접 판매" and '구분' in df_f.columns:
                df_f = df_f[df_f['구분'] == '직접']
            elif channel_option == "간접 판매" and '구분' in df_f.columns:
                df_f = df_f[df_f['구분'] == '간접']
            
            return df_f
        
        # =====================================================================
        # 모든 연도 데이터 수집
        # =====================================================================
        all_years_data_raw = {}  # 원본 (필터 전)
        all_years_data = {}      # 필터 적용 후
        
        # 금년/전년
        if not df_current.empty:
            yr = get_year_from_df(df_current)
            if yr:
                all_years_data_raw[yr] = df_current
                all_years_data[yr] = apply_tab_b_filters(df_current)
        
        if not df_previous.empty:
            yr = get_year_from_df(df_previous)
            if yr:
                all_years_data_raw[yr] = df_previous
                all_years_data[yr] = apply_tab_b_filters(df_previous)
        
        # 과거 데이터 (이미 등록된 연도도 덮어쓰기 가능하게 수정)
        for df_past in [df_year_2, df_year_3, df_year_4, df_year_5, df_year_6, df_year_7]:
            if df_past is not None and not df_past.empty and len(df_past) > 0:
                yr = get_year_from_df(df_past)
                if yr:
                    # 이미 있어도 덮어쓰지 않음 (금년/전년 우선)
                    if yr not in all_years_data_raw:
                        all_years_data_raw[yr] = df_past
                        all_years_data[yr] = apply_tab_b_filters(df_past)
        
        available_years = sorted([y for y in all_years_data.keys() if not all_years_data[y].empty])
        max_year = max(available_years) if available_years else None
        
        # 조회기간에 따른 연도 필터링 (base_year, prev_year 범위)
        # SECTION A는 전체 연도 표시, SECTION B/C는 조회기간 연도만 표시
        query_years = [y for y in available_years if prev_year <= y <= base_year]
        
        # 데이터 상태 표시 (필터 적용 전후 비교)
        if len(available_years) >= 1:
            filter_info = []
            for yr in available_years:
                raw_cnt = len(all_years_data_raw.get(yr, []))
                filtered_cnt = len(all_years_data.get(yr, []))
                filter_info.append(f"{yr}년: {filtered_cnt:,}건/{raw_cnt:,}건")
            
            if len(available_years) >= 2:
                st.success(f"✅ **{len(available_years)}개년 데이터:** {min(available_years)}~{max(available_years)}년 | 필터 적용: {', '.join(filter_info)}")
            else:
                st.warning(f"⚠️ {available_years[0]}년 데이터만 있습니다. | {filter_info[0]}")
        else:
            st.error("❌ 필터 조건에 맞는 데이터가 없습니다. 조건을 완화해주세요.")
            st.stop()
            st.stop()
        
        # =====================================================================
        # 📊 SECTION A: 연도별 종합 현황 (필터 적용)
        # =====================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 SECTION A: 연도별 종합 현황")
        
        # 적용 필터 구성 (B, C와 동일 스타일)
        filter_parts_a = []
        if search_clients and len(search_clients) > 0:
            if len(search_clients) <= 2:
                filter_parts_a.append(f"거래처: {', '.join(search_clients)}")
            else:
                filter_parts_a.append(f"거래처: {', '.join(search_clients[:2])} 외 {len(search_clients)-2}개")
        if search_items and len(search_items) > 0:
            if len(search_items) <= 2:
                filter_parts_a.append(f"품목: {', '.join(search_items)}")
            else:
                filter_parts_a.append(f"품목: {', '.join(search_items[:2])} 외 {len(search_items)-2}개")
        if search_managers and len(search_managers) > 0:
            filter_parts_a.append(f"담당자: {', '.join(search_managers)}")
        if channel_option != "전체 보기":
            filter_parts_a.append(f"채널: {channel_option}")
        
        # 진한 회색 배너로 통합 표시 (B, C와 동일)
        filter_text_a = f" | 📌 적용 필터: {' | '.join(filter_parts_a)}" if filter_parts_a else ""
        if query_years:
            st.markdown(f'<div style="background-color: #2D3748; padding: 12px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid #4FD1C5;"><span style="color: #E2E8F0; font-weight: bold;">🔍 조회기간 연도 범위: {min(query_years)}년 ~ {max(query_years)}년 | 💡 조회기간: {start_month}~{end_month}월{filter_text_a}</span></div>', unsafe_allow_html=True)
        else:
            st.warning("데이터가 없습니다.")
        
        yearly_data = []
        for yr in available_years:
            df_yr = all_years_data[yr]
            if df_yr.empty:
                continue
            
            sales = df_yr['공급가액'].sum() if '공급가액' in df_yr.columns else 0
            qty = df_yr['수량_드럼'].sum() if '수량_드럼' in df_yr.columns else 0
            
            cost = 0
            if '매입금액' in df_yr.columns:
                cost = pd.to_numeric(df_yr['매입금액'], errors='coerce').fillna(0).sum()
            elif '입고단가' in df_yr.columns and '수량' in df_yr.columns:
                cost = (pd.to_numeric(df_yr['입고단가'], errors='coerce').fillna(0) * 
                       pd.to_numeric(df_yr['수량'], errors='coerce').fillna(0)).sum()
            
            profit = sales - cost
            profit_rate = (profit / sales * 100) if sales > 0 else 0
            yearly_data.append({'연도': yr, '매출액': sales, '수량': qty, '매출총이익': profit, '이익률': profit_rate})
        
        if not yearly_data:
            st.warning("필터 조건에 맞는 데이터가 없습니다.")
        else:
            df_yearly = pd.DataFrame(yearly_data).sort_values('연도')
            df_yearly['전년비'] = df_yearly['매출액'].pct_change() * 100
            
            st.markdown("##### 📋 연도별 매출/수량/이익 종합")
            table_data = {'항목': ['매출액(억)', '매출(YoY)', '수량_드럼환산', '수량(YoY)', '매출총이익(억)', '이익률(%)']}
            
            for i, yr in enumerate(available_years):
                if yr not in df_yearly['연도'].values:
                    continue
                row = df_yearly[df_yearly['연도'] == yr].iloc[0]
                sales_yoy = row['전년비'] if pd.notna(row['전년비']) else None
                qty_yoy = None
                if i > 0:
                    prev_yr = available_years[i-1]
                    if prev_yr in df_yearly['연도'].values:
                        prev_row = df_yearly[df_yearly['연도'] == prev_yr].iloc[0]
                        qty_yoy = ((row['수량'] / prev_row['수량']) - 1) * 100 if prev_row['수량'] > 0 else None
                
                table_data[str(yr)] = [
                    f"{row['매출액']/100000000:.1f}",
                    f"{sales_yoy:+.1f}%" if sales_yoy is not None else "-",
                    f"{row['수량']:,.0f}",
                    f"{qty_yoy:+.1f}%" if qty_yoy is not None else "-",
                    f"{row['매출총이익']/100000000:.1f}",
                    f"{row['이익률']:.1f}%"
                ]
            
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
            
            # 차트
            st.markdown("##### 📊 연도별 매출/수량 추이 차트")
            fig_a = go.Figure()
            
            # Y축 최대값 계산 (텍스트 공간 확보)
            max_sales = df_yearly['매출액'].max() / 100000000
            max_qty = df_yearly['수량'].max()
            
            fig_a.add_trace(go.Bar(x=df_yearly['연도'].astype(str), y=df_yearly['매출액']/100000000, name='매출액(억)', marker_color='#2E86AB', text=[f'{v:.1f}' for v in df_yearly['매출액']/100000000], textposition='outside', textfont=dict(color='#FFFFFF', size=14)))
            fig_a.add_trace(go.Scatter(x=df_yearly['연도'].astype(str), y=df_yearly['수량'], name='수량_드럼환산', mode='lines+markers+text', line=dict(color='#E94F37', width=3), marker=dict(size=12), yaxis='y2', text=[f'{v:.0f}' for v in df_yearly['수량']], textposition='top center', textfont=dict(color='#E94F37', size=14, family='Arial Black')))
            fig_a.update_layout(
                title=dict(text=f'연도별 매출/수량 추이 ({start_month}~{end_month}월)', font=dict(size=16, color='#FFFFFF')),
                yaxis=dict(title=dict(text='매출액(억원)', font=dict(color='#2E86AB', size=14)), side='left', tickfont=dict(color='#FFFFFF', size=12), range=[0, max_sales * 1.3]),
                yaxis2=dict(title=dict(text='수량_드럼환산', font=dict(color='#E94F37', size=14)), overlaying='y', side='right', tickfont=dict(color='#FFFFFF', size=12), range=[0, max_qty * 1.3]),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font=dict(color='#FFFFFF', size=14), bgcolor='rgba(0,0,0,0.5)'),
                height=480,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                margin=dict(t=100)
            )
            st.plotly_chart(fig_a, use_container_width=True)
        
        st.markdown("---")
        
        # =====================================================================
        # 📊 SECTION B: 상세현황(Drill Down)
        # =====================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 SECTION B: 상세현황(Drill Down)")
        
        # 적용 필터 구성
        filter_parts_b = []
        if search_clients and len(search_clients) > 0:
            if len(search_clients) <= 2:
                filter_parts_b.append(f"거래처: {', '.join(search_clients)}")
            else:
                filter_parts_b.append(f"거래처: {', '.join(search_clients[:2])} 외 {len(search_clients)-2}개")
        if search_items and len(search_items) > 0:
            if len(search_items) <= 2:
                filter_parts_b.append(f"품목: {', '.join(search_items)}")
            else:
                filter_parts_b.append(f"품목: {', '.join(search_items[:2])} 외 {len(search_items)-2}개")
        if search_managers and len(search_managers) > 0:
            filter_parts_b.append(f"담당자: {', '.join(search_managers)}")
        if channel_option != "전체 보기":
            filter_parts_b.append(f"채널: {channel_option}")
        
        # 진한 회색 배너로 통합 표시 (SECTION A 스타일)
        filter_text_b = f" | 📌 적용 필터: {' | '.join(filter_parts_b)}" if filter_parts_b else ""
        if query_years:
            st.markdown(f'<div style="background-color: #2D3748; padding: 12px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid #4FD1C5;"><span style="color: #E2E8F0; font-weight: bold;">🔍 조회기간 연도 범위: {min(query_years)}년 ~ {max(query_years)}년 | 💡 조회기간: {start_month}~{end_month}월{filter_text_b}</span></div>', unsafe_allow_html=True)
        else:
            st.warning("데이터가 없습니다.")
        
        has_filter = bool(search_clients) or bool(search_items) or bool(search_managers) or channel_option != "전체 보기"
        
        if has_filter:
            drill_data = []
            
            # query_years: 조회기간 연도 범위만 사용
            for yr in query_years:
                if yr not in all_years_data:
                    continue
                df_yr = all_years_data[yr]
                if df_yr.empty:
                    continue
                
                # 그룹핑
                group_cols = ['거래처명', '구분', '품목명', '단위']
                group_cols = [c for c in group_cols if c in df_yr.columns]
                
                if group_cols:
                    for keys, grp in df_yr.groupby(group_cols, dropna=False):
                        if not isinstance(keys, tuple):
                            keys = (keys,)
                        
                        row_dict = {'연도': yr}
                        for j, col in enumerate(group_cols):
                            row_dict[col] = keys[j] if j < len(keys) else ''
                        
                        row_dict['판매수량'] = grp['수량'].sum() if '수량' in grp.columns else 0
                        row_dict['매출액'] = grp['공급가액'].sum() if '공급가액' in grp.columns else 0
                        
                        if '매입금액' in grp.columns:
                            row_dict['매입금액'] = pd.to_numeric(grp['매입금액'], errors='coerce').fillna(0).sum()
                        elif '입고단가' in grp.columns and '수량' in grp.columns:
                            row_dict['매입금액'] = (pd.to_numeric(grp['입고단가'], errors='coerce').fillna(0) * pd.to_numeric(grp['수량'], errors='coerce').fillna(0)).sum()
                        else:
                            row_dict['매입금액'] = 0
                        
                        row_dict['이익금'] = row_dict['매출액'] - row_dict['매입금액']
                        row_dict['이익률'] = (row_dict['이익금'] / row_dict['매출액'] * 100) if row_dict['매출액'] > 0 else 0
                        drill_data.append(row_dict)
            
            if drill_data:
                df_drill = pd.DataFrame(drill_data)
                col_order = ['연도', '거래처명', '구분', '품목명', '단위', '판매수량', '매출액', '매입금액', '이익금', '이익률']
                df_drill = df_drill[[c for c in col_order if c in df_drill.columns]]
                df_drill = df_drill.sort_values(['연도', '거래처명'] if '거래처명' in df_drill.columns else ['연도'])
                
                st.dataframe(
                    df_drill.style.format({'판매수량': '{:,.0f}', '매출액': '{:,.0f}', '매입금액': '{:,.0f}', '이익금': '{:,.0f}', '이익률': '{:.1f}%'}),
                    use_container_width=True, hide_index=True, height=400
                )
                st.markdown(f"📊 **조회 결과:** {len(df_drill)}건 | 조회기간: {start_month}~{end_month}월")
            else:
                st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
        else:
            st.info("👈 좌측 사이드바에서 **거래처, 품목, 담당자** 중 하나 이상을 선택해주세요.")
        
        st.markdown("---")
        
        # =====================================================================
        # 📊 SECTION C: 가격 히스토리
        # =====================================================================
        st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 SECTION C: 가격 히스토리")
        
        # 연한 파란색 안내 (SECTION C만)
        st.info(f"📅 **통합 조회기간 설정에서 금년도 12월까지 설정을 해주세요**")
        
        # 적용 필터 구성
        filter_parts_c = []
        if search_clients and len(search_clients) > 0:
            if len(search_clients) <= 2:
                filter_parts_c.append(f"거래처: {', '.join(search_clients)}")
            else:
                filter_parts_c.append(f"거래처: {', '.join(search_clients[:2])} 외 {len(search_clients)-2}개")
        if search_items and len(search_items) > 0:
            if len(search_items) <= 2:
                filter_parts_c.append(f"품목: {', '.join(search_items)}")
            else:
                filter_parts_c.append(f"품목: {', '.join(search_items[:2])} 외 {len(search_items)-2}개")
        if search_managers and len(search_managers) > 0:
            filter_parts_c.append(f"담당자: {', '.join(search_managers)}")
        
        # 진한 회색 배너로 통합 표시 (SECTION A 스타일)
        filter_text_c = f" | 📌 적용 필터: {' | '.join(filter_parts_c)}" if filter_parts_c else ""
        if query_years:
            st.markdown(f'<div style="background-color: #2D3748; padding: 12px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid #4FD1C5;"><span style="color: #E2E8F0; font-weight: bold;">🔍 조회기간 연도 범위: {min(query_years)}년 ~ {max(query_years)}년 | 💡 조회기간: {start_month}~{end_month}월 | 단가 변동 시점 파악{filter_text_c}</span></div>', unsafe_allow_html=True)
        else:
            st.warning("데이터가 없습니다.")
        
        has_filter_c = bool(search_clients) or bool(search_items)
        
        if has_filter_c:
            price_data = []
            
            # query_years: 조회기간 연도 범위만 사용
            for yr in query_years:
                if yr not in all_years_data:
                    continue
                df_yr = all_years_data[yr].copy()
                if df_yr.empty:
                    continue
                
                # 월 컬럼 확인/생성
                if '월' not in df_yr.columns and '일자_dt' in df_yr.columns:
                    df_yr['월'] = df_yr['일자_dt'].dt.month
                
                # ★★★ 핵심: 거래처+구분+품목+단위+월별로 그룹핑 (단가는 그룹핑에서 제외!) ★★★
                group_cols = ['거래처명', '구분', '품목명', '단위', '월']
                group_cols = [c for c in group_cols if c in df_yr.columns]
                
                if len(group_cols) >= 4:
                    for keys, grp in df_yr.groupby(group_cols, dropna=False):
                        if not isinstance(keys, tuple):
                            keys = (keys,)
                        
                        # 해당 월의 마지막 거래 단가 (최신 단가)
                        grp_sorted = grp.sort_values('일자_dt') if '일자_dt' in grp.columns else grp
                        last_row = grp_sorted.iloc[-1]
                        
                        buy_price = pd.to_numeric(last_row.get('입고단가', 0), errors='coerce') or 0
                        sell_price = pd.to_numeric(last_row.get('단가', 0), errors='coerce') or 0
                        
                        row_dict = {
                            '연도': yr,
                            '거래처명': keys[0] if len(keys) > 0 else '',
                            '구분': keys[1] if len(keys) > 1 else '',
                            '품목명': keys[2] if len(keys) > 2 else '',
                            '단위': keys[3] if len(keys) > 3 else '',
                            '월': keys[4] if len(keys) > 4 else 1,
                            '사용량': grp['수량'].sum() if '수량' in grp.columns else 0,
                            '매입단가': buy_price,
                            '매출단가': sell_price,
                        }
                        
                        row_dict['매출이익'] = row_dict['매출단가'] - row_dict['매입단가']
                        row_dict['이익률'] = (row_dict['매출이익'] / row_dict['매출단가'] * 100) if row_dict['매출단가'] > 0 else 0
                        
                        price_data.append(row_dict)
            
            if price_data:
                df_price = pd.DataFrame(price_data)
                # 거래처 + 품목 + 단위 + 연도 + 월 순으로 정렬
                df_price = df_price.sort_values(['거래처명', '품목명', '단위', '연도', '월'])
                df_price['비고'] = ''
                
                # ★★★ 거래처 + 품목 + 단위별로 단가 변동 감지 (실제 변동 시점 표시) ★★★
                for (client, item, unit), grp in df_price.groupby(['거래처명', '품목명', '단위'], dropna=False):
                    indices = grp.index.tolist()
                    
                    prev_sell = None  # 이전 매출단가
                    prev_yr = None    # 이전 연도
                    
                    for i, idx in enumerate(indices):
                        yr = df_price.loc[idx, '연도']
                        month = df_price.loc[idx, '월']
                        sell = df_price.loc[idx, '매출단가']
                        
                        # 이전 단가 대비 변동 감지 (연도 포함하여 표시)
                        if prev_sell is not None:
                            if sell > prev_sell:
                                df_price.loc[idx, '비고'] = f'{int(yr)}년 {int(month)}월 인상'
                            elif sell < prev_sell:
                                df_price.loc[idx, '비고'] = f'{int(yr)}년 {int(month)}월 인하'
                            # 변동없으면 비고 비워둠
                        
                        prev_sell = sell
                        prev_yr = yr
                    
                    # ★★★ 마지막 행 = "마지막 판매가격" 표시 ★★★
                    if indices:
                        last_idx = indices[-1]
                        last_yr = df_price.loc[last_idx, '연도']
                        last_month = df_price.loc[last_idx, '월']
                        current_note = df_price.loc[last_idx, '비고']
                        
                        if current_note:
                            df_price.loc[last_idx, '비고'] = f'{current_note} (마지막 판매가격)'
                        else:
                            df_price.loc[last_idx, '비고'] = '마지막 판매가격'
                
                display_cols = ['연도', '거래처명', '구분', '품목명', '단위', '월', '사용량', '매입단가', '매출단가', '매출이익', '이익률', '비고']
                df_price = df_price[[c for c in display_cols if c in df_price.columns]]
                
                st.dataframe(
                    df_price.style.format({'사용량': '{:,.0f}', '매입단가': '{:,.0f}', '매출단가': '{:,.0f}', '매출이익': '{:,.0f}', '이익률': '{:.1f}%'}),
                    use_container_width=True, hide_index=True, height=500
                )
                st.markdown(f"📊 **조회 결과:** {len(df_price)}건 | 조회기간: {start_month}~{end_month}월")
                
                # CSV 다운로드 버튼
                st.download_button(
                    label="📥 가격 히스토리 CSV 다운로드",
                    data=df_price.to_csv(index=False).encode('utf-8-sig'),
                    file_name=f"가격히스토리_{base_year}_{start_month}_{end_month}월.csv",
                    mime="text/csv",
                    key="price_history_csv"
                )
            else:
                st.warning("선택한 조건에 해당하는 가격 데이터가 없습니다.")
        else:
            st.info("👈 좌측 사이드바에서 **거래처** 또는 **품목**을 선택하면 가격 히스토리가 표시됩니다.")
        
        # =====================================================================
        # 📄 TAB B 전체 리포트 다운로드 (엑셀 기반)
        # =====================================================================
        st.markdown("---")
        st.markdown("### 📄 시계열 분석 리포트 다운로드")
        
        try:
            import io
            
            # 엑셀 파일 생성 (멀티시트)
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 시트 1: 연도별 종합 (SECTION A)
                if 'df_yearly' in dir() and not df_yearly.empty:
                    df_yearly.to_excel(writer, sheet_name='연도별종합', index=False)
                
                # 시트 2: 상세현황 (SECTION B)
                if 'df_drill' in dir() and not df_drill.empty:
                    df_drill.to_excel(writer, sheet_name='상세현황', index=False)
                
                # 시트 3: 가격히스토리 (SECTION C)
                if 'df_price' in dir() and not df_price.empty:
                    df_price.to_excel(writer, sheet_name='가격히스토리', index=False)
            
            excel_buffer.seek(0)
            
            # 다운로드 버튼
            tab_b_col1, tab_b_col2, tab_b_col3 = st.columns(3)
            
            with tab_b_col1:
                st.download_button(
                    label="📥 전체 Excel (모든 섹션)",
                    data=excel_buffer.getvalue(),
                    file_name=f"시계열분석_{prev_year}_{base_year}년.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="tab_b_excel_all"
                )
            
            with tab_b_col2:
                # SECTION A CSV
                if 'df_yearly' in dir() and not df_yearly.empty:
                    st.download_button(
                        label="📥 연도별종합 (CSV)",
                        data=df_yearly.to_csv(index=False).encode('utf-8-sig'),
                        file_name=f"연도별종합_{prev_year}_{base_year}.csv",
                        mime="text/csv",
                        key="section_a_csv"
                    )
            
            with tab_b_col3:
                # SECTION C CSV (가격히스토리)
                if 'df_price' in dir() and not df_price.empty:
                    st.download_button(
                        label="📥 가격히스토리 (CSV)",
                        data=df_price.to_csv(index=False).encode('utf-8-sig'),
                        file_name=f"가격히스토리_{prev_year}_{base_year}.csv",
                        mime="text/csv",
                        key="section_c_csv"
                    )
        except Exception as e:
            st.warning(f"리포트 생성 오류")

else:
    st.warning("👈 사이드바에서 파일을 업로드해주세요.")
    st.markdown("""
    ### 📋 필수 파일 (TAB A: KPI 대시보드):
    1. **사업계획서**를 업로드해주세요 (.csv)
    2. **금년 실적**을 업로드해주세요 (.csv)
    3. **전년 실적**을 업로드해주세요 (.csv)
    
    ---
    
    ### 📈 선택 파일 (TAB B: 시계열 확장분석):
    > 과거 데이터를 업로드하면 **연도별 추이 분석, 가격 히스토리** 등 확장 분석이 가능합니다.
    
    4. **2년전 실적** (.csv) - 선택
    5. **3년전 실적** (.csv) - 선택
    6. **4년전 실적** (.csv) - 선택
    7. **5년전 실적** (.csv) - 선택
    8. **6년전 실적** (.csv) - 선택
    9. **7년전 실적** (.csv) - 선택
    
    💡 *Secrets에 Google Drive 파일 ID를 저장하면 자동으로 로드됩니다.*
    """)
