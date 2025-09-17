import streamlit as st
import plotly.express as px
from src.utils import dataset_load, counter_data_total, aggregate_by_gender, multiple_aggregate_by_year, top_name

col1,col2 = st.columns([1,4])
logo = col1.image(image="src/assets/rodez_logo_propre.png", width=150)
title = col2.title("Rodez : histoire en données !")


st.markdown("""### Bienvenue dans l'explorateur des données de la ville de Rodez !""")
st.markdown("""#### 1. Objectif""")
st.write("L'objectif de cet explorateur est avant tout pour découvrir l'utilisation de *Streamlit*, un framework python"
         "UI pour la divulgation de données sous forme de applications *data* simplement."
         "Le second étant de me familiariser avec la manipulation des données, l'analyse sur un ou plusieurs dataset.\n"
         "Et il s'avère que la ville de Rodez -*que je remercie au passage*- à mise a disposition 3 datasets "
         "qui sont parfait pour démarrer sur le sujet ! 😉")

st.markdown("""##### Notes""")
st.write(
    "Les données proviennent de cette source : https://www.data.gouv.fr/datasets/population-mariages-deces-naissances-1/ en date du 17/10/2016.\n\n"
    "Les données publiées comptabilisent l’ensemble des naissances, décès et mariages célébrés depuis 1891.\n\n"
    "Les données sont classées par années et sur le dataset des naissances figurent  en plus le prénom de la personne concernée.")

st.error("#### Important !\n\n "
         "Certaines données peuvent contenir des erreurs ou être incomplètes et les analyses ont été faites en "
         "conséquences, au mieux de ce que les datasets donnent. Les datasets ont vu leurs entêtes ajoutés et le dataset "
         "des mariages a été repris pour corriger des erreurs de décalage des données manuellement.")

st.markdown("""#### 2. Quelques chiffres clés pour démarrer !""")

st.write("Dans ce premier set, les valeurs sont les totaux relevés sans tri des valeurs nulles.")
# carte ou metrics simples
n, m, d = st.columns(3)
birth_load = dataset_load("liste_des_naissances.csv")
birth = counter_data_total(birth_load)
death_load = dataset_load("liste_des_deces.csv")
death = counter_data_total(death_load)
wedding_load = dataset_load("liste_des_mariages.csv")
wedding = counter_data_total(wedding_load)
n.metric(label="Nombre total des naissances", value=f"{birth}", border=True)
m.metric(label="Nombre total des mariages", value=f"{wedding}", border=True)
d.metric(label="Nombre total des décès", value=f"{death}", border=True)

st.markdown("""#### 3. Timeline des naissances, mariages et décès""")

st.info("Ici les valeurs avec une année inférieur à 1981 ont été ignorées.")

timeline = multiple_aggregate_by_year(birth_load, death_load, wedding_load).rename(columns={0: "Naissances", 1: "Décès", 2: "Mariages"})
with st.container():
    st.line_chart(timeline, color=["#1CAEED", "#000000", "#ED1C6E"], x="annee", x_label="Années")

    st.write(
        "Cette timeline permet rapidement d'avoir un coup d'oeil sur les périodes importante des dernière décennies. "
        "\n"
        "1) 1ère guerre mondiale 1914-1918 avec un pic 1918\n"
        "2) 2ème guerre  mondiale 1939-1944 avec deux pics de décès en 1940 et 1944\n"
        "3) La période des 30 glorieuses : 1945-1973")


st.markdown("""#### 4. Focus rapide sur certaines données""")

st.write("Répartition Hommes/Femmes sur la période 1981-2016")
n2, d2 = st.columns(2)
fig = px.pie(aggregate_by_gender(dataset=birth_load, column_name="genre"), values=0, title="Répartition au niveau des naissances")
n2.plotly_chart(fig, theme=None)
fig2 = px.pie(aggregate_by_gender(dataset=death_load, column_name="genre"), values=0, title="Répartition au niveau des décès")
d2.plotly_chart(fig2, theme=None)


st.write("Top 5 des prénoms sur la période 1981-2016")
st.bar_chart(data=top_name(dataset=birth_load, column_name="pr1", limiter=5), x_label="Prénoms", y_label="Nombre d'occurrences")

st.markdown("""#### 4. Approfondir l'exploration ?""")

left, middle, right = st.columns(3)
left.page_link(label="Explorons les naissances", page="src/pages/birth.py", width="stretch")
middle.page_link(label="Explorons les mariages", page="src/pages/wedding.py", width="stretch")
right.page_link(label="Explorons les décès", page="src/pages/death.py", width="stretch")
