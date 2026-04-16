import streamlit as st

# --- 1. ページ設定（ワイドモードで広く使う） ---
st.set_page_config(page_title="神シフト作成：密着・復活版", layout="wide")

# --- 2. 隙間を極限まで削るCSS ---
st.markdown("""
    <style>
    /* 画面全体の余白を削る */
    .block-container { padding: 2rem 2rem !important; }
    
    /* カラム（列）同士の隙間をゼロにする */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }
    
    /* 1つ1つのセルの枠線とサイズ設定 */
    [data-testid="column"] {
        border: 0.5px solid #ddd !important; /* 境界線を引く */
        margin: 0px !important;
        padding: 0px !important;
    }

    /* ボタンのデザイン：枠いっぱいに広げて画像のようなカレンダーに */
    div.stButton > button {
        width: 100% !important;
        height: 90px !important; /* 高さをしっかり確保 */
        border: none !important; /* ボタン自体の線は消す */
        border-radius: 0px !important;
        background-color: white;
        color: #333;
        font-size: 20px !important; /* 日付を大きく */
        font-weight: bold;
        white-space: pre-wrap !important;
    }

    /* 公休・有給の時の色（確実に反映） */
    button:has(div p:contains("公休")) { background-color: #ffb6c1 !important; color: white !important; }
    button:has(div p:contains("有給")) { background-color: #ffa500 !important; color: white !important; }

    /* 月と曜日のヘッダーデザイン */
    .month-bar { 
        background-color: #ffb6c1; color: white; text-align: center; 
        padding: 10px; font-weight: bold; font-size: 1.5em; margin-top: 10px;
    }
    .weekday { 
        text-align: center; background-color: #f8f9fa; color: #ff69b4; 
        border: 0.5px solid #ddd; font-weight: bold; padding: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. データの記録（セッション） ---
if "requests" not in st.session_state:
    st.session_state.requests = {}

# --- 4. メイン画面の構築 ---
st.title("🌸 シフト自動作成アプリ")

# 設定エリア
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a:
        target_month = st.selectbox("📅 対象月", ["2026年6月分", "2026年7月分"])
    with col_b:
        off_count = st.number_input("🔢 公休回数", value=8)

st.write("### ｜ ステップ1：希望入力")
tab1, tab2 = st.tabs(["👥 スタッフ休み希望", "🏢 全員出勤（会議）設定"])

with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("スタッフを選択してください", staff_list)
    
    if selected_staff not in st.session_state.requests:
        st.session_state.requests[selected_staff] = {}

    # 全スタッフの休み状況を集計
    total_offs = {}
    for s, days in st.session_state.requests.items():
        for d, val in days.items():
            if val > 0: total_offs[d] = total_offs.get(d, 0) + 1

    # カレンダーを描く関数
    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-bar'>{month_label}月</div>", unsafe_allow_html=True)
        
        # 曜日ヘッダー
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        header_cols = st.columns(7)
        for i, wd in enumerate(weekdays):
            header_cols[i].markdown(f"<div class='weekday'>{wd}</div>", unsafe_allow_html=True)

        # 日付ボタン
        day = start_day
        while day <= end_day:
            cols = st.columns(7)
            for i in range(7):
                if day <= end_day:
                    date_key = f"{month_label}/{day}"
                    state = st.session_state.requests[selected_staff].get(date_key, 0)
                    warning = " ⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                    
                    if state == 1: label = f"公休\n{day}{warning}"
                    elif state == 2: label = f"有給\n{day}{warning}"
                    else: label = f"\n{day}{warning}"

                    if cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1

    # カレンダー表示
    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

with tab2:
    st.info("会議日などの設定をここに追加予定です。")

st.write("---")
if st.button("🚀 この希望でシフトを作成する", type="primary", use_container_width=True):
    st.balloons()
    st.success("希望を受け付けました！")
