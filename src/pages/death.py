import altair as alt
import plotly.graph_objects as go
import streamlit as st
import streamlit_shadcn_ui as ui
from src.utils import (
    dataset_load,
    aggregate_by_year,
    aggregate_by_gender_and_by_year,
    top_year_and_down_year,
    average_death_age_by_year,
    death_age_histogram,
    average_death_age_by_year_and_genre,
    death_by_season_month,
    death_by_month_chart,
    death_by_day,
)

# data
death_load = dataset_load("liste_des_deces.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/static/rodez_logo_propre.png", width=150)
right.title("Exploration des décès")

st.write(
    "Le dataset des décès est plutôt léger en terme de richesse des données.\n\n"
    "On notera cependant les élements suivant qui permettent : \n\n"
    "1) D'explorer temporellement les décès sur les années, d'avoir un focus sur certaines périodes traversées ou sur le genre \n"
    "2) D'effectuer une analyse des répartitions en fonctions des horaires \n"
    "3) D'avoir une focus sur certains indicateurs comme les centenaires par exemple"
)

st.divider()
st.markdown("""### 1. Timelines""")

st.markdown("""#### a. Vue générale""")

df = aggregate_by_year(death_load)
with st.container():
    st.bar_chart(df, x_label="Années", y_label="Nombre de naissances total")

st.write(
    "#### Note\n"
    "On remarque les pics historique sur les années des deux grandes guerres mondiales mais également après "
    "la période des 30 glorieuses que le nombre de décès ne cesse de croitre. Une analyse croisée avec les naissances "
    "pourrait expliquer cette tendance à la hausse si la population vieillissante n'est pas renouvelée..."
)

st.markdown("""#### b. Vue par genres""")
dfg = aggregate_by_gender_and_by_year(death_load).reset_index()
genre_cols = [col for col in ["Féminin", "Masculin"] if col in dfg.columns]
dfg = dfg[dfg[genre_cols].max(axis=1) > 2]
dfg["annee"] = dfg["annee"].astype(int)

fig = go.Figure()
for genre, color in zip(["Féminin", "Masculin"], ["#FF69B4", "#1f77b4"]):
    fig.add_trace(
        go.Scatter(
            x=dfg["annee"],
            y=dfg[genre],
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            name=genre,
            opacity=0.3,
        )
    )
st.plotly_chart(fig, use_container_width=True)

st.write(
    "#### Note : \n"
    "La vue par genre n'est pas parfaite car beaucoup de lignes sont incomplète et la précision du genre est "
    "plus représenté dans le relevé à partir des années 2000..."
)
st.divider()
st.markdown("""### 2. Quelques indicateurs """)

result = top_year_and_down_year(death_load)
top, down = st.columns(2)

with top:
    ui.metric_card(
        title="📊 Année la plus haute",
        content=result["highest_year"]["year"],
        description=f"{result['highest_year']['value']} décès",
    )


with down:
    ui.metric_card(
        title="📉 Année la plus basse",
        content=result["lowest_year"]["year"],
        description=f"{result['lowest_year']['value']} décès",
    )

st.markdown("""### 3. Analyses de moyennes """)

st.write("""#### a. Histogramme de l'age moyen du décès""")

st.info("""##### Note
Les données ici ne prennent en compte que les lignes complètes avec date de décès et date de naissances!""")


year_range = st.slider(
    label="Période à sélectionner", min_value=1981, max_value=2016, value=(1981, 2016)
)
histo = death_age_histogram(death_load, 20, year_range)
st.bar_chart(histo)

st.write("""#### b. Espérance de vie moyenne par année""")

df_av1 = average_death_age_by_year(death_load).reset_index()
df_av1.columns = ["annee", "age_deces_moyen"]

chart1 = (
    alt.Chart(df_av1)
    .mark_area(opacity=0.3)
    .encode(
        x=alt.X("annee:O", title="Années"),
        y=alt.Y("age_deces_moyen:Q", title="Âges moyen des décès"),
    )
)

st.altair_chart(chart1, use_container_width=True)

st.write("""#### c. Espérance de vie moyenne par année et par genre""")

df_av2 = average_death_age_by_year_and_genre(death_load).reset_index()

chart2 = (
    alt.Chart(df_av2)
    .mark_area(opacity=0.3)
    .encode(
        x=alt.X("annee:O", title="Années"),  # ':O' = force ordinal axis -> no separator
        y=alt.Y("age_deces:Q", title="Âge moyen au décès", stack=None),
        color=alt.Color(
            "genre:N",
            title="Genre",
            scale=alt.Scale(domain=["Masculin", "Feminin"], range=["blue", "red"]),
        ),
        tooltip=["annee", "genre", "age_deces"],
    )
    .interactive()
)  # allow zoom

st.altair_chart(chart2, use_container_width=True)

st.divider()
st.write("""### 4. Analyses temporelle""")

st.write("""#### a. Analyses par mois sur la période complète""")
df_plot = death_by_month_chart(death_load).reset_index()
df_plot.columns = ["Mois", "Décès"]

months = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]

chart = (
    alt.Chart(df_plot)
    .mark_bar()
    .encode(
        x=alt.X("Mois:N", sort=months, title="Mois"),
        y=alt.Y("Décès:Q", title="Nombre de décès"),
        tooltip=["Mois", "Décès"],
    )
)

st.altair_chart(chart, use_container_width=True)


st.write("""#### b. Analyses par saison sur la période complète""")

df_season = death_by_season_month(death_load)

df_plot1 = df_season.reset_index()
df_plot1.columns = ["Catégorie", "Décès"]


chart = (
    alt.Chart(df_plot1)
    .mark_bar()
    .encode(
        x=alt.X("Catégorie:N", sort=df_plot1.index.tolist(), title=""),
        y=alt.Y("Décès:Q", title="Nombre de décès"),
        color=alt.Color("Décès:Q", scale=alt.Scale(scheme="reds")),
        tooltip=["Catégorie", "Décès"],
    )
    .properties(title="Décès par saison", width=600, height=400)
)

st.altair_chart(chart, use_container_width=True)


st.write("""#### c. Analyses par jours entre 1891-2016 """)

df_days = death_by_day(death_load)
df_plot3 = df_days.reset_index()
df_plot3.columns = ["Jour", "Décès"]

days_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

chart3 = (
    alt.Chart(df_plot3)
    .mark_line(point=True, color="steelblue")
    .encode(
        x=alt.X("Jour:N", sort=days_order, title="Jours de la semaine"),
        y=alt.Y("Décès:Q", title="Nombre de décès"),
        tooltip=["Jour", "Décès"],
    )
    .properties(title="Décès par jour de la semaine", width=600, height=400)
)

st.altair_chart(chart3, use_container_width=True)
