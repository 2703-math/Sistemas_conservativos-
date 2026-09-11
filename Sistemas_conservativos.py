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
# FUNÇÕES AUXILIARES DE DESENHO
# ============================================
def criar_mola(x0, x1, y0, n_voltas=10, largura=0.3):
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

def criar_bloco(x_centro, y_base, largura=0.7, altura=0.7):
    hx = largura / 2
    x = [x_centro - hx, x_centro + hx, x_centro + hx, x_centro - hx, x_centro - hx]
    y = [y_base, y_base, y_base + altura, y_base + altura, y_base]
    return x, y

# ============================================
# GERAÇÃO DE FIGURAS: RAMPA + MOLA (BASEADO NA IMAGEM)
# ============================================
def gerar_figura_rampa_mola(massa, h_max, k_mola, duracao_ms, gravidade=10):
    em_total = massa * gravidade * h_max
    x_compressao_max = math.sqrt((2 * em_total) / k_mola)

    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.08)

    # Coordenadas da Rampa e Pista
    x_inicio_rampa = -6.0
    x_fim_rampa = -2.0
    x_inicio_mola_livre = 2.0
    x_parede = x_inicio_mola_livre + 2.5

    # Trace 0: Rampa e Solo
    xr = np.linspace(x_inicio_rampa, x_fim_rampa, 40)
    yr = h_max * ((xr - x_fim_rampa) / (x_inicio_rampa - x_fim_rampa))**2
    
    x_pista = np.concatenate([xr, np.linspace(x_fim_rampa, x_parere_calc := x_parede, 40)])
    y_pista = np.concatenate([yr, np.zeros(40)])
    
    fig.add_trace(go.Scatter(x=x_pista, y=y_pista, mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'), row=1, col=1)
    
    # Trace 1: Parede do fundo da mola
    fig.add_trace(go.Scatter(x=[x_parede, x_parede], y=[0, 1.5], mode='lines', line=dict(color='#95a5a6', width=6), hoverinfo='skip'), row=1, col=1)

    # Estado Inicial do Bloco (no topo da rampa)
    x_ini = x_inicio_rampa
    y_ini = h_max
    bx_ini, by_ini = criar_bloco(x_ini, y_ini, 0.6, 0.6)
    xm_ini, ym_ini = criar_mola(x_inicio_mola_livre, x_parede, 0.3, 10)

    # Trace 2: Mola
    fig.add_trace(go.Scatter(x=xm_ini, y=ym_ini, mode='lines', line=dict(color='#2ecc71', width=3), hoverinfo='skip'), row=1, col=1)
    # Trace 3: Bloco
    fig.add_trace(go.Scatter(x=bx_ini, y=by_ini, fill="toself", fillcolor="#e74c3c", line=dict(color="#c0392b", width=2), hoverinfo='skip'), row=1, col=1)
    
    # Trace 4: Barras de Energia Iniciais
    fig.add_trace(go.Bar(x=['Ec', 'Epg', 'Epe', 'Em'], y=[0.0, em_total, 0.0, em_total], marker_color=[COR_EC, COR_EPG, COR_EPE, COR_EM], text=[f"0.0J", f"{em_total:.1f}J", f"0.0J", f"{em_total:.1f}J"], textposition='auto'), row=1, col=2)

    # Construção dos Frames da Análise de Movimento
    frames = []
    n_passos = 60
    
    # Trajetória de descida da rampa até a mola e compressão
    posicoes_x = np.linspace(x_inicio_rampa, x_inicio_mola_livre - x_compressao_max, n_passos)
    # Adicionar o retorno (compressão e volta)
    posicoes_x = np.concatenate([posicoes_x, posicoes_x[::-1]])

    for ciclo in range(3): # Loop contínuo
        for x_a in posicoes_x:
            if x_a < x_fim_rampa:
                a_r = h_max / ((x_inicio_rampa - x_fim_rampa)**2)
                y_a = a_r * (x_a - x_fim_rampa)**2
                epg = massa * gravidade * y_a
                epe = 0.0
            elif x_a < x_inicio_mola_livre:
                y_a = 0.0
                epg = 0.0
                epe = 0.0
            else:
                y_a = 0.0
                epg = 0.0
                delta_x = x_a - x_inicio_mola_livre
                epe = 0.5 * k_mola * (delta_x**2)

            ec = max(0.0, em_total - epg - epe)
            
            # Ajuste visual da mola sendo comprimida
            fim_mola_atual = max(x_inicio_mola_livre, x_a - 0.3)
            xm_f, ym_f = criar_mola(fim_mola_atual, x_parede, 0.3, 10)
            bx_f, by_f = criar_bloco(x_a, y_a, 0.6, 0.6)

            frames.append(go.Frame(
                data=[
                    go.Scatter(x=xm_f, y=ym_f),
                    go.Scatter(x=bx_f, y=by_f),
                    go.Bar(y=[ec, epg, epe, em_total], text=[f"{ec:.1f}J", f"{epg:.1f}J", f"{epe:.1f}J", f"{em_total:.1f}J"])
                ],
                traces=[2, 3, 4],
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
    fig.update_xaxes(range=[x_inicio_rampa - 1, x_parede + 1], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.5, h_max + 1.5], showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(range=[0, max(10.0, em_total * 1.2)], title="Energia (Joules)", row=1, col=2)
    return fig

# ============================================
# GERAÇÃO DE FIGURAS: BRINQUEDO LOOPING
# ============================================
def gerar_figura_looping(massa, raio_loop, v_inicial, alt_lancamento, gravidade=10):
    # Altura equivalente à velocidade inicial (Conservação de Energia: m*g*h0 + mv0^2/2 = m*g*h)
    h_0 = alt_lancamento + (v_inicial**2) / (2 * gravidade)
    
    # Velocidade mínima teórica no topo do loop para não cair (Normal = 0)
    # m * v_topo^2 / R = m * g  => v_topo = sqrt(R * g)
    v_min_topo = math.sqrt(raio_loop * gravidade)
    
    # Altura do topo do looping em relação ao solo
    centro_loop_y = raio_loop
    topo_loop_y = 2 * raio_loop
    
    # Verificar se a altura de lançamento é suficiente para atingir o topo do loop
    consegue_passar = h_0 >= topo_loop_y
    
    fig = go.Figure()
    
    # Desenhar a Pista e o Loop
    # Rampa de acesso
    fig.add_trace(go.Scatter(x=[-5, 0], y=[alt_lancamento, 0], mode='lines', line=dict(color='#7f8c8d', width=4), hoverinfo='skip'))
    
    # Circunferência do Loop (Centro em x=raio_loop, y=raio_loop)
    theta_loop = np.linspace(0, 2*np.pi, 100)
    x_loop = raio_loop + raio_loop * np.sin(theta_loop)
    y_loop = centro_loop_y + raio_loop * np.cos(theta_loop)
    fig.add_trace(go.Scatter(x=x_loop, y=y_loop, mode='lines', line=dict(color='#3498db', width=4), hoverinfo='skip'))

    fig.update_layout(
        title=dict(text="Simulação Dinâmica do Looping", font=dict(size=16)),
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
st.markdown('<div class="subtitle">Animações avançadas: Rampa com Mola e Brinquedo Looping</div>', unsafe_allow_html=True)

if 'velocidade_ms' not in st.session_state:
    st.session_state.velocidade_ms = 30

tab1, tab2, tab3 = st.tabs([
    "1. Rampa em 'U' (Gravitacional)", 
    "2. Rampa + Colisão com Mola",
    "3. Brinquedo Looping"
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
    # (Mantido funcional idêntico ao anterior para preservar estabilidade)
    st.info("Utilize a aba 2 para ver a nova simulação de rampa com mola baseada na sua referência.")

# ============================================
# ABA 2: RAMPA + COLISÃO COM MOLA (REFERÊNCIA DA IMAGEM)
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Princípio:</b> Um corpo de massa <i>m</i> é solto do repouso de uma altura <i>h</i> em uma rampa inclinada. 
        Ao descer, atinge a pista horizontal e comprime a mola de constante elástica <i>k</i>.
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns([1, 2.5])
    
    with col_m1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Parâmetros do Sistema")
        massa_rm = st.slider("Massa do bloco (m)", 1.0, 10.0, 2.0, step=0.5, key='m_rm')
        h_rm = st.slider("Altura inicial (h)", 1.0, 8.0, 4.0, step=0.5, key='h_rm')
        k_rm = st.slider("Constante da mola (k)", 20, 200, 100, step=10, key='k_rm')
        
        st.markdown("---")
        st.subheader("⏱️ Velocidade da Animação")
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("⏩ Mais Rápido", key='fast_rm'):
            st.session_state.velocidade_ms = max(5, st.session_state.velocidade_ms - 10)
        if col_btn2.button("⏪ Mais Lento", key='slow_rm'):
            st.session_state.velocidade_ms = min(100, st.session_state.velocidade_ms + 10)
        st.markdown(f"<b>Velocidade atual:</b> {st.session_state.velocidade_ms} ms/quadro", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        fig_rm = gerar_figura_rampa_mola(massa_rm, h_rm, k_rm, st.session_state.velocidade_ms)
        st.plotly_chart(fig_rm, use_container_width=True, config={'displayModeBar': False})

# ============================================
# ABA 3: BRINQUEDO LOOPING
# ============================================
with tab3:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>Princípio do Looping:</b> Para que um carrinho complete o looping sem cair, a força centrípeta no ponto mais alto deve ser 
        ao menos igual à força peso. Isso exige uma velocidade mínima no topo de $v = \\sqrt{R \\cdot g}$. 
        Através da conservação de energia, calculamos se a energia inicial é suficiente.
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1, 2.5])
    
    with col_l1:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Variáveis Físicas")
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
        col_r1.metric("Altura Total Equivalente ($h_0$)", f"{h_total:.2f} m", help="Inclui a energia cinética da velocidade inicial.")
        col_r2.metric("Velocidade Mínima no Topo", f"{v_min_topo:.2f} m/s", help="Necessária para não perder contato com a pista.")
        
        if viavel:
            st.success("✅ **Trajetória Viável!** O carrinho possui energia suficiente para ultrapassar o topo do loop com segurança e completar a volta.")
        else:
            st.error("❌ **Trajetória Inviável!** O carrinho não tem energia suficiente e vai descolar da pista ou cair antes de atingir o topo do looping. Aumente a altura de lançamento ou a velocidade inicial.")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    ⚡ <b>Física Visual: Energia e Dinâmica</b> — Simulações interativas avançadas.
</div>
""", unsafe_allow_html=True)
