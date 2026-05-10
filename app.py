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
# 페이지 1: 1차원 운동 (깜빡임 완벽 해결 버전)
# ==========================================
if page == "1차원 운동":
    st.title("📈 1차원 운동 시뮬레이션")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 속도와 가속도")
        st.caption("초기 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        
        st.markdown("---")
        st.info("💡 **그래프 하단의 '▶️ 재생' 버튼을 누르면 부드러운 애니메이션이 시작됩니다.** (초기화하려면 슬라이더를 다시 조절하세요)")

    with col_main:
        # 데이터 계산 (0~10초, 100프레임으로 부드럽게)
        max_t = 10.0
        frames_count = 100
        t_array = np.linspace(0, max_t, frames_count)
        x_array = v0 * t_array + 0.5 * a * t_array**2
        v_array = v0 + a * t_array
        a_array = np.full_like(t_array, a)

        # Plotly 서브플롯 생성 (위: 시뮬레이션, 아래: 3개의 그래프)
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=("🚗 물체의 이동 시뮬레이션", "위치-시간 (x-t)", "속도-시간 (v-t)", "가속도-시간 (a-t)"),
            vertical_spacing=0.25
        )

        # --- 정적 배경 (Trace 0 ~ 3) ---
        # 0: 시뮬레이션 도로
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2)), row=1, col=1)
        # 1,2,3: 예상 전체 궤적 (흐린 점선)
        fig.add_trace(go.Scatter(x=t_array, y=x_array, mode='lines', line=dict(color='lightgray', dash='dash')), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', line=dict(color='lightgray', dash='dash')), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_array, y=a_array, mode='lines', line=dict(color='lightgray', dash='dash')), row=2, col=3)

        # --- 동적 요소 (초기 상태, Trace 4 ~ 10) ---
        # 4: 물체
        fig.add_trace(go.Scatter(x=[x_array[0]], y=[0], mode='markers', marker=dict(size=20, color='red')), row=1, col=1)
        # 5,6,7: 그려지는 선
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='lines', line=dict(color='blue', width=3)), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='lines', line=dict(color='green', width=3)), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='lines', line=dict(color='orange', width=3)), row=2, col=3)
        # 8,9,10: 끝점 마커
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='markers', marker=dict(color='blue', size=8)), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='markers', marker=dict(color='green', size=8)), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='markers', marker=dict(color='orange', size=8)), row=2, col=3)

        # --- Plotly 프레임(애니메이션) 생성 ---
        frames = []
        for i in range(frames_count):
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_array[i]], y=[0]), # Trace 4
                    go.Scatter(x=t_array[:i+1], y=x_array[:i+1]), # Trace 5
                    go.Scatter(x=t_array[:i+1], y=v_array[:i+1]), # Trace 6
                    go.Scatter(x=t_array[:i+1], y=a_array[:i+1]), # Trace 7
                    go.Scatter(x=[t_array[i]], y=[x_array[i]]), # Trace 8
                    go.Scatter(x=[t_array[i]], y=[v_array[i]]), # Trace 9
                    go.Scatter(x=[t_array[i]], y=[a_array[i]])  # Trace 10
                ],
                traces=[4, 5, 6, 7, 8, 9, 10]
            ))
        fig.frames = frames

        # --- 그래프 사이 화살표 주석 (기울기/넓이) ---
        arrow_style = dict(showarrow=False, font=dict(size=13, color="black"), align="center", bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=0.33, y=0.2, xref="paper", yref="paper", text="<b>기울기 ➡</b><br><span style='font-size:10px;color:gray;'>(속도)</span><br><br><b>⬅ 넓이</b><br><span style='font-size:10px;color:gray;'>(위치)</span>", **arrow_style)
        fig.add_annotation(x=0.69, y=0.2, xref="paper", yref="paper", text="<b>기울기 ➡</b><br><span style='font-size:10px;color:gray;'>(가속도)</span><br><br><b>⬅ 넓이</b><br><span style='font-size:10px;color:gray;'>(속도)</span>", **arrow_style)

        # --- 레이아웃 및 플레이 버튼 ---
        fig.update_layout(
            height=600, showlegend=False,
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 50, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, xanchor="left", y=-0.15, yanchor="top"
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), yaxis=dict(showticklabels=False, range=[-1, 1]),
            xaxis2=dict(range=[0, max_t], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 (m)"),
            xaxis3=dict(range=[0, max_t], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 (m/s)"),
            xaxis4=dict(range=[0, max_t], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 (m/s²)")
        )

        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 페이지 2: 2차원 운동 (이전 코드와 동일)
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
        fig_free.add_trace(go.Scatter(x=[0], y=[y_free], mode='markers', marker=dict(size=15, color='blue'), name="물체"))
        if t_free > 0:
            fig_free.add_annotation(x=0, y=y_free + vy_free/2, ax=0, ay=y_free, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="green", text="속도 v")
        fig_free.add_annotation(x=0.5, y=y_free - g, ax=0.5, ay=y_free, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="orange", text="가속도 g (일정)")
        fig_free.update_layout(xaxis=dict(range=[-2, 2], showticklabels=False), yaxis=dict(range=[-50, 5], title="높이 (m)"), height=400)
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
        fig_proj.update_layout(xaxis=dict(range=[0, 40], title="수평 거리 (m)"), yaxis=dict(range=[0, 50], title="높이 (m)"), height=400, showlegend=False)
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
        fig_circ.update_layout(xaxis=dict(range=[-15, 15], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-15, 15]), height=500, showlegend=False)
        st.plotly_chart(fig_circ, use_container_width=True)
