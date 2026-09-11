import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Física Visual: Energia",
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
# GERAÇÃO DE FIGURAS COM LOOP E CONTROLE DE VELOCIDADE
# ============================================
def gerar_figura_rampa_u(massa, altura_max, duracao_ms, gravidade=10):
    x_max = 5
    k_rampa = altura_max / (x_max**2)
    em = massa * gravidade * altura_max

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    # Trace 0: Pista em U
    x_pista = np.linspace(-x_max, x_max, 80)
    y_pista = k_rampa * (x_pista**2)
    fig.add_trace(go.Scatter(x=x_pista, y=y_pista, mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'), row=1, col=1)

    # Trace 1: Esfera (Estado inicial)
    fig.add_trace(go.Scatter(x=[x_max], y=[k_rampa*(x_max**2) + 0.3], mode='markers', marker=dict(color='#e74c3c', size=22, line=dict(color='#c0392b', width=2)), hoverinfo='skip'), row=1, col=1)

    # Trace 2: Barras de Energia
    epg_ini = massa * gravidade * (k_rampa*(x_max**2))
    ec_ini = max(0.0, em - epg_ini)
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Em'], y=[ec_ini, epg_ini, em], marker_color=[COR_EC, COR_EPG, COR_EM], text=[f"{ec_ini:.1f}J", f"{epg_ini:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)

    # Construção de múltiplos ciclos para garantir o loop contínuo nativo
    frames = []
    # 5 ciclos completos de repetição para simular loop contínuo fluido
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

def gerar_figura_massa_mola(massa, k_mola, amplitude, duracao_ms):
    em = 0.5 * k_mola * (amplitude**2)
    limite_x = amplitude + 3.5

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    # Trace 0: Chão
    fig.add_trace(go.Scatter(x=[-limite_x, limite_x, limite_x, -limite_x, -limite_x], y=[-0.8, -0.8, 0, 0, -0.8], fill="toself", fillcolor="#bdc3c7", line=dict(width=0), hoverinfo='skip'), row=1, col=1)
    # Trace 1: Parede
    fig.add_trace(go.Scatter(x=[-limite_x, -limite_x + 0.4, -limite_x + 0.4, -limite_x, -limite_x], y=[0, 0, 2.2, 2.2, 0], fill="toself", fillcolor="#95a5a6", line=dict(width=0), hoverinfo='skip'), row=1, col=1)

    # Estado Inicial
    x_ini = amplitude
    xm, ym = criar_mola(-limite_x + 0.4, x_ini - 0.4, 0.4, n_voltas=12)
    bx, by = criar_bloco(x_ini, 0)
    epe_ini = 0.5 * k_mola * (x_ini**2)
    ec_ini = max(0.0, em - epe_ini)

    # Trace 2: Mola
    fig.add_trace(go.Scatter(x=xm, y=ym, mode='lines', line=dict(color='#7f8c8d', width=3), hoverinfo='skip'), row=1, col=1)
    # Trace 3: Bloco
    fig.add_trace(go.Scatter(x=bx, y=by, fill="toself", fillcolor="#3498db", line=dict(color="#2980b9", width=2), hoverinfo='skip'), row=1, col=1)
    # Trace 4: Barras de Energia
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
# TÍTULO E NAVEGAÇÃO POR ABAS SUPERIORES
# ============================================
st.markdown('<div class="main-title">⚡ Sistemas Conservativos de Energia</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Animações em loop contínuo e controle de velocidade</div>', unsafe_allow_html=True)

# Gerenciamento de estado para a velocidade (em milissegundos por quadro)
if 'velocidade_ms' not in st.session_state:
    st.session_state.velocidade_ms = 30  # valor padrão inicial

tab1, tab2 = st.tabs([
    "1. Rampa em 'U' (Gravitacional)", 
    "2. Sistema Massa-Mola (Elástica)"
])

# ============================================
# ABA 1: RAMPA EM U
# ============================================
with tab1:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>Princípio:</b> Ao descer a rampa, a esfera perde altura e ganha velocidade. 
        Utilize os botões de velocidade abaixo e clique em <b>▶ Play</b> para ver o loop contínuo.
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 2.5])
    
    with col_c1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Parâmetros")
        massa_u = st.slider("Massa da esfera (kg)", 1.0, 10.0, 2.0, step=0.5, key='mu')
        h_max_u = st.slider("Altura inicial (m)", 2.0, 10.0, 5.0, step=0.5, key='hu')
        
        st.markdown("---")
        st.subheader("⏱️ Velocidade da Animação")
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("⏩ Mais Rápido", key='fast_u'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_btn2.button("⏪ Mais Lento", key='slow_u'):
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
        <b>Princípio:</b> O bloco oscila perpetuamente entre energia elástica e cinética. 
        Ajuste a velocidade nos botões e clique em <b>▶ Play</b>.
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns([1, 2.5])
    
    with col_m1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Parâmetros")
        massa_m = st.slider("Massa do bloco (kg)", 1.0, 10.0, 2.0, step=0.5, key='mm')
        k_m = st.slider("Constante elástica (N/m)", 10, 100, 50, step=10, key='km')
        amp_m = st.slider("Amplitude (m)", 1.0, 5.0, 3.0, step=0.5, key='ampm')
        
        st.markdown("---")
        st.subheader("⏱️ Velocidade da Animação")
        col_btnm1, col_btnm2 = st.columns(2)
        if col_btnm1.button("⏩ Mais Rápido", key='fast_m'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_btnm2.button("⏪ Mais Lento", key='slow_m'):
            st.session_state.velocidade_ms = min(100, st.session_state.velocidade_ms + 10)
            
        st.markdown(f"<b>Velocidade atual:</b> {st.session_state.velocidade_ms} ms/quadro", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        fig_m = gerar_figura_massa_mola(massa_m, k_m, amp_m, st.session_state.velocidade_ms)
        st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    ⚡ <b>Física Visual: Energia</b> — Simulações contínuas em loop com controle de velocidade.
</div>
""", unsafe_allow_html=True)
