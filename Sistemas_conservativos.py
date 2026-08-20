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
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Cores para as Energias
COR_EC = "#3498db"   # Cinética (Azul)
COR_EPG = "#9b59b6"  # Potencial Gravitacional (Roxo)
COR_EPE = "#2ecc71"  # Potencial Elástica (Verde)
COR_EM = "#34495e"   # Mecânica (Cinza Escuro)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def criar_mola(x0, x1, y0, n_voltas=10, largura=0.5):
    """Gera coordenadas x,y para desenhar uma mola em zigue-zague"""
    if x0 == x1: # Prevenção de erro se a mola colapsar
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
# FUNÇÕES DE PLOTAGEM (CENÁRIOS)
# ============================================

def plot_rampa_u(angulo_deg, massa, altura_max, gravidade=10):
    """Simulação 1: Esfera na Rampa em U"""
    # Matemática do movimento (aproximação harmônica para visualização)
    x_max = 5
    # y = k * x^2 -> altura_max = k * x_max^2 -> k = altura_max / 25
    k_rampa = altura_max / (x_max**2)
    
    # Posição atual baseada no ângulo (fase da animação)
    theta = math.radians(angulo_deg)
    x_atual = x_max * math.cos(theta)
    y_atual = k_rampa * (x_atual**2)
    
    # Energias
    em = massa * gravidade * altura_max
    epg = massa * gravidade * y_atual
    ec = em - epg
    if ec < 0: ec = 0 # Prevenção float
    
    # Construção do Gráfico Misto (Cenário + Barras)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], horizontal_spacing=0.05)
    
    # 1. Pista em U
    x_pista = np.linspace(-x_max, x_max, 100)
    y_pista = k_rampa * (x_pista**2)
    fig.add_trace(go.Scatter(x=x_pista, y=y_pista, mode='lines', line=dict(color='#7f8c8d', width=5), name="Pista"), row=1, col=1)
    
    # 2. Esfera
    fig.add_trace(go.Scatter(x=[x_atual], y=[y_atual + 0.3], mode='markers', marker=dict(color='#e74c3c', size=25, line=dict(color='#c0392b', width=2)), name="Esfera"), row=1, col=1)
    
    # 3. Gráfico de Barras (Energias)
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Em'], y=[ec, epg, em], marker_color=[COR_EC, COR_EPG, COR_EM], text=[f"{ec:.1f}J", f"{epg:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)
    
    # Layouts
    fig.update_layout(showlegend=False, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0), height=400)
    fig.update_xaxes(range=[-6, 6], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, altura_max + 2], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, em * 1.1], title="Energia (Joules)", row=1, col=2)
    
    return fig

def plot_massa_mola(angulo_deg, massa, k_mola, amplitude):
    """Simulação 2: Sistema Massa-Mola Horizontal"""
    # Posição
    theta = math.radians(angulo_deg)
    x_atual = amplitude * math.cos(theta)
    
    # Energias
    em = 0.5 * k_mola * (amplitude**2)
    epe = 0.5 * k_mola * (x_atual**2)
    ec = em - epe
    if ec < 0: ec = 0
    
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], horizontal_spacing=0.05)
    
    # 1. Chão e Parede
    fig.add_shape(type="rect", x0=-amplitude-3, y0=-1, x1=amplitude+2, y1=0, fillcolor="#bdc3c7", line=dict(width=0), row=1, col=1)
    fig.add_shape(type="rect", x0=-amplitude-3, y0=0, x1=-amplitude-2.5, y1=2, fillcolor="#95a5a6", line=dict(width=0), row=1, col=1)
    
    # 2. Mola
    x_mola, y_mola = criar_mola(-amplitude-2.5, x_atual - 0.5, 0.5, n_voltas=15)
    fig.add_trace(go.Scatter(x=x_mola, y=y_mola, mode='lines', line=dict(color='#7f8c8d', width=2)), row=1, col=1)
    
    # 3. Bloco
    fig.add_shape(type="rect", x0=x_atual-0.5, y0=0, x1=x_atual+0.5, y1=1, fillcolor="#3498db", line=dict(color="#2980b9", width=2), row=1, col=1)
    
    # 4. Barras
    fig.add_trace(go.Bar(x=['Ec', 'Epe', 'Em'], y=[ec, epe, em], marker_color=[COR_EC, COR_EPE, COR_EM], text=[f"{ec:.1f}J", f"{epe:.1f}J", f"{em:.1f}J"], textposition='auto'), row=1, col=2)
    
    fig.update_layout(showlegend=False, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0), height=400)
    fig.update_xaxes(range=[-amplitude-3, amplitude+2], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, 3], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, em * 1.1], title="Energia (Joules)", row=1, col=2)
    
    return fig

