import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 페이지 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

# 사이드바 메뉴 (슬라이더만 유지)
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["1차원 운동", "2차원 운동"])

if page == "1차원 운동":
    st.title("📈 1차원 운동 시뮬레이션")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 운동 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        st.markdown("---")
        # 초기화 버튼
        if st.button("🔄 초기화", use_container_width=True):
            st.rerun()

    with col_main:
        # 고정된 소제목
        st.subheader("■ 물체의 위치와 속도")

        # 데이터 생성 (100프레임)
        max_t = 10.0
        frames_count = 100
        t_arr = np.linspace(0, max_t, frames_count)
        x_arr = v0 * t_arr + 0.5 * a * t_arr**2
        v_arr = v0 + a * t_arr
        a_arr = np.full_like(t_arr, a)

        # 서브플롯 구성
        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            subplot_titles=("", "■ 위치-시간 그래프", "■ 속도-시간 그래프", "■ 가속도-시간 그래프"),
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25
        )

        # [0~3번 트레이스] 배경 (도로 및 예상 점선)
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False, hoverinfo='skip'), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=x_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=v_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_arr, y=a_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=3)

        # [4번 트레이스] 움직이는 빨간 점 (초기값 설정)
        fig.add_trace(go.Scatter(x=[x_arr[0]], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)
        
        # [5~7번 트레이스] 실시간으로 그려질 실선 (초기에는 첫 점만)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=2, col=3)

        # [8~10번 트레이스] 현재 위치 마커
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=2, col=3)

        # --- 애니메이션 프레임 (데이터 중복 방지 로직) ---
        frames = []
        for i in range(frames_count):
            curr_v = v_arr[i]
            v_len = curr_v * 1.5 
            
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_arr[i]], y=[0]), # Index 4 (점)
                    go.Scatter(x=t_arr[:i+1], y=x_arr[:i+1]), # Index 5 (x-t 선)
                    go.Scatter(x=t_arr[:i+1], y=v_arr[:i+1]), # Index 6 (v-t 선)
                    go.Scatter(x=t_arr[:i+1], y=a_arr[:i+1]), # Index 7 (a-t 선)
                    go.Scatter(x=[t_arr[i]], y=[x_arr[i]]), # Index 8 (x-t 점)
                    go.Scatter(x=[t_arr[i]], y=[v_arr[i]]), # Index 9 (v-t 점)
                    go.Scatter(x=[t_arr[i]], y=[a_arr[i]])  # Index 10 (a-t 점)
                ],
                traces=[4, 5, 6, 7, 8, 9, 10], # 정확히 해당 인덱스만 교체하여 이중 그리기 방지
                layout=go.Layout(annotations=[
                    # 속도 화살표: 청록색, 두께 12, 작은 머리(0.3)
                    dict(
                        x=x_arr[i] + v_len, y=0.7, ax=x_arr[i], ay=0.7,
                        xref="x1", yref="y1", axref="x1", ayref="y1",
                        showarrow=True, arrowhead=2, arrowsize=0.3, arrowwidth=12, arrowcolor="#00CED1"
                    ),
                    # 속도 값 텍스트 (화살표 상단 배치)
                    dict(
                        x=x_arr[i], y=1.7, xref="x1", yref="y1",
                        text=f"<b>속도 = {curr_v:.1f} m/s</b>", showarrow=False, 
                        font=dict(color="#008B8B", size=15)
                    )
                ])
            ))
        fig.frames = frames

        # --- 안내 상자 위치 (요청하신 정밀 좌표 엄수) ---
        slope_box = dict(showarrow=False, font=dict(size=14, color="white"), bgcolor="#1f77b4", borderpad=6)
        fig.add_annotation(x=0.28, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 속도 정보", **slope_box)
        fig.add_annotation(x=0.69, y=0.62, xref="paper", yref="paper", text="<b>기울기 ➡</b> 가속도 정보", **slope_box)
        
        area_box = dict(showarrow=False, font=dict(size=14, color="white"), bgcolor="#ff7f0e", borderpad=6)
        fig.add_annotation(x=0.28, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 위치 변화량", **area_box)
        fig.add_annotation(x=0.69, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 속도 변화량", **area_box)

        # 레이아웃 설정 (버튼을 시뮬레이터 위쪽으로 배치)
        fig.update_layout(
            height=850,
            margin=dict(l=20, r=20, t=60, b=150),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 40, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", x=0.0, y=1.12, xanchor="left", yanchor="top"
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), 
            yaxis=dict(range=[-1, 2.5], showticklabels=False),
            xaxis2=dict(range=[0, 10], title="시간 (s)"), yaxis2=dict(range=[-50, 50]),
            xaxis3=dict(range=[0, 10], title="시간 (s)"), yaxis3=dict(range=[-20, 20]),
            xaxis4=dict(range=[0, 10], title="시간 (s)"), yaxis4=dict(range=[-10, 10])
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tabs = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    with tabs[0]:
        st.subheader("■ 자유낙하 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="f_v11")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=450)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        st.subheader("■ 수평 투사 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v11")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=450)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v11")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
