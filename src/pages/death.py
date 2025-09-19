"""
📊 Timeline interactive des décès par année/mois.
⚰️ Distribution des âges au décès (histogramme, boxplot).
🔄 Ratio hommes/femmes au décès.
⏰ Répartition des heures de décès (matin, après-midi, nuit).
🎂 Centenaires recensés (liste, stats, courbes).

Note : beaucoup de données ont que al date de deces mais pas la date de naissance.
"""

import streamlit as st
import plotly.graph_objects as go
import streamlit_shadcn_ui as ui

from src.utils import dataset_load, aggregate_by_year, aggregate_birth_by_gender_and_by_year
from src.utils import (dataset_load, aggregate_by_year, aggregate_birth_by_gender_and_by_year,
                       top_and_down_death_year, average_death_age_by_year, death_age_histogram)

#data
death_load = dataset_load("liste_des_deces.csv")

# header
left,right = st.columns([1, 4])
logo = left.image(image="src/assets/rodez_logo_propre.png", width=150)
right.title("Exploration des décès")

st.write("Le dataset des décès est très léger en terme de richesse des données.\n\n"
         "On notera cependant les élements suivant qui permettent : \n\n"
         "1) D'explorer temporellement les décès sur les années, d'avoir un focus sur certaines périodes traversées ou sur le genre \n"
         "2) D'effectuer une analyse des répartitions en fonctions des horaires \n"
         "3) D'avoir une focus sur certains indicateurs comme les centenaires par exemple")

st.divider()
## exploration temporelle
# timeline des deces + repartition homme/femme
st.markdown("""### 1. Timelines""")

st.markdown("""#### a. Vue générale""")

df = aggregate_by_year(death_load)
with st.container():
    st.bar_chart(df, x_label="Années", y_label="Nombre de naissances total")

st.write("#### Note\n"
         "On remarque les pics historique sur les années des deux grandes guerres mondiales mais également apres "
         "la période des 30 glorieuses que le nombre de décès ne cesse de croire. Une analyse croisée avec les naissances "
         "pourra expliquer cette tendance à la hausse si la population vieillissante n'est pas renouvelée...")

st.markdown("""#### b. Vue par genres""")
dfg = aggregate_birth_by_gender_and_by_year(death_load).reset_index()

fig = go.Figure()
for genre, color in zip(["Féminin", "Masculin"], ["#FF69B4", "#1f77b4"]):
    fig.add_trace(go.Scatter(
        x=dfg["annee"],
        y=dfg[genre],
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        name=genre,
        opacity=0.3
    ))
st.plotly_chart(fig, use_container_width=True)

st.write("#### Note\n"
         "La vue par genre n'est pas parfaite car beaucoup de lignes ne sont pas complète et la précision du genre est "
         "plus présente dans le relevé vers les années 2000...")

st.markdown("""### 2. Quelques indicateurs """)

# Année la plus haute / la plus basse en nombre de décès avec ui.metric_card.

result = top_and_down_death_year(death_load)
top, down = st.columns(2)

with top:
    ui.metric_card(
        title="📊 Année la plus haute",
        content=result["highest_year"]["year"],
        description=f"{result['highest_year']['value']} décès"
    )


with down:
    ui.metric_card(
        title="📉 Année la plus basse",
        content=result["lowest_year"]["year"],
        description=f"{result['lowest_year']['value']} décès"
    )

st.write("""Espérance de vie moyenne par année""")
#
# Comparaison hommes vs femmes.
#3. Analyse temporelle dans l’année

#Avec date_deces et heure_deces :

#Décès par mois → saisonnalité (hiver/été).
#Décès par jour de la semaine
#Décès par tranche horaire (matin / après-midi / nuit)?


