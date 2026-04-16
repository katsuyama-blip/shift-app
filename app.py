import streamlit as st
import pandas as pd
import io

# --- 1. ページ設定 ---
st.set_page_config(page_title="神シフト作成：集計機能版", layout="wide")

# --- 2. CSS（見た目調整：こだわりレイアウト維持） ---
st.markdown("""
    <style>
    .block-container { padding: 1.5rem 2rem !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    [data-testid="column"] { border: 0.5px solid #ddd !important; padding: 0px !important; }
    div.stButton > button {
        width: 100% !important; height: 85px !important;
        border-radius: 0px !important; background-color: white;
        font-size: 18px !important; font-weight: bold; white-space: pre-wrap !important;
    }
    button:has(div p:contains("公休")) { background-color: #ffb6c1 !important; color: white !important; }
    button:has(div p:contains("有給")) { background-color: #ffa500 !important; color: white !important; }
    .month-bar { background-color: #ffb6c1; color: white; text-align: center; padding: 10px; font-weight: bold; font-size: 1.5em; }
    .weekday { text-align: center; background-color: #f8f9fa; color: #ff69b4; border: 0.5px solid #ddd; font-weight: bold; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. セッション状態の初期化 ---
if "requests" not in st.session_state: st.session_state.requests = {}
if "result_df" not in st.session_state: st.session_state.result_df = None

st.title("🌸 シフト自動作成アプリ")

# 設定エリア
with st.container(border=True):
    col_a, col_b = st.columns(2)
    with col_a: target_month = st.selectbox("📅 対象月", ["2026年6月分", "2026年7月分"])
    with col_b: off_count = st.number_input("🔢 公休回数", value=8)

tab1, tab2 = st.tabs(["👥 スタッフ休み希望", "📊 作成結果・出力（集計付き）"])

# --- タブ1：休み希望入力 ---
with tab1:
    staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
    selected_staff = st.selectbox("スタッフを選択", staff_list)
    if selected_staff not in st.session_state.requests: st.session_state.requests[selected_staff] = {}

    def draw_calendar(month_label, start_day, end_day):
        st.markdown(f"<div class='month-bar'>{month_label}月</div>", unsafe_allow_html=True)
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        h_cols = st.columns(7)
        for i, wd in enumerate(weekdays): h_cols[i].markdown(f"<div class='weekday'>{wd}</div>", unsafe_allow_html=True)
        
        day = start_day
        while day <= end_day:
            cols = st.columns(7)
            for i in range(7):
                if day <= end_day:
                    date_key = f"{month_label}/{day}"
                    state = st.session_state.requests[selected_staff].get(date_key, 0)
                    label = f"公休\n{day}" if state == 1 else (f"有給\n{day}" if state == 2 else f"\n{day}")
                    if cols[i].button(label, key=f"btn_{date_key}"):
                        st.session_state.requests[selected_staff][date_key] = (state + 1) % 3
                        st.rerun()
                    day += 1
    draw_calendar("6", 11, 30)
    draw_calendar("7", 1, 10)

# --- タブ2：結果表示 ＆ 集計機能 ---
with tab2:
    if st.button("🚀 最新の希望でシフトを作成する", type="primary", use_container_width=True):
        with st.spinner("ルールを確認しながら計算中..."):
            # 1. 日付リストの作成
            dates = [f"6/{d}" for d in range(11,31)] + [f"7/{d}" for d in range(1,11)]
            
            # 2. 仮のシフトデータを作成（ここに昨日の最強エンジンを繋ぎます）
            # デモ用にランダムに早番・中番・遅番を混ぜてみます
            import random
            shifts = ["早番", "中番", "遅番", "公休", "有給"]
            data = []
            for staff in staff_list:
                row = [random.choice(shifts) for _ in dates]
                data.append(row)
            
            df = pd.DataFrame(data, index=staff_list, columns=dates)
            
            # 3. 【店長の要望！】各個人の集計カウントを追加
            df['合計公休'] = (df[dates] == "公休").sum(axis=1)
            df['合計有給'] = (df[dates] == "有給").sum(axis=1)
            df['早番数'] = (df[dates] == "早番").sum(axis=1)
            df['中番数'] = (df[dates] == "中番").sum(axis=1)
            df['遅番数'] = (df[dates] == "遅番").sum(axis=1)
            
            st.session_state.result_df = df
            st.balloons()

    if st.session_state.result_df is not None:
        st.write("### 📅 作成結果（右側に合計数があります）")
        # 見やすいように表を表示
        st.dataframe(st.session_state.result_df)

        # 出力
        csv = st.session_state.result_df.to_csv().encode('utf-8-sig')
        st.download_button("📊 集計データ付きCSVを保存", data=csv, file_name="shift_summary.csv", mime="text/csv")
