import streamlit as st
import pandas as pd

st.title("NBA Boxscore Scorigami")

@st.cache_data
def load_data():
    """Carrega o parquet e mantém só as colunas necessárias."""
    df = pd.read_parquet("nbastatsgami.parquet")

    cols = [
        "points",
        "reboundsTotal",
        "assists",
        "blocks",
        "steals",
        "firstName",
        "lastName",
        "gameDateTimeEst",
        "playerteamName",
        "opponentteamName",
    ]
    cols = [c for c in cols if c in df.columns]
    df = df[cols].copy()

    return df


# 1) Carrega dataset com tratamento de erro em volta do cache
try:
    df = load_data()
except Exception as e:
    st.error("❌ Erro ao carregar o arquivo 'nbastatsgami.parquet'.")
    st.write("### Tipo do erro:", type(e).__name__)
    st.write("### Mensagem do erro:", str(e))
    st.stop()

st.write("✅ Dataset carregado com sucesso!")
st.write("Colunas disponíveis:", list(df.columns))

# 2) Verifica se as colunas necessárias existem
required_cols = [
    "points",
    "reboundsTotal",
    "assists",
    "blocks",
    "steals",
    "firstName",
    "lastName",
    "gameDateTimeEst",
    "playerteamName",
    "opponentteamName",
]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error("Estas colunas necessárias não existem no dataset:")
    st.write(missing)
    st.stop()

st.write("✅ Todas as colunas necessárias foram encontradas.")
st.write("Digite os stats para ver se esse combo já aconteceu na história do dataset.")

# 3) Inputs
points = st.number_input("Points", min_value=0, step=1)
rebounds = st.number_input("Rebounds (reboundsTotal)", min_value=0, step=1)
assists = st.number_input("Assists", min_value=0, step=1)
blocks = st.number_input("Blocks", min_value=0, step=1)
steals = st.number_input("Steals", min_value=0, step=1)

# 4) Lógica do scorigami com try/except
if st.button("Checar Scorigami"):
    try:
        mask = (
            (df["points"] == points)
            & (df["reboundsTotal"] == rebounds)
            & (df["assists"] == assists)
            & (df["blocks"] == blocks)
            & (df["steals"] == steals)
        )

        matches = df[mask]

        st.write(
            f"Checando stats: {points} PTS, {rebounds} REB, {assists} AST, "
            f"{blocks} BLK, {steals} STL"
        )

        if matches.empty:
            st.success("🟢 SCORIGAMI! Esse combo de stats nunca apareceu no dataset.")
        else:
            st.error(f"🔴 Esse combo já aconteceu {len(matches)} vez(es).")
            st.write("Jogos em que isso aconteceu:")

            cols_to_show = [
                "firstName",
                "lastName",
                "gameDateTimeEst",
                "playerteamName",
                "opponentteamName",
                "points",
                "reboundsTotal",
                "assists",
                "blocks",
                "steals",
            ]
            cols_to_show = [c for c in cols_to_show if c in matches.columns]

            st.dataframe(
                matches[cols_to_show]
                .sort_values("gameDateTimeEst")
                .reset_index(drop=True)
            )
    except Exception as e:
        st.error("❌ Erro ao processar a checagem de scorigami.")
        st.write("### Tipo do erro:", type(e).__name__)
        st.write("### Mensagem do erro:", str(e))
