import streamlit as st
import pandas as pd
import kagglehub
import os

@st.cache_data
def load_data():
    # Baixa a versão mais recente do dataset no cache do kagglehub
    path = kagglehub.dataset_download(
        "eoinamoore/historical-nba-data-and-player-box-scores"
    )

    # Lista os arquivos pra você debugar se precisar
    files = os.listdir(path)
    # st.write("Arquivos encontrados na pasta do dataset:", files)

    # 🔴 IMPORTANTE: ajuste o nome do arquivo CSV aqui
    # Use o mesmo nome que você usou no Colab (por ex: "player_box_scores.csv")
    csv_name = "PlayerStatistics.csv"  # <-- troque se o nome for outro

    full_path = os.path.join(path, csv_name)
    df = pd.read_csv(full_path)

    return df

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
