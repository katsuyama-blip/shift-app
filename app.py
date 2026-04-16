import streamlit as st
import pandas as pd

# --- 1. ページ設定（スタイリッシュにするため、あえてwideにせず中央寄せ） ---
st.set_page_config(page_title="神シフト作成：スタイリッシュ版", layout="centered")

# --- 2. 店長のこだわりデザイン（CSS） ---
st.markdown("""
    <style>
    /* 全体のフォントと背景 */
    html, body, [class*="css"]  {
        font-family: 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
    }
    
    /* カレンダーの横幅をキュッと絞る */
    .stMainBlockContainer {
        max-width: 500px !important;
        margin: 0 auto;
    }

    /* 【店長のこだわり】枠を消して、数字の周りに色をつける */
    div.stButton > button {
        border: none !important; /* 枠を消去 */
        background-color: transparent !important; /* 基本は透明 */
        color: #333 !important;
        font-size: 18px !important;
        height: 50px !important;
        width: 50px !important;
        margin: 5px auto !important;
        border-radius: 50% !important; /* 丸くする */
        transition: 0.3s;
    }

    /* 公休（ピンク） */
    button:has(div p:contains("公休")) {
        background-color: #ffb6c1 !important;
        color: white !important;
    }
    /* 有給（オレンジ） */
    button:has(div p:contains("有給")) {
        background-color: #ffa500 !important;
        color: white !important;
    }

    /* 曜日ヘッダー */
    .weekday {
        text-align: center;
        color: #ff69b4;
        font-weight: bold;
        font-size: 14px;
        padding-bottom: 10px;
    }
    
    /* 月ヘッダー */
    .month-header {
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        color: #ffb6c1;
        margin: 20px 0 10px 0;
    }

    /* タブのデザイン微調整 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. セッション状態の初期化 ---
if "requests" not in st.session_state:
    st.session_state.requests = {}

st.title("🌸 シフト自動作成")

# --- 設定エリア ---
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        target_month = st.selectbox("対象月", ["2026年6月分", "2026年7月分"])
    with col_b:
        off_count = st.number_input("公休回数", value=8)

tab1, tab2 = st.tabs(["👥 休み希望", "📊 作成・出力"])

with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("スタッフを選択", staff_list)
    if selected_staff not in st.session_state.requests:
        st.session_state.requests[selected_staff] = {}

    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-header'>{month_label}月</div>", unsafe_allow_html=True)
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        cols = st.columns(7)
        for i, wd in enumerate(weekdays):
            cols[i].markdown(f"<div class='weekday'>{wd}</div>", unsafe_allow_html=True)
        
        day = start_day
        while day <= end_day:
            row_cols = st.columns(7)
            for i in range(7):
                if day <= end_day:
                    date_key = f"{month_label}/{day}"
                    state = st.session_state.requests[selected_staff].get(date_key, 0)
                    
                    # ラベル。枠がないので、状態がわかるように文字を変える
                    if state == 1: label = f"公休\n{day}"
                    elif state == 2: label = f"有給\n{day}"
                    else: label = f"{day}"

                    if row_cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1

    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

with tab2:
    st.info("集計結果がここに表示されます")
    if st.button("🚀 シフトを作成する", type="primary", use_container_width=True):
        st.balloons()
