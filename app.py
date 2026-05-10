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
# 1차원 운동 페이지 (완벽한 부드러움 구현)
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
        st.info("버벅거림 없는 부드러운 화면을 위해 **우측 그래프 상단에 통합된 [▶️ 재생] 버튼**을 눌러주세요.")
        
        # 초기화 버튼
        if st.button("🔄 초기화", use_container_width=True):
            st.rerun()

    with col_main:
        # 100프레임 데이터 생성 (부드러운 60fps급 애니메이션용)
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
            subplot_titles=("■ 물체의 위치 및 속도 벡터 시뮬레이션", "■ 위치-시간 그래프", "■ 속도-시간 그래프", "■ 가속도-시간 그래프"),
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25
        )

        # 정적 배경 (도로 및 가이드라인)
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=x_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=v_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_arr, y=a_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False), row=2, col=3)

        # 동적 요소 초기화 (Trace Index 4 ~ 10)
        fig.add_trace(go.Scatter(x=[x_arr[0]], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='lines', line=dict(color='blue', width=3), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='lines', line=dict(color='green', width=3), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='lines', line=dict(color='orange', width=3), showlegend=False), row=2, col=3)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=2, col=3)

        # --- 프레임 생성 (브라우저 가속 방식) ---
        frames = []
        for i in range(frames_count):
            curr_v = v_arr[i]
            v_len = curr_v * 1.5 # 막대 길이 1.5배
            
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_arr[i]], y=[0]), # 물체
                    go.Scatter(x=t_arr[:i+1], y=x_arr[:i+1]), # x-t 선
                    go.Scatter(x=t_arr[:i+1], y=v_arr[:i+1]), # v-t 선
                    go.Scatter(x=t_arr[:i+1], y=a_arr[:i+1]), # a-t 선
                    go.Scatter(x=[t_arr[i]], y=[x_arr[i]]), # x-t 점
                    go.Scatter(x=[t_arr[i]], y=[v_arr[i]]), # v-t 점
                    go.Scatter(x=[t_arr[i]], y=[a_arr[i]])  # a-t 점
                ],
                traces=[4, 5, 6, 7, 8, 9, 10],
                layout=go.Layout(annotations=[
                    # 속도 화살표: 두껍고 긴 막대, 작은 삼각형 머리, 청록색
                    dict(
                        x=x_arr[i] + v_len, y=0.7, ax=x_arr[i], ay=0.7,
                        xref="x1", yref="y1", axref="x1", ayref="y1",
                        showarrow=True, arrowhead=2, arrowsize=0.5, arrowwidth=9, arrowcolor="#00CED1"
                    ),
                    # 속도 텍스트: 화살표 위쪽에 배치
                    dict(
                        x=x_arr[i], y=1.6, xref="x1", yref="y1",
                        text=f"<b>속도 = {curr_v:.1f} m/s</b>", showarrow=False, 
                        font=dict(color="#008B8B", size=14)
                    )
                ])
            ))
        fig.frames = frames

        # --- 안내 상자 위치 및 텍스트 (요청사항 반영) ---
        slope_box = dict(showarrow=False, font=dict(size=13, color="white"), bgcolor="#1f77b4", borderpad=5)
        # 기울기(속도) 상자: 왼쪽(x=0.25) 및 위쪽(y=0.65)으로 이동
        fig.add_annotation(x=0.25, y=0.65, xref="paper", yref="paper", text="<b>기울기 ➡</b> 속도 정보", **slope_box)
        # 기울기(가속도) 상자: 높이만 위쪽(y=0.65)으로 이동
        fig.add_annotation(x=0.69, y=0.65, xref="paper", yref="paper", text="<b>기울기 ➡</b> 가속도 정보", **slope_box)
        
        area_box = dict(showarrow=False, font=dict(size=13, color="white"), bgcolor="#ff7f0e", borderpad=5)
        # 밑넓이(위치 변화량) 상자: 왼쪽(x=0.25) 및 축 아래 배치
        fig.add_annotation(x=0.25, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 위치 변화량", **area_box)
        # 밑넓이(속도 변화량) 상자: 축 아래 배치
        fig.add_annotation(x=0.69, y=-0.15, xref="paper", yref="paper", text="<b>⬅ 밑넓이</b> 속도 변화량", **area_box)

        # 레이아웃 설정 (버튼 그룹화)
        fig.update_layout(
            height=850,
            margin=dict(l=20, r=20, t=80, b=100),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 40, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", x=0.0, y=1.12, xanchor="left", yanchor="top"
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), 
            yaxis=dict(range=[-1, 2.2], showticklabels=False),
            xaxis2=dict(range=[0, max_t], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 (m)"),
            xaxis3=dict(range=[0, max_t], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 (m/s)"),
            xaxis4=dict(range=[0, max_t], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 (m/s²)")
        )

        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 2차원 운동 페이지
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    tabs = st.tabs(["자유낙하", "수평 투사", "등속 원운동"])
    g = 9.8
    
    with tabs[0]:
        st.subheader("■ 자유낙하 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="f_v4")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[1]:
        st.subheader("■ 수평 투사 시뮬레이션")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v4")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v4")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
