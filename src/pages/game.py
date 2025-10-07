"""
Moteur de recherche (par prénom, année, type d’événement).
Exploration générationnelle ludique : cliquer sur une décennie → voir prénoms les plus donnés, âge moyen au mariage, espérance de vie.
Quiz interactif :
"Quel était le prénom le plus donné en 1920 ?"
"Quel était l’âge moyen au mariage dans les années 1950 ?"
Battle de prénoms : comparer deux prénoms (ex. Jean vs Paul) sur un graphe interactif.
"""

import streamlit as st

from src.utils import name_vs_name, find_name_query, dataset_load


# header
left, right = st.columns([1, 4])
logo = left.image(image="src/static/rodez_logo_propre.png", width=150)
right.title("Exploration ludique des jeux de données!")

# data
birth_load = dataset_load("liste_des_naissances.csv")

# Naissance

st.write("#### 1. 💪 Versus 💪!")
st.write("Objectif : Découvrir qui est le prénom le plus utilisé sur la période au complet ! 😎")

left, right = st.columns(2)

with left:
    name1 = st.text_input("Inscrire un 1er prénom ?  👇", key="prenom1")
with right:
    name2 = st.text_input("Inscrire un 2ème prénom ? 👇", key="prenom2")

if name1 and name2:
    result = name_vs_name(birth_load, name1, name2)
    left.metric(name1, result[name1])
    right.metric(name2, result[name2])

    if result[name1] == result[name2]:
        st.success(f"{result['winner']}")

    else:
        st.balloons()
        st.success(f"🏆 Et le.a gagnant.e est : {result['winner']}")

    result1 = find_name_query(birth_load, name1)
    df_linechart1 = result1["occurence_by_time"].reset_index()
    df_linechart1["annee"] = df_linechart1["annee"].astype(str)
    df_linechart1.columns = ["annee", "naissances"]
    left.line_chart(
        df_linechart1.set_index("annee"),
        y="naissances",
        x_label="Années",
        y_label="Naissances",
        use_container_width=True,
    )
    result2 = find_name_query(birth_load, name2)
    df_linechart2 = result2["occurence_by_time"].reset_index()
    df_linechart2["annee"] = df_linechart2["annee"].astype(str)
    df_linechart2.columns = ["annee", "naissances"]
    right.line_chart(
        df_linechart2.set_index("annee"),
        y="naissances",
        x_label="Années",
        y_label="Naissances",
        use_container_width=True,
    )


st.write("#### 2.  🤔 Quizz !")
st.write("Objectif : Découvrez votre score en répondant à ces 5 question ! 🤓")

st.write("#### 3. 💭 Devine qui c'est !")
st.write(
    "Objectif : click pour une periode d'une année, un random est fait, affiche un graphe (deces, naissance et "
    "mariage confondu, selectionne ton resultat et visualisez les résultats ! 🤗"
)
