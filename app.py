import streamlit as st
import random
import time

# 비밀 숫자 생성
def generate_secret_number():
    return random.sample(range(1, 10), 3)

# 스트라이크와 볼 계산
def calculate_score(secret, guess):
    strikes = sum(s == g for s, g in zip(secret, guess))
    balls = len(set(secret) & set(guess)) - strikes
    return strikes, balls

# Streamlit 앱
st.set_page_config(page_title="숫자 야구 게임", page_icon="⚾️", layout="centered")

# 배경 스타일 설정
st.markdown(
    """
    <style>
    .main {
        background-image: url('https://images.unsplash.com/photo-1531763711878-5a7c8e7de9c3'); /* 야구장 배경 */
        background-size: cover;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        color: white; /* 글자 색상 */
    }
    h1 {
        color: #ff6347; /* 토마토 색 */
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }
    .stButton>button {
        background-color: #28a745; /* 초록색 */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin: 10px; /* 버튼 간격 */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton>button:hover {
        background-color: #218838; /* 어두운 초록색 */
        transform: translateY(-2px); /* 버튼 상승 효과 */
    }
    .bottom-button {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }
    .input-field {
        border: 2px solid #ff6347; /* 테두리 색상 */
        border-radius: 50px; /* 둥근 모서리 */
        padding: 10px 20px; /* 여백 */
        font-size: 20px; /* 글자 크기 */
        text-align: center; /* 텍스트 중앙 정렬 */
        background: white; /* 배경색 */
        color: black; /* 글자 색상 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 게임 초기화
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = generate_secret_number()
    st.session_state.attempts = 0
    st.session_state.user_input = ""  # 사용자 입력 초기화
    st.session_state.result_messages = []  # 결과 메시지를 저장할 리스트 초기화

st.title("⚾️ 숫자 야구 게임 ⚾️")
st.write("세 자리의 서로 다른 숫자를 맞춰보세요!")

# 숫자 입력 필드
def handle_input():
    if st.session_state.user_input and len(st.session_state.user_input) == 3 and st.session_state.user_input.isdigit():
        submit_guess()
        st.session_state.user_input = ""  # 입력 칸 비우기
    else:
        st.error("유효한 3자리 숫자를 입력하세요.")

user_input = st.text_input("숫자 입력 (예: 123):", value=st.session_state.user_input, key="user_input", on_change=handle_input, 
                           help="3자리 숫자를 입력하세요.", 
                           placeholder="예: 123", 
                           label_visibility="collapsed")

# CSS로 클래스 추가
st.markdown('<style>.stTextInput input { border-radius: 50px; border: 2px solid #ff6347; padding: 10px; font-size: 20px; text-align: center; }</style>', unsafe_allow_html=True)

# 제출 버튼과 연결된 함수
def submit_guess():
    guess = [int(digit) for digit in st.session_state.user_input]
    st.session_state.attempts += 1
    
    strikes, balls = calculate_score(st.session_state.secret_number, guess)

    if strikes == 3:
        result_message = f"🎉 축하합니다! 🎉 비밀 숫자는 {''.join(map(str, st.session_state.secret_number))}입니다! 🎊\n" \
                         f"정말 대단해요! 총 시도 횟수: {st.session_state.attempts}\n" \
                         f"다시 도전해 보시겠어요?"
        st.session_state.result_messages.append(result_message)  # 결과 메시지 추가
        st.balloons()  # 풍선 애니메이션
        time.sleep(1)  # 잠시 대기
        st.success(result_message)  # 성공 메시지 팝업
        st.warning("🌟 화면을 캡처하고 공유하세요! 🌟")  # 캡처 안내 메시지
        
        # 게임 초기화
        st.session_state.secret_number = generate_secret_number()
        st.session_state.attempts = 0
    else:
        result_message = f"입력한 숫자: {''.join(map(str, guess))}\n" \
                         f"{strikes} 스트라이크, {balls} 볼"
        st.session_state.result_messages.append(result_message)  # 결과 메시지 추가

# 제출 버튼
if st.button("제출"):
    if st.session_state.user_input and len(st.session_state.user_input) == 3 and st.session_state.user_input.isdigit():
        submit_guess()
        st.session_state.user_input = ""  # 입력 칸 비우기
    else:
        st.error("유효한 3자리 숫자를 입력하세요.")

# 결과 메시지 표시
st.sidebar.title("결과")
for message in st.session_state.result_messages:
    st.sidebar.write(message)

# 게임 재시작 버튼을 화면 하단에 배치
st.markdown('<div class="bottom-button">', unsafe_allow_html=True)
if st.button("게임 재시작"):
    st.session_state.secret_number = generate_secret_number()
    st.session_state.attempts = 0
    st.session_state.result_messages = []  # 결과 메시지 초기화
    st.success("게임이 재시작되었습니다!")
st.markdown('</div>', unsafe_allow_html=True)
