import streamlit as st
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：店長カスタム", layout="centered")

# --- デザイン調整（CSS） ---
st.markdown("""
    <style>
    /* 個室風のグリッド枠線 */
    .day-cell {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
    }
    /* 曜日ヘッダー */
    .weekday-header {
        font-weight: bold;
        color: #ff69b4;
        text-align: center;
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        padding: 5px;
    }
    /* 月ヘッダー */
    .calendar-header {
        background-color: #ffb6c1;
        color: white;
        text-align: center;
        padding: 8px;
        font-weight: bold;
        margin-top: 20px;
    }
    /* 警告のビックリマーク */
    .warning-icon {
        color: red;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- データの記録（セッション状態）の初期化 ---
if "requests" not in st.session_state:
    st.session_state.requests = {} # {スタッフ名: {日付: 状態(0,1,2)}}

# --- メイン画面 ---
st.title("🌸 シフト自動作成アプリ")

# 設定エリア
with st.expander("⚙️ 基本設定"):
    target_month = st.selectbox("対象月：", ["2026年6月分", "2026年7月分"])
    off_count = st.number_input("公休回数：", value=8)

st.write("### ｜ ステップ1：希望入力")
mode = st.radio("入力モード：", ["希望入力モード（クリックで切り替え）", "全員出勤日設定"], horizontal=True)

staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("スタッフを選択：", staff_list)

# そのスタッフのデータがなければ作る
if selected_staff not in st.session_state.requests:
    st.session_state.requests[selected_staff] = {}

# --- 警告チェック用：全スタッフの休み合計を計算 ---
def get_total_offs_per_day():
    total_counts = {}
    for staff in st.session_state.requests:
        for date, state in st.session_state.requests[staff].items():
            if state > 0: # 公休(1)または有給(2)
                total_counts[date] = total_counts.get(date, 0) + 1
    return total_counts

total_offs = get_total_offs_per_day()

# --- カレンダー描画関数 ---
def draw_calendar(month_label, start_day, end_day):
    st.markdown(f"<div class='calendar-header'>{month_label}月</div>", unsafe_allow_html=True)
    
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        cols[i].markdown(f"<div class='weekday-header'>{wd}</div>", unsafe_allow_html=True)

    current_day = start_day
    while current_day <= end_day:
        cols = st.columns(7)
        for i in range(7):
            if current_day <= end_day:
                date_key = f"{month_label}/{current_day}"
                
                # 今のスタッフの状態
                state = st.session_state.requests[selected_staff].get(date_key, 0)
                
                # 警告アイコンの有無
                warning = " ⚠️" if total_offs.get(date_key, 0) >= 3 else ""
                
                # 状態に応じたラベルと色
                if state == 1:
                    label = f"公休\n{current_day}{warning}"
                    color = "#ffb6c1" # ピンク
                elif state == 2:
                    label = f"有給\n{current_day}{warning}"
                    color = "#ffa500" # オレンジ
                else:
                    label = f"{current_day}{warning}"
                    color = "#ffffff" # 白

                # ボタン（CSSで色を上書き）
                if cols[i].button(label, key=f"btn_{date_key}", use_container_width=True, help=f"合計休み数: {total_offs.get(date_key, 0)}"):
                    # 状態をサイクルさせる (0 -> 1 -> 2 -> 0)
                    new_state = (state + 1) % 3
                    st.session_state.requests[selected_staff][date_key] = new_state
                    st.rerun()
                
                # 背景色をつけるためのちょっとした工夫（簡易版）
                st.markdown(f"<style>div[data-testid='stButton'] button[key='btn_{date_key}'] {{ background-color: {color}; }}</style>", unsafe_allow_html=True)
                
                current_day += 1

# カレンダー表示
draw_calendar("6", 11, 30)
draw_calendar("7", 1, 10)

# --- 最終確認エリア ---
st.write("---")
st.write(f"#### 📝 {selected_staff}さんの入力状況")
staff_data = st.session_state.requests[selected_staff]
koukyu = [k for k, v in staff_data.items() if v == 1]
yukyu = [k for k, v in staff_data.items() if v == 2]

col1, col2 = st.columns(2)
with col1:
    st.write("【公休】", ", ".join(koukyu) if koukyu else "なし")
with col2:
    st.write("【有給】", ", ".join(yukyu) if yukyu else "なし")

if st.button("✨ シフト自動作成開始（スプレッドシート連動）", type="primary"):
    st.balloons()
