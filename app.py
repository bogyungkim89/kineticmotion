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
# 페이지 1: 1차원 운동 (디자인 개선 버전)
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
        st.info("부드러운 애니메이션을 위해 **우측 그래프 상단에 있는 [▶️ 재생] 버튼**을 이용해 주세요.")
        
        # 초기화 버튼만 사이드바에 배치 (재생/정지는 Plotly 내부에서 제어하여 깜빡임 방지)
        if st.button("🔄 시뮬레이션 초기화", use_container_width=True):
            st.rerun()

    with col_main:
        # 데이터 계산
        max_t = 10.0
        frames_count = 100
        t_array = np.linspace(0, max_t, frames_count)
        x_array = v0 * t_array + 0.5 * a * t_array**2
        v_array = v0 + a * t_array
        a_array = np.full_like(t_array, a)

        # 서브플롯 생성 (수직 간격을 넓혀 안내 상자 공간 확보)
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=("🚗 물체의 이동 및 속도 벡터", "위치-시간 (x-t)", "속도-시간 (v-t)", "가속도-시간 (a-t)"),
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25 # 그래프 사이 간격 확장
        )

        # 1. 배경 설정
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_array, y=x_array, mode='lines', line=dict(color='rgba(220,220,220,0.5)', dash='dash')), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', line=dict(color='rgba(220,220,220,0.5)', dash='dash')), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_array, y=a_array, mode='lines', line=dict(color='rgba(220,220,220,0.5)', dash='dash')), row=2, col=3)

        # 2. 동적 물체 (빨간 점)
        fig.add_trace(go.Scatter(x=[x_array[0]], y=[0], mode='markers', marker=dict(size=18, color='red')), row=1, col=1)
        
        # 3. 그래프 선 및 마커
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='lines', line=dict(color='blue', width=3)), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='lines', line=dict(color='green', width=3)), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='lines', line=dict(color='orange', width=3)), row=2, col=3)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[x_array[0]], mode='markers', marker=dict(color='blue', size=8)), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[v_array[0]], mode='markers', marker=dict(color='green', size=8)), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_array[0]], y=[a_array[0]], mode='markers', marker=dict(color='orange', size=8)), row=2, col=3)

        # --- 프레임 구성 (애니메이션) ---
        frames = []
        for i in range(frames_count):
            # 속도 비례 화살표 길이 (기존의 1.5배인 1.05배 적용)
            v_len = v_array[i] * 1.05 
            
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_array[i]], y=[0]), # 물체
                    go.Scatter(x=t_array[:i+1], y=x_array[:i+1]), # x-t 선
                    go.Scatter(x=t_array[:i+1], y=v_array[:i+1]), # v-t 선
                    go.Scatter(x=t_array[:i+1], y=a_array[:i+1]), # a-t 선
                    go.Scatter(x=[t_array[i]], y=[x_array[i]]), # x-t 점
                    go.Scatter(x=[t_array[i]], y=[v_array[i]]), # v-t 점
                    go.Scatter(x=[t_array[i]], y=[a_array[i]])  # a-t 점
                ],
                traces=[4, 5, 6, 7, 8, 9, 10],
                layout=go.Layout(annotations=[
                    # 속도 화살표 (청록색으로 변경, 두껍고 긴 막대, 작은 머리)
                    dict(
                        x=x_array[i] + v_len, y=0.8, ax=x_array[i], ay=0.8,
                        xref="x1", yref="y1", axref="x1", ayref="y1",
                        showarrow=True, arrowhead=2, arrowsize=0.6, arrowwidth=7, arrowcolor="#00CED1",
                    ),
                    # 속도 값 텍스트 (화살표 위에 위치하여 가려지지 않음)
                    dict(
                        x=x_array[i] + v_len/2, y=1.3, xref="x1", yref="y1",
                        text=f"<b>v = {v_array[i]:.1f}</b>", showarrow=False, 
                        font=dict(color="#008B8B", size=15)
                    )
                ])
            ))
        fig.frames = frames

        # --- 안내 상자 배치 (그래프 영역 침범 방지) ---
        # 기울기 정보 (그래프 row의 위쪽 여백)
        fig.add_annotation(x=0.33, y=0.48, xref="paper", yref="paper", text="<b>기울기 ➡</b><br>속도($v$)", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=6)
        fig.add_annotation(x=0.69, y=0.48, xref="paper", yref="paper", text="<b>기울기 ➡</b><br>가속도($a$)", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=6)
        
        # 밑넓이 정보 (그래프 row의 아래쪽 여백)
        fig.add_annotation(x=0.33, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b><br>위치 변화량($\Delta x$)", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=6)
        fig.add_annotation(x=0.69, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b><br>속도 변화량($\Delta v$)", 
                           showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=6)

        # 레이아웃 설정 (버튼을 상단으로 이동)
        fig.update_layout(
            height=950,
            showlegend=False,
            # 재생/일시정지 버튼을 그래프 좌측 상단(초기화 버튼 근처 위치)으로 배치
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 40, "redraw": False}, "fromcurrent": True}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, xanchor="left", y=1.1, yanchor="top"
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), yaxis=dict(range=[-1, 2], showticklabels=False),
            xaxis2=dict(range=[0, max_t], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 (m)"),
            xaxis3=dict(range=[0, max_t], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 (m/s)"),
            xaxis4=dict(range=[0, max_t], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 (m/s²)")
        )

        st.plotly_chart(fig, use_container_width=True)

# 2차원 운동 페이지 (기존 로직 유지)
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tab1, tab2, tab3 = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    with tab1:
        st.header("🍎 자유낙하 운동")
        t = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t1")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=500)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.header("☄️ 수평 투사 운동")
        t = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t2")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=500)
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.header("🎡 등속 원운동")
        ang = st.slider("각도 (도)", 0, 360, 45, key="t3")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=500)
        st.plotly_chart(fig, use_container_width=True)
