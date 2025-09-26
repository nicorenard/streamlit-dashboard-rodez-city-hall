"""
Évolution démographique : naissances vs décès → tendance naturelle de croissance/déclin.
Âge au mariage par cohorte (ex. génération née dans les années 1920 → mariée en moyenne à 25 ans).
Espérance de vie moyenne par cohorte (décès − naissance).
Impact des événements historiques : guerres mondiales, baby-boom, crises sanitaires → mise en évidence des variations.
Comparaison inter-périodes : avant/après-guerre, baby-boom, crises.
"""

import streamlit as st
import plotly.express as px
from src.utils import dataset_load, multiple_event_by_year

# data
birth_load = dataset_load("liste_des_naissances.csv")
death_load = dataset_load("liste_des_deces.csv")
wedding_load = dataset_load("liste_des_mariages.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/assets/rodez_logo_propre.png", width=150)
right.title("Explorations temporelles transversale")

st.write("""L'objectif de cette page est de metre en avant les données des 3 datasets et d'analyser d'un point de 
vue historique, démographique les données. Le but but est de comparer les tendances et les interactions temporelles.""")

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
st.markdown("""### 2. Indicateurs dynamiques""")
# carte de metriques / barre empilées
# naissances/deces ( soldes naturels)
# mariages/naissances ( indicateur indirecte de ma contexte social)
# deces/mariages ( chox demographique pendant les crises)

st.divider()
st.markdown("""### 3. Décalages générationnels""")
# naissance vs mariages 20-30 + tard
## objectif : illustrer les effet generationnel comme le babyboom

st.divider()
st.markdown("""### 4. Focus historique""")
# selecteur de periode (menu deroulant, 14-18, 39-45, 68-75)
# graphique qui evolue et montre les valeurs de mariages, deces etc....
