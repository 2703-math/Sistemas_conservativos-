import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Física Visual: Energia e Dinâmica",
    page_icon="⚡",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cores padrão para as Energias
COR_EC = "#3498db"   # Cinética (Azul)
COR_EPG = "#9b59b6"  # Potencial Gravitacional (Roxo)
COR_EPE = "#2ecc71"  # Potencial Elástica (Verde)
COR_EM = "#34495e"   # Mecânica (Cinza Escuro)

# ============================================
# FUNÇÕES AUXILIARES DE DESENHO ESTÁVEL
# ============================================
def criar_mola(x0, x1, y0, n_voltas=12, largura=0.35):
    if x0 >= x1:
        return [x0, x1], [y0, y0]
    x_vals = np.linspace(x0, x1, n_voltas * 2)
    y_vals = np.zeros_like(x_vals)
    for i in range(len(x_vals)):
        if i == 0 or i == len(x_vals) - 1:
            y_vals[i] = y0
        elif i % 2 == 0:
            y_vals[i] = y0 + largura
        else:
            y_vals[i] = y0 - largura
    return x_vals, y_vals

def criar_bloco(x_centro, y_base, largura=0.8, altura=0.8):
    hx = largura / 2
    x = [x_centro - hx, x_centro + hx, x_centro + hx, x_centro - hx, x_centro - hx]
    y = [y_base, y_base, y_base + altura, y_base + altura, y_base]
    return x, y

# ============================================
# GERAÇÃO DE FIGURAS: ABA 1 (RAMPA EM U)
# ============================================
def gerar_figura_rampa_u(massa, altura_max, duracao_ms, gravidade=10):
    x_max = 5
    k_rampa = altura_max / (x_max**2)
    em = massa * gravidade * altura_max

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    x_pista = np.linspace(-x_max, x_max, 80)
    y_pista = k_rampa * (x_pista**2)
    fig.add_trace(go.Scatter(x=x_pista, y=y_pista, mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'), row=1, col=1)

    fig.add_trace(go.Scatter(x=[x_max], y=[k_rampa*(x_max**2) + 0.3], mode='markers', marker=dict(color='#e74c3c', size=22, line=dict(color='#c0392b', width=2)), hoverinfo='skip'), row=1, col=1)

    epg_ini = massa * gravidade * (k_rampa*(x_max**2))
    ec_ini = max(0.0, em - epg_ini)
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Em'], y=[ec_ini, epg_ini, em], marker_color=[COR_EC, COR_EPG, COR_EM], text=[f"{ec_ini:.1f}J", f"{epg_ini:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)

    frames = []
    for ciclo in range(5):
        for ang in range(0, 360, 6):
            theta = math.radians(ang)
            x_a = x_max * math.cos(theta)
            y_a = k_rampa * (x_a**2)
            epg = massa * gravidade * y_a
            ec = max(0.0, em - epg)

            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[x_a], y=[y_a + 0.3]),
                    go.Bar(y=[ec, epg, em], text=[f"{ec:.1f}J", f"{epg:.1f}J", f"{em:.1f}J"])
                ],
                traces=[1, 2],
                name=f"c{ciclo}_a{ang}"
            ))

    fig.frames = frames

    fig.update_layout(
        showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10), height=400,
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "x": 0.0, "y": 1.15,
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": duracao_ms, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}, "mode": "immediate"}]
                },
                {
                    "label": "❚❚ Pause",
                    "method": "animate",
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                }
            ]
        }]
    )
    fig.update_xaxes(range=[-6.5, 6.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, altura_max + 2.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, max(10.0, em * 1.2)], title="Energia (Joules)", row=1, col=2)
    return fig

