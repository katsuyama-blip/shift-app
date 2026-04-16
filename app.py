import streamlit as st

# --- 1. ページ設定（スタイリッシュな中央寄せ） ---
st.set_page_config(page_title="神シフト作成", layout="centered")

# --- 2. 徹底的に見た目を整える【真・完成版CSS】 ---
st.markdown("""
    <style>
    /* 画面の横幅をスマホっぽくキュッと絞る */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
        margin: auto !important;
    }

    /* タブの並び順調整（会議設定を休み希望の横に） */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }

    /* 曜日の見た目（ピンクでスタイリッシュ） */
    .weekday {
        text-align: center;
        color: #ff69b4;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    /* 月ヘッダー */
    .month-header {
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        color: #ffb6c1;
        margin: 30px 0 10px 0;
    }

    /* 【店長のこだわり】カレンダーボタンを丸く、色常時固定 */
    /* ※下の「作成ボタン」には影響しないように、カレンダー専用のキー(btn_)をターゲットにする */
    div.stButton > button[key^="btn_"] {
        border: none !important;
        background-color: #f0f2f6 !important; /* 通常時は薄いグレー */
        color: #333 !important;
        width: 60px !important;
        height: 60px !important;
        margin: 5px auto !important;
        border-radius: 50% !important; /* まん丸 */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.1 !important;
        transition: all 0.2s ease-in-out;
    }

    /* ボタン内のテキストのフォント設定（Markdownの改行を有効化） */
    div.stButton > button[key^="btn_"] div p {
        margin: 0 !important;
        padding: 0 !important;
        white-space: pre-wrap !important;
        font-size: 18px !important; /* 日付のサイズ（大きく） */
        font-weight: bold !important;
    }
    
    /* 公休・有給の文字サイズ（極小） */
    div.stButton > button[key^="btn_"] div p small {
        font-size: 9px !important; /* 文字を極小に */
        font-weight: normal !important;
        display: block !important;
    }

    /* ★公休（ピンク）常時固定★ */
    div.stButton > button[key^="btn_"]:has(small:contains("公休")) {
        background-color: #ffb6c1 !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(255, 182, 193, 0.4);
    }
    div.stButton > button[key^="btn_"]:has(small:contains("公休")) div p {
        color: white !important;
    }

    /* ★有給（オレンジ）常時固定★ */
    div.stButton > button[key^="btn_"]:has(small:contains("有給")) {
        background-color: #ffa500 !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(255, 165, 0, 0.4);
    }
    div.stButton > button[key^="btn_"]:has(small:contains("有給")) div p {
        color: white !important;
    }

    /* 【リベンジ】一番下の「作成・出力」ボタンをスタイリッシュなピンクに */
    div.stButton > button[kind="primary"] {
        background-color: #ffb6c1 !important;
        border: none !important;
        color: white !important;
        height: 50px !important;
        border-radius: 25px !important; /* 丸ではなく、角丸のスタイリッシュなボタン */
        font-size: 18px !important;
        font-weight: bold !important;
        margin-top: 40px !important;
        width: 100% !important; /* カレンダーの幅に合わせる */
    }
    div.stButton > button[kind="primary"]:hover {
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# データの記録（セッション）
if "requests" not in st.session_state: st.session_state.requests = {}
if "meetings" not in st.session_state: st.session_state.meetings = {}

st.title("🌸 シフト自動作成")

# --- 設定エリア ---
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a: target_month = st.selectbox("対象月", ["2026年6月分", "2026年7月分"])
    with col_b: off_count = st.number_input("公休回数", value=8)

st.write("### ｜ ステップ1：希望入力")

# --- タブ設定：並び替え（休み希望 の横を 全員出勤設定 に） ---
tab1, tab2 = st.tabs(["👥 休み希望（スタッフ）", "🏢 全員出勤（会議）設定"])

# --- タブ1：休み希望（スタッフ） ---
with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("スタッフを選択してください", staff_list)
    if selected_staff not in st.session_state.requests:
        st.session_state.requests[selected_staff] = {}

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
                    
                    # 💡 【修正】数字の下に極小文字を配置（Markdownの <br> と <small> を活用）
                    # white-space: pre-wrap と組み合わせることで綺麗に並びます
                    if state == 1: label = f"**{day}**&nbsp;<br><small>公休</small>"
                    elif state == 2: label = f"**{day}**&nbsp;<br><small>有給</small>"
                    else: label = f"**{day}**&nbsp;<br>&nbsp;" # 空白を入れて、丸の高さを合わせる

                    if row_cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun() # 画面を更新して色を反映
                    day += 1

    # カレンダー表示（6月11日から）
    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

# --- タブ2：全員出勤（会議）設定 ---
with tab2:
    st.write("#### 🏢 会議日（全員出勤）を設定")
    st.info("会議、研修など、全員が出勤しなければならない日をカレンダーで選んでください（準備中）。")

# --- ページの一番下に配置：作成ボタン ---
st.write("---")
st.write("### ｜ ステップ2：シフト作成と保存")
# 【修正】type="primary" にすることで、CSSでピンクのスタイリッシュなボタンに変更
if st.button("🚀 最新の希望でシフトを作成し、スプレッドシートへ出力する", type="primary", use_container_width=True):
    st.balloons()
    st.success("スプレッドシートへの出力準備が完了しました！")
