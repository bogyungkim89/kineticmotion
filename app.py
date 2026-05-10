import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# 페이지 기본 설정
st.set_page_config(page_title="운동학 시뮬레이션", page_icon="물리", layout="wide")

# 세션 상태 초기화 (애니메이션을 위한 시간 및 실행 상태 관리)
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
    
    # 좌측 컨트롤, 우측 시뮬레이션 영역 분리
    col_ctrl, col_main = st.columns([1, 4])
    
    with col_ctrl:
        st.markdown("### ⚙️ 속도와 가속도")
        st.caption("초기 조건 설정")
        # 세로 배치 슬라이더
        v0 = st.slider("초기 속도 (m/s)", -10.0, 10.0, 2.0, step=1.0)
        a = st.slider("가속도 (m/s²)", -5.0, 5.0, 0.5, step=0.5)
        
        st.markdown("---")
        st.markdown("### 🎬 시뮬레이션 제어")
        
        # 버튼 컨트롤
        if st.button("▶️ 시작", use_container_width=True):
            if st.session_state.time >= 10.0:
                st.session_state.time = 0.0
            st.session_state.running = True
            st.rerun()
            
        if st.button("⏸️ 일시정지", use_container_width=True):
            st.session_state.running = False
            st.rerun()
            
        if st.button("⏹️ 종료 (초기화)", use_container_width=True):
            st.session_state.running = False
            st.session_state.time = 0.0
            st.rerun()
            
        st.markdown(f"**현재 시간:** {st.session_state.time:.1f} 초")

    with col_main:
        # 애니메이션이 표시될 빈 공간(placeholder) 생성
        sim_placeholder = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        graph_placeholder = st.empty()

        # 데이터 계산 (0~10초)
        max_t = 10.0
        t_array = np.linspace(0, max_t, 200)
        x_array = v0 * t_array + 0.5 * a * t_array**2
        v_array = v0 + a * t_array
        a_array = np.full_like(t_array, a)

        # 현재 시간까지의 데이터 마스킹
        mask = t_array <= st.session_state.time
        current_t = t_array[mask]
        current_x = x_array[mask]
        current_v = v_array[mask]
        current_a = a_array[mask]
        
        # 1. 물체 이동 시뮬레이션 그리기
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Scatter(x=[-50, 50], y=[0, 0], mode='lines', line=dict(color='gray', width=2)))
        
        # 현재 위치에 점 표시
        if len(current_x) > 0:
            fig_sim.add_trace(go.Scatter(x=[current_x[-1]], y=[0], mode='markers', marker=dict(size=20, color='red')))
            
        fig_sim.update_layout(
            title="🚗 물체의 이동 (현재 위치)",
            xaxis_title="위치 (m)",
            yaxis=dict(showticklabels=False, range=[-1, 1]),
            height=200, margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(range=[-50, 50]), showlegend=False
        )
        sim_placeholder.plotly_chart(fig_sim, use_container_width=True)

        # 2. 3개의 그래프와 화살표 관계 그리기
        col_g1, col_arr1, col_g2, col_arr2, col_g3 = st.columns([3, 1, 3, 1, 3])
        
        # 화살표 UI (가운데 정렬)
        arrow_html_1 = """
        <div style='text-align: center; margin-top: 120px; font-size: 14px;'>
            <b>기울기 ➡</b><br><span style='font-size: 11px; color:gray;'>(속도 정보 획득)</span><br><br>
            <b>⬅ 넓이</b><br><span style='font-size: 11px; color:gray;'>(위치 정보 획득)</span>
        </div>
        """
        arrow_html_2 = """
        <div style='text-align: center; margin-top: 120px; font-size: 14px;'>
            <b>기울기 ➡</b><br><span style='font-size: 11px; color:gray;'>(가속도 정보 획득)</span><br><br>
            <b>⬅ 넓이</b><br><span style='font-size: 11px; color:gray;'>(속도 정보 획득)</span>
        </div>
        """
        
        with col_arr1: st.markdown(arrow_html_1, unsafe_allow_html=True)
        with col_arr2: st.markdown(arrow_html_2, unsafe_allow_html=True)

        # 그래프 생성 함수
        def create_graph(x_data, y_data, title, y_label, color, max_y_range):
            fig = go.Figure()
            # 전체 궤적은 흐리게 배경으로 표시 (학생들이 예상 궤적을 볼 수 있게)
            fig.add_trace(go.Scatter(x=t_array, y=y_data if type(y_data) == np.ndarray else np.full_like(t_array, y_data), 
                                     mode='lines', line=dict(color='lightgray', dash='dash')))
            # 현재 시간까지의 궤적은 진하게 표시
            if len(x_data) > 0:
                fig.add_trace(go.Scatter(x=x_data, y=y_data[:len(x_data)] if type(y_data) == np.ndarray else np.full_like(x_data, y_data), 
                                         mode='lines', line=dict(color=color, width=3)))
                fig.add_trace(go.Scatter(x=[x_data[-1]], y=[y_data[len(x_data)-1]] if type(y_data) == np.ndarray else [y_data], 
                                         mode='markers', marker=dict(color=color, size=10)))
            
            fig.update_layout(title=title, xaxis_title="시간 (s)", yaxis_title=y_label, 
                              height=300, margin=dict(l=20, r=20, t=40, b=20),
                              xaxis=dict(range=[0, max_t]), yaxis=dict(range=max_y_range), showlegend=False)
            return fig

        with col_g1: st.plotly_chart(create_graph(current_t, x_array, "위치-시간 (x-t)", "위치 (m)", "blue", [-50, 50]), use_container_width=True)
        with col_g2: st.plotly_chart(create_graph(current_t, v_array, "속도-시간 (v-t)", "속도 (m/s)", "green", [-20, 20]), use_container_width=True)
        with col_g3: st.plotly_chart(create_graph(current_t, a_array, "가속도-시간 (a-t)", "가속도 (m/s²)", "orange", [-10, 10]), use_container_width=True)

    # 애니메이션 진행 로직 (running이 True일 때 계속 페이지를 재실행하며 시간을 증가시킴)
    if st.session_state.running:
        time.sleep(0.05) # 속도 조절
        st.session_state.time += 0.1
        if st.session_state.time > max_t:
            st.session_state.running = False
        st.rerun()

