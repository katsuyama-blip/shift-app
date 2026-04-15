import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：隙間なし・崩れなし版", layout="centered")

# --- 隙間をなくしつつ、形をキープする魔法のCSS ---
st.markdown("""
    <style>
    /* 縦方向の隙間を消す */
    [data-testid="stVerticalBlock"] > div {
        gap: 0px !important;
    }
    /* 横方向の行の隙間を消す */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }
    
    /* カラム（列）の設定：幅を均等にして余計なパディングを削る */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* ボタンのデザイン：幅100%で隣と密着させる */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        border-radius: 0px !important; /* 四角くして密着 */
        margin: 0px !important;
        padding: 0px !important;
        border: 1px solid #eeeeee !important; /* 薄い線で区切る */
        font-size: 14px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 曜日ヘッダー */
    .weekday-header {
        font-weight: bold;
        color: #ff69b4;
        text-align: center;
        background-color: #fdfdfd;
        border: 1px solid #eeeeee;
        padding: 10px 0;
        font-size: 14px;
        width: 100%;
    }

    /* 月ヘッダー */
    .calendar-header {
        background-color: #ffb6c1;
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        margin-top: 20px;
        border: 1px solid #ffb6c1;
    }
    </style>
    """, unsafe_allow_html=True)

# データの記録
if "requests" not in st.session_state:
    st.session_state.requests = {}

st.title("🌸 シフト自動作成アプリ")

# 設定
with st.sidebar:
    st.write("### ⚙️ 設定")
    off_count = st.number_input("公休回数：", value=8)

st.write("### ｜ ステップ1：希望入力")
staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("スタッフを選択：", staff_list)

if selected_staff not in st.session_state.requests:
    st.session_state.requests[selected_staff] = {}

# 合計休み数チェック
def get_total_offs_per_day():
    counts = {}
    for staff in st.session_state.requests:
        for d, s in st.session_state.requests[staff].items():
            if s > 0: counts[d] = counts.get(d, 0) + 1
    return counts

total_offs = get_total_offs_per_day()

# --- カレンダー描画 ---
def draw_calendar(month_label, start_day, end_day):
    st.markdown(f"<div class='calendar-header'>{month_label}月</div>", unsafe_allow_html=True)
    
    # 曜日
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        cols[i].markdown(f"<div class='weekday-header'>{wd}</div>", unsafe_allow_html=True)

    # 日付ボタンを1週間（7日）ごとに並べる
    current_day = start_day
    while current_day <= end_day:
        row_cols = st.columns(7)
        for i in range(7):
            if current_day <= end_day:
                date_key = f"{month_label}/{current_day}"
                state = st.session_state.requests[selected_staff].get(date_key, 0)
                warning = " ⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                
                if state == 1:
                    label = f"公休\n{current_day}{warning}"
                    bg = "#ffb6c1"
                elif state == 2:
                    label = f"有給\n{current_day}{warning}"
                    bg = "#ffa500"
                else:
                    label = f"{current_day}{warning}"
                    bg = "#ffffff"

                if row_cols[i].button(label, key=f"btn_{date_key}"):
                    st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                    st.rerun()
                
                # ボタン色設定
                st.markdown(f"<style>div[data-testid='stButton'] button[key='btn_{date_key}'] {{ background-color: {bg} !important; }}</style>", unsafe_allow_html=True)
                current_day += 1

draw_calendar("6", 11, 30)
draw_calendar("7", 1, 10)

st.write("---")
if st.button("🚀 この希望でシフトを作成する", type="primary", use_container_width=True):
    st.balloons()
