import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 페이지 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

# 사이드바 메뉴 
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["위치/속도/가속도", "중력에 의한 운동"])

# ==========================================
# 1페이지: 위치/속도/가속도 (기존 기능 유지)
# ==========================================
if page == "위치/속도/가속도":
    st.title("📈 물체의 운동에 따른 시뮬레이션과 위치/속도/가속도 분석")
    
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 운동 조건 설정")
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)

    with col_main:
        st.subheader("■ 물체의 위치와 속도")

        max_t = 10.0
        frames_count = 100
        t_arr = np.linspace(0, max_t, frames_count)
        x_arr = v0 * t_arr + 0.5 * a * t_arr**2
        v_arr = v0 + a * t_arr
        a_arr = np.full_like(t_arr, a)

        fig = make_subplots(
            rows=2, cols=3, 
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            row_heights=[0.3, 0.7],
            vertical_spacing=0.25
        )

        fig.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False, hoverinfo='skip'), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=x_arr, mode='lines', line=dict(color='rgba(0,0,255,0.4)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=v_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_arr, y=a_arr, mode='lines', line=dict(color='rgba(200,200,200,0.3)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=3)

        fig.add_trace(go.Scatter(x=[x_arr[0]], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=2, col=3)

        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=2, col=3)

        def get_title_annotations():
            return [
                dict(x=0.15, y=0.62, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=16)),
                dict(x=0.50, y=0.62, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=16)),
                dict(x=0.85, y=0.62, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=16))
            ]

        frames = []
        for i in range(frames_count):
            curr_v = v_arr[i]
            v_len = curr_v * 1.5 
            
            frame_annotations = get_title_annotations()
            frame_annotations.append(
                dict(
                    x=x_arr[i] + v_len, y=0.7, ax=x_arr[i], ay=0.7,
                    xref="x1", yref="y1", axref="x1", ayref="y1",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor="#00CED1"
                )
            )
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
                    go.Scatter(x=[x_arr[i]], y=[0]),
                    go.Scatter(x=t_arr[:i+1], y=v_arr[:i+1]),
                    go.Scatter(x=t_arr[:i+1], y=a_arr[:i+1]),
                    go.Scatter(x=[t_arr[i]], y=[v_arr[i]]),
                    go.Scatter(x=[t_arr[i]], y=[a_arr[i]])
                ],
                traces=[4, 5, 6, 7, 8], 
                layout=go.Layout(annotations=frame_annotations)
            ))
        fig.frames = frames

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
            height=650, margin=dict(l=20, r=20, t=60, b=60), annotations=initial_annotations,
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

        # 하단 관계 표
        st.markdown("### 📊 시간에 따른 위치, 속도, 가속도 그래프의 관계")
        table_html = """
        <style>
            .relation-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 16px; margin-top: 10px; margin-bottom: 20px; }
            .relation-table th { background-color: #f1f5f9; color: #333; padding: 12px; border: 1px solid #cbd5e1; font-weight: bold; }
            .relation-table td { padding: 12px; border: 1px solid #cbd5e1; }
            .highlight-slope { color: #1f77b4; font-weight: bold; }
            .highlight-area { color: #ff7f0e; font-weight: bold; }
        </style>
        <table class="relation-table">
            <thead><tr><th>그래프 종류</th><th>기울기가 의미하는 정보 (➡)</th><th>밑넓이가 의미하는 정보 (⬅)</th></tr></thead>
            <tbody>
                <tr><td><b>위치-시간 그래프</b></td><td class="highlight-slope">속도</td><td>-</td></tr>
                <tr><td><b>속도-시간 그래프</b></td><td class="highlight-slope">가속도</td><td class="highlight-area">위치 변화량 (변위)</td></tr>
                <tr><td><b>가속도-시간 그래프</b></td><td>-</td><td class="highlight-area">속도 변화량</td></tr>
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

# ==========================================
# 2페이지: 중력에 의한 운동 (대폭 수정 영역)
# ==========================================
elif page == "중력에 의한 운동":
    st.title("🌐 중력에 의한 운동 분석 시뮬레이션")
    tabs = st.tabs(["자유낙하운동(등가속도직선운동)", "포물선운동(수평으로 던진 운동)", "등속 원운동"])
    
    # ------------------------------------------
    # Tab 1: 자유낙하운동 (실시간 인터랙티브 엔진)
    # ------------------------------------------
    with tabs[0]:
        st.subheader("■ 자유낙하운동(등가속도직선운동)")
        
        # 가속도 조절 슬라이더 (양수만 가능, 지구 중력 가속도 명시)
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            g_input = st.slider("중력 가속도 설정 (m/s²)", min_value=1.0, max_value=25.0, value=9.8, step=0.1)
        with col_s2:
            if abs(g_input - 9.8) < 1e-4:
                st.success("🌍 **9.8 m/s²: 지구 중력 가속도**")
            else:
                st.info(f"선택된 가속도: {g_input} m/s²")
        
        # 물리 데이터 연산 구조 정의
        y_start = 100.0  # 최고 높이 100m에서 고정 낙하 스타트
        t_final = np.sqrt(2 * y_start / g_input) # 지표면 도달 시간 역산
        f_counts = 100
        
        t_space = np.linspace(0, t_final, f_counts)
        y_space = y_start - 0.5 * g_input * t_space**2
        v_space = -g_input * t_space  # 하방 낙하이므로 물리적 속도는 음수 유도
        a_space = np.full_like(t_space, -g_input)
        
        # 시뮬레이터 및 3대 연동 그래프 서브플롯 빌드
        fig_ff = make_subplots(
            rows=2, cols=3,
            specs=[[{"colspan": 3}, None, None], [{}, {}, {}]],
            row_heights=[0.35, 0.65],
            vertical_spacing=0.22
        )
        
        # [0번 트레이스] 지표면 가이드라인 (초록색 바닥선 배치)
        fig_ff.add_trace(go.Scatter(x=[-1, 1], y=[0, 0], mode='lines', line=dict(color='green', width=5), showlegend=False, hoverinfo='skip'), row=1, col=1)
        
        # [1번 트레이스] 낙하하는 메인 빨간 점 (초기 낙하 지점에 안착)
        fig_ff.add_trace(go.Scatter(x=[0], y=[y_space[0]], mode='markers', marker=dict(size=22, color='red'), showlegend=False), row=1, col=1)
        
        # [2~4번 트레이스] 실시간 갱신용 3대 궤적 라인선 (초기 점 세팅)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=2, col=1)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=2, col=3)
        
        # [5~7번 트레이스] 각 그래프의 끝점을 따라가는 실시간 마커 점
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=2, col=3)
        
        # 고정 레이아웃 타이틀 구조화 정의
        def get_ff_annotations():
            return [
                dict(x=0.15, y=0.58, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=15)),
                dict(x=0.50, y=0.58, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=15)),
                dict(x=0.85, y=0.58, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=15))
            ]
            
        # 프레임 순차 배열 빌드 (실시간 드로우 제어 엔진)
        frames_ff = []
        for i in range(f_counts):
            current_ann = get_ff_annotations()
            frames_ff.append(go.Frame(
                name=f'ff_frame_{i}',
                data=[
                    go.Scatter(x=[0], y=[y_space[i]]),            # 1번: 빨간 물체 수직 추락
                    go.Scatter(x=t_space[:i+1], y=y_space[:i+1]), # 2번: 위치 선 실시간 드로우
                    go.Scatter(x=t_space[:i+1], y=v_space[:i+1]), # 3번: 속도 선 실시간 드로우
                    go.Scatter(x=t_space[:i+1], y=a_space[:i+1]), # 4번: 가속도 선 실시간 드로우
                    go.Scatter(x=[t_space[i]], y=[y_space[i]]),   # 5번: 위치 끝 점
                    go.Scatter(x=[t_space[i]], y=[v_space[i]]),   # 6번: 속도 끝 점
                    go.Scatter(x=[t_space[i]], y=[a_space[i]])    # 7번: 가속도 끝 점
                ],
                traces=[1, 2, 3, 4, 5, 6, 7],
                layout=go.Layout(annotations=current_ann)
            ))
        fig_ff.frames = frames_ff
        
        # 전체 도표 초기화 및 인터페이스 스타일 일원화
        fig_ff.update_layout(
            height=700,
            margin=dict(l=30, r=20, t=50, b=50),
            annotations=get_ff_annotations(),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="🚀 낙하", method="animate", args=[None, {"frame": {"duration": 35, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 초기화", method="animate", args=[["ff_frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.14, xanchor="left", yanchor="top"
            )],
            # 상단 자유낙하 뷰포트 축 제어
            xaxis=dict(range=[-1, 1], showticklabels=False, fixedrange=True),
            yaxis=dict(range=[-5, 115], title="높이 (m)", fixedrange=True),
            # 하단 그래프 3대 멀티 축 레이블링 제어
            xaxis2=dict(range=[0, t_final], title="시간 (s)"), yaxis2=dict(range=[-5, 105], title="위치 (m)"),
            xaxis3=dict(range=[0, t_final], title="시간 (s)"), yaxis3=dict(range=[min(v_space)-5, 5], title="속도 (m/s)"),
            xaxis4=dict(range=[0, t_final], title="시간 (s)"), yaxis4=dict(range=[-g_input-5, 5], title="가속도 (m/s²)")
        )
        st.plotly_chart(fig_ff, use_container_width=True, config={'displayModeBar': False})

    # ------------------------------------------
    # Tab 2 & 3: 포물선 및 원운동 (기존 레이아웃 규격 보존)
    # ------------------------------------------
    with tabs[1]:
        st.subheader("■ 포물선운동(수평으로 던진 운동)")
        t_p = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v19")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t_p], y=[44.1-0.5*g*t_p**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40], title="수평 거리 (m)"), yaxis=dict(range=[0, 50], title="연직 높이 (m)"), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v19")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