# ============================================
# GERAÇÃO DE FIGURAS: ABA 2 (MASSA-MOLA)
# ============================================
def gerar_figura_massa_mola(massa, k_mola, amplitude, duracao_ms):
    em = 0.5 * k_mola * (amplitude**2)
    limite_x = amplitude + 3.5

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    fig.add_trace(go.Scatter(x=[-limite_x, limite_x, limite_x, -limite_x, -limite_x], y=[-0.8, -0.8, 0, 0, -0.8], fill="toself", fillcolor="#bdc3c7", line=dict(width=0), hoverinfo='skip'), row=1, col=1)
    fig.add_trace(go.Scatter(x=[-limite_x, -limite_x + 0.4, -limite_x + 0.4, -limite_x, -limite_x], y=[0, 0, 2.2, 2.2, 0], fill="toself", fillcolor="#95a5a6", line=dict(width=0), hoverinfo='skip'), row=1, col=1)

    x_ini = amplitude
    xm, ym = criar_mola(-limite_x + 0.4, x_ini - 0.4, 0.4, n_voltas=12)
    bx, by = criar_bloco(x_ini, 0)
    epe_ini = 0.5 * k_mola * (x_ini**2)
    ec_ini = max(0.0, em - epe_ini)

    fig.add_trace(go.Scatter(x=xm, y=ym, mode='lines', line=dict(color='#7f8c8d', width=3), hoverinfo='skip'), row=1, col=1)
    fig.add_trace(go.Scatter(x=bx, y=by, fill="toself", fillcolor="#3498db", line=dict(color="#2980b9", width=2), hoverinfo='skip'), row=1, col=1)
    fig.add_trace(go.Bar(x=['Ec', 'Epe', 'Em'], y=[ec_ini, epe_ini, em], marker_color=[COR_EC, COR_EPE, COR_EM], text=[f"{ec_ini:.1f}J", f"{epe_ini:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)

    frames = []
    for ciclo in range(5):
        for ang in range(0, 360, 6):
            theta = math.radians(ang)
            x_a = amplitude * math.cos(theta)
            epe = 0.5 * k_mola * (x_a**2)
            ec = max(0.0, em - epe)
            xm_f, ym_f = criar_mola(-limite_x + 0.4, x_a - 0.4, 0.4, n_voltas=12)
            bx_f, by_f = criar_bloco(x_a, 0)

            frames.append(go.Frame(
                data=[
                    go.Scatter(x=xm_f, y=ym_f),
                    go.Scatter(x=bx_f, y=by_f),
                    go.Bar(y=[ec, epe, em], text=[f"{ec:.1f}J", f"{epe:.1f}J", f"{em:.1f}J"])
                ],
                traces=[2, 3, 4],
                name=f"c{ciclo}_a{ang}"
            ))

    fig.frames = frames

    fig.update_layout(
        showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10), height=400,
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "x": 0.0, "y": 1.15,
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": duracao_ms, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}, "mode": "immediate"}]
                },
                {
                    "label": "❚❚ Pause",
                    "method": "animate",
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                }
            ]
        }]
    )
    fig.update_xaxes(range=[-limite_x - 0.5, limite_x + 0.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1.2, 2.8], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, max(10.0, em * 1.2)], title="Energia (Joules)", row=1, col=2)
    return fig

