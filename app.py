import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 페이지 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

# 사이드바 메뉴 
st.sidebar.title("📚 학습 메뉴")
# [수정] 2페이지 메뉴 이름 변경
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["위치/속도/가속도", "중력에 의한 운동"])

if page == "위치/속도/가속도":
    st.title("📈 물체의 운동에 따른 시뮬레이션과 위치/속도/가속도 분석")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 운동 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)

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
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25
        )

        # [0번 트레이스] 배경 도로 선만 남기고 예상 점선 궤적 모두 삭제
        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False, hoverinfo='skip'), row=1, col=1)

        # [1번 트레이스] 움직이는 빨간 점 (초기값)
        fig.add_trace(go.Scatter(x=[x_arr[0]], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)
        
        # [2~4번 트레이스] 실시간 라인 (위치, 속도, 가속도)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=2, col=3)

        # [5~7번 트레이스] 그래프 현재 위치 마커
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=2, col=3)

        # 각 그래프의 고정된 제목을 생성하는 함수
        def get_title_annotations():
            return [
                dict(x=0.15, y=0.62, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=16)),
                dict(x=0.50, y=0.62, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=16)),
                dict(x=0.85, y=0.62, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=16))
            ]

        # --- 애니메이션 프레임 ---
        frames = []
        for i in range(frames_count):
            curr_v = v_arr[i]
            v_len = curr_v * 1.5 
            
            frame_annotations = get_title_annotations()
            
            # 속도 화살표
            frame_annotations.append(
                dict(
                    x=x_arr[i] + v_len, y=0.7, ax=x_arr[i], ay=0.7,
                    xref="x1", yref="y1", axref="x1", ayref="y1",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor="#00CED1"
                )
            )
            # 동적 속도 값 텍스트
            frame_annotations.append(
                dict(
                    x=x_arr[i], y=1.7, xref="x1", yref="y1",
                    text=f"<b>속도 = {curr_v:.1f} m/s</b>", showarrow=False, 
                    font=dict(color="#008B8B", size=15)
                )
            )

            frames.append(go.Frame(
                name=f'frame_{i}',
                data=[
                    go.Scatter(x=[x_arr[i]], y=[0]), # 1번: 물체 점
                    go.Scatter(x=t_arr[:i+1], y=x_arr[:i+1]), # 2번: x-t 선 
                    go.Scatter(x=t_arr[:i+1], y=v_arr[:i+1]), # 3번: v-t 선
                    go.Scatter(x=t_arr[:i+1], y=a_arr[:i+1]), # 4번: a-t 선
                    go.Scatter(x=[t_arr[i]], y=[x_arr[i]]), # 5번: x-t 점
                    go.Scatter(x=[t_arr[i]], y=[v_arr[i]]), # 6번: v-t 점
                    go.Scatter(x=[t_arr[i]], y=[a_arr[i]])  # 7번: a-t 점
                ],
                traces=[1, 2, 3, 4, 5, 6, 7], 
                layout=go.Layout(annotations=frame_annotations)
            ))
        fig.frames = frames

        # 초기 상태(프레임 0)의 레이아웃 Annotation 설정
        initial_annotations = get_title_annotations()
        initial_annotations.append(dict(
            x=x_arr[0] + v_arr[0] * 1.5, y=0.7, ax=x_arr[0], ay=0.7, 
            xref="x1", yref="y1", axref="x1", ayref="y1", 
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor="#00CED1"
        ))
        initial_annotations.append(dict(
            x=x_arr[0], y=1.7, xref="x1", yref="y1", 
            text=f"<b>속도 = {v_arr[0]:.1f} m/s</b>", showarrow=False, font=dict(color="#008B8B", size=15)
        ))

        fig.update_layout(
            height=650, 
            margin=dict(l=20, r=20, t=60, b=60), 
            annotations=initial_annotations,
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="▶️ 재생", method="animate", args=[None, {"frame": {"duration": 40, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 초기화", method="animate", args=[["frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.12, xanchor="left", yanchor="top"
            )],
            xaxis=dict(range=[-50, 50], title="위치 (m)"), 
            yaxis=dict(range=[-1, 2.5], showticklabels=False),
            xaxis2=dict(range=[0, 10], title="시간 (s)"), yaxis2=dict(range=[-50, 50], title="위치 (m)"),
            xaxis3=dict(range=[0, 10], title="시간 (s)"), yaxis3=dict(range=[-20, 20], title="속도 (m/s)"),
            xaxis4=dict(range=[0, 10], title="시간 (s)"), yaxis4=dict(range=[-10, 10], title="가속도 (m/s²)")
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # ==========================================
        # 그래프 간의 관계 표
        # ==========================================
        st.markdown("### 📊 시간에 따른 위치, 속도, 가속도 그래프의 관계")
        
        table_html = """
        <style>
            .relation-table {
                width: 100%;
                border-collapse: collapse;
                text-align: center;
                font-size: 16px;
                margin-top: 10px;
                margin-bottom: 20px;
            }
            .relation-table th {
                background-color: #f1f5f9;
                color: #333;
                padding: 12px;
                border: 1px solid #cbd5e1;
                font-weight: bold;
            }
            .relation-table td {
                padding: 12px;
                border: 1px solid #cbd5e1;
            }
            .highlight-slope {
                color: #1f77b4; /* 파란색 계열 */
                font-weight: bold;
            }
            .highlight-area {
                color: #ff7f0e; /* 주황색 계열 */
                font-weight: bold;
            }
        </style>
        
        <table class="relation-table">
            <thead>
                <tr>
                    <th>그래프 종류</th>
                    <th>기울기가 의미하는 정보 (➡)</th>
                    <th>밑넓이가 의미하는 정보 (⬅)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>위치-시간 그래프</b></td>
                    <td class="highlight-slope">속도</td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><b>속도-시간 그래프</b></td>
                    <td class="highlight-slope">가속도</td>
                    <td class="highlight-area">위치 변화량 (변위)</td>
                </tr>
                <tr>
                    <td><b>가속도-시간 그래프</b></td>
                    <td>-</td>
                    <td class="highlight-area">속도 변화량</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

# [수정] 2페이지 로직
elif page == "중력에 의한 운동":
    st.title("🌐 중력에 의한 운동")
    # [수정] 탭 이름 변경
    tabs = st.tabs(["자유낙하운동(등가속도직선운동)", "포물선운동(수평으로 던진 운동)", "등속 원운동"])
    g = 9.8
    
    with tabs[0]:
        st.subheader("■ 자유낙하운동(등가속도직선운동)")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="f_v18")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-50, 5]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[1]:
        st.subheader("■ 포물선운동(수평으로 던진 운동)")
        t = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v18")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t], y=[44.1-0.5*g*t**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40]), yaxis=dict(range=[0, 50]), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v18")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
