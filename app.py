import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 페이지 설정 및 세션 상태 초기화
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="🏎️", layout="wide")

if 'g_val' not in st.session_state:
    st.session_state.g_val = 9.8

# 사이드바 메뉴 
st.sidebar.title("📚 학습 메뉴")
page = st.sidebar.radio("원하는 페이지를 선택하세요:", ["위치/속도/가속도", "중력에 의한 운동"])

# ==========================================
# 1페이지: 위치/속도/가속도
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

# ==========================================
# 2페이지: 중력에 의한 운동 (완벽한 상하 레이아웃 및 깜빡임 제거)
# ==========================================
elif page == "중력에 의한 운동":
    st.title("🌐 중력에 의한 운동 분석 시뮬레이션")
    g_default = 9.8 
    tabs = st.tabs(["자유낙하운동(등가속도직선운동)", "포물선운동(수평으로 던진 운동)", "등속 원운동"])
    
    with tabs[0]:
        st.subheader("■ 자유낙하운동(등가속도직선운동)")
        
        # 1. [최상단] 가속도 슬라이더와 지구 가속도 선택 버튼 배치
        col_slider, col_btn = st.columns([3, 1])
        
        with col_slider:
            g_input = st.slider("중력 가속도 설정 (m/s²)", min_value=1.0, max_value=25.0, value=st.session_state.g_val, step=0.1, key="g_slider_v4")
            st.session_state.g_val = g_input
        
        with col_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # 슬라이더 높이 맞춤용 여백
            if st.button("🌍 지구 중력 가속도 선택 (9.8 m/s²)", use_container_width=True):
                st.session_state.g_val = 9.8
                st.rerun()

        if abs(g_input - 9.8) < 1e-4:
            st.success("🌍 **9.8 m/s²: 지구 중력 가속도 환경입니다.**")
        else:
            st.info(f"현재 가속도 설정값: {g_input} m/s²")
            
        st.markdown("---")

        # 2. [하단] 부드러운 재생을 위한 Plotly 고속 프레임 데이터 선계산
        y_start = 100.0  
        g_curr = st.session_state.g_val
        t_max = np.sqrt(2 * y_start / g_curr)
        frames_count = 100
        
        t_space = np.linspace(0, t_max, frames_count)
        y_space = y_start - 0.5 * g_curr * t_space**2
        v_space = -g_curr * t_space  
        a_space = np.full_like(t_space, -g_curr)
        
        # 1행 4열 구조 서브플롯 빌드 (가로폭 절반, 세로 연장 비율 충족)
        fig_ff = make_subplots(
            rows=1, cols=4,
            column_widths=[0.14, 0.28, 0.28, 0.28],
            horizontal_spacing=0.06
        )
        
        # 정적 기본 요소 추가
        fig_ff.add_trace(go.Scatter(x=[-0.5, 0.5], y=[0, 0], mode='lines', line=dict(color='green', width=6), showlegend=False, hoverinfo='skip'), row=1, col=1) # 바닥선
        fig_ff.add_trace(go.Scatter(x=[0], y=[y_space[0]], mode='markers', marker=dict(size=22, color='red'), showlegend=False), row=1, col=1) # 빨간 공
        
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=1, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=1, col=3)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=1, col=4)
        
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=1, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=1, col=3)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=1, col=4)
        
        # 고정 제목 어노테이션 정의
        def get_ff_annotations():
            return [
                dict(x=0.07, y=1.05, xref="paper", yref="paper", text="<b>■ 자유낙하 시뮬레이션</b>", showarrow=False, font=dict(color="black", size=14), xanchor="center"),
                dict(x=0.35, y=1.05, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=14), xanchor="center"),
                dict(x=0.64, y=1.05, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=14), xanchor="center"),
                dict(x=0.92, y=1.05, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=14), xanchor="center")
            ]

        # 브라우저 GPU 가속용 내장 프레임 적재
        frames_ff = []
        for i in range(frames_count):
            frames_ff.append(go.Frame(
                name=f'ff_frame_{i}',
                data=[
                    go.Scatter(x=[0], y=[y_space[i]]),            
                    go.Scatter(x=t_space[:i+1], y=y_space[:i+1]), 
                    go.Scatter(x=t_space[:i+1], y=v_space[:i+1]), 
                    go.Scatter(x=t_space[:i+1], y=a_space[:i+1]), 
                    go.Scatter(x=[t_space[i]], y=[y_space[i]]),   
                    go.Scatter(x=[t_space[i]], y=[v_space[i]]),   
                    go.Scatter(x=[t_space[i]], y=[a_space[i]])    
                ],
                traces=[1, 2, 3, 4, 5, 6, 7],
                layout=go.Layout(annotations=get_ff_annotations())
            ))
        fig_ff.frames = frames_ff
        
        # [💡 핵심 해결책] 시뮬레이터 바로 상단 위치에 Plotly 내장 재생 버튼 배치 (깜빡임 0%)
        fig_ff.update_layout(
            height=680,
            margin=dict(l=40, r=20, t=60, b=50),
            annotations=get_ff_annotations(),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="🚀 낙하 시작", method="animate", args=[None, {"frame": {"duration": 30, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시 정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 시뮬레이션 초기화", method="animate", args=[["ff_frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.12, xanchor="left", yanchor="top"
            )],
            xaxis=dict(range=[-1, 1], showticklabels=False, fixedrange=True),
            yaxis=dict(range=[-5, 115], title="높이 (m)", fixedrange=True),
            xaxis2=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis2=dict(range=[-5, 105], title="위치 (m)", fixedrange=True),
            xaxis3=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis3=dict(range=[min(v_space)-5, 5], title="속도 (m/s)", fixedrange=True),
            xaxis4=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis4=dict(range=[-30, 5], title="가속도 (m/s²)", fixedrange=True)
        )
        
        st.plotly_chart(fig_ff, use_container_width=True, config={'displayModeBar': False})

    # ------------------------------------------
    # Tab 2 & 3: 포물선 및 등속 원운동 (기존 기능 유지)
    # ------------------------------------------
    with tabs[1]:
        st.subheader("■ 포물선운동(수평으로 던진 운동)")
        t_p = st.slider("시간(s)", 0.0, 3.0, 1.5, key="p_v22")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*t_p], y=[44.1-0.5*g_default*t_p**2], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[0, 40], title="수평 거리 (m)"), yaxis=dict(range=[0, 50], title="연직 높이 (m)"), height=450)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        ang = st.slider("각도(도)", 0, 360, 45, key="c_v22")
        r = np.radians(ang)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[10*np.cos(r)], y=[10*np.sin(r)], mode='markers', marker=dict(size=15, color='red')))
        fig.update_layout(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), height=450)
        st.plotly_chart(fig, use_container_width=True)
