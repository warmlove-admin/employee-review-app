import streamlit as st
import pandas as pd
from datetime import datetime
from config import password

st.set_page_config(page_title="沃恩員工考核平台", layout="centered")

# === 登入驗證 ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.image("assets/logo.png", width=120)
    st.title("沃恩員工考核平台")
    pwd = st.text_input("請輸入主管密碼", type="password")
    if pwd == password:
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.stop()

# === 基本資訊 ===
st.success("✅ 登入成功")
col1, col2 = st.columns(2)
with col1:
    reviewer = st.text_input("請輸入考核人姓名", max_chars=20)
with col2:
    cycle = st.text_input("考核週期（例：2025 Q2）", max_chars=20)

months = st.text_input("考核月份（例：4,5,6月）")
employee = st.selectbox("受評對象", ["林婉雯", "陳穎萱", "郝力"])

# === 評分表單 ===
st.subheader("📋 考核項目評分")
criteria = {
    "第1月AA01達成率": "",
    "第2月AA01達成率": "",
    "第3月AA01達成率": "",
}
rating_options = ["++", "+", "無", "-", "--"]
score_map = {"++": 2, "+": 1, "無": 0, "-": -1, "--": -2}

scores = {}
for item in criteria:
    choice = st.radio(item, rating_options, horizontal=True, key=item)
    scores[item] = choice

adjust = st.number_input("補充加/扣分（可不填）", value=0, step=1)

# === 計算總分與獎金 ===
if st.button("計算考核結果"):
    raw_score = sum([score_map[s] for s in scores.values()])
    total_score = raw_score + adjust
    st.write(f"✅ 考核總分為：`{total_score}` 分")

    bonus_base = st.number_input("請輸入部門總獎金（元）", value=10000, step=100)
    # 假設只有 3 人，總分 = 3 人分數相加（此處簡化）
    dummy_total = 30
    personal_ratio = total_score / dummy_total
    bonus = int(bonus_base * personal_ratio)
    st.success(f"💰 該員工預估獎金：`{bonus} 元`")

    # 儲存
    df = pd.DataFrame([{
        "考核人員": reviewer,
        "考核週期": cycle,
        "月份": months,
        "受評對象": employee,
        "得分": total_score,
        "預估獎金": bonus,
        "日期": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])
    df.to_csv("records.csv", mode="a", header=False, index=False)
    st.download_button("📄 下載 PDF（模擬）", data=f"{employee} 考核成績：{total_score} 分，獎金：{bonus} 元", file_name=f"{employee}_result.txt")
