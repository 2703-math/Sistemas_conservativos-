import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Função do 2º Grau Interativa",
    page_icon="🎢",
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
    .equation-box {
        background: #1a1a2e;
        color: #fff;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Courier New', monospace;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
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

# ============================================
# FUNÇÕES DE PLOTAGEM OTIMIZADAS (PLOTLY)
# ============================================
def criar_layout_cartesiano(fig, title="Plano Cartesiano", y_range=[-15, 15]):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        height=500,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)")
    )
    
    fig.update_xaxes(
        range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=1
    )
    
    fig.update_yaxes(
        range=y_range, zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=2
    )
    return fig

def plot_parabola(a, b, c, mostrar_raizes=False, mostrar_vertice=False):
    fig = go.Figure()
    
    # Reduzido para 150 pontos para garantir máxima fluidez sem perder a curvatura
    x = np.linspace(-15, 15, 150)
    y = a * (x**2) + b * x + c
    
    cor_linha = '#2980b9' if a > 0 else '#e67e22'
    nome_linha = 'f(x) (Boca pra cima)' if a > 0 else 'f(x) (Boca pra baixo)'
    
    # Curva principal
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines', name=nome_linha,
        line=dict(color=cor_linha, width=3.5),
        hoverinfo='x+y'
    ))
    
    # Corte no eixo Y
    if -15 <= c <= 15:
        fig.add_trace(go.Scatter(
            x=[0], y=[c], mode='markers+text', name='Corte no Eixo Y (c)',
            marker=dict(color='#8e44ad', size=10, line=dict(color='white', width=2)),
            text=[f' c = {c}'], textposition='middle right', textfont=dict(color='#8e44ad', size=13)
        ))

    delta = b**2 - 4*a*c
    
    # Raízes
    if mostrar_raizes and delta >= 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        
        raizes_x = [r for r in [x1, x2] if -10 <= r <= 10]
        raizes_y = [0] * len(raizes_x)
        textos = [f'x = {r:.1f}' for r in raizes_x]
        
        if raizes_x:
            fig.add_trace(go.Scatter(
                x=raizes_x, y=raizes_y, mode='markers+text', name='Raízes (Zeros)',
                marker=dict(color='#2ecc71', size=12, symbol='diamond', line=dict(color='white', width=2)),
                text=textos, textposition='bottom center', textfont=dict(color='#27ae60', size=14, family="Arial Black")
            ))

    # Vértice
    if mostrar_vertice:
        xv = -b / (2*a)
        yv = -delta / (4*a)
        
        fig.add_trace(go.Scatter(
            x=[xv, xv], y=[-20, 20], mode='lines', name='Eixo de Simetria',
            line=dict(color='#7f8c8d', width=2, dash='dot'), hoverinfo='skip'
        ))
        
        if -10 <= xv <= 10 and -15 <= yv <= 15:
            tipo_extremo = "Mínimo" if a > 0 else "Máximo"
            fig.add_trace(go.Scatter(
                x=[xv], y=[yv], mode='markers+text', name=f'Vértice ({tipo_extremo})',
                marker=dict(color='#e74c3c', size=14, symbol='star', line=dict(color='white', width=2)),
                text=[f' V({xv:.1f}, {yv:.1f})'], textposition='middle right', 
                textfont=dict(color='#c0392b', size=14, family="Arial Black")
            ))

    return criar_layout_cartesiano(fig, title="Gráfico da Parábola")

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.markdown('<div class="main-title">🎢 Estudo da Função do 2º Grau</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaja com os coeficientes e explore a anatomia da parábola em tempo real</div>', unsafe_allow_html=True)

# ============================================
# NAVEGAÇÃO EM ABAS SUPERIORES
# ============================================
tab1, tab2, tab3 = st.tabs([
    "1. Raízes: Bhaskara e Soma/Produto", 
    "2. O Gráfico da Parábola",
    "3. O Vértice (Máximos e Mínimos)"
])

