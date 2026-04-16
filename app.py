import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="神シフト作成：密着版", layout="wide")

st.markdown("""
    <style>
    /* 1. 全体の余白を完全に殺す */
    .block-container { padding: 1rem 1rem !important; }
    
    /* 2. カラム間の隙間（溝）を完全にゼロにする */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        border: 0.5px solid #ddd; /* カラム自体に線を引いて隣とつなげる */
    }

    /* 3. ボタンを枠いっぱいに広げる */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important;
        border: none !important; /* ボタンの線は消して、カラムの線を見せる */
        border-radius: 0px !important;
        margin: 0px !important;
        background-color: white;
        font-size: 16px !important;
        font-weight: bold;
    }

    /* 色の設定 */
    button:has(div p:contains("公休")) { background-color: #ffb6c1 !important; color: white !important; }
    button:has(div p:contains("有給")) { background-color: #ffa500 !important; color: white !important; }

    /* 月と曜日のヘッダー */
    .month-bar { background-color: #ffb6c1; color: white; text-align: center; padding: 10px; font-weight: bold; }
    .weekday { text-align: center; background-color: #f8f9fa; color: #ff69b4; border: 0.5px solid #ddd; font-weight: bold; padding: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

# (以下、これまでのロジック部分は同じなので省略しますが、このCSS部分を差し替えてみてください)
