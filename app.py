import streamlit as st
from api_football import (
    get_leagues,
    get_fixtures,
    get_seasons_for_league,
    get_fixtures_today,
    get_teams_for_league,
    get_statistics_for_fixture
)

st.set_page_config(page_title="MoneyBall", layout="wide")
st.title("📊 Análise de Partidas - API-Football")

# Menu lateral
aba = st.sidebar.radio("Escolha uma opção", ["Pesquisar por Liga/Temporada", "Jogos do Dia"])

# Função para exibir estatísticas
def mostrar_estatisticas(fixture_id):
    stats = get_statistics_for_fixture(fixture_id)
    if stats:
        for team_stats in stats:
            team = team_stats['team']['name']
            st.markdown(f"#### 📌 Estatísticas: {team}")
            for stat in team_stats['statistics']:
                st.write(f"{stat['type']}: {stat['value']}")
    else:
        st.warning("⚠️ Estatísticas indisponíveis para esta partida.")

# Função para exibir partidas
def exibir_jogos(lista):
    for jogo in lista:
        home = jogo['teams']['home']['name']
        away = jogo['teams']['away']['name']
        status = jogo['fixture']['status']['long']
        horario = jogo['fixture']['date']
        liga = f"{jogo['league']['name']} - {jogo['league']['country']}"
        fixture_id = jogo['fixture']['id']

        with st.expander(f"⚽ {home} x {away} — {status}"):
            st.write(f"**Liga:** {liga}")
            st.write(f"**Horário:** {horario}")
            st.write(f"**Status:** {status}")

            if st.button(f"📊 Ver Estatísticas - {fixture_id}"):
                mostrar_estatisticas(fixture_id)

# Aba 1: Pesquisa por Liga e Temporada
if aba == "Pesquisar por Liga/Temporada":
    st.subheader("🔍 Buscar Partidas por Liga e Temporada")

    leagues = get_leagues()
    if not leagues:
        st.error("⚠️ Não foi possível carregar as ligas. Verifique sua conexão com a internet ou a chave da API.")
        st.stop()

    liga_nome_id = {f"{l['league']['name']} - {l['country']['name']}": l['league']['id'] for l in leagues}
    liga_escolhida_nome = st.selectbox("Escolha uma liga", list(liga_nome_id.keys()))

    if not liga_escolhida_nome or liga_escolhida_nome not in liga_nome_id:
        st.warning("Por favor, selecione uma liga válida.")
        st.stop()

    liga_id = liga_nome_id[liga_escolhida_nome]

    seasons_info = get_seasons_for_league(liga_id)
    temporadas = [s["year"] for s in seasons_info]
    temporada_escolhida = st.selectbox("Temporada", sorted(temporadas, reverse=True))

    times = get_teams_for_league(liga_id, temporada_escolhida)
    opcoes_times = {t['team']['name']: t['team']['id'] for t in times}
    time_escolhido_nome = st.selectbox("Filtrar por Time (opcional)", ["Todos"] + list(opcoes_times.keys()))

    if st.button("🔍 Carregar Partidas"):
        st.write("🔄 Buscando partidas...")
        fixtures = get_fixtures(liga_id, temporada_escolhida)

        if time_escolhido_nome != "Todos":
            time_id = opcoes_times[time_escolhido_nome]
            fixtures = [j for j in fixtures if j['teams']['home']['id'] == time_id or j['teams']['away']['id'] == time_id]

        if not fixtures:
            st.warning("⚠️ Nenhuma partida encontrada para os filtros selecionados.")
        else:
            st.success(f"✅ {len(fixtures)} partidas encontradas.")
            exibir_jogos(fixtures[:20])


# Aba 2: Jogos do Dia
elif aba == "Jogos do Dia":
    st.subheader("📅 Partidas do Dia Atual")
    st.write("🔄 Carregando partidas do dia...")

    jogos_hoje = get_fixtures_today()

    if not jogos_hoje:
        st.warning("⚠️ Nenhum jogo encontrado para hoje.")
    else:
        st.success(f"✅ {len(jogos_hoje)} partidas encontradas hoje.")

        abas = st.tabs(["📆 Agendados", "🟢 Ao Vivo", "✅ Finalizados"])

        agendados = [j for j in jogos_hoje if j['fixture']['status']['short'] == 'NS']
        ao_vivo = [j for j in jogos_hoje if j['fixture']['status']['short'] in ['1H', '2H', 'ET', 'P', 'LIVE']]
        finalizados = [j for j in jogos_hoje if j['fixture']['status']['short'] == 'FT']

        with abas[0]:
            st.subheader("📆 Jogos Agendados")
            exibir_jogos(agendados)

        with abas[1]:
            st.subheader("🟢 Jogos Ao Vivo")
            exibir_jogos(ao_vivo)

        with abas[2]:
            st.subheader("✅ Jogos Finalizados")
            exibir_jogos(finalizados)
