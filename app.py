import streamlit as st

# --- 1. ページ設定 ---
st.set_page_config(page_title="神シフト作成", layout="centered")

# --- 2. デザイン調整パネル（サイドバー） ---
st.sidebar.title("🎨 見た目の微調整")
date_size = st.sidebar.slider("日付の大きさ", 10, 30, 20)
text_size = st.sidebar.slider("公休・有給の文字", 5, 15, 9)
btn_round = st.sidebar.slider("ボタンの丸み", 0, 50, 50)

# --- 3. 動的CSS（スライダーの値がここに反映されます） ---
st.markdown(f"""
    <style>
    .block-container {{ max-width: 500px !important; }}

    /* ボタンの基本スタイル */
    div.stButton > button[key^="btn_"] {{
        border: none !important;
        background-color: #f0f2f6 !important;
        color: #333 !important;
        width: 60px !important;
        height: 60px !important;
        margin: 5px auto !important;
        border-radius: {btn_round}% !important;
        display: block !important;
        white-space: pre-wrap !important;
        line-height: 1.1 !important;
        padding: 0 !important;
    }}

    /* ★ここがポイント：日付（1行目）と文字（2行目）のサイズ分け */
    div.stButton > button[key^="btn_"] p {{
        font-size: {text_size}px !important; /* 全体の基本サイズ（文字用） */
        font-weight: normal !important;
    }}
    div.stButton > button[key^="btn_"] p::first-line {{
        font-size: {date_size}px !important; /* 1行目（日付）だけ大きく */
        font-weight: bold !important;
    }}

    /* 公休（ピンク）常時固定 */
    div.stButton > button[key^="btn_"]:has(div p:contains("公休")) {{
        background-color: #ffb6c1 !important;
        color: white !important;
    }}
    /* 有給（オレンジ）常時固定 */
    div.stButton > button[key^="btn_"]:has(div p:contains("有給")) {{
        background-color: #ffa500 !important;
        color: white !important;
    }}

    /* 作成ボタン（ピンク） */
    div.stButton > button[kind="primary"] {{
        background-color: #ffb6c1 !important;
        width: 100% !important;
        height: 55px !important;
        border-radius: 30px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }}
    
    .weekday {{ text-align: center; color: #ff69b4; font-weight: bold; font-size: 14px; margin-bottom: 10px; }}
    .month-header {{ text-align: center; font-weight: bold; font-size: 22px; color: #ffb6c1; margin: 25px 0 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

# セッション管理
if "requests" not in st.session_state: st.session_state.requests = {}

st.title("🌸 シフト自動作成")

# 設定
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a: target_month = st.selectbox("対象月", ["2026年6月分", "2026年7月分"])
    with col_b: off_count = st.number_input("公休回数", value=8)

tab1, tab2 = st.tabs(["👥 休み希望（スタッフ）", "🏢 全員出勤（会議）設定"])

with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("スタッフを選択", staff_list)
    if selected_staff not in st.session_state.requests: st.session_state.requests[selected_staff] = {}

    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-header'>{month_label}月</div>", unsafe_allow_html=True)
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        cols = st.columns(7)
        for i, wd in enumerate(weekdays): cols[i].markdown(f"<div class='weekday'>{wd}</div>", unsafe_allow_html=True)
        
        day = start_day
        while day <= end_day:
            row_cols = st.columns(7)
            for i in range(7):
                if day <= end_day:
                    date_key = f"{month_label}/{day}"
                    state = st.session_state.requests[selected_staff].get(date_key, 0)
                    if state == 1: label = f"{day}\n公休"
                    elif state == 2: label = f"{day}\n有給"
                    else: label = f"{day}\n "

                    if row_cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1
    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

st.write("---")
st.write("### ｜ ステップ2：作成と保存")
if st.button("🚀 この内容でシフトを作成する", type="primary"):
    st.balloons()
