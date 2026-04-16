import streamlit as st

# --- 1. ページ設定（スタイリッシュな中央寄せ） ---
st.set_page_config(page_title="神シフト作成", layout="centered")

# --- 2. デザインの修正（色固定・タブ・ピンクボタン） ---
st.markdown("""
    <style>
    /* 画面の横幅を絞る */
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }

    /* 【こだわり】カレンダーボタン：丸型、色固定、数字が上・文字が下 */
    div.stButton > button {
        border: none !important;
        background-color: #f0f2f6 !important;
        color: #333 !important;
        width: 60px !important;
        height: 60px !important;
        margin: 5px auto !important;
        border-radius: 50% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.1 !important;
    }

    /* 公休（ピンク）を常時固定 */
    div.stButton > button:has(div p:contains("公休")) {
        background-color: #ffb6c1 !important;
        color: white !important;
    }

    /* 有給（オレンジ）を常時固定 */
    div.stButton > button:has(div p:contains("有給")) {
        background-color: #ffa500 !important;
        color: white !important;
    }

    /* 【新規】一番下の「作成・出力」ボタンをピンクにする */
    div.stButton > button[kind="primary"] {
        background-color: #ffb6c1 !important;
        border-color: #ffb6c1 !important;
        color: white !important;
        height: 50px !important;
        border-radius: 25px !important; /* 角丸でスタイリッシュに */
        font-size: 18px !important;
        margin-top: 30px !important;
    }

    /* 曜日の見た目 */
    .weekday { text-align: center; color: #ff69b4; font-weight: bold; font-size: 14px; margin-bottom: 10px; }
    /* 月の見た目 */
    .month-header { text-align: center; font-weight: bold; font-size: 22px; color: #ffb6c1; margin: 25px 0 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# データの記録
if "requests" not in st.session_state: st.session_state.requests = {}
if "meetings" not in st.session_state: st.session_state.meetings = {}

st.title("🌸 シフト自動作成")

# 設定エリア
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a: target_month = st.selectbox("対象月", ["2026年6月分", "2026年7月分"])
    with col_b: off_count = st.number_input("公休回数", value=8)

# --- タブ設定：作成・出力を外して「全員出勤設定」を入れる ---
st.write("### ｜ ステップ1：希望入力")
tab1, tab2 = st.tabs(["👥 休み希望", "📅 全員出勤設定"])

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
                    
                    if state == 1: label = f"{day}\n公休"
                    elif state == 2: label = f"{day}\n有給"
                    else: label = f"{day}"

                    if row_cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1
    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

with tab2:
    st.write("#### 🏢 全員出勤日（会議）の設定")
    st.info("会議や研修など、全員が出勤しなければならない日をカレンダーで選んでください。")
    # 会議設定用のカレンダーも同様に作れますが、まずは構成を優先しました

# --- ページの一番下に配置：作成・出力 ---
st.write("---")
st.write("### ｜ ステップ2：作成と保存")
if st.button("🚀 シフトを作成してスプレッドシートへ出力", type="primary", use_container_width=True):
    st.balloons()
    st.success("スプレッドシートへの出力準備が整いました！")