def plot_rampa_mola(x_atual, massa, k_mola, h_max, gravidade=10):
    """Simulação 3: Rampa com Colisão na Mola"""
    em = massa * gravidade * h_max
    x_compressao_max = math.sqrt((2 * em) / k_mola)
    
    # Geometria do cenário
    x_inicio = -10
    x_fim_rampa = -4
    x_inicio_mola = 0
    x_parede = 4
    
    y_atual = 0
    epe = 0
    epg = 0
    
    # Lógica de posições e energias baseadas no X
    if x_atual < x_fim_rampa:
        # Descendo a rampa (Curva suave: y = a*(x-x_fim)^2 )
        a = h_max / ((x_inicio - x_fim_rampa)**2)
        y_atual = a * (x_atual - x_fim_rampa)**2
        epg = massa * gravidade * y_atual
    elif x_atual < x_inicio_mola:
        # Plano reto
        y_atual = 0
        epg = 0
    else:
        # Comprimindo a mola
        y_atual = 0
        epg = 0
        epe = 0.5 * k_mola * (x_atual**2)
    
    ec = em - epg - epe
    if ec < 0: ec = 0
    
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], horizontal_spacing=0.05)
    
    # 1. Chão e Parede
    # Rampa
    xr = np.linspace(x_inicio, x_fim_rampa, 50)
    yr = (h_max / ((x_inicio - x_fim_rampa)**2)) * (xr - x_fim_rampa)**2
    fig.add_trace(go.Scatter(x=xr, y=yr, mode='lines', line=dict(color='#bdc3c7', width=5), fill='tozeroy', fillcolor="#ecf0f1"), row=1, col=1)
    # Chão plano
    fig.add_shape(type="rect", x0=x_fim_rampa, y0=-1, x1=x_parede+1, y1=0, fillcolor="#ecf0f1", line=dict(color="#bdc3c7", width=2), row=1, col=1)
    # Parede
    fig.add_shape(type="rect", x0=x_parede, y0=0, x1=x_parede+1, y1=2, fillcolor="#95a5a6", line=dict(width=0), row=1, col=1)
    
    # 2. Mola
    fim_mola = x_atual + 0.5 if x_atual > x_inicio_mola else x_inicio_mola
    x_mola, y_mola = criar_mola(x_parede, fim_mola, 0.5, n_voltas=12)
    fig.add_trace(go.Scatter(x=x_mola, y=y_mola, mode='lines', line=dict(color='#7f8c8d', width=2)), row=1, col=1)
    
    # 3. Bloco
    fig.add_shape(type="rect", x0=x_atual-0.5, y0=y_atual, x1=x_atual+0.5, y1=y_atual+1, fillcolor="#f39c12", line=dict(color="#e67e22", width=2), row=1, col=1)
    
    # 4. Barras
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Epe', 'Em'], y=[ec, epg, epe, em], marker_color=[COR_EC, COR_EPG, COR_EPE, COR_EM], text=[f"{ec:.0f}J", f"{epg:.0f}J", f"{epe:.0f}J", f"{em:.0f}J"], textposition='auto'), row=1, col=2)
    
    fig.update_layout(showlegend=False, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0), height=400)
    fig.update_xaxes(range=[x_inicio-1, x_parede+1], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-1, h_max + 1], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, em * 1.1], title="Energia (Joules)", row=1, col=2)
    
    return fig

