import streamlit as st
from api_football import get_leagues, get_fixtures

st.title("📊 Dados de Futebol com API-Football")

# Carregar ligas
st.subheader("Selecione a Liga e Temporada")
leagues = get_leagues()
ligas = {f"{l['league']['name']} - {l['country']['name']}": l['league']['id'] for l in leagues}

liga_escolhida = st.selectbox("Liga", list(ligas.keys()))
temporada = st.selectbox("Temporada", list(range(2020, 2025)))

if st.button("Carregar Partidas"):
    st.write("🔄 Carregando partidas...")
    fixtures = get_fixtures(ligas[liga_escolhida], temporada)
    
    for game in fixtures[:10]:  # Exibe só os 10 primeiros
        st.markdown(f"**{game['teams']['home']['name']} x {game['teams']['away']['name']}**")
        st.write(f"Data: {game['fixture']['date']}")
        st.write(f"Status: {game['fixture']['status']['long']}")
        st.markdown("---")
