import streamlit as st
import google.generativeai as genai
from time import sleep

# 페이지 설정
st.set_page_config(
    page_title="Gemini Chat App",
    page_icon="🤖",
    layout="centered"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    .stTextArea textarea {
        font-size: 16px !important;
    }
    .gemini-response {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Gemini API 초기화
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ Gemini API 초기화 중 오류가 발생했습니다. API 키를 확인해주세요.")
    st.stop()

# 페이지 제목
st.title("💬 Gemini Chat")
st.caption("Powered by Gemini 1.5 Flash")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 채팅 기록 표시
for q, a in st.session_state.chat_history:
    st.text_area("질문:", value=q, height=100, disabled=True)
    st.markdown("**Gemini 답변:**")
    st.markdown(f'<div class="gemini-response">{a}</div>', unsafe_allow_html=True)
    st.divider()

# 사용자 입력
user_input = st.text_area(
    "새로운 질문을 입력하세요:",
    height=100,
    placeholder="궁금한 내용을 자유롭게 물어보세요...",
    key="new_question"
)

# 전송 버튼
if st.button("전송", type="primary", key="send_button"):
    if not user_input or user_input.strip() == "":
        st.warning("⚠️ 질문을 입력해주세요.")
    else:
        try:
            # 로딩 스피너 표시
            with st.spinner("🤖 Gemini가 답변을 생성하고 있습니다..."):
                # Gemini API 호출
                response = model.generate_content(user_input)
                
                # 응답 텍스트 정리
                response_text = response.text.strip()
                
                # 채팅 기록에 추가
                st.session_state.chat_history.append((user_input, response_text))
                
                # 입력창 초기화
                st.session_state.new_question = ""
                
                # 페이지 새로고침
                st.rerun()
                
        except Exception as e:
            st.error(f"⚠️ 오류가 발생했습니다: {str(e)}")
            st.info("잠시 후 다시 시도해주세요.")

# 채팅 기록 초기화 버튼
if st.session_state.chat_history:
    if st.button("💫 대화 내용 초기화"):
        st.session_state.chat_history = []
        st.rerun()

# 페이지 하단 정보
st.divider()
st.caption("© 2024 Gemini Chat App. Powered by Google's Gemini 1.5 Flash")
