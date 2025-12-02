import streamlit as st
import pandas as pd
import requests
from io import StringIO


@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1bSWKcYcyDBFXiF3qdzBi6CaZjBTBJGNG"

    # Baixa o conteúdo bruto
    resp = requests.get(url)
    resp.raise_for_status()

    content = resp.text

    # Tentativa 1: CSV padrão com vírgula
    try:
        df = pd.read_csv(StringIO(content))
        return df
    except pd.errors.ParserError:
        pass

    # Tentativa 2: CSV com ponto e vírgula (bem comum em pt-BR)
    try:
        df = pd.read_csv(StringIO(content), sep=";")
        return df
    except pd.errors.ParserError:
        pass

    # Se nada funcionar, mostramos um pedaço do conteúdo pra debug
    first_500 = content[:500]
    st.error("Não consegui ler o arquivo como CSV. Veja abaixo os primeiros caracteres do arquivo para debug:")
    st.code(first_500)
    raise RuntimeError("Falha ao fazer o parse do CSV.")

df = load_data()

st.title("NBA Boxscore Scorigami")

st.write("Digite os stats para ver se esse combo já aconteceu na história do dataset.")

points = st.number_input("Points", min_value=0, step=1)
rebounds = st.number_input("Rebounds (reboundsTotal)", min_value=0, step=1)
assists = st.number_input("Assists", min_value=0, step=1)
blocks = st.number_input("Blocks", min_value=0, step=1)
steals = st.number_input("Steals", min_value=0, step=1)

if st.button("Checar Scorigami"):
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
