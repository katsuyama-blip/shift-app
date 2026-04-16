import streamlit as st
import pandas as pd
import datetime

# --- 1. ページ設定（ユーザーの理想を実現するためにワイド画面に挑戦） ---
st.set_page_config(page_title="神シフト作成：究極カレンダー版", layout="wide")

# --- 2. 究極のCSS（ユーザーの理想の見た目と機能性を両立） ---
st.markdown("""
    <style>
    /* 設定エリアの枠 */
    [data-testid="stExpander"] { border: 2px solid #ffb6c1; border-radius: 10px; background-color: #fffaf0; }
    
    /* カレンダー全体の設定（隙間をゼロに、崩れ防止） */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        padding-top: 0px !important;
    }
    
    /* カラム（列）の設定：幅を均等にして、崩れない最低の幅を確保 */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 【究極のボタン】画像のような見た目を実現 */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important; /* セルを大きく */
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 1px solid #ddd !important;
        font-weight: bold !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: white;
        color: black;
    }

    /* 状態ごとのボタンの色（魔法のセレクタで確実に上書き） */
    /* 公休（ピンク） */
    div.stButton > button:has(p:contains("公休")) {
        background-color: #ffb6c1 !important;
        color: white !important;
    }
    /* 有給（オレンジ） */
    div.stButton > button:has(p:contains("有給")) {
        background-color: #ffa500 !important;
        color: white !important;
    }
    
    /* ミーティング日（ダミー：後ほど実装） */
    div.stButton > button:has(p:contains("全員")) {
        background-color: #87ceeb !important; /* 水色 */
        color: white !important;
    }

    /* 警告のビックリマーク */
    .warning-icon {
        color: red;
        font-weight: bold;
        font-size: 20px;
    }

    /* 曜日ヘッダー */
    .weekday {
        text-align: center;
        background-color: #f8f9fa;
        color: #ff69b4;
        font-weight: bold;
        border: 1px solid #ddd;
        padding: 10px 0;
        font-size: 1.2em; /* 曜日を大きく */
    }
    .month-bar {
        background-color: #ffb6c1;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 10px;
        font-size: 1.5em; /* 月を大きく */
        margin-top: 20px;
    }
    
    /* フォントサイズの調整（日付を画像のように大きく） */
    div.stButton > button div p {
        font-size: 2.5em !important; /* 日付を大きく */
        margin: 0px !important;
        padding: 0px !important;
    }
    /* 公休・有給の文字サイズ */
    div.stButton > button div span {
        font-size: 0.8em !important; 
        margin: 0px !important;
        padding: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. セッション状態の初期化 ---
if "requests" not in st.session_state:
    st.session_state.requests = {} # {スタッフ名: {日付: 状態(0,1,2)}}

if "meeting_days" not in st.session_state:
    st.session_state.meeting_days = {} # {日付: True}

# --- 4. メイン画面 ---
st.title("🌸 神シフト作成：究極カレンダー版")

# 設定エリア（前回の枠を維持）
st.markdown("<div class='config-box'>", unsafe_allow_html=True)
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        target_month = st.selectbox("📅 対象月：", ["2026年6月分", "2026年7月分"])
    with col_b:
        off_count = st.number_input("🔢 公休回数：", value=8)
st.markdown("</div>", unsafe_allow_html=True)

st.write("### ｜ ステップ1：希望入力")

# モード切替（ミーティング設定タブの復活）
tab1, tab2 = st.tabs(["休み希望（スタッフ）", "全員出勤日（会議）設定"])

# --- タブ1：休み希望（スタッフ） ---
with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("👤 スタッフを選択：", staff_list)
    
    if selected_staff not in st.session_state.requests:
        st.session_state.requests[selected_staff] = {}
    
    # 全スタッフの休み合計を計算（警告用）
    def get_total_offs_per_day():
        total_counts = {}
        for staff in st.session_state.requests:
            for date, state in st.session_state.requests[staff].items():
                if state > 0: # 公休(1)または有給(2)
                    total_counts[date] = total_counts.get(date, 0) + 1
        return total_counts
    
    total_offs = get_total_offs_per_day()
    
    # カレンダー描画関数
    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-bar'>{month_label}月</div>", unsafe_allow_html=True)
        
        # 曜日ヘッダー
        weekdays = ["月", "火",