# ============================================
# GERAÇÃO DE FIGURAS: ABA 3 (RAMPA + MOLA - CORRIGIDO)
# ============================================
def gerar_figura_rampa_mola_ref(massa, h_max, k_mola, duracao_ms, gravidade=10):
    em_total = massa * gravidade * h_max
    x_max_comp = math.sqrt((2 * em_total) / k_mola)

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    # Coordenadas geométricas do sistema da imagem
    x_topo_rampa = -6.0
    x_base_rampa = -2.0
    x_inicio_mola = 2.0
    x_parede = x_inicio_mola + 3.0

    # Trace 0: Pista (Rampa inclinada + trecho plano)
    xr = np.linspace(x_topo_rampa, x_base_rampa, 30)
    yr = h_max * ((xr - x_base_rampa) / (x_topo_rampa - x_base_rampa))**2
    
    xp = np.concatenate([xr, np.linspace(x_base_rampa, x_parede, 40)])
    yp = np.concatenate([yr, np.zeros(40)])
    fig.add_trace(go.Scatter(x=xp, y=yp, mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'), row=1, col=1)
    
    # Trace 1: Parede fixa da mola
    fig.add_trace(go.Scatter(x=[x_parede, x_parede], y=[0, 1.8], mode='lines', line=dict(color='#95a5a6', width=6), hoverinfo='skip'), row=1, col=1)

    # Estado Inicial (no topo da rampa)
    bx_ini, by_ini = criar_bloco(x_topo_rampa, h_max, 0.7, 0.7)
    xm_ini, ym_ini = criar_mola(x_inicio_mola, x_parede, 0.35, 12)

    # Trace 2: Mola
    fig.add_trace(go.Scatter(x=xm_ini, y=ym_ini, mode='lines', line=dict(color='#2ecc71', width=3), hoverinfo='skip'), row=1, col=1)
    # Trace 3: Bloco
    fig.add_trace(go.Scatter(x=bx_ini, y=by_ini, fill="toself", fillcolor="#e74c3c", line=dict(color="#c0392b", width=2), hoverinfo='skip'), row=1, col=1)
    # Trace 4: Barras de Energia
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Epe', 'Em'], y=[0.0, em_total, 0.0, em_total], marker_color=[COR_EC, COR_EPG, COR_EPE, COR_EM], text=[f"0.0J", f"{em_total:.1f}J", f"0.0J", f"{em_total:.1f}J"], textposition='auto'), row=1, col=2)

    frames = []
    n_q = 35
    t_rampa = np.linspace(x_topo_rampa, x_base_rampa, n_q)
    t_plano = np.linspace(x_base_rampa, x_inicio_mola, n_q)
    t_compr = np.linspace(x_inicio_mola, x_inicio_mola + x_max_comp, n_q)
    t_volta = np.linspace(x_inicio_mola + x_max_comp, x_topo_rampa, n_q * 2)
    
    trajetoria_x = np.concatenate([t_rampa, t_plano[1:], t_compr[1:], t_volta[1:]])

    for ciclo in range(3):
        for x_a in trajetoria_x:
            if x_a < x_base_rampa:
                a_r = h_max / ((x_topo_rampa - x_base_rampa)**2)
                y_a = a_r * (x_a - x_base_rampa)**2
                epg = massa * gravidade * y_a
                epe = 0.0
            elif x_a <= x_inicio_mola:
                y_a = 0.0
                epg = 0.0
                epe = 0.0
            else:
                y_a = 0.0
                epg = 0.0
                comp = x_a - x_inicio_mola
                epe = 0.5 * k_mola * (comp**2)

            ec = max(0.0, em_total - epg - epe)

            ponto_inicio_mola = max(x_inicio_mola, x_a)
            xm_f, ym_f = criar_mola(ponto_inicio_mola, x_parede, 0.35, 12)
            bx_f, by_f = criar_bloco(x_a, y_a, 0.7, 0.7)

            frames.append(go.Frame(
                data=[
                    go.Scatter(x=xm_f, y=ym_f),
                    go.Scatter(x=bx_f, y=by_f),
                    go.Bar(y=[ec, epg, epe, em_total], text=[f"{ec:.1f}J", f"{epg:.1f}J", f"{epe:.1f}J", f"{em_total:.1f}J"])
                ],
                traces=[2, 3, 4],  # Índices exatos correspondentes a Mola (2), Bloco (3) e Gráfico de Barras (4)
                name=f"x_{x_a}"
            ))

    fig.frames = frames

    fig.update_layout(
        showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10), height=400,
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "x": 0.0, "y": 1.15,
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": duracao_ms, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}, "mode": "immediate"}]
                },
                {
                    "label": "❚❚ Pause",
                    "method": "animate",
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                }
            ]
        }]
    )
    fig.update_xaxes(range=[x_topo_rampa - 1, x_parede + 1], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.5, h_max + 1.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, max(10.0, em_total * 1.2)], title="Energia (Joules)", row=1, col=2)
    return fig

