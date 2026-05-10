import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 페이지 기본 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="물리", layout="wide")

# 세션 상태 관리 (애니메이션 및 버튼 조작용)
if 'time_step' not in st.session_state:
    st.session_state.time_step = 0.0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

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
        st.markdown("### 🎬 조작 방법")
        
        # 버튼 배치 (재생, 일시정지)
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("▶️ 재생", use_container_width=True):
                st.session_state.is_playing = True
        with btn_col2:
            if st.button("⏸️ 일시정지", use_container_width=True):
                st.session_state.is_playing = False
        
        # 초기화 버튼
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.is_playing = False
            st.session_state.time_step = 0.0
            st.rerun()
            
        st.write(f"**현재 진행 시간:** {st.session_state.time_step:.1f} s")

    with col_main:
        # 데이터 계산
        max_t = 10.0
        t_full = np.linspace(0, max_t, 200)
        x_full = v0 * t_full + 0.5 * a * t_full**2
        v_full = v0 + a * t_full
        a_full = np.full_like(t_full, a)

        # 현재 시간 마스킹
        t_now = st.session_state.time_step
        mask = t_full <= t_now
        t_data, x_data, v_data, a_data = t_full[mask], x_full[mask], v_full[mask], a_full[mask]

        curr_x = x_data[-1] if len(x_data) > 0 else 0
        curr_v = v_data[-1] if len(v_data) > 0 else v0

        # 서브플롯 생성
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=("■ 물체의 위치 및 속도 벡터 시뮬레이션", "■ 위치-시간 그래프 (x-t)", "■ 속도-시간 그래프 (v-t)", "■ 가속도-시간 그래프 (a-t)"),
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25 # 상자 배치를 위한 충분한 간격 확보
        )

        # 1. 시뮬레이션 (상단)
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=[curr_x], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)

        # 속도 화살표 디자인 (청록색, 두껍고 긴 막대, 작은 머리)
        v_arrow_scale = curr_v * 1.5 
        fig.add_annotation(
            x=curr_x + v_arrow_scale, y=0.7, ax=curr_x, ay=0.7,
            xref="x1", yref="y1", axref="x1", ayref="y1",
            showarrow=True, arrowhead=2, arrowsize=0.5, arrowwidth=8, arrowcolor="#00CED1", row=1, col=1
        )
        # 속도 값 텍스트
        fig.add_annotation(
            x=curr_x, y=1.6, text=f"<b>v = {curr_v:.1f} m/s</b>", 
            showarrow=False, font=dict(color="#008B8B", size=15), row=1, col=1
        )

        # 2. 그래프 (하단)
        def add_plot(row, col, x, y, f_y, color):
            fig.add_trace(go.Scatter(x=t_full, y=f_y, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False), row=row, col=col)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=3), showlegend=False), row=row, col=col)
            if len(x) > 0:
                fig.add_trace(go.Scatter(x=[x[-1]], y=[y[-1]], mode='markers', marker=dict(color=color, size=8), showlegend=False), row=row, col=col)

        add_plot(2, 1, t_data, x_data, x_full, "blue")
        add_plot(2, 2, t_data, v_data, v_full, "green")
        add_plot(2, 3, t_data, a_data, a_full, "orange")

        # --- 기울기 및 밑넓이 정보 상자 위치 조정 ---
        # 1. 기울기 정보 (파랑 상자 - 축 위 배치)
        slope_style = dict(showarrow=False, font=dict(size=13, color="white"), bgcolor="#1f77b4", borderpad=5)
        # 속도 정보 상자: 왼쪽으로 이동(x=0.28) 및 위로 이동(y=0.62)
        fig.add_annotation(x=0.28, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 속도($v$)", **slope_style)
        # 가속도 정보 상자: 높이만 위로 이동(y=0.62)
        fig.add_annotation(x=0.69, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 가속도($a$)", **slope_style)
        
        # 2. 밑넓이 정보 (주황 상자 - 축 아래 배치)
        area_style = dict(showarrow=False, font=dict(size=13, color="white"), bgcolor="#ff7f0e", borderpad=5)
        # 위치 변화량 상자: 왼쪽으로 이동(x=0.28)
        fig.add_annotation(x=0.28, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 위치 변화량", **area_style)
        # 속도 변화량 상자: 기존 위치 유지
        fig.add_annotation(x=0.69, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 속도 변화량", **area_style)

        # 레이아웃 설정
        fig.update_layout(
            height=850,
            margin=dict(l=20, r=20, t=60, b=100),
            xaxis=dict(range=[-50, 50], title="위치 (m)"), 
            yaxis=dict(range=[-1, 2.2], showticklabels=False),
            xaxis2=dict(range=[0, 10], title="시간 (s)"), yaxis2=dict(range=[-50, 50]),
            xaxis3=dict(range=[0, 10], title="시간 (s)"), yaxis3=dict(range=[-20, 20]),
            xaxis4=dict(range=[0, 10], title="시간 (s)"), yaxis4=dict(range=[-10, 10])
        )

        st.plotly_chart(fig, use_container_width=True)

    # 애니메이션 실행 루프
    if st.session_state.is_playing and st.session_state.time_step < max_t:
        time.sleep(0.05)
        st.session_state.time_step += 0.1
        st.rerun()

# ==========================================
# 페이지 2: 2차원 운동
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tabs = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    
    with tabs[0]:
        st.subheader("■ 자유낙하 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="f_v2")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[1]:
        st.subheader("■ 수평 투사 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v2")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v2")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
