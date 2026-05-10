import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. 페이지 및 스타일 설정 (깜빡임 완화를 위한 설정)
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

# 2. 세션 상태 관리 (상태 유지)
if 'time_step' not in st.session_state:
    st.session_state.time_step = 0.0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# 메뉴 구성
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["1차원 운동", "2차원 운동"])

# ==========================================
# 1차원 운동 페이지 (성능 최적화 및 위치 고정)
# ==========================================
if page == "1차원 운동":
    st.title("📈 1차원 운동 시뮬레이션")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 운동 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        
        st.markdown("---")
        # [요청사항] 재생, 일시정지, 초기화 버튼 좌측 배치
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("▶️ 재생", use_container_width=True):
                st.session_state.is_playing = True
        with btn_col2:
            if st.button("⏸️ 일시정지", use_container_width=True):
                st.session_state.is_playing = False
        
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.is_playing = False
            st.session_state.time_step = 0.0
            st.rerun()
            
        st.write(f"**진행 시간:** {st.session_state.time_step:.1f} s")

    with col_main:
        # [요청사항] 고정된 소제목 (부제목으로 표현)
        st.subheader("■ 물체의 위치와 속도")
        
        # 그래프 영역 고정 (깜빡임 방지용 placeholder)
        chart_container = st.empty()

        # 데이터 미리 계산 (루프 부하 감소)
        max_t = 10.0
        t_full = np.linspace(0, max_t, 100)
        x_full = v0 * t_full + 0.5 * a * t_full**2
        v_full = v0 + a * t_full
        a_full = np.full_like(t_full, a)

        # 애니메이션 구동 루프
        while True:
            t_now = st.session_state.time_step
            mask = t_full <= t_now
            t_data, x_data, v_data, a_data = t_full[mask], x_full[mask], v_full[mask], a_full[mask]

            curr_x = x_data[-1] if len(x_data) > 0 else 0
            curr_v = v_data[-1] if len(v_data) > 0 else v0

            # 서브플롯 생성
            fig = make_subplots(
                rows=2, cols=3, 
                specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
                subplot_titles=("", "■ 위치-시간 그래프", "■ 속도-시간 그래프", "■ 가속도-시간 그래프"),
                row_heights=[0.3, 0.7],
                vertical_spacing=0.25
            )

            # 1. 시뮬레이션 영역
            fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False, hoverinfo='skip'), row=1, col=1)
            fig.add_trace(go.Scatter(x=[curr_x], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False, hoverinfo='skip'), row=1, col=1)

            # [요청사항] 속도 화살표: 청록색, 두껍고 긴 막대, 작은 머리, 1.5배 길이
            v_arrow_scale = curr_v * 1.5 
            fig.add_annotation(
                x=curr_x + v_arrow_scale, y=0.8, ax=curr_x, ay=0.8,
                xref="x1", yref="y1", axref="x1", ayref="y1",
                showarrow=True, arrowhead=2, arrowsize=0.4, arrowwidth=12, arrowcolor="#00CED1", row=1, col=1
            )
            # 속도 값 텍스트 (화살표 위 배치)
            fig.add_annotation(
                x=curr_x, y=1.7, text=f"<b>속도 = {curr_v:.1f} m/s</b>", 
                showarrow=False, font=dict(color="#008B8B", size=15), row=1, col=1
            )

            # 2. 하단 그래프 영역
            def add_plot(row, col, x, y, f_y, color):
                fig.add_trace(go.Scatter(x=t_full, y=f_y, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=row, col=col)
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=3.5), showlegend=False, hoverinfo='skip'), row=row, col=col)
                if len(x) > 0:
                    fig.add_trace(go.Scatter(x=[x[-1]], y=[y[-1]], mode='markers', marker=dict(color=color, size=8), showlegend=False, hoverinfo='skip'), row=row, col=col)

            add_plot(2, 1, t_data, x_data, x_full, "blue")
            add_plot(2, 2, t_data, v_data, v_full, "green")
            add_plot(2, 3, t_data, a_data, a_full, "orange")

            # [요청사항] 상자 위치 및 기호 제거 한글화 (좌표 엄수)
            # 기울기 상자 (파랑)
            slope_style = dict(showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=6)
            fig.add_annotation(x=0.28, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 속도 정보", **slope_style)
            fig.add_annotation(x=0.69, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 가속도 정보", **slope_style)
            
            # 밑넓이 상자 (주황)
            area_style = dict(showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=6)
            fig.add_annotation(x=0.28, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 위치 변화량", **area_style)
            fig.add_annotation(x=0.69, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 속도 변화량", **area_style)

            # 레이아웃 최적화 (하단 짤림 방지 b=160)
            fig.update_layout(
                height=850,
                margin=dict(l=20, r=20, t=30, b=160),
                showlegend=False,
                xaxis=dict(range=[-50, 50], title="위치 (m)", fixedrange=True), 
                yaxis=dict(range=[-1, 2.5], showticklabels=False, fixedrange=True),
                xaxis2=dict(range=[0, 10], title="시간 (s)", fixedrange=True), yaxis2=dict(range=[-50, 50], fixedrange=True),
                xaxis3=dict(range=[0, 10], title="시간 (s)", fixedrange=True), yaxis3=dict(range=[-20, 20], fixedrange=True),
                xaxis4=dict(range=[0, 10], title="시간 (s)", fixedrange=True), yaxis4=dict(range=[-10, 10], fixedrange=True),
                template="plotly_white"
            )

            # 그래프 업데이트 (render_mode='webgl' 시도 불가시 기본 사용, config로 도구바 숨김)
            chart_container.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # 애니메이션 제어 루프
            if st.session_state.is_playing and st.session_state.time_step < 10.0:
                time.sleep(0.01) # 루프 속도 최적화
                st.session_state.time_step = round(st.session_state.time_step + 0.1, 1)
            else:
                break # 정지 상태거나 종료 시 루프 탈출

# ==========================================
# 2차원 운동 페이지 (기능 유지)
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tabs = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    with tabs[0]:
        st.subheader("■ 자유낙하 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="f_v9")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=450)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        st.subheader("■ 수평 투사 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v9")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=450)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v9")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
