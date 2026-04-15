import streamlit as st
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：隙間なしカスタム", layout="centered")

# --- 【超重要】隙間をなくすための魔法のCSS ---
st.markdown("""
    <style>
    /* 全体のコンテナの隙間を消す */
    [data-testid="stVerticalBlock"] > div {
        gap: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    
    /* カラム（列）同士の左右の隙間を最小にする */
    [data-testid="column"] {
        padding: 0px 1px !important;
    }

    /* ボタン自体の設定 */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 0px !important; /* 四角くして密着感を出す */
        margin: 0px !important;
        padding: 0px !important;
        border: 1px solid #ddd !important;
        line-height: 1.2 !important;
        display: block !important;
    }

    /* 曜日ヘッダーの設定 */
    .weekday-header {
        font-weight: bold;
        color: #ff69b4;
        text-align: center;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        padding: 5px 0;
        font-size: 14px;
    }

    /* 月ヘッダーの設定 */
    .calendar-header {
        background-color: #ffb6c1;
        color: white;
        text-align: center;
        padding: 8px;
        font-weight: bold;
        margin-top: 20px;
        border: 1px solid #ffb6c1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- データの記録（セッション状態）の初期化 ---
if "requests" not in st.session_state:
    st.session_state.requests = {}

# --- メイン画面 ---
st.title("🌸 シフト自動作成アプリ")

with st.expander("⚙️ 基本設定"):
    target_month = st.selectbox("対象月：", ["2026年6月分", "2026年7月分"])
    off_count = st.number_input("公休回数：", value=8)

st.write("### ｜ ステップ1：希望入力")
mode = st.radio("入力モード：", ["希望入力モード", "全員出勤日設定"], horizontal=True)

staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("スタッフを選択：", staff_list)

if selected_staff not in st.session_state.requests:
    st.session_state.requests[selected_staff] = {}

# 警告チェック用
def get_total_offs_per_day():
    total_counts = {}
    for staff in st.session_state.requests:
        for date, state in st.session_state.requests[staff].items():
            if state > 0: total_counts[date] = total_counts.get(date, 0) + 1
    return total_counts

total_offs = get_total_offs_per_day()

# --- カレンダー描画関数 ---
def draw_calendar(month_label, start_day, end_day):
    st.markdown(f"<div class='calendar-header'>{month_label}月</div>", unsafe_allow_html=True)
    
    # 曜日
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        cols[i].markdown(f"<div class='weekday-header'>{wd}</div>", unsafe_allow_html=True)

    # 日付（ここからボタンをギュッと並べる）
    current_day = start_day
    while current_day <= end_day:
        cols = st.columns(7)
        for i in range(7):
            if current_day <= end_day:
                date_key = f"{month_label}/{current_day}"
                state = st.session_state.requests[selected_staff].get(date_key, 0)
                warning = "⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                
                # 状態ごとの設定
                if state == 1:
                    label = f"公休\n{current_day}{warning}"
                    bg_color = "#ffb6c1"
                elif state == 2:
                    label = f"有給\n{current_day}{warning}"
                    bg_color = "#ffa500"
                else:
                    label = f"{current_day}{warning}"
                    bg_color = "#ffffff"

                # ボタン
                if cols[i].button(label, key=f"btn_{date_key}"):
                    st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                    st.rerun()
                
                # 個別に色を塗る
                st.markdown(f"<style>div[data-testid='stButton'] button[key='btn_{date_key}'] {{ background-color: {bg_color} !important; }}</style>", unsafe_allow_html=True)
                current_day += 1

# カレンダー表示
draw_calendar("6", 11, 30)
draw_calendar("7", 1, 10)

st.write("---")
if st.button("✨ シフト自動作成開始", type="primary", use_container_width=True):
    st.balloons()
