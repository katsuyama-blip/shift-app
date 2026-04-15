import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：完成版", layout="centered")

# --- 究極のCSS（色・隙間・崩れ防止） ---
st.markdown("""
    <style>
    /* 1. タイトル下の謎の空欄を消し、設定エリアを綺麗にする */
    [data-testid="stExpander"] { border: 1px solid #ffb6c1; border-radius: 10px; }
    
    /* 2. カレンダーの「個室」を正しく作る */
    .stButton > button {
        width: 100% !important;
        min-height: 70px !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 0.5px solid #eee !important;
        font-weight: bold !important;
        display: block !important;
    }

    /* 3. 【最重要】文字を見て色を変える（魔法のセレクタ） */
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

    /* 4. 隙間をピシッと埋める */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }
    
    /* 曜日ヘッダー */
    .weekday {
        text-align: center;
        background-color: #f8f9fa;
        color: #ff69b4;
        font-weight: bold;
        border: 0.5px solid #eee;
        padding: 10px 0;
        font-size: 0.8em;
    }
    .month-bar {
        background-color: #ffb6c1;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 5px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# データの記録
if "requests" not in st.session_state:
    st.session_state.requests = {}

st.title("🌸 シフト自動作成アプリ")

# --- 設定エリア（枠で囲む） ---
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        target_month = st.selectbox("📅 対象月", ["2026年6月分", "2026年7月分"])
    with col_b:
        off_count = st.number_input("🔢 公休回数", value=8)

st.write("### ｜ ステップ1：希望入力")
staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("👤 スタッフを選択", staff_list)

if selected_staff not in st.session_state.requests:
    st.session_state.requests[selected_staff] = {}

# 警告チェック
total_offs = {}
for staff, days in st.session_state.requests.items():
    for d, s in days.items():
        if s > 0: total_offs[d] = total_offs.get(d, 0) + 1

# --- カレンダー描画 ---
def draw_calendar(month_name, start_day, end_day):
    st.markdown(f"<div class='month-bar'>{month_name}月</div>", unsafe_allow_html=True)
    
    # 曜日
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        cols[i].markdown(f"<div class='weekday'>{wd}</div>", unsafe_allow_html=True)

    # 日付
    day = start_day
    while day <= end_day:
        cols = st.columns(7)
        for i in range(7):
            if day <= end_day:
                date_key = f"{month_name}/{day}"
                state = st.session_state.requests[selected_staff].get(date_key, 0)
                warning = "⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                
                # ラベル作成
                if state == 1: label = f"公休\n{day}{warning}"
                elif state == 2: label = f"有給\n{day}{warning}"
                else: label = f"\n{day}{warning}"

                if cols[i].button(label, key=f"b_{date_key}"):
                    st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                    st.rerun()
                day += 1

draw_calendar("6", 11, 30)
draw_calendar("7", 1, 10)

st.write("---")
if st.button("🚀 この内容でシフトを作成する", type="primary", use_container_width=True):
    st.balloons()
