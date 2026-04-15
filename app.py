import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：完全修正版", layout="centered")

# --- 崩れを防止しつつ密着させる最強CSS ---
st.markdown("""
    <style>
    /* 設定エリアの見た目 */
    .config-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ffb6c1;
        margin-bottom: 20px;
    }

    /* カレンダーの列が潰れないように固定 */
    [data-testid="column"] {
        min-width: 50px !important;
        padding: 0px 1px !important;
    }
    
    /* 縦方向の隙間をカット */
    [data-testid="stVerticalBlock"] > div {
        gap: 0px !important;
    }

    /* ボタンを正方形に近い形に固定 */
    div.stButton > button {
        width: 100% !important;
        height: 70px !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 2px !important;
        border: 1px solid #ddd !important;
        font-size: 13px !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
    }

    /* 曜日ヘッダー */
    .weekday-header {
        font-weight: bold;
        color: #ff69b4;
        text-align: center;
        background-color: #fdfdfd;
        border: 1px solid #ddd;
        padding: 10px 0;
        font-size: 14px;
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

# --- 設定エリア（メイン画面に配置） ---
st.markdown("<div class='config-box'>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    target_month = st.selectbox("📅 対象月：", ["2026年6月分", "2026年7月分"])
with col_b:
    off_count = st.number_input("🔢 公休回数：", value=8)
st.markdown("</div>", unsafe_allow_html=True)

st.write("### ｜ ステップ1：希望入力")
staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("👤 スタッフを選択：", staff_list)

if selected_staff not in st.session_state.requests:
    st.session_state.requests[selected_staff] = {}

# 警告チェック用（合計休み数）
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

    # 日付ボタンを7日ごとに折り返して表示
    current_day = start_day
    while current_day <= end_day:
        row_cols = st.columns(7)
        for i in range(7):
            if current_day <= end_day:
                date_key = f"{month_label}/{current_day}"
                state = st.session_state.requests[selected_staff].get(date_key, 0)
                
                # 警告アイコン（3人以上休み）
                count = total_offs.get(date_key, 0)
                warning = "⚠️" if count >= 3 else ""
                
                if state == 1:
                    label = f"公休\n{current_day}{warning}"
                    bg = "#ffb6c1"
                elif state == 2:
                    label = f"有給\n{current_day}{warning}"
                    bg = "#ffa500"
                else:
                    label = f"\n{current_day}{warning}" # 白の状態はシンプルに
                    bg = "#ffffff"

                if row_cols[i].button(label, key=f"btn_{date_key}"):
                    st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                    st.rerun()
                
                # 個別に色を設定
                st.markdown(f"<style>div[data-testid='stButton'] button[key='btn_{date_key}'] {{ background-color: {bg} !important; color: black !important; }}</style>", unsafe_allow_html=True)
                current_day += 1

draw_calendar("6", 11, 30)
draw_calendar("7", 1, 10)

st.write("---")
if st.button("🚀 この希望内容でシフトを自動作成する", type="primary", use_container_width=True):
    st.balloons()
    st.success("スプレッドシートへの保存機能は、次のステップで実装します！")
