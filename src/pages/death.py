"""
📊 Timeline interactive des décès par année/mois.
⚰️ Distribution des âges au décès (histogramme, boxplot).
🔄 Ratio hommes/femmes au décès.
⏰ Répartition des heures de décès (matin, après-midi, nuit).
🎂 Centenaires recensés (liste, stats, courbes).

Note : beaucoup de données ont que al date de deces mais pas la date de naissance.
"""

import streamlit as st
import altair as alt
import plotly.graph_objects as go
import streamlit_shadcn_ui as ui

from src.utils import (dataset_load, aggregate_by_year, aggregate_by_gender_and_by_year,
                       top_and_down_death_year, average_death_age_by_year, death_age_histogram,
                       average_death_age_by_year_and_genre, death_by_season_month, death_by_month_chart,
                       death_by_day)

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
dfg = aggregate_by_gender_and_by_year(death_load).reset_index()

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
st.divider()
st.markdown("""### 2. Quelques indicateurs """)

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

st.write("""#### a. Histogramme de l'age moyen du décès""")

st.info("""##### Note
Les données ici ne prennent pas en compte que les lignes complètes avec date de décès et de naissances!""")


year_range = st.slider(label="Période à sélectionner", min_value=1981, max_value=2016, value=(1981, 2016))
histo = death_age_histogram(death_load, 20, year_range)
st.bar_chart(histo)

st.write("""#### b. Espérance de vie moyenne par année""")

df_av1 = average_death_age_by_year(death_load).reset_index()
df_av1.columns = ["annee", "age_deces_moyen"]

chart1 = alt.Chart(df_av1).mark_area(opacity=0.3).encode(
    x=alt.X("annee:O", title="Années"),
    y=alt.Y("age_deces_moyen:Q", title="Âges moyen des décès")
)

st.altair_chart(chart1, use_container_width=True)

st.write("""#### c. Espérance de vie moyenne par année et par genre""")

df_av2 = average_death_age_by_year_and_genre(death_load).reset_index()

chart2 = alt.Chart(df_av2).mark_area(opacity=0.3).encode(
    x=alt.X("annee:O", title="Années"),  # ':O' = force ordinal axis -> no separator
    y=alt.Y("age_deces:Q", title="Âge moyen au décès", stack=None),
    color=alt.Color("genre:N", title="Genre",
                    scale=alt.Scale(
                        domain=["Masculin", "Feminin"],
                        range=["blue", "red"]
                        )
                    ),
    tooltip=["annee", "genre", "age_deces"]
).interactive()  # allow zoom

st.altair_chart(chart2, use_container_width=True)

st.write("""### 3. Analyses temporelle""")

st.write("""#### a. Analyses par mois sur la période complète""")
df_plot = death_by_month_chart(death_load).reset_index()
df_plot.columns = ["Mois", "Décès"]

months = [
    "Janvier","Février","Mars","Avril","Mai","Juin",
    "Juillet","Août","Septembre","Octobre","Novembre","Décembre"
]

chart = alt.Chart(df_plot).mark_bar().encode(
    x=alt.X("Mois:N", sort=months, title="Mois"),
    y=alt.Y("Décès:Q", title="Nombre de décès"),
    tooltip=["Mois", "Décès"]
)

st.altair_chart(chart, use_container_width=True)

# deces par saisonnalité (hiver/été).
st.write("""#### b. Analyses par saison sur la période complète""")

df_season = death_by_season_month(death_load)

df_plot1 = df_season.reset_index()
df_plot1.columns = ["Catégorie", "Décès"]

# Color scale simple
chart = alt.Chart(df_plot1).mark_bar().encode(
    x=alt.X("Catégorie:N", sort=df_plot1.index.tolist(), title=""),
    y=alt.Y("Décès:Q", title="Nombre de décès"),
    color=alt.Color("Décès:Q", scale=alt.Scale(scheme="reds")),
    tooltip=["Catégorie", "Décès"]
).properties(
    title="Décès par saison",
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)

#Décès par jour de la semaine
st.write("""#### c. Analyses par jours sur la période complète""")

df_days = death_by_day(death_load)
df_plot3 = df_days.reset_index()
df_plot3.columns = ["Jour", "Décès"]

days_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Créer le line chart
chart3 = alt.Chart(df_plot3).mark_line(point=True, color="steelblue").encode(
    x=alt.X("Jour:N", sort=days_order, title="Jour de la semaine"),
    y=alt.Y("Décès:Q", title="Nombre de décès"),
    tooltip=["Jour", "Décès"]
).properties(
    title="Décès par jour de la semaine",
    width=600,
    height=400
)

st.altair_chart(chart3, use_container_width=True)

#4. Genre
# Proportion des décès par genre chaque année.
# Espérance de vie hommes vs femmes.

# 5. Comparatifs
# Comparaison de l’âge moyen au décès sur différentes périodes (ex. avant 1950 vs après 2000).

