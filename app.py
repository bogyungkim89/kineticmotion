import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 기본 설정
st.set_page_config(page_title="속도와 가속도 시뮬레이션", page_icon="🏎️", layout="wide")

# 사이드바 네비게이션
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 학습 페이지를 선택하세요:", 
                        ["1. 개념 학습: 속도와 가속도", "2. 시뮬레이션 및 그래프"])

# ==========================================
# 페이지 1: 개념 학습
# ==========================================
if page == "1. 개념 학습: 속도와 가속도":
    st.title("속도와 가속도, 그리고 방향 🧭")
    
    st.header("1. 속도 (Velocity)와 가속도 (Acceleration)")
    st.markdown("""
    * **속도 ($v$)**: 물체의 위치가 변하는 정도입니다. 얼마나 '빨리' 이동하는지뿐만 아니라, **어느 '방향'으로** 이동하는지도 포함하는 개념입니다.
    * **가속도 ($a$)**: 물체의 속도가 변하는 정도입니다. 속도가 빨라지거나 느려지는 것, 혹은 방향이 바뀌는 것 모두 가속도가 존재하는 상태입니다.
    """)
    
    st.header("2. 부호(+, -)가 의미하는 것")
    st.info("물리학에서 속도와 가속도의 **부호(+, -)**는 값의 크기가 아니라 **방향**을 의미합니다. 기준이 되는 방향을 (+)로 두면, 반대 방향은 (-)가 됩니다.")
    
    st.subheader("속도와 가속도의 부호에 따른 운동 상태 변화")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("🟢 속도가 빨라지는 경우 (부호가 같을 때)")
        st.markdown("""
        * **$v > 0, a > 0$**: (+) 방향으로 이동하며 점점 빨라집니다.
        * **$v < 0, a < 0$**: (-) 방향으로 이동하며 점점 빨라집니다.
        > **핵심:** 속도와 가속도의 방향이 같으면 물체는 속력을 냅니다!
        """)
        
    with col2:
        st.warning("🔴 속도가 느려지는 경우 (부호가 다를 때)")
        st.markdown("""
        * **$v > 0, a < 0$**: (+) 방향으로 이동하지만 점점 느려집니다. (브레이크를 밟는 상황)
        * **$v < 0, a > 0$**: (-) 방향으로 이동하지만 점점 느려집니다.
        > **핵심:** 속도와 가속도의 방향이 반대면 물체의 속력은 줄어듭니다!
        """)

# ==========================================
# 페이지 2: 시뮬레이션 및 그래프
# ==========================================
elif page == "2. 시뮬레이션 및 그래프":
    st.title("📈 1차원 운동 시뮬레이션 및 그래프")
    st.write("슬라이더를 조절하여 초기 속도와 가속도를 설정하고, 물체의 운동이 그래프로 어떻게 표현되는지 확인해 보세요.")

    # 사용자 입력 (사이드바 또는 상단 컨트롤)
    st.markdown("### ⚙️ 운동 조건 설정")
    col1, col2 = st.columns(2)
    with col1:
        v0 = st.slider("초기 속도 ($v_0$) [m/s]", -10.0, 10.0, 2.0, step=1.0)
        st.caption("0이면 정지 상태에서 출발합니다.")
    with col2:
        a = st.slider("가속도 ($a$) [m/s²]", -5.0, 5.0, 0.0, step=0.5)
        st.caption("0이면 등속도 운동, 0이 아니면 등가속도 운동을 합니다.")

    # 데이터 생성
    t = np.linspace(0, 10, 500) # 0초부터 10초까지
    # 등가속도 직선 운동 공식: x = v0*t + 1/2*a*t^2, v = v0 + a*t
    x = v0 * t + 0.5 * a * t**2
    v = v0 + a * t
    accel = np.full_like(t, a) # 가속도는 일정

    st.markdown("---")
    
    # 애니메이션 시뮬레이션 (간단한 1D 위치 점으로 표현)
    st.markdown("### 🚗 물체의 이동 시뮬레이션")
    current_time = st.slider("현재 시간 확인 (초)", 0.0, 10.0, 0.0, step=0.1)
    
    # 현재 시간에 해당하는 위치 계산
    current_x = v0 * current_time + 0.5 * a * current_time**2
    
    # 1D 궤적 시각화
    fig_sim = go.Figure()
    # 배경 기준선
    fig_sim.add_trace(go.Scatter(x=[-100, 100], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False))
    # 현재 물체의 위치
    fig_sim.add_trace(go.Scatter(x=[current_x], y=[0], mode='markers', 
                                 marker=dict(size=20, color='red'), name='현재 위치'))
    
    fig_sim.update_layout(
        xaxis_title="위치 (m)",
        yaxis=dict(showticklabels=False, range=[-1, 1]),
        height=200,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(range=[-50, 50]) # 화면에 보일 위치 범위
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")

    # 그래프 그리기 (위치-시간, 속도-시간, 가속도-시간)
    st.markdown("### 📊 시간에 따른 위치, 속도, 가속도 그래프")
    
    fig = make_subplots(rows=1, cols=3, subplot_titles=("위치-시간 (x-t) 그래프", "속도-시간 (v-t) 그래프", "가속도-시간 (a-t) 그래프"))

    # 위치-시간 그래프
    fig.add_trace(go.Scatter(x=t, y=x, mode='lines', name='위치 x(t)', line=dict(color='blue')), row=1, col=1)
    
    # 속도-시간 그래프
    fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='속도 v(t)', line=dict(color='green')), row=1, col=2)
    # v=0 인 기준선 추가
    fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)

    # 가속도-시간 그래프
    fig.add_trace(go.Scatter(x=t, y=accel, mode='lines', name='가속도 a(t)', line=dict(color='orange')), row=1, col=3)
    # a=0 인 기준선 추가
    fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=3)

    # 현재 시간에 해당하는 위치에 마커 표시
    current_v = v0 + a * current_time
    fig.add_trace(go.Scatter(x=[current_time], y=[current_x], mode='markers', marker=dict(color='red', size=8), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=[current_time], y=[current_v], mode='markers', marker=dict(color='red', size=8), showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[current_time], y=[a], mode='markers', marker=dict(color='red', size=8), showlegend=False), row=1, col=3)

    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(title_text="시간 t (s)")
    fig.update_yaxes(title_text="위치 x (m)", row=1, col=1)
    fig.update_yaxes(title_text="속도 v (m/s)", row=1, col=2)
    fig.update_yaxes(title_text="가속도 a (m/s²)", row=1, col=3)

    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **그래프 분석 팁:** 속도-시간 그래프의 기울기는 '가속도'를 의미하며, 그래프 아래의 면적은 '이동 거리(변위)'를 의미합니다.")