# ==========================================
# 페이지 2: 2차원 운동
# ==========================================
elif page == "2차원 운동":
    st.title("🌐 2차원 운동 분석")
    st.write("다양한 2차원 운동에서 속도와 가속도의 특징을 확인해 보세요.")
    
    # 3가지 운동을 탭으로 분리하여 깔끔하게 제공
    tab1, tab2, tab3 = st.tabs(["1. 자유낙하 운동", "2. 수평 투사 (포물선) 운동", "3. 등속 원운동"])
    
    g = 9.8 # 중력가속도
    
    with tab1:
        st.header("🍎 자유낙하 운동")
        st.markdown("**특징:** 중력만 받아 연직 아래 방향으로 **가속도가 일정한(등가속도)** 운동입니다.")
        t_free = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t_free")
        
        y_free = -0.5 * g * t_free**2
        vy_free = -g * t_free
        
        fig_free = go.Figure()
        # 물체
        fig_free.add_trace(go.Scatter(x=[0], y=[y_free], mode='markers', marker=dict(size=15, color='blue'), name="물체"))
        # 속도 벡터 (녹색)
        if t_free > 0:
            fig_free.add_annotation(x=0, y=y_free + vy_free/2, ax=0, ay=y_free, xref="x", yref="y", axref="x", ayref="y",
                                    showarrow=True, arrowhead=2, arrowsize=1.5, arrowcolor="green", text="속도 v")
        # 가속도 벡터 (주황색, 크기 일정)
        fig_free.add_annotation(x=0.5, y=y_free - g, ax=0.5, ay=y_free, xref="x", yref="y", axref="x", ayref="y",
                                showarrow=True, arrowhead=2, arrowsize=1.5, arrowcolor="orange", text="가속도 g (일정)")
                                
        fig_free.update_layout(xaxis=dict(range=[-2, 2], showticklabels=False), yaxis=dict(range=[-50, 5], title="높이 (m)"), height=400)
        st.plotly_chart(fig_free, use_container_width=True)

    with tab2:
        st.header("☄️ 지표면 위에서 수평으로 던진 포물선 운동")
        st.markdown("**특징:** 수평 방향으로는 힘을 받지 않아 **등속 직선 운동**을, 연직 방향으로는 중력을 받아 **자유낙하 운동**을 동시에 합니다.")
        
        t_proj = st.slider("시간 (s)", 0.0, 3.0, 1.5, key="t_proj")
        H = 44.1 # 초기 높이
        vx0 = 10.0 # 수평 초기 속도
        
        x_proj = vx0 * t_proj
        y_proj = H - 0.5 * g * t_proj**2
        vy_proj = -g * t_proj
        
        # 궤적 그리기 (0 ~ 3초)
        t_array_proj = np.linspace(0, 3, 100)
        traj_x = vx0 * t_array_proj
        traj_y = H - 0.5 * g * t_array_proj**2
        
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(x=traj_x, y=traj_y, mode='lines', line=dict(color='gray', dash='dot'), name="궤적"))
        fig_proj.add_trace(go.Scatter(x=[x_proj], y=[y_proj], mode='markers', marker=dict(size=15, color='blue'), name="물체"))
        
        # 수평 속도 벡터 (일정)
        fig_proj.add_annotation(x=x_proj + vx0/2, y=y_proj, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y",
                                showarrow=True, arrowhead=2, arrowcolor="green", text="수평 속도(일정)")
        # 연직 속도 벡터 (증가)
        if t_proj > 0:
            fig_proj.add_annotation(x=x_proj, y=y_proj + vy_proj/2, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y",
                                    showarrow=True, arrowhead=2, arrowcolor="green", text="연직 속도(증가)")
        # 가속도 벡터 (중력)
        fig_proj.add_annotation(x=x_proj, y=y_proj - 10, ax=x_proj, ay=y_proj, xref="x", yref="y", axref="x", ayref="y",
                                showarrow=True, arrowhead=2, arrowcolor="orange", text="중력가속도 g")
                                
        fig_proj.update_layout(xaxis=dict(range=[0, 40], title="수평 거리 (m)"), yaxis=dict(range=[0, 50], title="높이 (m)"), height=400)
        st.plotly_chart(fig_proj, use_container_width=True)

    with tab3:
        st.header("🎡 등속 원운동")
        st.markdown("**특징:** 속력(크기)은 일정하지만, 원궤도를 돌며 **방향이 계속 바뀌므로 가속도 운동**입니다. 가속도(구심가속도)의 크기는 일정하고 방향은 항상 중심을 향합니다.")
        
        angle = st.slider("회전 각도 (도)", 0, 360, 45, key="angle_circ")
        theta = np.radians(angle)
        R = 10 # 반지름
        
        x_circ = R * np.cos(theta)
        y_circ = R * np.sin(theta)
        
        # 속도 벡터 (접선 방향)
        vx_circ = -R * np.sin(theta)
        vy_circ = R * np.cos(theta)
        
        # 가속도 벡터 (중심 방향)
        ax_circ = -x_circ
        ay_circ = -y_circ
        
        # 원 궤적
        theta_array = np.linspace(0, 2*np.pi, 100)
        circle_x = R * np.cos(theta_array)
        circle_y = R * np.sin(theta_array)
        
        fig_circ = go.Figure()
        fig_circ.add_trace(go.Scatter(x=circle_x, y=circle_y, mode='lines', line=dict(color='gray', dash='dot'), name="궤적"))
        # 중심점
        fig_circ.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='black', symbol='cross'), name="중심"))
        # 물체
        fig_circ.add_trace(go.Scatter(x=[x_circ], y=[y_circ], mode='markers', marker=dict(size=15, color='blue'), name="물체"))
        
        # 속도 벡터 그리기
        fig_circ.add_annotation(x=x_circ + vx_circ/2, y=y_circ + vy_circ/2, ax=x_circ, ay=y_circ, xref="x", yref="y", axref="x", ayref="y",
                                showarrow=True, arrowhead=2, arrowcolor="green", text="속도(접선 방향)")
        # 가속도 벡터 그리기
        fig_circ.add_annotation(x=x_circ + ax_circ/2, y=y_circ + ay_circ/2, ax=x_circ, ay=y_circ, xref="x", yref="y", axref="x", ayref="y",
                                showarrow=True, arrowhead=2, arrowcolor="orange", text="가속도(중심 방향)")
                                
        fig_circ.update_layout(xaxis=dict(range=[-15, 15], scaleanchor="y", scaleratio=1, title="X"), 
                               yaxis=dict(range=[-15, 15], title="Y"), height=500, showlegend=False)
        st.plotly_chart(fig_circ, use_container_width=True)
