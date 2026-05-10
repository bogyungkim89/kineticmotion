import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 기본 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="물리", layout="wide")

# 사이드바 네비게이션
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["1차원 운동", "2차원 운동"])

# ==========================================
# 페이지 1: 1차원 운동
# ==========================================
if page == "1차원 운동":
    st.title("📈 1차원 운동 시뮬레이션")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 운동 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        
        st.markdown("---")
        st.markdown("### 🎬 시뮬레이션 조작")
        st.info("부드러운 구동을 위해 **그래프 하단의 [▶️ 재생] 버튼**을 눌러주세요.")
        
        if st.button("🔄 시뮬레이션 초기화", use_container_width=True):
            st.rerun()

    with col_main:
        # 데이터 계산 (0~10초, 100프레임)
        max_t = 10.0
        frames_count = 100
        t_array = np.linspace(0, max_t, frames_count)
        x_array = v0 * t_array + 0.5 * a * t_array**2
        v_array = v0 + a * t_array
        a_array = np.full_like(t_array, a)

        # 서브플롯 생성
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=("🚗 물체의 이동 및 속도 벡터", "위치-시간 (x-t)", "속도-시간 (v-t)", "가속도-시간 (a-t)"),
            row_heights=[0.3, 0.7],
            vertical_spacing=0.15
        )

        # 1. 정적 배경
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_array, y=x_array, mode='lines', line=dict(color='rgba(200,200,200,0.4)', dash='dash')), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', line=dict(color='rgba(200,200,200,0.4)', dash='dash')), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_array, y=a_array, mode='lines', line=dict(color='rgba(200,200,200,0.4)', dash='dash')), row=2, col=3)

        # 2. 동적 물체 및 선 (초기값)
        fig.add_trace(go.Scatter(x=[x_array[0]], y=[0], mode='markers', marker=dict(size=20, color='red')), row=1, col=1) # Index 4
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='lines', line=dict(color='blue', width=3)), row=2, col=1) # Index 5
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='lines', line=dict(color='green', width=3)), row=2, col=2) # Index 6
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='lines', line=dict(color='orange', width=3)), row=2, col=3) # Index 7
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='markers', marker=dict(color='blue', size=8)), row=2, col=1) # Index 8
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='markers', marker=dict(color='green', size=8)), row=2, col=2) # Index 9
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='markers', marker=dict(color='orange', size=8)), row=2, col=3) # Index 10

        # --- 프레임 생성 ---
        frames = []
        for i in range(frames_count):
            v_len = v_array[i] * 0.7 # 화살표 길이
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_array[i]], y=[0]),
                    go.Scatter(x=t_array[:i+1], y=x_array[:i+1]),
                    go.Scatter(x=t_array[:i+1], y=v_array[:i+1]),
                    go.Scatter(x=t_array[:i+1], y=a_array[:i+1]),
                    go.Scatter(x=[t_array[i]], y=[x_array[i]]),
                    go.Scatter(x=[t_array[i]], y=[v_array[i]]),
                    go.Scatter(x=[t_array[i]], y=[a_array[i]])
                ],
                traces=[4, 5, 6, 7, 8, 9, 10],
                layout=go.Layout(annotations=[
                    dict(
                        x=x_array[i] + v_len, y=0.6, ax=x_array[i], ay=0.6,
                        xref="x1", yref="y1", axref="x1", ayref="y1",
                        showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=4, arrowcolor="red",
                        text=f"v={v_array[i]:.1f}", yanchor="bottom"
                    )
                ])
            ))
        fig.frames = frames

        # --- 학습 지표 (기울기 및 밑넓이) ---
        # 1. 기울기 (상단 배치 - 파란색)
        fig.add_annotation(x=0.33, y=0.55, xref="paper", yref="paper", text="<b>기울기 ➡</b><br>속도 정보", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=5)
        fig.add_annotation(x=0.69, y=0.55, xref="paper", yref="paper", text="<b>기울기 ➡</b><br>가속도 정보", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=5)
        
        # 2. 밑넓이 (하단 배치 - 주황색)
        fig.add_annotation(x=0.33, y=-0.12, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b><br>위치(변위) 정보", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=5)
        fig.add_annotation(x=0.69, y=-0.12, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b><br>속도 변화량", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=5)

        # 레이아웃
        fig.update_layout(
            height=900, showlegend=False,
            updatemenus=[dict(
                type="buttons", buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 40, "redraw": False}, "fromcurrent": True}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                ],
                direction="left", x=0.0, y=-0.05
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), yaxis=dict(range=[-0.5, 1.5], showticklabels=False),
            xaxis2=dict(range=[0, max_t], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 (m)"),
            xaxis3=dict(range=[0, max_t], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 (m/s)"),
            xaxis4=dict(range=[0, max_t], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 (m/s²)")
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 페이지 2: 2차원 운동
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tab1, tab2, tab3 = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    
    with tab1:
        st.header("🍎 자유낙하 운동")
        t_free = st.slider("시간 (s)", 0.0, 3.0, 1.5)
        y_f, v_f = -0.5 * g * t_free**2, -g * t_free
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[y_f], mode='markers', marker=dict(size=15, color='red')))
        if t_free > 0:
            fig.add_annotation(x=0, y=y_f + v_f/2, ax=0, ay=y_f, showarrow=True, arrowhead=2, arrowcolor="green", text="v")
        fig.add_annotation(x=0.5, y=y_f - g, ax=0.5, ay=y_f, showarrow=True, arrowhead=2, arrowcolor="orange", text="g")
        fig.update_layout(xaxis=dict(range=[-2, 2], showticklabels=False), yaxis=dict(range=[-50, 5]), height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("☄️ 수평 투사 운동")
        t_p = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="p2")
        vx0 = 10.0
        x_p, y_p = vx0 * t_p, 44.1 - 0.5 * g * t_p**2
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[x_p], y=[y_p], mode='markers', marker=dict(size=15, color='red')))
        fig.add_annotation(x=x_p + vx0/2, y=y_p, ax=x_p, ay=y_p, showarrow=True, arrowcolor="green", text="vx (일정)")
        fig.add_annotation(x=x_p, y=y_p - 10, ax=x_p, ay=y_p, showarrow=True, arrowcolor="orange", text="g")
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🎡 등속 원운동")
        angle = st.slider("각도 (도)", 0, 360, 45)
        rad = np.radians(angle)
        R = 10
        x, y = R * np.cos(rad), R * np.sin(rad)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=15, color='red')))
        fig.add_annotation(x=x - R*np.sin(rad)/2, y=y + R*np.cos(rad)/2, ax=x, ay=y, showarrow=True, arrowcolor="green", text="v")
        fig.add_annotation(x=x/2, y=y/2, ax=x, ay=y, showarrow=True, arrowcolor="orange", text="a (중심)")
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=500)
        st.plotly_chart(fig, use_container_width=True)
