import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import time

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
# FUNÇÕES AUXILIARES DE DESENHO
# ============================================
def criar_mola(x0, x1, y0, n_voltas=10, largura=0.4):
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

# ============================================
# PLOTAGENS OTIMIZADAS PARA FLUIDEZ
# ============================================
def plot_rampa_u(angulo_deg, massa, altura_max, gravidade=10):
    x_max = 5
    k_rampa = altura_max / (x_max**2)
    
    theta = math.radians(angulo_deg)
    x_atual = x_max * math.cos(theta)
    y_atual = k_rampa * (x_atual**2)
    
    em = massa * gravidade * altura_max
    epg = massa * gravidade * y_atual
    ec = max(0.0, em - epg)
    
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], horizontal_spacing=0.05)
    
    # Pista
    x_pista = np.linspace(-x_max, x_max, 80)
    y_pista = k_rampa * (x_pista**2)
    fig.add_trace(go.Scatter(x=x_pista, y=y_pista, mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'), row=1, col=1)
    
    # Esfera
    fig.add_trace(go.Scatter(x=[x_atual], y=[y_atual + 0.3], mode='markers', marker=dict(color='#e74c3c', size=22, line=dict(color='#c0392b', width=2)), hoverinfo='skip'), row=1, col=1)
    
    # Barras de Energia
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Em'], y=[ec, epg, em], marker_color=[COR_EC, COR_EPG, COR_EM], text=[f"{ec:.1f}J", f"{epg:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)
    
    fig.update_layout(showlegend=False, plot_bgcolor='white', margin=dict(l=10, r=10, t=20, b=10), height=380)
    fig.update_xaxes(range=[-6, 6], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, altura_max + 2], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, em * 1.15], title="Energia (Joules)", row=1, col=2)
    return fig

def plot_massa_mola(angulo_deg, massa, k_mola, amplitude):
    theta = math.radians(angulo_deg)
    x_atual = amplitude * math.cos(theta)
    
    em = 0.5 * k_mola * (amplitude**2)
    epe = 0.5 * k_mola * (x_atual**2)
    ec = max(0.0, em - epe)
    
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], horizontal_spacing=0.05)
    
    # Base e Parede
    fig.add_shape(type="rect", x0=-amplitude-3, y0=-0.8, x1=amplitude+2, y1=0, fillcolor="#bdc3c7", line=dict(width=0), row=1, col=1)
    fig.add_shape(type="rect", x0=-amplitude-3, y0=0, x1=-amplitude-2.5, y1=1.8, fillcolor="#95a5a6", line=dict(width=0), row=1, col=1)
    
    # Mola
    x_mola, y_mola = criar_mola(-amplitude-2.5, x_atual - 0.4, 0.4, n_voltas=12)
    fig.add_trace(go.Scatter(x=x_mola, y=y_mola, mode='lines', line=dict(color='#7f8c8d', width=2), hoverinfo='skip'), row=1, col=1)
    
    # Bloco
    fig.add_shape(type="rect", x0=x_atual-0.4, y0=0, x1=x_atual+0.4, y1=0.8, fillcolor="#3498db", line=dict(color="#2980b9", width=2), row=1, col=1)
    
    # Barras
    fig.add_trace(go.Bar(x=['Ec', 'Epe', 'Em'], y=[ec, epe, em], marker_color=[COR_EC, COR_EPE, COR_EM], text=[f"{ec:.1f}J", f"{epe:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)
    
    fig.update_layout(showlegend=False, plot_bgcolor='white', margin=dict(l=10, r=10, t=20, b=10), height=380)
    fig.update_xaxes(range=[-amplitude-3, amplitude+2], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, 2.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, em * 1.15], title="Energia (Joules)", row=1, col=2)
    return fig

# ============================================
# TÍTULO E NAVEGAÇÃO POR ABAS SUPERIORES
# ============================================
st.markdown('<div class="main-title">⚡ Sistemas Conservativos de Energia</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Acompanhe a transformação da energia mecânica em tempo real com alta fluidez</div>', unsafe_allow_html=True)

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
        <b>Princípio:</b> Ao descer a rampa, a esfera perde altura (perde Energia Potencial Gravitacional) e ganha velocidade (ganha Energia Cinética). 
        A soma permanece constante na ausência de atrito!
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 2.5])
    
    with col_c1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Parâmetros")
        massa_u = st.slider("Massa da esfera (kg)", 1.0, 10.0, 2.0, step=0.5, key='mu')
        h_max_u = st.slider("Altura inicial (m)", 2.0, 10.0, 5.0, step=0.5, key='hu')
        
        # Controle de estado para animação fluida sem travamento de loop pesado
        if 'animando_u' not in st.session_state:
            st.session_state.animando_u = False
            st.session_state.angulo_u = 0

        col_b1, col_b2 = st.columns(2)
        if col_b1.button("▶️ Iniciar / Pausar", key='btn_u'):
            st.session_state.animando_u = not st.session_state.animando_u
        if col_b2.button("⏹️ Resetar", key='btn_res_u'):
            st.session_state.animando_u = False
            st.session_state.angulo_u = 0
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        # Placeholder único para atualizar o gráfico suavemente sem redesenhar a página inteira
        grafico_u = st.empty()
        fig_u = plot_rampa_u(st.session_state.angulo_u, massa_u, h_max_u)
        grafico_u.plotly_chart(fig_u, use_container_width=True, config={'displayModeBar': False})
        
        if st.session_state.animando_u:
            st.session_state.angulo_u = (st.session_state.angulo_u + 8) % 360
            time.sleep(0.02)
            st.rerun()

# ============================================
# ABA 2: SISTEMA MASSA-MOLA
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Princípio:</b> Ao comprimir a mola, acumulamos Energia Potencial Elástica. Ao soltar, a energia se converte em movimento (Energia Cinética).
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns([1, 2.5])
    
    with col_m1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Parâmetros")
        massa_m = st.slider("Massa do bloco (kg)", 1.0, 10.0, 2.0, step=0.5, key='mm')
        k_m = st.slider("Constante elástica (N/m)", 10, 100, 50, step=10, key='km')
        amp_m = st.slider("Amplitude (m)", 1.0, 5.0, 3.0, step=0.5, key='ampm')
        
        if 'animando_m' not in st.session_state:
            st.session_state.animando_m = False
            st.session_state.angulo_m = 0

        col_bm1, col_bm2 = st.columns(2)
        if col_bm1.button("▶️ Iniciar / Pausar", key='btn_m'):
            st.session_state.animando_m = not st.session_state.animando_m
        if col_bm2.button("⏹️ Resetar", key='btn_res_m'):
            st.session_state.animando_m = False
            st.session_state.angulo_m = 0
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        grafico_m = st.empty()
        fig_m = plot_massa_mola(st.session_state.angulo_m, massa_m, k_m, amp_m)
        grafico_m.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})
        
        if st.session_state.animando_m:
            st.session_state.angulo_m = (st.session_state.angulo_m + 8) % 360
            time.sleep(0.02)
            st.rerun()

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    ⚡ <b>Física Visual: Energia</b> — Ferramenta educacional otimizada para alta fluidez interativa.
</div>
""", unsafe_allow_html=True)