# ============================================
# GERAÇÃO DE FIGURAS: ABA 4 (BRINQUEDO LOOPING)
# ============================================
def gerar_figura_looping(massa, raio_loop, v_inicial, alt_lancamento, gravidade=10):
    h_0 = alt_lancamento + (v_inicial**2) / (2 * gravidade)
    v_min_topo = math.sqrt(raio_loop * gravidade)
    topo_loop_y = 2 * raio_loop
    consegue_passar = h_0 >= topo_loop_y
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-5, 0], y=[alt_lancamento, 0], mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'))
    
    theta_loop = np.linspace(0, 2*np.pi, 100)
    x_loop = raio_loop + raio_loop * np.sin(theta_loop)
    y_loop = raio_loop + raio_loop * np.cos(theta_loop)
    fig.add_trace(go.Scatter(x=x_loop, y=y_loop, mode='lines', line=dict(color='#3498db', width=4), hoverinfo='skip'))

    fig.update_layout(
        title=dict(text="Esquema da Trajetória no Looping", font=dict(size=16)),
        showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10), height=400
    )
    fig.update_xaxes(range=[-6, raio_loop * 3], showgrid=True, zeroline=True)
    fig.update_yaxes(range=[-1, max(4.0, topo_loop_y + 1.5)], showgrid=True, zeroline=True)
    
    return fig, h_0, v_min_topo, consegue_passar

# ============================================
# TÍTULO E NAVEGAÇÃO POR ABAS SUPERIORES
# ============================================
st.markdown('<div class="main-title">⚡ Sistemas Conservativos e Dinâmica</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Simulações físicas completas com controle total de animação e loop</div>', unsafe_allow_html=True)

if 'velocidade_ms' not in st.session_state:
    st.session_state.velocidade_ms = 30

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Rampa em 'U' (Gravitacional)", 
    "2. Sistema Massa-Mola (Elástica)",
    "3. Rampa Inclinada + Mola",
    "4. Brinquedo Looping"
])

