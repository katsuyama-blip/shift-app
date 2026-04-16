import streamlit as st

# --- 1. ページ設定 ---
st.set_page_config(page_title="神シフト作成：バランス調整版", layout="wide")

# --- 2. CSS調整（文字サイズを「ちょうどいい」大きさに） ---
st.markdown("""
    <style>
    /* カレンダー全体の設定 */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; padding: 0px !important; }

    /* ボタンのデザイン：枠に対して「程よい」サイズ感 */
    div.stButton > button {
        width: 100% !important;
        height: 85px !important; /* 高さを少し抑えてバランス調整 */
        border-radius: 0px !important;
        margin: 0px !important;
        border: 0.5px solid #eee !important;
        background-color: white;
        color: #333;
        display: flex !important;
        white-space: pre-wrap !important;
        font-size: 18px !important; /* 日付を「程よく」大きく */
        font-weight: bold !important;
        line-height: 1.2 !important;
    }

    /* 公休・有給の時の色と文字の見え方 */
    button:has(div p:contains("公休")) { 
        background-color: #ffb6c1 !important; 
        color: white !important; 
        font-size: 14px !important; /* 文字が入る時は少しフォントを調整 */
    }
    button:has(div p:contains("有給")) { 
        background-color: #ffa500 !important; 
        color: white !important;
        font-size: 14px !important;
    }

    /* 曜日・月ヘッダー */
    .weekday { text-align: center; background-color: #f8f9fa; color: #ff69b4; font-weight: bold; border: 0.5px solid #eee; padding: 10px 0; font-size: 14px; }
    .month-bar { background-color: #ffb6c1; color: white; text-align: center; font-weight: bold; padding: 10px; font-size: 1.2em; margin-top: 20px; }
    
    /* ボタン内のテキストの余白調整 */
    div.stButton > button p {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. セッション状態の初期化 ---
if "requests" not in st.session_state:
    st.session_state.requests = {}

# --- 4. メイン画面 ---
st.title("🌸 シフト自動作成アプリ")

with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        target_month = st.selectbox("📅 対象月", ["2026年6月分", "2026年7月分"])
    with col_b:
        off_count = st.number_input("🔢 公休回数", value=8)

st.write("### ｜ ステップ1：希望入力")
tab1, tab2 = st.tabs(["休み希望（スタッフ）", "全員出勤日（会議）設定"])

with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("👤 スタッフを選択", staff_list)
    if selected_staff not in st.session_state.requests:
        st.session_state.requests[selected_staff] = {}

    # 合計休みチェック
    total_offs = {}
    for s in st.session_state.requests:
        for d, val in st.session_state.requests[s].items():
            if val > 0: total_offs[d] = total_offs.get(d, 0) + 1

    # カレンダー描画
    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-bar'>{month_label}月</div>", unsafe_allow_html=True)
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
                    warning = "⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                    
                    if state == 1: label = f"公休\n{day}{warning}"
                    elif state == 2: label = f"有給\n{day}{warning}"
                    else: label = f"\n{day}{warning}"

                    if row_cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1

    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

with tab2:
    st.write("🏢 会議日（全員出勤）の設定（準備中）")

st.write("---")
if st.button("🚀 この内容でシフトを作成する", type="primary", use_container_width=True):
    st.balloons()
    st.success("希望を保存しました！スプレッドシートへの連動を開始します。")
