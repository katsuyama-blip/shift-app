import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from ortools.sat.python import cp_model
import pandas as pd
import datetime

# --- アプリの見た目設定 ---
st.set_page_config(page_title="店長専用！神シフト作成", layout="centered")
st.markdown("""
    <style>
    .stButton>button { background-color: #ffb6c1; color: white; border-radius: 20px; height: 3em; width: 100%; }
    .stSelectbox, .stNumberInput { border-radius: 10px; }
    h3 { color: #ff69b4; border-left: 5px solid #ffb6c1; padding-left: 10px; margin-top: 20px; }
    .calendar-header { background-color: #ffb6c1; color: white; text-align: center; padding: 5px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌸 シフト自動作成アプリ")

# --- 設定エリア ---
target_month = st.selectbox("対象月：", ["2026年6月分", "2026年7月分"])
off_count = st.number_input("公休回数：", value=8)

st.write("### ｜ ステップ1：希望入力")
mode = st.segmented_control("モード切替：", ["休み希望", "全員出勤日設定"], default="休み希望")

staff_list = ["板橋", "佐野", "山本", "坂田", "A", "時短さん"]
selected_staff = st.selectbox("スタッフ：", staff_list)

# カレンダーの見た目（イメージ）
st.markdown("<div class='calendar-header'>6月</div>", unsafe_allow_html=True)
cols = st.columns(7)
for i in range(11, 31):
    with cols[(i-11)%7]:
        st.button(f"{i}", key=f"d6_{i}")

st.markdown("<div class='calendar-header'>7月</div>", unsafe_allow_html=True)
cols7 = st.columns(7)
for i in range(1, 11):
    with cols7[(i-1)%7]:
        st.button(f"{i}", key=f"d7_{i}")

# --- 実行エリア ---
st.write("---")
if st.button("✨ 自動作成開始", use_container_width=True):
    # ここに昨日のロジックが組み込まれます（接続設定はデプロイ後に完了させます）
    st.info("現在、Googleスプレッドシートへの接続を準備中...（デプロイ後に設定します）")
    st.balloons()

st.write("---")
col_pdf, col_csv = st.columns(2)
with col_pdf: st.button("📄 PDFで出力")
with col_csv: st.button("📊 CSVで出力")
