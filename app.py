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
        fig.add_trace(go.Scatter(x=t_arr, y=x_arr, mode='lines', line=dict(color='rgba(0,0,255,0.15)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=v_arr, mode='lines', line=dict(color='rgba(0,128,0,0.15)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=2)
        fig.add_trace(go.Scatter(x=t_arr, y=a_arr, mode='lines', line=dict(color='rgba(255,165,0,0.15)', dash='dash'), showlegend=False, hoverinfo='skip'), row=2, col=3)

        fig.add_trace(go.Scatter(x=[x_arr[0]], y=[0], mode='markers', marker=dict(size=20, color='red'), showlegend=False), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[v_arr[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=2)
        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[a_arr[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=2, col=3)

        fig.add_trace(go.Scatter(x=[t_arr[0]], y=[x_arr[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
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
                    go.Scatter(x=t_arr[:i+1], y=x_arr[:i+1]), 
                    go.Scatter(x=t_arr[:i+1], y=v_arr[:i+1]), 
                    go.Scatter(x=t_arr[:i+1], y=a_arr[:i+1]), 
                    go.Scatter(x=[t_arr[i]], y=[x_arr[i]]),   
                    go.Scatter(x=[t_arr[i]], y=[v_arr[i]]),   
                    go.Scatter(x=[t_arr[i]], y=[a_arr[i]])    
                ],
                traces=[1, 2, 3, 4, 5, 6, 7], 
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
# 2페이지: 중력에 의한 운동
# ==========================================
elif page == "중력에 의한 운동":
    st.title("🌐 중력에 의한 운동 분석 시뮬레이션")
    tabs = st.tabs(["자유낙하운동(등가속도직선운동)", "포물선운동(수평으로 던진 운동)", "등속 원운동"])
    
    # ------------------------------------------
    # Tab 1: 자유낙하운동
    # ------------------------------------------
    with tabs[0]:
        st.subheader("■ 자유낙하운동(등가속도직선운동)")
        col_slider, col_btn = st.columns([3, 1])
        with col_slider:
            g_input = st.slider("중력 가속도 설정 (m/s²)", min_value=1.0, max_value=25.0, value=st.session_state.g_val, step=0.1, key="g_slider_v7")
            st.session_state.g_val = g_input
        with col_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🌍 지구 중력 가속도 선택 (9.8 m/s²)", use_container_width=True):
                st.session_state.g_val = 9.8
                st.rerun()

        st.info(f"현재 가속도 설정값: {g_input} m/s²\n\n:red[지구 중력 가속도: 9.8 m/s²]")
        st.markdown("---")

        y_start = 100.0  
        g_curr = st.session_state.g_val
        t_max = np.sqrt(2 * y_start / g_curr)
        frames_count = 100
        
        t_space = np.linspace(0, t_max, frames_count)
        y_space = y_start - 0.5 * g_curr * t_space**2
        v_space = -g_curr * t_space  
        a_space = np.full_like(t_space, -g_curr)
        
        fig_ff = make_subplots(rows=1, cols=4, column_widths=[0.14, 0.28, 0.28, 0.28], horizontal_spacing=0.06)
        fig_ff.add_trace(go.Scatter(x=[-0.5, 0.5], y=[0, 0], mode='lines', line=dict(color='green', width=6), showlegend=False, hoverinfo='skip'), row=1, col=1)
        fig_ff.add_trace(go.Scatter(x=[0], y=[y_space[0]], mode='markers', marker=dict(size=22, color='red'), showlegend=False), row=1, col=1)
        
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=1, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=1, col=3)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='lines', line=dict(color='orange', width=3.5), showlegend=False), row=1, col=4)
        
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[y_space[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=1, col=2)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[v_space[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=1, col=3)
        fig_ff.add_trace(go.Scatter(x=[t_space[0]], y=[a_space[0]], mode='markers', marker=dict(color='orange', size=8), showlegend=False), row=1, col=4)
        
        def get_ff_annotations():
            return [
                dict(x=0.07, y=1.05, xref="paper", yref="paper", text="<b>■ 자유낙하 시뮬레이션</b>", showarrow=False, font=dict(color="black", size=14), xanchor="center"),
                dict(x=0.35, y=1.05, xref="paper", yref="paper", text="<b>■ 위치-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=14), xanchor="center"),
                dict(x=0.64, y=1.05, xref="paper", yref="paper", text="<b>■ 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=14), xanchor="center"),
                dict(x=0.92, y=1.05, xref="paper", yref="paper", text="<b>■ 가속도-시간 그래프</b>", showarrow=False, font=dict(color="orange", size=14), xanchor="center")
            ]

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
        
        fig_ff.update_layout(
            height=680, margin=dict(l=40, r=20, t=110, b=50), annotations=get_ff_annotations(),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="🚀 낙하 시작", method="animate", args=[None, {"frame": {"duration": 30, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시 정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 시뮬레이션 초기화", method="animate", args=[["ff_frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.18, xanchor="left", yanchor="top" 
            )],
            xaxis=dict(range=[-1, 1], showticklabels=False, fixedrange=True),
            yaxis=dict(range=[-5, 115], title="높이 (m)", fixedrange=True),
            xaxis2=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis2=dict(range=[-5, 105], title="위치 (m)", fixedrange=True),
            xaxis3=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis3=dict(range=[min(v_space)-5, 5], title="속도 (m/s)", fixedrange=True),
            xaxis4=dict(range=[0, t_max], title="시간 (s)", fixedrange=True), yaxis4=dict(range=[-30, 5], title="가속도 (m/s²)", fixedrange=True)
        )
        st.plotly_chart(fig_ff, use_container_width=True, config={'displayModeBar': False})

    # ------------------------------------------
    # Tab 2: 포물선운동
    # ------------------------------------------
    with tabs[1]:
        st.subheader("■ 포물선운동(수평으로 던진 운동)")
        st.info("💡 **동기화 분석**: 파란색 실시간 보조선은 **자유낙하운동(연직)과의 일치**를, 주황색 보조선은 **등속도운동(수평)과의 일치**를 보여줍니다. 시뮬레이터 구동 시 아래의 그래프들도 동시에 그려집니다.")
        
        g_p = 9.8
        y0_p = 100.0
        v_x_p = 15.0 
        t_max_p = np.sqrt(2 * y0_p / g_p)
        f_count_p = 100
        
        t_space_p = np.linspace(0, t_max_p, f_count_p)
        x_p_data = v_x_p * t_space_p
        y_p_data = y0_p - 0.5 * g_p * t_space_p**2
        
        v_y_data = -g_p * t_space_p
        v_x_data = np.full_like(t_space_p, v_x_p)
        
        fig_p = make_subplots(
            rows=2, cols=3,
            column_widths=[0.33, 0.33, 0.34],
            row_heights=[0.65, 0.35],
            horizontal_spacing=0.08,
            vertical_spacing=0.25,
            specs=[[{"colspan": 3}, None, None], [{}, None, {}]]
        )
        
        fig_p.add_trace(go.Scatter(x=[-15, -15], y=[0, 100], mode='lines', line=dict(color='darkgray', width=2), showlegend=False, hoverinfo='skip'), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[-25, max(x_p_data)+15], y=[0, 0], mode='lines', line=dict(color='green', width=4), showlegend=False, hoverinfo='skip'), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[0, max(x_p_data)+15], y=[-15, -15], mode='lines', line=dict(color='gray', width=2, dash='solid'), showlegend=False, hoverinfo='skip'), row=1, col=1)
        
        fig_p.add_trace(go.Scatter(x=[-15], y=[y_p_data[0]], mode='markers', marker=dict(size=18, color='red'), showlegend=False), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[x_p_data[0]], y=[y_p_data[0]], mode='lines', line=dict(color='purple', width=2.5, dash='dot'), showlegend=False), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[x_p_data[0]], y=[y_p_data[0]], mode='markers', marker=dict(size=18, color='red'), showlegend=False), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[x_p_data[0]], y=[-15], mode='markers', marker=dict(size=18, color='red'), showlegend=False), row=1, col=1)
        
        fig_p.add_trace(go.Scatter(x=[-15, x_p_data[0]], y=[y_p_data[0], y_p_data[0]], mode='lines', line=dict(color='rgba(0, 0, 255, 0.6)', width=1.5, dash='dash'), showlegend=False), row=1, col=1)
        fig_p.add_trace(go.Scatter(x=[x_p_data[0], x_p_data[0]], y=[-15, y_p_data[0]], mode='lines', line=dict(color='rgba(255,140,0,0.7)', width=1.5, dash='dash'), showlegend=False), row=1, col=1)
        
        fig_p.add_trace(go.Scatter(x=[t_space_p[0]], y=[v_y_data[0]], mode='lines', line=dict(color='blue', width=3.5), showlegend=False), row=2, col=1)
        fig_p.add_trace(go.Scatter(x=[t_space_p[0]], y=[v_y_data[0]], mode='markers', marker=dict(color='blue', size=8), showlegend=False), row=2, col=1)
        
        fig_p.add_trace(go.Scatter(x=[t_space_p[0]], y=[v_x_data[0]], mode='lines', line=dict(color='green', width=3.5), showlegend=False), row=2, col=3)
        fig_p.add_trace(go.Scatter(x=[t_space_p[0]], y=[v_x_data[0]], mode='markers', marker=dict(color='green', size=8), showlegend=False), row=2, col=3)
        
        def get_p_annotations():
            return [
                dict(x=0.03, y=0.98, xref="paper", yref="paper", text="<b>■ 연직(자유낙하)</b>", showarrow=False, font=dict(color="blue", size=13)),
                dict(x=0.50, y=0.98, xref="paper", yref="paper", text="<b>■ 합성 투사운동 (포물선 궤도)</b>", showarrow=False, font=dict(color="purple", size=15), xanchor="center"),
                dict(x=0.50, y=0.30, xref="paper", yref="paper", text="<b>■ 수평(등속도)</b>", showarrow=False, font=dict(color="green", size=13), xanchor="center"),
                dict(x=0.16, y=0.20, xref="paper", yref="paper", text="<b>[연직 성분] 속도-시간 그래프</b>", showarrow=False, font=dict(color="blue", size=14), xanchor="center"),
                dict(x=0.84, y=0.20, xref="paper", yref="paper", text="<b>[수평 성분] 속도-시간 그래프</b>", showarrow=False, font=dict(color="green", size=14), xanchor="center")
            ]
            
        frames_p = []
        for i in range(f_count_p):
            frames_p.append(go.Frame(
                name=f'proj_frame_{i}',
                data=[
                    go.Scatter(x=[-15], y=[y_p_data[i]]),                                 
                    go.Scatter(x=x_p_data[:i+1], y=y_p_data[:i+1]),                       
                    go.Scatter(x=[x_p_data[i]], y=[y_p_data[i]]),                         
                    go.Scatter(x=[x_p_data[i]], y=[-15]),                                 
                    go.Scatter(x=[-15, x_p_data[i]], y=[y_p_data[i], y_p_data[i]]),       
                    go.Scatter(x=[x_p_data[i], x_p_data[i]], y=[-15, y_p_data[i]]),       
                    go.Scatter(x=t_space_p[:i+1], y=v_y_data[:i+1]),                      
                    go.Scatter(x=[t_space_p[i]], y=[v_y_data[i]]),                        
                    go.Scatter(x=t_space_p[:i+1], y=v_x_data[:i+1]),                      
                    go.Scatter(x=[t_space_p[i]], y=[v_x_data[i]])                         
                ],
                traces=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                layout=go.Layout(annotations=get_p_annotations())
            ))
        fig_p.frames = frames_p
        
        fig_p.update_layout(
            height=900,
            margin=dict(l=50, r=40, t=110, b=50),
            annotations=get_p_annotations(),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="🚀 발사 및 투사 시작", method="animate", args=[None, {"frame": {"duration": 35, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시 정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 시뮬레이션 초기화", method="animate", args=[["proj_frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.10, xanchor="left", yanchor="top"
            )],
            xaxis=dict(range=[-28, max(x_p_data)+20], title="수평 이동 거리 (m)", fixedrange=True),
            yaxis=dict(range=[-32, 120], title="연직 높이 (m)", fixedrange=True),
            xaxis2=dict(range=[0, t_max_p], title="시간 (s)", fixedrange=True),
            yaxis2=dict(range=[-50, 5], title="속도 (m/s)", fixedrange=True),
            xaxis3=dict(range=[0, t_max_p], title="시간 (s)", fixedrange=True),
            yaxis3=dict(range=[0, 30], title="속도 (m/s)", fixedrange=True)
        )
        st.plotly_chart(fig_p, use_container_width=True, config={'displayModeBar': False})

    # ------------------------------------------
    # Tab 3: 등속 원운동 (x/y축 제거 및 벡터 레이블 겹침 해결)
    # ------------------------------------------
    with tabs[2]:
        st.subheader("■ 등속 원운동 시뮬레이션")
        st.info("💡 **등속 원운동의 핵심**: 물체의 운동 방향(**속도 화살표**)과 힘의 방향(**가속도 화살표**)은 항상 **90°** 직각을 이룹니다. 가속도(구심력)는 언제나 원의 중심을 향합니다.")
        
        R_c = 10.0
        f_count_c = 120
        t_space_c = np.linspace(0, 2 * np.pi, f_count_c)
        
        x_c_data = R_c * np.cos(t_space_c)
        y_c_data = R_c * np.sin(t_space_c)
        
        fig_c = go.Figure()
        
        t_track = np.linspace(0, 2 * np.pi, 200)
        fig_c.add_trace(go.Scatter(x=R_c*np.cos(t_track), y=R_c*np.sin(t_track), mode='lines', line=dict(color='gray', width=1.5, dash='dash'), showlegend=False, hoverinfo='skip'))
        fig_c.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=6, color='black'), showlegend=False, hoverinfo='skip'))
        fig_c.add_trace(go.Scatter(x=[x_c_data[0]], y=[y_c_data[0]], mode='markers', marker=dict(size=18, color='red'), showlegend=False))
        
        # [💡 수정 사항] 텍스트 레이블의 좌표를 화살표 꼬리(중심)가 아닌 화살표 끝(머리)으로 밀어내어 분리함
        def get_circular_vector_annotations(cx, cy, theta):
            arrow_scale = 4.5
            
            vx = -arrow_scale * np.sin(theta)
            vy = arrow_scale * np.cos(theta)
            
            ax_v = -arrow_scale * np.cos(theta)
            ay_v = -arrow_scale * np.sin(theta)
            
            # v(속도) 라벨 좌표: 원 궤도 바깥쪽 (접선 화살표의 끝부분 근처)
            v_text_x = cx + vx * 1.15
            v_text_y = cy + vy * 1.15
            
            # a(가속도) 라벨 좌표: 원 궤도 안쪽 (가속도 화살표의 끝부분/중심 근처)
            a_text_x = cx + ax_v * 0.7
            a_text_y = cy + ay_v * 0.7
            
            text_x = cx * 0.82
            text_y = cy * 0.82
            
            return [
                # 화살표 드로우 (글씨는 제거)
                dict(x=cx + vx, y=cy + vy, ax=cx, ay=cy, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3.5, arrowcolor="green"),
                dict(x=cx + ax_v, y=cy + ay_v, ax=cx, ay=cy, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3.5, arrowcolor="orange"),
                
                # [💡 독립된 텍스트 레이블] 위치를 화살표 머리 기준으로 띄워서 겹침 완전 방지
                dict(x=v_text_x, y=v_text_y, text="<b>v (속도)</b>", showarrow=False, font=dict(color="green", size=14)),
                dict(x=a_text_x, y=a_text_y, text="<b>a (가속도)</b>", showarrow=False, font=dict(color="orange", size=14)),
                
                dict(x=text_x, y=text_y, text="<b>90°</b>", showarrow=False, font=dict(color="red", size=15))
            ]
            
        frames_c = []
        for i in range(f_count_c):
            th = t_space_c[i]
            cx = x_c_data[i]
            cy = y_c_data[i]
            frames_c.append(go.Frame(
                name=f'circle_frame_{i}',
                data=[go.Scatter(x=[cx], y=[cy])], 
                traces=[2],
                layout=go.Layout(annotations=get_circular_vector_annotations(cx, cy, th))
            ))
        fig_c.frames = frames_c
        
        fig_c.update_layout(
            height=650,
            margin=dict(l=50, r=40, t=110, b=50),
            annotations=get_circular_vector_annotations(x_c_data[0], y_c_data[0], t_space_c[0]),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="🚀 회전 시작", method="animate", args=[None, {"frame": {"duration": 35, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸️ 일시 정지", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="🔄 시뮬레이션 초기화", method="animate", args=[["circle_frame_0"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left", pad={"r": 10, "t": 10}, x=0.0, y=1.14, xanchor="left", yanchor="top"
            )],
            # [💡 수정 완료] showticklabels=False 속성으로 x축과 y축 눈금/숫자를 완전히 보이지 않게 처리
            xaxis=dict(range=[-17, 17], scaleanchor="y", scaleratio=1, showticklabels=False, fixedrange=True, zeroline=False, showgrid=False),
            yaxis=dict(range=[-17, 17], showticklabels=False, fixedrange=True, zeroline=False, showgrid=False)
        )
        st.plotly_chart(fig_c, use_container_width=True, config={'displayModeBar': False})
