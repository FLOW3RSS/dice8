import streamlit as st
import random
import time

st.set_page_config(page_title="🎲 주사위 합 지우기 게임", layout="wide")

# 상태 초기화
if "selected_tiles" not in st.session_state:
    st.session_state.selected_tiles = set()
if "confirmed_tiles" not in st.session_state:
    st.session_state.confirmed_tiles = set()
if "crossed_tiles" not in st.session_state:
    st.session_state.crossed_tiles = set()
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "max_select" not in st.session_state:
    st.session_state.max_select = 5
if "start_error" not in st.session_state:
    st.session_state.start_error = ""
if "dice_result" not in st.session_state:
    st.session_state.dice_result = None

# 스타일
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
    }
    .tile-btn {
        background-color: #bbb;
        border: 2px solid white;
        width: 50px;
        height: 50px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin: 4px auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b, #ff4757);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff4757, #ff2e2e);
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.title("🎯 주사위 합 지우기 게임")

# 게임 설명
st.markdown("""
**게임 방법**
- 2부터 12까지의 숫자 중 `n개`를 선택하세요.
- 선택한 n개 숫자는 **게임이 시작되면 확정**됩니다.
- 실제 주사위 두 개를 굴려 나온 합과 일치하는 칸을 클릭하여 **빨간 X로 표시**하세요.
- 모든 타일에 X를 표시하면 게임 승리입니다!
- 실수로 X를 눌렀을 경우 다시 클릭하면 취소됩니다.
""")

def tile_id(num, row):
    return f"{num}_{row}"

# 타일 UI
def render_tile(num, row):
    tid = tile_id(num, row)
    crossed = tid in st.session_state.crossed_tiles
    selected = tid in st.session_state.selected_tiles
    confirmed = tid in st.session_state.confirmed_tiles
    game_on = st.session_state.game_started

    if game_on and not confirmed:
        return  # 숨김 처리

    if game_on:
        color = "#f66" if crossed else "#4ecdc4"
        label = "X" if crossed else " "
    else:
        color = "#4ecdc4" if selected else "#bbb"
        label = str(num)

    btn_key = f"btn_{tid}"
    clicked = st.button(" ", key=btn_key)

    st.markdown(f"""
        <div class="tile-btn" style="background-color: {color};">
            {label}
        </div>
    """, unsafe_allow_html=True)

    if clicked:
        if game_on:
            if confirmed:
                if crossed:
                    st.session_state.crossed_tiles.remove(tid)
                else:
                    st.session_state.crossed_tiles.add(tid)
        else:
            if selected:
                st.session_state.selected_tiles.remove(tid)
            else:
                if len(st.session_state.selected_tiles) < st.session_state.max_select:
                    st.session_state.selected_tiles.add(tid)
                else:
                    st.warning(f"{st.session_state.max_select}개를 초과하였습니다.")

# 선택 개수 슬라이더
st.session_state.max_select = st.slider("선택 가능한 타일 개수 (n)", 1, 30, st.session_state.max_select)

# 주사위 굴리기
def roll_dice():
    a, b = random.randint(1, 6), random.randint(1, 6)
    st.session_state.dice_result = (a, b)
    st.success(f'주사위를 굴려서 나온 두 눈의 합에 해당하는 파란 타일을 지워! 졌다면 전략을 수정해야겠지?')
    time.sleep(1)

# 게임 시작
if st.button("🚀 게임 시작!"):
    if len(st.session_state.selected_tiles) != st.session_state.max_select:
        st.session_state.start_error = "n개를 모두 선택하지 않았습니다."
    else:
        st.session_state.confirmed_tiles = st.session_state.selected_tiles.copy()
        st.session_state.selected_tiles.clear()
        st.session_state.crossed_tiles.clear()
        st.session_state.game_started = True
        st.session_state.start_error = ""
        roll_dice()

if st.session_state.start_error:
    st.warning(st.session_state.start_error)

# 숫자 라벨
header_cols = st.columns(11)
for i, col in zip(range(2, 13), header_cols):
    with col:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{i}</div>", unsafe_allow_html=True)

# 타일 출력 (10줄)
for row in range(10):
    cols = st.columns(11)
    for i, col in zip(range(2, 13), cols):
        with col:
            render_tile(i, row)

# 결과 확인
if st.session_state.game_started:
    total = len(st.session_state.confirmed_tiles)
    done = len(st.session_state.crossed_tiles)
    st.info(f"남은 타일: {total - done}개")
    if total > 0 and done == total:
        st.balloons()
        st.success("🎉 모든 타일을 제거했습니다! 당신이 승리했습니다!")
        if st.button("🔄 다시 시작하기"):
            st.session_state.selected_tiles.clear()
            st.session_state.confirmed_tiles.clear()
            st.session_state.crossed_tiles.clear()
            st.session_state.game_started = False
            st.session_state.dice_result = None