# ============================================
# ABA 1: RAMPA EM U
# ============================================
with tab1:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>Princípio:</b> Esfera oscilando livremente em pista sem atrito.
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 2.5])
    with col_c1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        massa_u = st.slider("Massa da esfera (kg)", 1.0, 10.0, 2.0, step=0.5, key='mu')
        h_max_u = st.slider("Altura inicial (m)", 2.0, 10.0, 5.0, step=0.5, key='hu')
        
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("⏩ Mais Rápido", key='fast_u'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_b2.button("⏪ Mais Lento", key='slow_u'):
            st.session_state.velocidade_ms = min(100, st.session_state.velocidade_ms + 10)
        st.markdown(f"<b>Velocidade atual:</b> {st.session_state.velocidade_ms} ms/quadro", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        fig_u = gerar_figura_rampa_u(massa_u, h_max_u, st.session_state.velocidade_ms)
        st.plotly_chart(fig_u, use_container_width=True, config={'displayModeBar': False})

# ============================================
# ABA 2: SISTEMA MASSA-MOLA
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Princípio:</b> Bloco oscilando horizontalmente preso a uma mola elástica.
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns([1, 2.5])
    with col_m1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        massa_m = st.slider("Massa do bloco (kg)", 1.0, 10.0, 2.0, step=0.5, key='mm')
        k_m = st.slider("Constante elástica (N/m)", 10, 100, 50, step=10, key='km')
        amp_m = st.slider("Amplitude (m)", 1.0, 5.0, 3.0, step=0.5, key='ampm')
        
        col_bm1, col_bm2 = st.columns(2)
        if col_bm1.button("⏩ Mais Rápido", key='fast_m'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_bm2.button("⏪ Mais Lento", key='slow_m'):
            st.session_state.velocidade_ms = min(100, st.session_state.velocidade_ms + 10)
        st.markdown(f"<b>Velocidade atual:</b> {st.session_state.velocidade_ms} ms/quadro", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        fig_m = gerar_figura_massa_mola(massa_m, k_m, amp_m, st.session_state.velocidade_ms)
        st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})

# ============================================
# ABA 3: RAMPA + MOLA (REFERÊNCIA DA IMAGEM)
# ============================================
with tab3:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Princípio:</b> Um bloco é solto do repouso no alto de uma rampa inclinada. Ao atingir o trecho plano, 
        ele colide com a mola, comprimindo-a proporcionalmente à energia mecânica acumulada.
    </div>
    """, unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([1, 2.5])
    with col_r1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        massa_rm = st.slider("Massa do bloco (m)", 1.0, 10.0, 2.0, step=0.5, key='m_rm')
        h_rm = st.slider("Altura inicial (h)", 1.0, 8.0, 4.0, step=0.5, key='h_rm')
        k_rm = st.slider("Constante da mola (k)", 20, 200, 100, step=10, key='k_rm')
        
        col_brm1, col_brm2 = st.columns(2)
        if col_brm1.button("⏩ Mais Rápido", key='fast_rm'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_brm2.button("⏪ Mais Lento", key='slow_rm'):
            st.session_state.velocidade_ms = min(100, st.session_state.velocidade_ms + 10)
        st.markdown(f"<b>Velocidade atual:</b> {st.session_state.velocidade_ms} ms/quadro", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r2:
        fig_rm = gerar_figura_rampa_mola_ref(massa_rm, h_rm, k_rm, st.session_state.velocidade_ms)
        st.plotly_chart(fig_rm, use_container_width=True, config={'displayModeBar': False})

# ============================================
# ABA 4: BRINQUEDO LOOPING
# ============================================
with tab4:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>Princípio do Looping:</b> Para que o carrinho complete a volta sem cair, a velocidade no ponto mais alto deve superar 
        o limiar físico $v = \\sqrt{R \\cdot g}$. Verifique a viabilidade em tempo real alterando os parâmetros abaixo.
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1, 2.5])
    with col_l1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        massa_l = st.slider("Massa do carrinho (kg)", 0.1, 5.0, 1.0, step=0.1, key='m_l')
        raio_l = st.slider("Raio do Looping (R)", 0.5, 3.0, 1.0, step=0.25, key='r_l')
        alt_l = st.slider("Altura de lançamento (h)", 0.0, 5.0, 2.5, step=0.25, key='alt_l')
        v_ini_l = st.slider("Velocidade inicial ($v_0$)", 0.0, 10.0, 0.0, step=0.5, key='v_ini_l')
        st.markdown("</div>", unsafe_allow_html=True)

    with col_l2:
        fig_l, h_total, v_min_topo, viavel = gerar_figura_looping(massa_l, raio_l, v_ini_l, alt_l)
        st.plotly_chart(fig_l, use_container_width=True, config={'displayModeBar': False})
        
        st.subheader("📊 Relatório de Viabilidade do Looping")
        col_r1, col_r2 = st.columns(2)
        col_r1.metric("Altura Total Equivalente ($h_0$)", f"{h_total:.2f} m")
        col_r2.metric("Velocidade Mínima no Topo", f"{v_min_topo:.2f} m/s")
        
        if viavel:
            st.success("✅ **Trajetória Viável!** O carrinho possui energia mecânica suficiente para completar o looping com segurança.")
        else:
            st.error("❌ **Trajetória Inviável!** O carrinho não atingirá o topo com velocidade suficiente e perderá o contato com a pista.")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    ⚡ <b>Física Visual: Energia e Dinâmica</b> — Simulações otimizadas com motor gráfico nativo.
</div>
""", unsafe_allow_html=True)
