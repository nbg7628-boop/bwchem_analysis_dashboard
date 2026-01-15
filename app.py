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
    
    /* ★★★ 통합검색 멀티셀렉트 - 흰색 배경, 검정색 글씨/화살표 ★★★ */
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        border-radius: 5px;
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
    }
    .stMultiSelect [data-baseweb="icon"] {
        color: #000000 !important;
    }
    
    /* 일반 입력 필드 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    
    /* 버튼 */
    .stButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #4a4a4a !important;
    }
    
    /* 탭 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #fafafa !important;
    }
    
    /* 데이터프레임 */
    .stDataFrame {
        background-color: #262730 !important;
    }
    
    /* 정보 박스 */
    .stAlert {
        background-color: #262730 !important;
    }
    
    /* 라디오 버튼 */
    .stRadio > div {
        background-color: transparent !important;
    }
    
    /* 페이지 나눔 (인쇄용) */
    .print-page-break {
        page-break-before: always;
        break-before: page;
    }
    
    /* ★★★ 인쇄 시 스타일 변경 ★★★ */
    @media print {
        /* 전체 배경 흰색 */
        .stApp, body, html {
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* 메인 컨텐츠 */
        .main .block-container {
            background-color: #ffffff !important;
        }
        
        /* 사이드바 숨기기 */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* 모든 텍스트 검정색 */
        h1, h2, h3, h4, h5, h6, p, span, label, div, td, th {
            color: #000000 !important;
            background-color: transparent !important;
        }
        
        /* 마크다운 텍스트 */
        .stMarkdown, .stMarkdown p, .stMarkdown span {
            color: #000000 !important;
        }
        
        /* 데이터프레임 테이블 */
        .stDataFrame, table, tr, td, th {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-color: #333333 !important;
        }
        
        /* 차트 영역 */
        .js-plotly-plot, .plotly {
            background-color: #ffffff !important;
        }
        
        /* 페이지 나눔 적용 */
        .print-page-break {
            page-break-before: always !important;
            break-before: page !important;
        }
        
        /* 차트 텍스트 */
        .gtitle, .xtitle, .ytitle, .xtick text, .ytick text {
            fill: #000000 !important;
        }
        
        /* Plotly 차트 내부 텍스트 */
        svg text, svg tspan {
            fill: #000000 !important;
        }
        
        /* 범례 배경 */
        .legend, .legendtext {
            fill: #000000 !important;
        }
        
        /* 탭 버튼 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f0f0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        
        /* 버튼 */
        .stButton > button, .stDownloadButton > button {
            background-color: #f0f0f0 !important;
            color: #000000 !important;
            border: 1px solid #333333 !important;
        }
        
        /* 라디오/체크박스 레이블 */
        .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        
        /* 익스팬더 */
        .streamlit-expanderHeader {
            background-color: #f0f0f0 !important;
            color: #000000 !important;
        }
        
        /* 마크다운 텍스트 */
        .stMarkdown, .stMarkdown p, .stMarkdown span,
        .stMarkdown div, .stMarkdown li {
            color: #000000 !important;
        }
        
        /* 컬럼 내부 */
        [data-testid="column"] {
            background-color: #ffffff !important;
        }
        
        /* 차트 그리드 라인 */
        .gridlayer line, .zerolinelayer line {
            stroke: #cccccc !important;
        }
        
        /* 바 차트 텍스트 */
        .bars text, .bar text {
            fill: #000000 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# ★★★ 비밀번호 인증 (secrets에서 읽어옴) ★★★
# =============================================================================
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    
    st.warning("🔒 관계자 외 접속을 제한합니다.")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    # secrets에서 비밀번호 읽기
    correct_password = st.secrets.get("password", "bumwoo1234")
    
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
    try:
        url = f"https://drive.google.com/uc?id={file_id}&export=download"
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"파일 로드 실패: {e}")
        return None

@st.cache_data(ttl=300, show_spinner=False)
def get_file_list_from_folder(folder_id):
    """Google Drive 폴더의 파일 목록 가져오기 (공개 폴더용)"""
    # 공개 폴더에서 직접 파일 목록을 가져오는 것은 API 없이 어려움
    # 대신 파일 ID를 secrets에 저장하거나, 알려진 파일명으로 접근
    return {}

# =============================================================================
# 1. 데이터 로드 함수 (캐시 적용)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_erp_data(file_content, filename="data.csv"):
    """ERP 마감 데이터 로드 - 캐시 적용"""
    if file_content is None:
        return pd.DataFrame()
    
    try:
        # 인코딩 시도
        try:
            df = pd.read_csv(io.BytesIO(file_content), header=1, encoding='utf-8', thousands=',')
        except:
            df = pd.read_csv(io.BytesIO(file_content), header=1, encoding='cp949', thousands=',')
        
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
        
        # 출고단가 (단가 컬럼 사용)
        if '단가' in df.columns:
            df['출고단가'] = df['단가']
        
        return df
    
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_plan_data(file_content):
    """사업계획서 로드 - 캐시 적용"""
    if file_content is None:
        return pd.DataFrame()
    
    try:
        # 인코딩 시도
        try:
            df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8')
        except:
            df = pd.read_csv(io.BytesIO(file_content), encoding='cp949')
        
        # 컬럼명 정리
        df.columns = df.columns.str.strip()
        
        # 숫자 컬럼 처리
        for col in df.columns:
            if col not in ['거래처명', '구분', '품목명', '담당자명']:
                if df[col].dtype == object:
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace(',', ''), 
                        errors='coerce'
                    ).fillna(0)
        
        return df
    
    except Exception as e:
        st.error(f"계획 데이터 로드 오류: {e}")
        return pd.DataFrame()


# =============================================================================
# ★★★ Google Drive 파일 ID 설정 (secrets에서 읽기) ★★★
# =============================================================================
# secrets.toml 예시:
# [gdrive]
# folder_id = "1mJzkNb5kfuXQc_e-xx95ZCDPxY7TKuXP"
# plan_2026 = "파일ID"
# sales_2026 = "파일ID"
# sales_2025 = "파일ID"
# ...

# 파일 ID 가져오기 (secrets 또는 기본값)
gdrive_config = st.secrets.get("gdrive", {})
FOLDER_ID = gdrive_config.get("folder_id", "1mJzkNb5kfuXQc_e-xx95ZCDPxY7TKuXP")

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
        prev_year = st.selectbox(
            "비교년도", 
            range(2019, 2070), 
            index=6,  # 2025년 기본
            key="prev_year"
        )
    with col_year2:
        base_year = st.selectbox(
            "금년도", 
            range(2020, 2071), 
            index=6,  # 2026년 기본
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
    
    # ★★★ Google Drive 파일 ID 입력 ★★★
    st.subheader("📂 Google Drive 파일 ID")
    st.caption("Google Drive에서 파일 우클릭 → 링크 복사 → ID 부분만 입력")
    
    # 파일 ID 입력 (secrets에서 기본값 가져오기)
    file_id_plan = st.text_input(
        "사업계획서 파일 ID",
        value=gdrive_config.get("plan_2026", ""),
        key="file_id_plan"
    )
    file_id_current = st.text_input(
        "금년 실적 파일 ID", 
        value=gdrive_config.get("sales_2026", ""),
        key="file_id_current"
    )
    file_id_previous = st.text_input(
        "전년 실적 파일 ID",
        value=gdrive_config.get("sales_2025", ""),
        key="file_id_previous"
    )
    
    # 과거 시계열 데이터
    with st.expander("📁 과거 시계열 데이터 (B탭 확장분석)", expanded=False):
        file_id_year_2 = st.text_input("2년전 실적 ID", value=gdrive_config.get("sales_2024", ""), key="file_id_2")
        file_id_year_3 = st.text_input("3년전 실적 ID", value=gdrive_config.get("sales_2023", ""), key="file_id_3")
        file_id_year_4 = st.text_input("4년전 실적 ID", value=gdrive_config.get("sales_2022", ""), key="file_id_4")
        file_id_year_5 = st.text_input("5년전 실적 ID", value=gdrive_config.get("sales_2021", ""), key="file_id_5")
        file_id_year_6 = st.text_input("6년전 실적 ID", value=gdrive_config.get("sales_2020", ""), key="file_id_6")


# =============================================================================
# 3. 메인 대시보드
# =============================================================================

# 데이터 로드 상태 확인
has_required_files = file_id_plan and file_id_current and file_id_previous

if has_required_files:
    with st.spinner("📊 Google Drive에서 데이터 로드 중..."):
        # Google Drive에서 파일 로드
        content_plan = load_csv_from_gdrive(file_id_plan)
        content_current = load_csv_from_gdrive(file_id_current)
        content_previous = load_csv_from_gdrive(file_id_previous)
        
        # 과거 데이터 로드
        content_year_2 = load_csv_from_gdrive(file_id_year_2) if file_id_year_2 else None
        content_year_3 = load_csv_from_gdrive(file_id_year_3) if file_id_year_3 else None
        content_year_4 = load_csv_from_gdrive(file_id_year_4) if file_id_year_4 else None
        content_year_5 = load_csv_from_gdrive(file_id_year_5) if file_id_year_5 else None
        content_year_6 = load_csv_from_gdrive(file_id_year_6) if file_id_year_6 else None
    
    # 데이터프레임 변환
    df_plan = load_plan_data(content_plan)
    df_current = load_erp_data(content_current, "current.csv")
    df_previous = load_erp_data(content_previous, "previous.csv")
    
    # 과거 시계열 데이터
    df_year_2 = load_erp_data(content_year_2, "year_2.csv") if content_year_2 else pd.DataFrame()
    df_year_3 = load_erp_data(content_year_3, "year_3.csv") if content_year_3 else pd.DataFrame()
    df_year_4 = load_erp_data(content_year_4, "year_4.csv") if content_year_4 else pd.DataFrame()
    df_year_5 = load_erp_data(content_year_5, "year_5.csv") if content_year_5 else pd.DataFrame()
    df_year_6 = load_erp_data(content_year_6, "year_6.csv") if content_year_6 else pd.DataFrame()
    
    # 데이터 로드 확인
    if df_plan.empty or df_current.empty or df_previous.empty:
        st.error("❌ 데이터 로드에 실패했습니다. 파일 ID를 확인해주세요.")
        st.info("""
        **파일 ID 찾는 방법:**
        1. Google Drive에서 파일 우클릭
        2. "공유" 클릭
        3. "링크 복사" 클릭
        4. 링크에서 ID 부분만 복사
        
        예시: https://drive.google.com/file/d/**1ABC123xyz**/view
        → ID: **1ABC123xyz**
        """)
        st.stop()
    
    # 마스터 데이터에서 옵션 추출 (검색용)
    all_clients = sorted(set(
        df_current['거래처명'].dropna().unique().tolist() + 
        df_previous['거래처명'].dropna().unique().tolist()
    )) if '거래처명' in df_current.columns else []
    
    all_items = sorted(set(
        df_current['품목명'].dropna().unique().tolist() + 
        df_previous['품목명'].dropna().unique().tolist()
    )) if '품목명' in df_current.columns else []
    
    all_managers = sorted(set(
        df_current['담당자명'].dropna().unique().tolist() + 
        df_previous['담당자명'].dropna().unique().tolist()
    )) if '담당자명' in df_current.columns else []
    
    # 세션에 저장 (검색 옵션용)
    st.session_state['all_clients'] = [c for c in all_clients if c and str(c) != 'nan']
    st.session_state['all_items'] = [i for i in all_items if i and str(i) != 'nan']
    st.session_state['all_managers'] = [m for m in all_managers if m and str(m) != 'nan']
    
    # 성공 메시지
    st.success(f"✅ 데이터 로드 완료! 금년: {len(df_current):,}건, 전년: {len(df_previous):,}건")
    
    # ★★★ 여기에 기존 대시보드 코드가 들어갑니다 ★★★
    # (TAB A, TAB B 전체 코드)
    
    st.info("🎉 Google Drive 연동 성공! 대시보드 기능을 추가하려면 기존 코드를 병합하세요.")

else:
    # 파일 ID 미입력 시 안내
    st.warning("👈 좌측 사이드바에서 Google Drive 파일 ID를 입력해주세요.")
    
    st.markdown("""
    ### 📖 사용 방법
    
    **1단계: Google Drive에서 파일 ID 찾기**
    ```
    1. Google Drive에서 CSV 파일 우클릭
    2. "공유" → "링크 복사"
    3. 링크에서 ID 부분 복사
    
    예시: https://drive.google.com/file/d/1ABC123xyz/view
    → ID: 1ABC123xyz
    ```
    
    **2단계: 좌측 사이드바에 ID 입력**
    - 사업계획서 파일 ID
    - 금년 실적 파일 ID  
    - 전년 실적 파일 ID
    
    **3단계: 자동 로드**
    - ID 입력하면 자동으로 데이터 로드
    - 5분마다 자동 갱신
    """)
