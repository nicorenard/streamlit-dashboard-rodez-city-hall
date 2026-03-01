"""
Évolution démographique : naissances vs décès → tendance naturelle de croissance/déclin.
Âge au mariage par cohorte (ex. génération née dans les années 1920 → mariée en moyenne à 25 ans).
Espérance de vie moyenne par cohorte (décès − naissance).
Impact des événements historiques : guerres mondiales, baby-boom, crises sanitaires → mise en évidence des variations.
Comparaison inter-périodes : avant/après-guerre, baby-boom, crises.
"""

import plotly.express as px
import streamlit as st
from src.utils import dataset_load, multiple_event_by_year, multiple_aggregate_by_year

# data
birth_load = dataset_load("liste_des_naissances.csv")
death_load = dataset_load("liste_des_deces.csv")
wedding_load = dataset_load("liste_des_mariages.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/static/rodez_logo_propre.png", width=150)
right.title("Explorations temporelles transversale")

st.write("""L'objectif de cette page est de mettre en avant les données des 3 datasets et d'analyser d'un point de 
vue historique, démographique les données. Le but est de comparer les tendances et les interactions temporelles.""")

st.divider()
st.markdown("""### 1. Volumétries annuelles""")
st.write(
    "Le but de cette analyse est permettre l'identification rapide des tendances synchrones (croissance, stagnation, chutes)"
    "ainsi que les ruptures (pics, creux, croisements)"
)


radar_df = multiple_event_by_year(birth_load, death_load, wedding_load)
years_choices = radar_df.index.tolist()
selected_years = st.multiselect(
    "Sélectionnez les années à comparer :", options=years_choices, default=[years_choices[50]]
)

# Préparation des données pour Plotly radar
if selected_years:
    radar_data = (
        radar_df.loc[selected_years]
        .reset_index()
        .melt(id_vars="annee", var_name="Événement", value_name="Valeur")
    )
    radar_data.rename(columns={"annee": "Années"}, inplace=True)

    # Radar chart
    fig = px.line_polar(
        radar_data, r="Valeur", theta="Événement", color="Années", line_close=True, markers=True
    )
    fig.update_traces(fill="toself")  # for polygons
    st.plotly_chart(fig, use_container_width=True)


st.divider()
st.markdown("### 2. Indicateurs dynamiques")
st.markdown(
    "Les indicateurs combinent naissances, mariages et décès pour analyser "
    "les dynamiques démographiques et sociales au fil du temps."
)

# --- Préparation timeline ---
timeline = multiple_aggregate_by_year(
    birth_load,
    death_load,
    wedding_load
)

timeline = timeline.sort_values("annee").copy()

# colonne affichage pour éviter 1,950
timeline["annee_label"] = timeline["annee"].astype(str)

# --- Slider temporel ---
year_min = int(timeline["annee"].min())
year_max = int(timeline["annee"].max())

year_range = st.slider(
    "Période d'analyse",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# filtrage sécurisé
filtered = timeline[
    (timeline["annee"] >= year_range[0]) &
    (timeline["annee"] <= year_range[1])
].copy()

# --- Choix indicateur ---
indicator = st.radio(
    "Indicateur",
    [
        "Solde naturel (Naissances - Décès)",
        "Mariages / Naissances",
        "Décès / Mariages"
    ],
    horizontal=True
)

if indicator == "Solde naturel (Naissances - Décès)":
    filtered["indicateur"] = filtered["Naissances"] - filtered["Décès"]
    label = "Solde naturel"

elif indicator == "Mariages / Naissances":
    filtered["indicateur"] = (
        filtered["Mariages"] / filtered["Naissances"].replace(0, None)
    )
    label = "Mariages / Naissances"

else:
    filtered["indicateur"] = (
        filtered["Décès"] / filtered["Mariages"].replace(0, None)
    )
    label = "Décès / Mariages"

# --- Metrics ---
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Moyenne", round(filtered["indicateur"].mean(), 2))

with c2:
    st.metric("Maximum", round(filtered["indicateur"].max(), 2))

with c3:
    st.metric("Minimum", round(filtered["indicateur"].min(), 2))

# --- Graphique ---
st.line_chart(
    filtered,
    x="annee_label",
    y="indicateur",
    y_label=label,
    x_label="Année"
)
st.markdown("### Comprendre le graphique")

if indicator == "Solde naturel (Naissances - Décès)":
    st.write(
        "Un solde positif indique une croissance naturelle de la population, "
        "un solde négatif un vieillissement ou une période de crise."
    )

elif indicator == "Mariages / Naissances":
    st.write(
        "Ce ratio reflète indirectement le contexte social et les comportements familiaux.\n"
        "Les analyses possibles:  \n"
        "- Ratio élevé = Mariages plus fréquents, Natalité plus tardive ou en baisse,\n"
        "- Ratio faible = Forte natalité avec de structures familiales plus traditionnelles ou plus jeunes"
    )

else:
    st.write(
        "L'Indicateur de stress démographique.\n "
        "Ce ratio est très sensible aux crises, un ratio élevé peut signaler une période de tension démographique ou sociale.\n"
        "Les analyses possibles:  \n"
        "- Ratio élevé : Moins de mariages, plus de décès, causes => Climat anxiogène (guerre, épidémie, crise économique)\n"
        "- Ratio faible : Société stable => Projection dans l’avenir (mariages nombreux)"
    )



st.divider()
st.markdown("""### 3. Décalages générationnels""")
# naissance vs mariages 20-30 + tard
## objectif : illustrer les effet generationnel comme le babyboom

st.divider()
st.markdown("""### 4. Focus historique""")
# selecteur de periode (menu deroulant, 14-18, 39-45, 68-75)
# graphique qui evolue et montre les valeurs de mariages, deces etc....
