import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1bSWKcYcyDBFXiF3qdzBi6CaZjBTBJGNG"
    df = pd.read_csv(url)
    return df


df = load_data()

st.write("Colunas do dataset:", list(df.columns))

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
