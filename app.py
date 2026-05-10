import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 페이지 기본 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="물리", layout="wide")

# 세션 상태 초기화
if 'time' not in st.session_state:
    st.session_state.time = 0.0
if 'running' not in st.session_state:
    st.session_state.running = False

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
        
        # 물체 모양 선택
        object_shape = st.selectbox("물체 모양", ["🚗 자동차", "🏃 사람", "🚲 자전거", "🔴 기본 점"])
        emoji = object_shape.split(" ")[0]
        
        # 초기 조건 설정 슬라이더
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        
        st.markdown("---")
        st.markdown("### 🎬 시뮬레이션 제어")
        
        # 버튼 3개 배치 (재생, 일시정지, 초기화)
        if st.button("▶️ 재생", use_container_width=True):
            if st.session_state.time >= 10.0:
                st.session_state.time = 0.0
            st.session_state.running = True
            st.rerun()
            
        if st.button("⏸️ 일시정지", use_container_width=True):
            st.session_state.running = False
            st.rerun()
            
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.running = False
            st.session_state.time = 0.0
            st.rerun()
            
        st.info(f"**현재 시간:** {st.session_state.time:.1f} s")

    with col_main:
        # 1. 데이터 계산 (0~10초)
        max_t = 10.0
        t_array = np.linspace(0, max_t, 200)
        x_array = v0 * t_array + 0.5 * a * t_array**2
        v_array = v0 + a * t_array
        a_array = np.full_like(t_array, a)

        current_t = st.session_state.time
        
        # 현재 시간에 해당하는 데이터 마스킹
        mask = t_array <= current_t
        t_past = t_array[mask]
        x_past = x_array[mask]
        v_past = v_array[mask]
        a_past = a_array[mask]

        current_x = x_past[-1] if len(x_past) > 0 else 0
        current_v = v_past[-1] if len(v_past) > 0 else v0
        current_a = a_past[-1] if len(a_past) > 0 else a

        # 2. 하나의 거대한 Plotly Figure 생성 (깜빡임 최소화 및 높이 확장)
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=(f"물체의 이동 시뮬레이션 (v = {current_v:.1f} m/s)", "위치-시간 (x-t)", "속도-시간 (v-t)", "가속도-시간 (a-t)"),
            row_heights=[0.25, 0.75], # 상단 시뮬레이션(25%), 하단 그래프(75%)로 세로 길이 대폭 확대
            vertical_spacing=0.1
        )

        # --- [상단] 시뮬레이션 ---
        # 기준선 도로
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=3)), row=1, col=1)
        
        # 물체 그리기 (이모지 또는 점)
        if emoji == "🔴":
            fig.add_trace(go.Scatter(x=[current_x], y=[0], mode='markers', marker=dict(size=25, color='red')), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(x=[current_x], y=[0], mode='text', text=[emoji], textfont=dict(size=45)), row=1, col=1)

        # 속도 벡터 화살표 그리기 (속도 크기에 비례하여 길이 변화)
        if abs(current_v) > 0.1: # 속도가 0에 가까울 때는 화살표 생략
            # 화살표 (x, y는 화살표 머리 / ax, ay는 꼬리)
            fig.add_annotation(
                x=current_x + current_v * 0.8, y=0.6,  # 머리 좌표 (속도에 0.8배 곱해서 길이 조정)
                ax=current_x, ay=0.6,                  # 꼬리 좌표 (물체 바로 위)
                xref="x1", yref="y1", axref="x1", ayref="y1",
                showarrow=True, arrowhead=2, arrowsize=2, arrowwidth=3, arrowcolor="red"
            )
            # 속도값 텍스트 표시
            fig.add_annotation(
                x=current_x + (current_v * 0.8) / 2, y=0.9,
                xref="x1", yref="y1",
                text=f"v={current_v:.1f}", showarrow=False, font=dict(color="red", size=14, weight="bold")
            )

        # --- [하단] 시간에 따른 그래프 3개 ---
        def add_graph(row, col, x_data, y_data_all, y_data_past, color, name):
            # 배경 점선 (전체 궤적 예상)
            fig.add_trace(go.Scatter(x=t_array, y=y_data_all, mode='lines', line=dict(color='lightgray', dash='dash')), row=row, col=col)
            if len(t_past) > 0:
                # 현재까지의 진한 선
                fig.add_trace(go.Scatter(x=t_past, y=y_data_past, mode='lines', line=dict(color=color, width=3)), row=row, col=col)
                # 현재 시점 마커
                fig.add_trace(go.Scatter(x=[t_past[-1]], y=[y_data_past[-1]], mode='markers', marker=dict(color=color, size=10)), row=row, col=col)

        add_graph(2, 1, t_array, x_array, x_past, "blue", "위치")
        add_graph(2, 2, t_array, v_array, v_past, "green", "속도")
        add_graph(2, 3, t_array, a_array, a_past, "orange", "가속도")

        # --- 그래프 사이 기울기/넓이 화살표 (HTML/CSS 사용 없이 Plotly 내부 주석으로 깔끔하게 처리) ---
        arrow_style = dict(showarrow=False, font=dict(size=14, color="black"), align="center", bgcolor="rgba(255,255,255,0.8)")
        # 1번과 2번 그래프 사이
        fig.add_annotation(x=0.32, y=0.35, xref="paper", yref="paper", 
                           text="<b>기울기 ➡</b><br><span style='font-size:11px;color:gray;'>(속도)</span><br><br><b>⬅ 넓이</b><br><span style='font-size:11px;color:gray;'>(위치)</span>", **arrow_style)
        # 2번과 3번 그래프 사이
        fig.add_annotation(x=0.68, y=0.35, xref="paper", yref="paper", 
                           text="<b>기울기 ➡</b><br><span style='font-size:11px;color:gray;'>(가속도)</span><br><br><b>⬅ 넓이</b><br><span style='font-size:11px;color:gray;'>(속도)</span>", **arrow_style)

        # 축 설정 및 높이 지정
        fig.update_layout(
            height=850, # 세로 길이 대폭 늘림
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(range=[-50, 50], title="위치 (m)", zeroline=True, zerolinecolor="black"),
            yaxis=dict(range=[-1, 2], showticklabels=False), # 시뮬레이션 위쪽 공간 확보 (화살표 렌더링용)
            xaxis2=dict(range=[0, max_t], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 x (m)"),
            xaxis3=dict(range=[0, max_t], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 v (m/s)"),
            xaxis4=dict(range=[0, max_t], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 a (m/s²)")
        )

        st.plotly_chart(fig, use_container_width=True)

    # 시뮬레이션 루프 (running 상태일 때 페이지를 리로드하여 시간 진행)
    if st.session_state.running:
        time.sleep(0.05)
        st.session_state.time += 0.1
        if st.session_state.time > max_t:
            st.session_state.running = False
            st.session_state.time = max_t
        st.rerun()


# ==========================================
# 페이지 2: 2차원 운동 (이전 내용 유지)
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    st.write("다양한 2차원 운동에서 속도와 가속도의 특징을 확인해 보세요.")
    
    tab1, tab2, tab3 = st.tabs(["1. 자유낙하 운동", "2. 수평 투사 (포물선) 운동", "3. 등속 원운동"])
    g = 9.8 
    
    with tab1:
        st.header("🍎 자유낙하 운동")
        st.markdown("**특징:** 중력만 받아 연직 아래 방향으로 **가속도가 일정한(등가속도)** 운동입니다.")
        t_free = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t_free")
        y_free = -0.5 * g * t_free**2
        vy_free = -g * t_free
        
        fig_free = go.Figure()
        fig_free.add_trace(go.Scatter(x=[0], y=[y_free], mode='markers', marker=dict(size=15, color='blue')))
        if t_free > 0:
            fig_free.add_annotation(x=0, y=y_free + vy_free/2, ax=0, ay=y_free, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="green", text="속도 v")
        fig_free.add_annotation(x=0.5, y=y_free - g, ax=0.5, ay=y_free, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="orange", text="가속도 g (일정)")
        fig_free.update_layout(xaxis=dict(range=[-2, 2], showticklabels=False), yaxis=dict(range=[-50, 5], title="높이 (m)"), height=500)
        st.plotly_chart(fig_free, use_container_width=True)

    with tab2:
        st.header("☄️ 지표면 위에서 수평으로 던진 포물선 운동")
        st.markdown("**특징:** 수평 방향으로는 **등속 직선 운동**을, 연직 방향으로는 **자유낙하 운동**을 동시에 합니다.")
        
        t_proj = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t_proj")
        H = 44.1 
        vx0 = 10.0 
        x_proj = vx0 * t_proj
        y_proj = H - 0.5 * g * t_proj**2
        vy_proj = -g * t_proj
        
        t_array_proj = np.linspace(0, 3, 100)
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(x=vx0 * t_array_proj, y=H - 0.5 * g * t_array_proj**2, mode='lines', line=dict(color='gray', dash='dot')))
        fig_proj.add_trace(go.Scatter(x=[x_proj], y=[y_proj], mode='markers', marker=dict(size=15, color='blue')))
        fig_proj.add_annotation(x=x_proj + vx0/2, y=y_proj, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="green", text="수평 속도(일정)")
        if t_proj > 0:
            fig_proj.add_annotation(x=x_proj, y=y_proj + vy_proj/2, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="green", text="연직 속도(증가)")
        fig_proj.add_annotation(x=x_proj, y=y_proj - 10, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="orange", text="중력가속도 g")
        fig_proj.update_layout(xaxis=dict(range=[0, 40], title="수평 거리 (m)"), yaxis=dict(range=[0, 50], title="높이 (m)"), height=500, showlegend=False)
        st.plotly_chart(fig_proj, use_container_width=True)

    with tab3:
        st.header("🎡 등속 원운동")
        st.markdown("**특징:** 속력은 일정하지만, **방향이 계속 바뀌므로 가속도 운동**입니다. 가속도는 항상 중심을 향합니다.")
        
        angle = st.slider("회전 각도 (도)", 0, 360, 45, key="angle_circ")
        theta = np.radians(angle)
        R = 10 
        x_circ, y_circ = R * np.cos(theta), R * np.sin(theta)
        
        theta_array = np.linspace(0, 2*np.pi, 100)
        fig_circ = go.Figure()
        fig_circ.add_trace(go.Scatter(x=R * np.cos(theta_array), y=R * np.sin(theta_array), mode='lines', line=dict(color='gray', dash='dot')))
        fig_circ.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='black', symbol='cross')))
        fig_circ.add_trace(go.Scatter(x=[x_circ], y=[y_circ], mode='markers', marker=dict(size=15, color='blue')))
        fig_circ.add_annotation(x=x_circ - R*np.sin(theta)/2, y=y_circ + R*np.cos(theta)/2, ax=x_circ, ay=y_circ, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="green", text="속도")
        fig_circ.add_annotation(x=x_circ - x_circ/2, y=y_circ - y_circ/2, ax=x_circ, ay=y_circ, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="orange", text="가속도")
        fig_circ.update_layout(xaxis=dict(range=[-15, 15], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-15, 15]), height=600, showlegend=False)
        st.plotly_chart(fig_circ, use_container_width=True)
