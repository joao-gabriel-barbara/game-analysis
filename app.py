import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Game Sales Analysis",
    page_icon="🎮",
    layout="wide",
)

# ── Estilo ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f0f13;
        color: #e8e8e8;
    }
    .stApp { background-color: #0f0f13; }

    h1, h2, h3 {
        font-family: 'Space Mono', monospace !important;
        color: #ffffff;
    }

    .metric-card {
        background: #1a1a24;
        border: 1px solid #2a2a3a;
        border-left: 3px solid #7c6af7;
        border-radius: 8px;
        padding: 20px 24px;
    }
    .metric-value {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #7c6af7;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    .section-title {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #7c6af7;
        margin-bottom: 16px;
    }

    [data-testid="stSidebar"] {
        background-color: #13131c;
        border-right: 1px solid #2a2a3a;
    }

    .stSelectbox label, .stMultiSelect label {
        color: #aaa !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .upload-hint {
        background: #1a1a24;
        border: 1px dashed #3a3a50;
        border-radius: 10px;
        padding: 48px;
        text-align: center;
        margin-top: 40px;
    }
    .upload-hint h2 { color: #7c6af7; margin-bottom: 8px; }
    .upload-hint p { color: #666; font-size: 0.9rem; }

    div[data-testid="stMetric"] {
        background: #1a1a24;
        border: 1px solid #2a2a3a;
        border-radius: 8px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Paleta de cores para gráficos ───────────────────────────────────────────
PALETTE   = ["#7c6af7", "#f7706a", "#6af7c8", "#f7c96a", "#a06af7"]
BG_COLOR  = "#0f0f13"
GRID_COLOR = "#2a2a3a"
TEXT_COLOR = "#aaaaaa"

def style_fig(fig, ax_list=None):
    fig.patch.set_facecolor(BG_COLOR)
    axes = ax_list if ax_list is not None else fig.axes
    for ax in axes:
        ax.set_facecolor("#1a1a24")
        ax.tick_params(colors=TEXT_COLOR, labelsize=9)
        ax.xaxis.label.set_color(TEXT_COLOR)
        ax.yaxis.label.set_color(TEXT_COLOR)
        ax.title.set_color("#ffffff")
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID_COLOR)
        ax.grid(color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    return fig

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎮 Game Sales")
    st.markdown("<p style='color:#666;font-size:0.8rem;margin-top:-12px'>Analysis Dashboard</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<p style='color:#666;font-size:0.75rem'>FILTROS</p>", unsafe_allow_html=True)

    region_map = {
        "Global": "Global_Sales",
        "América do Norte": "NA_Sales",
        "Europa": "EU_Sales",
        "Japão": "JP_Sales",
    }
    region_label = st.selectbox("Região", list(region_map.keys()))
    region_col   = region_map[region_label]

    genre_filter     = None
    platform_filter  = None
    publisher_filter = None

# ── Carrega dados ────────────────────────────────────────────────────────────
PARQUET_PATH = "data/output/vgsales.parquet"

@st.cache_data
def load():
    try:
        return pd.read_parquet(PARQUET_PATH)
    except FileNotFoundError:
        st.error("Arquivo 'data/vgsales.parquet' não encontrado. Rode o notebook para gerá-lo.")
        st.stop()

df_full = load()

# ── Filtros dinâmicos na sidebar ─────────────────────────────────────────────
with st.sidebar:
    genres     = ["Todos"] + sorted(df_full["Genre"].dropna().unique())
    platforms  = ["Todas"] + sorted(df_full["Platform"].dropna().unique())
    publishers = ["Todos"] + sorted(df_full["Publisher"].dropna().unique())

    genre_filter     = st.selectbox("Gênero",    genres)
    platform_filter  = st.selectbox("Plataforma", platforms)
    publisher_filter = st.selectbox("Publisher",  publishers)

df = df_full.copy()
if genre_filter     != "Todos":  df = df[df["Genre"]     == genre_filter]
if platform_filter  != "Todas":  df = df[df["Platform"]  == platform_filter]
if publisher_filter != "Todos":  df = df[df["Publisher"] == publisher_filter]

if df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🎮 Game Sales Analysis")
st.markdown(f"<p style='color:#666;margin-top:-12px'>{len(df):,} jogos · Região: {region_label}</p>", unsafe_allow_html=True)
st.divider()

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_sales   = df[region_col].sum()
total_games   = len(df)
avg_per_game  = df[region_col].mean()
top_publisher = df.groupby("Publisher")[region_col].sum().idxmax()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Vendas Totais", f"{total_sales:.0f}M")
with c2:
    st.metric("Jogos Analisados", f"{total_games:,}")
with c3:
    st.metric("Média por Jogo", f"{avg_per_game:.2f}M")
with c4:
    st.metric("Top Publisher", top_publisher)

st.divider()

# ── Linha 1: Vendas por Gênero + Vendas por Região ───────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='section-title'>Vendas por Gênero</p>", unsafe_allow_html=True)
    genre_sales = df.groupby("Genre")[region_col].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(genre_sales.index[::-1], genre_sales.values[::-1], color=PALETTE[0], alpha=0.85)
    ax.set_xlabel("Vendas (milhões)")
    ax.set_title("")
    style_fig(fig)
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("<p class='section-title'>Comparativo Regional por Gênero</p>", unsafe_allow_html=True)
    reg_data = df.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales"]].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(reg_data))
    w = 0.28
    ax.bar([i - w for i in x], reg_data["NA_Sales"], width=w, label="NA", color=PALETTE[0], alpha=0.85)
    ax.bar(x,                  reg_data["EU_Sales"], width=w, label="EU", color=PALETTE[1], alpha=0.85)
    ax.bar([i + w for i in x], reg_data["JP_Sales"], width=w, label="JP", color=PALETTE[2], alpha=0.85)
    ax.set_xticks(list(x))
    ax.set_xticklabels(reg_data.index, rotation=45, ha="right", fontsize=8)
    ax.legend(facecolor="#1a1a24", edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR, fontsize=8)
    style_fig(fig)
    st.pyplot(fig)
    plt.close()

# ── Linha 2: Evolução temporal + Média por gênero ────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("<p class='section-title'>Evolução das Vendas ao Longo do Tempo</p>", unsafe_allow_html=True)
    year_sales  = df.groupby("Year")[region_col].sum()
    year_count  = df.groupby("Year")["Name"].count()
    year_avg    = year_sales / year_count

    fig, axes = plt.subplots(2, 1, figsize=(6, 5), sharex=True)
    axes[0].plot(year_sales.index, year_sales.values, color=PALETTE[0], linewidth=2, marker="o", markersize=3)
    axes[0].set_title("Vendas Totais", fontsize=10, color="#fff")
    axes[1].plot(year_avg.index, year_avg.values, color=PALETTE[2], linewidth=2, marker="o", markersize=3)
    axes[1].set_title("Média por Jogo", fontsize=10, color="#fff")
    axes[1].set_xlabel("Ano")
    style_fig(fig, axes)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col4:
    st.markdown("<p class='section-title'>Retorno Médio por Gênero</p>", unsafe_allow_html=True)
    avg_genre = df.groupby("Genre")[region_col].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = [PALETTE[0] if v == avg_genre.max() else PALETTE[3] for v in avg_genre.values]
    ax.barh(avg_genre.index[::-1], avg_genre.values[::-1], color=colors[::-1], alpha=0.85)
    ax.set_xlabel("Média de vendas (milhões)")
    style_fig(fig)
    st.pyplot(fig)
    plt.close()

# ── Linha 3: Top Publishers + Concentração ───────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown("<p class='section-title'>Top 10 Publishers</p>", unsafe_allow_html=True)
    top_pub = df.groupby("Publisher")[region_col].sum().nlargest(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top_pub.index[::-1], top_pub.values[::-1], color=PALETTE[4], alpha=0.85)
    ax.set_xlabel("Vendas (milhões)")
    style_fig(fig)
    st.pyplot(fig)
    plt.close()

with col6:
    st.markdown("<p class='section-title'>Concentração de Mercado</p>", unsafe_allow_html=True)
    total      = df[region_col].sum()
    top10_pub  = df.groupby("Publisher")[region_col].sum().nlargest(10).sum()
    top10_game = df.nlargest(10, region_col)[region_col].sum()
    outros_pub  = total - top10_pub
    outros_game = total - top10_game

    fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))

    for ax, (vals, title) in zip(axes, [
        ([top10_pub,  outros_pub],  "Por Publisher"),
        ([top10_game, outros_game], "Por Jogo"),
    ]):
        
        labels = ["Top 10", "Outros"]
        
        bars = ax.bar(
            labels,
            vals,
            color=[PALETTE[0], "#2a2a3a"]
        )

        # valores acima das barras
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                color="#fff",
                fontsize=8
            )

        ax.set_title(title, color="#fff", fontsize=9)
        ax.set_facecolor(BG_COLOR)
        ax.tick_params(colors=TEXT_COLOR)

    fig.patch.set_facecolor(BG_COLOR)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Tabela de dados filtrados ─────────────────────────────────────────────────
st.divider()
st.markdown("<p class='section-title'>Dados Filtrados</p>", unsafe_allow_html=True)
cols_show = ["Name", "Platform", "Year", "Genre", "Publisher",
             "NA_Sales", "EU_Sales", "JP_Sales", "Global_Sales"]
st.dataframe(
    df[cols_show].sort_values(region_col, ascending=False).head(100),
    use_container_width=True,
    height=300,
)