import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. 페이지 설정 및 세션 상태 초기화
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

if 'ff_time' not in st.session_state:
    st.session_state.ff_time = 0.0
if 'ff_playing' not in st.session_state:
    st.session_state.ff_playing = False
if 'g_val' not in st.session_state:
    st.session_state.g_val = 9.8

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
# 2페이지: 중력에 의한 운동 (개편 및 버벅임 완전 해결)
# ==========================================
elif page == "중력에 의한 운동":
    st.title("🌐 중력에 의한 운동 분석 시뮬레이션")
    g = 9.8 
    tabs = st.tabs(["자유낙하운동(등가속도직선운동)", "포물선운동(수평으로 던진 운동)", "등속 원운동"])
    
    with tabs[0]:
        st.subheader("■ 자유낙하운동(등가속도직선운동)")
        
        # [혁신] 버벅임과 깜빡임을 원천 차단하기 위한 독립 프래그먼트 컴포넌트 선언
        @st.fragment
        def free_fall_isolated_engine():
            col_ctrl, col_main = st.columns([1, 4])
            
            with col_ctrl:
                st.markdown("### ⚙️ 가속도 및 제어")
                # 슬라이더 동기화 및 가속도 입력 설정
                g_input = st.slider("중력 가속도 설정 (m/s²)", min_value=1.0, max_value=25.0, value=st.session_state.g_val, step=0.1, key="ff_g_slider")
                st.session_state.g_val = g_input
                
                if abs(g_input - 9.8) < 1e-4:
                    st.success("🌍 **9.8 m/s²: 지구 중력 가속도**")
                else:
                    st.info(f"선택된 가속도: {g_input} m/s²")
                
                st.markdown("---")
                # [요청사항] 가속도 슬라이더 바로 아래로 버튼 그룹 배치
                if st.button("🚀 낙하 시작", use_container_width=True):
                    st.session_state.ff_playing = True
                if st.button("🌍 지구 중력 가속도 선택 (9.8)", use_container_width=True):
                    st.session_state.g_val = 9.8
                    st.session_state.ff_time = 0.0
                    st.session_state.ff_playing = False
                    st.rerun()
                if st.button("⏸️ 일시정지", use_container_width=True):
                    st.session_state.ff_playing = False
                if st.button("🔄 시뮬레이션 초기화", use_container_width=True):
                    st.session_state.ff_playing = False
                    st.session_state.ff_time = 0.0
                    st.rerun()
            
            with col_main:
                # 그래프 출력 전용 고정 placeholder (깜빡임 방지의 핵심 핵심 요쇼)
                chart_target = st.empty()
                
                # 물리 기초 상수 및 타임 스케일 연산
                y_start = 100.0  
                t_final = np.sqrt(2 * y_start / g_input)
                
                # 실시간 물리 엔진 구동 루프 (재생 상태일 때 프래그먼트 내부 고속 반복 처리)
                while st.session_state.ff_playing:
                    if st.session_state.ff_time < t_final:
                        st.session_state.ff_time = min(st.session_state.ff_time + 0.04, t_final)
                    else:
                        st.session_state.ff_playing = False
                    
                    # 헬퍼 함수를 통해 차트 객체 실시간 주입
                    fig = build_ff_figure(st.session_state.ff_time, t_final, g_input, y_start)
                    chart_target.plotly_chart(fig, key="ff_live_canvas", use_container_width=True, config={'displayModeBar': False})
                    time.sleep(0.02) # 최적의 프레임 레이트 유지용 미세 대기
                    
                    if not st.session_state.ff_playing:
                        st.rerun() # 재생 종료 동기화

                # 정지 혹은 초기화 상태일 때의 정적 뷰포트 출력 (동일한 키값 지정으로 프레임 전환 잔상 삭제)
                fig = build_ff_figure(st.session_state.ff_time, t_final, g_input, y_start)
                chart_target.plotly_chart(fig, key="ff_live_canvas", use_container_width=True, config={'displayModeBar': False})

        # 차트 빌더 함수 (1행 4열 구조 - 가로폭 절반 축소, 세로 높이 2배 연장 만족)
        def build_ff_figure(t_now, t_max, g_curr, y_max):
            t_space = np.linspace(0, t_max, 100)
            y_space = y_max - 0.5 * g_curr * t_space**2
            v_space = -g_curr * t_space
            a_space = np.full_like(t_space, -g_curr)
            
            mask = t_space <= t_now
            t_data, y_data, v_data, a_data = t_space[mask], y_space[mask], v_space[mask], a_space[mask]
            
            curr_y = y_data[-1] if len(y_data) > 0 else y_max
            
            # [요청사항] 1행 4열 그리드 설계로 시뮬레이터 가로폭 절반 축소 및 세로 높이 대폭 연장 실현
            fig = make_subplots(
                rows=1, cols=4,
                column_widths=[0.14, 0.28, 0.28, 0.28],
                horizontal_spacing=0.06,
                annotations=[
                    dict(x=0.07, y=1.05, xref="paper", yref="paper", text="<b>■ 자유낙하 시뮬레이션</b>", showarrow=False, font=dict(color="black", size=14), xanchor="center"),
                    dict(x=0.35, y=1.05, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=14), xanchor="center"),
                    dict(x=0.64, y=1.05, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=14), xanchor="center"),
                    dict(x=0.92, y=1.05, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=14), xanchor="center")
                ]
            )
            
            # Col 1: 수직 낙하 타워 뷰포트 (바닥 초록선 및 빨간 구체)
            fig.add_trace(go.Scatter(x=[-0.5, 0.5], y=[0, 0], mode='lines', line=dict(color='green', width=6), showlegend=False, hoverinfo='skip'), row=1, col=1)
            fig.add_trace(go.Scatter(x=[0], y=[curr_y], mode='markers', marker=dict(size=22, color='red'), showlegend=False), row=1, col=1)
            
            # Col 2~4: 멀티 연동 실시간 선 드로우
            fig.add_trace(go.Scatter(x=t_data, y=y_data, mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=1, col=2)
            fig.add_trace(go.Scatter(x=t_data, y=v_data, mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=1, col=3)
            fig.add_trace(go.Scatter(x=t_data, y=a_data, mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=1, col=4)
            
            # 각 추적선 끝 마커 동기화
            if len(t_data) > 0:
                fig.add_trace(go.Scatter(x=[t_data[-1]], y=[y_data[-1]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=1, col=2)
                fig.add_trace(go.Scatter(x=[t_data[-1]], y=[v_data[-1]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=1, col=3)
                fig.add_trace(go.Scatter(x=[t_data[-1]], y=[a_data[-1]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=1, col=4)
            
            # 레이아웃 스타일 획일화 및 축 레이블 고정
            fig.update_layout(
                height=680, # 단일 행 배치로 시뮬레이터 높이가 이전의 2배 이상 연장됨
                margin=dict(l=40, r=20, t=60, b=50),
                xaxis=dict(range=[-1, 1], showticklabels=False, fixedrange=True),
                yaxis=dict(range=[-5, 115], title="높이 (m)", fixedrange=True),
                xaxis2=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis2=dict(range=[-5, 105], title="위치 (m)", fixedrange=True),
                xaxis3=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis3=dict(range=[min(v_space)-5, 5], title="속도 (m/s)", fixedrange=True),
                xaxis4=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis4=dict(range=[-30, 5], title="가속도 (m/s²)", fixedrange=True)
            )
            return fig

        # 엔진 구동
        free_fall_isolated_engine()

    # ------------------------------------------
    # Tab 2 & 3: 포물선 및 등속 원운동 (규격 보존)
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