# ============================================
# TÓPICO 1: RAÍZES
# ============================================
with tab1:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>O que são as raízes?</b> São os valores de <b>x</b> que fazem a função ser igual a zero (onde o gráfico corta o eixo horizontal). 
        Podemos encontrá-las pela Fórmula de Bhaskara ou pelas relações lógicas de Soma e Produto.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_math = st.columns([1, 2.5])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Coeficientes")
        a = st.slider("Valor de 'a'", -5.0, 5.0, 1.0, step=0.5, key='a1')
        if a == 0:
            st.error("Se a = 0, a função não é do 2º grau!")
            st.stop()
        b = st.slider("Valor de 'b'", -10.0, 10.0, -2.0, step=0.5, key='b1')
        c = st.slider("Valor de 'c'", -15.0, 15.0, -8.0, step=0.5, key='c1')
        st.markdown("</div>", unsafe_allow_html=True)
        
        sinal_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        sinal_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
        st.markdown(f"<div class='equation-box'>f(x) = {a}x² {sinal_b}x {sinal_c}</div>", unsafe_allow_html=True)
        
        fig = plot_parabola(a, b, c, mostrar_raizes=True, mostrar_vertice=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_math:
        delta = b**2 - 4*a*c
        sub_tab1, sub_tab2 = st.tabs(["Fórmula de Bhaskara", "Soma e Produto"])
        
        with sub_tab1:
            st.subheader("1. Cálculo do Discriminante (Δ)")
            st.markdown(rf"$$ \Delta = b^2 - 4ac $$")
            st.markdown(rf"$$ \Delta = ({b})^2 - 4 \cdot ({a}) \cdot ({c}) = \mathbf{{{delta}}} $$")
            
            st.markdown("---")
            st.subheader("2. Aplicando Bhaskara")
            
            if delta < 0:
                st.error(f"Como Δ = {delta} (negativo), a equação **não possui raízes reais**.")
            elif delta == 0:
                x1 = -b / (2*a)
                st.warning(f"Como Δ = 0, a equação possui **duas raízes reais e iguais**.")
                st.markdown(rf"$$ x = \mathbf{{{x1:.2f}}} $$")
            else:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                st.success(f"Como Δ > 0, há **duas raízes reais distintas**.")
                st.markdown(rf"$$ x_1 = \mathbf{{{x1:.2f}}} \quad \text{{e}} \quad x_2 = \mathbf{{{x2:.2f}}} $$")

        with sub_tab2:
            st.subheader("Relações de Girard")
            soma = -b / a
            produto = c / a
            st.markdown(rf"**SOMA (S):** $$ x_1 + x_2 = \frac{{-b}}{{a}} = \mathbf{{{soma:.2f}}} $$")
            st.markdown(rf"**PRODUTO (P):** $$ x_1 \cdot x_2 = \frac{{c}}{{a}} = \mathbf{{{produto:.2f}}} $$")

# ============================================
# TÓPICO 2: O GRÁFICO DA PARÁBOLA
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>A Geometria da Equação:</b> O parâmetro <b>a</b> define a concavidade e a abertura. 
        O parâmetro <b>c</b> define o ponto de corte no eixo Y.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_graf = st.columns([1, 2.5])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        a = st.slider("Coeficiente 'a' (Concavidade)", -4.0, 4.0, 1.0, step=0.2, key='a2')
        if a == 0:
            st.stop()
        b = st.slider("Coeficiente 'b' (Inclinação)", -10.0, 10.0, 0.0, step=0.5, key='b2')
        c = st.slider("Coeficiente 'c' (Corte no eixo Y)", -15.0, 15.0, -5.0, step=1.0, key='c2')
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_graf:
        fig = plot_parabola(a, b, c, mostrar_raizes=False, mostrar_vertice=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# TÓPICO 3: O VÉRTICE
# ============================================
with tab3:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>O Ponto Extremo:</b> O Vértice representa o valor <b>Mínimo</b> (boca para cima) ou <b>Máximo</b> (boca para baixo) da função.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_graf = st.columns([1, 2.5])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        a = st.slider("Valor de 'a'", -3.0, 3.0, -1.0, step=0.5, key='a3')
        if a == 0:
            st.stop()
        b = st.slider("Valor de 'b'", -10.0, 10.0, 4.0, step=0.5, key='b3')
        c = st.slider("Valor de 'c'", -15.0, 15.0, 5.0, step=0.5, key='c3')
        st.markdown("</div>", unsafe_allow_html=True)
        
        delta = b**2 - 4*a*c
        xv = -b / (2*a)
        yv = -delta / (4*a)
        
        st.subheader("🧮 Coordenadas do Vértice")
        st.markdown(rf"$$ x_v = \mathbf{{{xv:.2f}}} \quad | \quad y_v = \mathbf{{{yv:.2f}}} $$")
        
        if a > 0:
            st.success(f"Ponto de **MÍNIMO**: valor mínimo = **{yv:.2f}**.")
        else:
            st.error(f"Ponto de **MÁXIMO**: valor máximo = **{yv:.2f}**.")
            
    with col_graf:
        fig = plot_parabola(a, b, c, mostrar_raizes=False, mostrar_vertice=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    🎢 <b>Matemática Visual</b> — Ferramenta otimizada para alta fluidez interativa.
</div>
""", unsafe_allow_html=True)
