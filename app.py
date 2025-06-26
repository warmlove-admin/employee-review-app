import streamlit as st
from config import REVIEW_CATEGORIES, REVIEW_OPTIONS, password

st.set_page_config(page_title="沃恩員工考核平台", layout="centered")
st.image("assets/logo.png", width=120)
st.title("🛡️ 主管登入")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    admin_pw = st.text_input("請輸入主管密碼", type="password")
    if st.button("登入"):
        if admin_pw == password:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("密碼錯誤，請重新輸入。")
    st.stop()

st.title("📝 員工考核平台")

# ➤ 基本資料填寫區
with st.form("review_form"):
    col1, col2 = st.columns(2)
    reviewer = col1.text_input("請輸入考核人姓名")
    review_period = col2.text_input("考核週期（例：2025 Q2）")
    review_months = st.text_input("考核月份（例：4,5,6月）")
    reviewee = st.selectbox("受評對象", ["林婉雯", "陳燕惠", "吳佩慈", "張怡如", "李芷涵"])

    st.markdown("## 📋 考核項目評分")

    results = {}
    for group_name, questions in REVIEW_CATEGORIES.items():
        with st.expander(group_name, expanded=True):
            for question, description in questions.items():
                st.markdown(f"**{question}**")
                selected = st.radio(
                    label=f"{question}_score",
                    options=REVIEW_OPTIONS,
                    index=2,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=question
                )
                st.caption(description)
                results[question] = selected

    bonus = st.number_input("補充加/扣分（可不填）", step=1.0, value=0.0)
    submitted = st.form_submit_button("計算考核結果")

if submitted:
    st.success("✅ 已提交考核")
    st.write("考核人：", reviewer)
    st.write("受評者：", reviewee)
    st.write("月份：", review_months)
    st.write("週期：", review_period)
    st.write("評分結果：")
    for q, s in results.items():
        st.write(f"- {q}：{s}")
    st.write("補充加/扣分：", bonus)
