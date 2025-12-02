import streamlit as st
import pandas as pd

st.title("NBA Boxscore Scorigami")

# 1) Carregar o parquet diretamente, sem função, e mostrar erro amigável se der ruim
try:
    df = pd.read_parquet("nbastatsgami.parquet")
except Exception as e:
    st.error("❌ Erro ao carregar o arquivo 'nbastatsgami.parquet'.")
    st.write("### Tipo do erro:", type(e).__name__)
    st.write("### Mensagem do erro:", str(e))
    st.stop()

st.write("✅ Dataset carregado com sucesso!")
st.write("Colunas disponíveis:", list(df.columns))

st.write("Digite os stats para ver se esse combo já aconteceu na história do dataset.")

# 2) Inputs
points = st.number_input("Points", min_value=0, step=1)
rebounds = st.number_input("Rebounds (reboundsTotal)", min_value=0, step=1)
assists = st.number_input("Assists", min_value=0, step=1)
blocks = st.number_input("Blocks", min_value=0, step=1)
steals = st.number_input("Steals", min_value=0, step=1)

# 3) Lógica do scorigami
if st.button("Checar Scorigami"):
    # se por algum motivo df não existir, isso aqui já vai acusar na hora
    mask = (
        (df['points'] == points) &
        (df['reboundsTotal'] == rebounds) &
        (df['assists'] == assists) &
        (df['blocks'] == blocks) &
        (df['steals'] == steals)
    )

    matches = df[mask]

    st.write(
        f"Checando stats: {points} PTS, {rebounds} REB, {assists} AST, {blocks} BLK, {steals} STL"
    )

    if matches.empty:
        st.success("🟢 SCORIGAMI! Esse combo de stats nunca apareceu no dataset.")
    else:
        st.error(f"🔴 Esse combo já aconteceu {len(matches)} vez(es).")
        st.write("Jogos em que isso aconteceu:")

        cols = [
            'firstName',
            'lastName',
            'gameDateTimeEst',
            'playerteamName',
            'opponentteamName'
        ]
        cols = [c for c in cols if c in matches.columns]

        st.dataframe(
            matches[cols].sort_values('gameDateTimeEst').reset_index(drop=True)
        )