# ============================================
# TÍTULO E MENU LATERAL
# ============================================
st.markdown('<div class="main-title">⚡ Sistemas Conservativos de Energia</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Acompanhe a transformação da energia mecânica em tempo real</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configurações")
    st.markdown("---")
    topico = st.radio(
        "📚 Escolha o cenário:",
        [
            "1. Rampa em 'U' (Gravitacional)", 
            "2. Sistema Massa-Mola (Elástica)",
            "3. Rampa + Colisão com Mola"
        ],
        index=0
    )
    st.markdown("---")

# ============================================
# CENÁRIO 1: RAMPA EM U
# ============================================
if topico == "1. Rampa em 'U' (Gravitacional)":
    st.header("🛹 Esfera na Pista em U")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>Princípio:</b> Ao descer a rampa, a esfera perde altura (perde Energia Potencial Gravitacional) e ganha velocidade (ganha Energia Cinética). 
        Na ausência de atrito, ela sobe exatamente até a mesma altura do lado oposto. A soma dessas duas é a <b>Energia Mecânica (E<sub>m</sub>)</b>, que permanece constante!
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        massa = st.slider("Massa da esfera (kg)", 1.0, 10.0, 2.0, step=0.5)
        h_max = st.slider("Altura inicial (m)", 2.0, 10.0, 5.0, step=0.5)
        
    st.markdown(r"$$ E_m = E_c + E_{pg} \implies E_m = \frac{m \cdot v^2}{2} + m \cdot g \cdot h $$")
    
    col_anim, col_text = st.columns([1, 4])
    animar = col_anim.button("▶️ Animar Sistema")
    
    espaco_grafico = st.empty()
    
    if animar:
        # Loop de animação
        for angulo in range(0, 360, 5):
            fig = plot_rampa_u(angulo, massa, h_max)
            espaco_grafico.plotly_chart(fig, use_container_width=True)
            time.sleep(0.03) # Controle de FPS
    else:
        # Estado inicial
        fig = plot_rampa_u(0, massa, h_max)
        espaco_grafico.plotly_chart(fig, use_container_width=True)

# ============================================
# CENÁRIO 2: SISTEMA MASSA-MOLA
# ============================================
elif topico == "2. Sistema Massa-Mola (Elástica)":
    st.header("〰️ Sistema Massa-Mola Horizontal")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Princípio:</b> Ao esticar ou comprimir uma mola, armazenamos Energia Potencial Elástica. 
        Ao soltar o bloco, a mola o empurra, transformando essa energia acumulada em movimento (Energia Cinética).
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        massa = st.slider("Massa do bloco (kg)", 1.0, 10.0, 2.0, step=0.5)
        k_mola = st.slider("Constante elástica (N/m)", 10, 100, 50, step=10)
        amplitude = st.slider("Amplitude (m)", 1.0, 5.0, 3.0, step=0.5)
        
    st.markdown(r"$$ E_m = E_c + E_{pe} \implies E_m = \frac{m \cdot v^2}{2} + \frac{k \cdot x^2}{2} $$")
    
    col_anim, col_text = st.columns([1, 4])
    animar = col_anim.button("▶️ Animar Sistema")
    
    espaco_grafico = st.empty()
    
    if animar:
        for angulo in range(0, 360, 5):
            fig = plot_massa_mola(angulo, massa, k_mola, amplitude)
            espaco_grafico.plotly_chart(fig, use_container_width=True)
            time.sleep(0.03)
    else:
        fig = plot_massa_mola(0, massa, k_mola, amplitude)
        espaco_grafico.plotly_chart(fig, use_container_width=True)

# ============================================
# CENÁRIO 3: RAMPA + MOLA
# ============================================
elif topico == "3. Rampa + Colisão com Mola":
    st.header("🎢 Rampa e Colisão com Mola")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #34495e;">
        <b>O Desafio Completo:</b> O bloco começa no alto da rampa com apenas Energia Gravitacional. 
        Na parte reta, toda essa energia virou Cinética (velocidade máxima). 
        Ao bater na mola, essa velocidade a comprime até parar, convertendo tudo em Energia Elástica!
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        massa = st.slider("Massa do bloco (kg)", 1.0, 10.0, 2.0, step=0.5)
        h_max = st.slider("Altura da rampa (m)", 1.0, 8.0, 4.0, step=0.5)
        k_mola = st.slider("Constante da mola (N/m)", 20, 200, 100, step=10)
        
    st.markdown(r"$$ E_m = E_c + E_{pg} + E_{pe} = \text{Constante!} $$")
    
    # Cálculo interno da compressão máxima para limitar a animação
    em_total = massa * 10 * h_max
    comp_max = math.sqrt((2 * em_total) / k_mola)
    
    col_anim, col_text = st.columns([1, 4])
    animar = col_anim.button("▶️ Iniciar Simulação")
    
    espaco_grafico = st.empty()
    
    if animar:
        # Cria um vetor de posições X (da rampa até a compressão máxima)
        caminho_ida = np.linspace(-10, comp_max, 60)
        caminho_volta = np.linspace(comp_max, -10, 60)
        caminho_total = np.concatenate((caminho_ida, caminho_volta))
        
        for pos_x in caminho_total:
            fig = plot_rampa_mola(pos_x, massa, k_mola, h_max)
            espaco_grafico.plotly_chart(fig, use_container_width=True)
            time.sleep(0.04)
    else:
        fig = plot_rampa_mola(-10, massa, k_mola, h_max)
        espaco_grafico.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    ⚡ <b>Física Visual: Energia</b> — Ferramenta educacional para simulação dinâmica<br>
    Clique em "Animar Sistema" para observar as transformações de energia.
</div>
""", unsafe_allow_html=True)
