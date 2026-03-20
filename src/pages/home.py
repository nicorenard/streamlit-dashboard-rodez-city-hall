import plotly.express as px
import streamlit as st
from src.components import render_footer
from src.utils import (
    dataset_load,
    size_dataset,
    aggregate_by_gender_df,
    multiple_aggregate_by_year,
    top_name,
    load_css,
)

load_css("style.css")


col1, col2 = st.columns([1, 4])
logo = col1.image(image="src/static/rodez_logo_propre.png", width=150)
title = col2.title("Bienvenue dans l'explorateur des données de la ville de Rodez !")


st.markdown("""#### 1. Objectif du projet""")
st.write(
    "L'objectif est avant tout formateur et pédagogique. L'idée est de créé un site d'exploration et de voir jusqu'ou les données de la ville peuvent"
    " être exploitées. De plus le dataset n'ayant pas de réutilisation c'est l'ocassion de leur donner un peu plus de visibilité ! 😉"
)

st.markdown("""##### Note sur les datasets""")
st.markdown(
    "* Les données publiées comptabilisent l’ensemble des naissances, décès et mariages célébrés depuis 1891 jusqu'à 2016.\n\n"
)

st.error(
    "#### Important !\n\n "
    "Certaines données peuvent contenir des erreurs ou être incomplètes et les analyses ont été faites en "
    "conséquences, c'est à dire au mieux de ce que les datasets donnent. Les datasets ont vu leurs entêtes ajoutés et le dataset "
    "des mariages a été repris pour corriger des erreurs de décalage des données mais de manière manuellement pour le site."
)

st.markdown("""#### 2. Quelques chiffres clés pour démarrer !""")

#  metriques simples
n, m, d = st.columns(3)
birth_load = dataset_load("liste_des_naissances.csv")
birth = size_dataset(birth_load)
death_load = dataset_load("liste_des_deces.csv")
death = size_dataset(death_load)
wedding_load = dataset_load("liste_des_mariages.csv")
wedding = size_dataset(wedding_load)
n.metric(label="Nombre total des naissances", value=f"{birth}", border=True)
m.metric(label="Nombre total des mariages", value=f"{wedding}", border=True)
d.metric(label="Nombre total des décès", value=f"{death}", border=True)

st.markdown("""#### 3. Timeline des naissances, mariages et décès""")

st.info("Note : les valeurs avec une année inférieure à 1891 ont été ignorées.")

timeline = multiple_aggregate_by_year(birth_load, death_load, wedding_load)
timeline = timeline.copy()
timeline["annee"] = timeline["annee"].astype(int).astype(str)

with st.container():
    st.line_chart(
        timeline,
        color=["#1CAEED", "#000000", "#ED1C6E"],
        x="annee",
        x_label="Années",
        y_label="Volume de Naissances/Déces/Mariages",
        use_container_width=True,
    )

    st.write(
        "Cette timeline permet rapidement d'avoir un coup d'oeil sur les périodes importantes des dernières décennies. "
        "\n"
        "1) 1ère guerre mondiale 1914-1918 avec un pic 1918\n"
        "2) 2ème guerre  mondiale 1939-1944 avec deux pics de décès en 1940 et 1944\n"
        "3) La période des 30 glorieuses : 1945-1973"
    )


st.markdown("""#### 4. Focus rapide sur certaines données""")

st.write("Ratio Hommes/Femmes sur la période 1891-2016")
st.info("Note : Homme  = bleu / Femme = rouge")
n2, d2 = st.columns(2)
fig = px.pie(
    aggregate_by_gender_df(dataset=birth_load, column_name="genre"),
    values="count",
    title="Ratio des Naissances",
)
n2.plotly_chart(fig, theme=None)

fig2 = px.pie(
    aggregate_by_gender_df(dataset=death_load, column_name="genre"),
    values="count",
    title="Ratio des Décès",
)
d2.plotly_chart(fig2, theme=None)


st.write("Top 5 des prénoms sur la période 1891-2016")
st.bar_chart(
    data=top_name(dataset=birth_load, column_name="pr1", limiter=5),
    x_label="Prénoms",
    y_label="Nombre d'occurrences",
)

st.markdown("""#### 4. Approfondir l'exploration ?""")

st.write("Pour approfondir l'exploration, vous pouvez cliquer sur les boutons suivants")
left, middle, right = st.columns(3)
left.page_link(label="Explorons les naissances", page="src/pages/birth.py", width="stretch")
middle.page_link(label="Explorons les mariages", page="src/pages/wedding.py", width="stretch")
right.page_link(label="Explorons les décès", page="src/pages/death.py", width="stretch")

# footer
render_footer()
