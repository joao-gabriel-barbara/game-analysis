# 🎮 Análise de Vendas do Mercado de Games

## Objetivo

Identificar gêneros, plataformas e publishers com melhor desempenho por região para orientar decisões estratégicas de investimento no mercado de games.

## Contexto

Uma publisher de games precisa decidir em qual gênero e plataforma investir. Para isso, analisamos o histórico de vendas globais com foco em três mercados: América do Norte (NA), Europa (EU) e Japão (JP).

---

## Dataset

- **Fonte:** [Video Game Sales — Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales)
- **Volume:** ~16.000 jogos registrados entre 1980 e 2016
- **Colunas principais:** Nome, Plataforma, Ano, Gênero, Publisher, Vendas por região e Global

---

## Ferramentas

- Python 3
- Pandas
- Matplotlib
- Seaborn
- Streamlit

---

## Estrutura do Projeto

```
games-analysis/
│
├── data/
│   └── output/
│       └── vgsales.parquet   ← gerado pelo notebook
├── notebooks/
│   └── analysis.ipynb
├── app.py
└── README.md
```

> O CSV original não está versionado. Para gerá-lo, baixe o dataset no [Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales), coloque em `data/vgsales.csv` e rode o notebook — o Parquet será gerado automaticamente.

---

## Principais Descobertas

### 🌍 Recomendações por Região

| Região | Gênero | Publishers em destaque | Plataformas em destaque |
|--------|--------|----------------------|------------------------|
| 🇯🇵 Japão | Role-Playing | Square Enix, Nintendo | DS |
| 🇺🇸 América do Norte | Action, Shooter | Take-Two Interactive, Activision | X360, PS2, PS3 |
| 🇪🇺 Europa | Action, Shooter, Sports | Take-Two Interactive, Ubisoft | PS3, X360, PS2 |

### 📊 Venda Média por Gênero (milhões por jogo)

Os gêneros com maior retorno médio por título lançado são:

| # | Gênero | Média (mi) |
|---|--------|-----------|
| 1 | Platform | 0.95 |
| 2 | Shooter | 0.80 |
| 3 | Role-Playing | 0.63 |
| 4 | Racing | 0.59 |
| 5 | Sports | 0.57 |

> Platform e Shooter têm o maior retorno médio por jogo, mesmo sem liderar em volume total.

### 📉 Tendência de Mercado

- O mercado atingiu seu **pico entre 2008 e 2009**
- Após 2010, houve queda progressiva nas vendas totais, correlacionada com a redução no número de jogos publicados
- A venda média por jogo também caiu no período, sugerindo menor retorno individual além do menor volume

### 🏢 Concentração de Mercado

- **Top 10 publishers** respondem por **70.5%** das vendas globais
- **Top 10 jogos** respondem por apenas **4.2%** das vendas globais

O mercado é dominado por grandes publishers com catálogos consolidados — a vantagem competitiva vem do volume de títulos, não de um único blockbuster. Isso eleva a barreira de entrada para novos competidores.

### 🌐 Diferenças e Semelhanças Regionais

- **NA e EU** compartilham preferência por Action, e pelas plataformas X360, PS2 e PS3
- **JP** é um mercado à parte: forte preferência por Role-Playing e pelo ecossistema Nintendo/DS
- Uma publisher com estratégia global precisa adaptar o produto ao mercado japonês — não basta replicar a estratégia ocidental

---

## Limitações

O dataset não possui dados pós-2016 nem informações de receita digital, o que impede determinar se a queda observada reflete uma mudança de comportamento do consumidor (migração para mobile e distribuição digital) ou subnotificação do próprio dataset. Uma análise complementar com dados de receita digital seria necessária para confirmar a tendência.

---

## Como Reproduzir

```bash
# Instalar dependências
pip install pandas matplotlib seaborn jupyter streamlit pyarrow
```

**1. Gerar o Parquet** — baixe o `vgsales.csv` do Kaggle, coloque em `data/` e rode o notebook:
```bash
jupyter notebook notebooks/analysis.ipynb
```

**2. Rodar o dashboard**
```bash
streamlit run app.py
```

Caso queira acessar sem baixar nada: https://game-analysis-joao.streamlit.app/
