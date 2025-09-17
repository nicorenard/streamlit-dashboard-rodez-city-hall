"""📊 Timeline interactive des naissances par année/mois.
🎨 Top prénoms par décennie (tableau + nuage de mots).
🔍 Comparateur de prénoms (Marie vs Emma, etc.).
"""
import streamlit as st
import plotly.graph_objects as go

from src.utils import (dataset_load, aggregate_birth_by_gender_and_by_year, top_or_down_birth,
                       top_name_by_year_and_gender, aggregate_by_year, top_name_by_genre, find_name_query)


#data
birth_load = dataset_load("liste_des_naissances.csv")

# header
col1,col2 = st.columns([1,4])
logo = col1.image(image="src/assets/rodez_logo_propre.png", width=150)
col2.title("Exploration des naissances à Rodez ")

st.write("Le dataset des naissances est plutôt léger en terme de richesse des données.\n\n"
         "On notera cependant les élements suivant qui permettent : \n\n"
         "1) D'explorer temporellement les naissances sur les années, d'avoir un focus sur certaines périodes traversées, quelques statistiques intéressantes\n"
         "2) D'effectuer une analyse des prénoms sous différents format ou comparaison \n"
         "3) D'avoir une focus sur certains indicateurs")

st.divider()
## exploration temporelle
# timeline des naissances -> line chart o
st.markdown("""### 1. Timelines""")

st.markdown("""#### a. Vue générale""")

df = aggregate_by_year(birth_load)
with st.container():
    st.bar_chart(df, x_label="Années", y_label="Nombre de naissances total")

st.markdown("""#### b. Vue par genres""")
dfg = aggregate_birth_by_gender_and_by_year(birth_load).reset_index()

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
         "La chute de natalité pour les année 1982-1983 fait partie d'un ensemble de facteurs économiques, sociale "
         "et culturel dont une partie des réponses peut se retrouver comme expliqué "
         "dans cet article du Monde : https://www.lemonde.fr/archives/article/1983/10/05/la-natalite-continue-de-baisser-en"
         "-france-50-000-naissances-de-moins-en-1983_3077597_1819218.html")

# filtre par année et décénie ? evènements important avec une checkbox
# heatmatp par mois pour voir les pics de naissance
# barchart avec ratio fille/garçon + année sur timeline


## analyse de prénoms
st.divider()
st.markdown("""### 2. Focus sur les prénoms """)
# top des prénoms par ans ou sur 10ans en bar chart/table

st.write("### Top prénoms par année et par genre")
result = top_name_by_year_and_gender(birth_load)
styled = (
    result.style
    .set_table_styles(
        [{"selector": "th", "props": [("font-size", "16px"), ("text-align", "center")]},
         {"selector": "td", "props": [("font-size", "16px"), ("text-align", "center")]}]
    )
    .map(lambda x: "background-color: #e6f2ff" if x else "")
)
st.dataframe(styled, use_container_width=True)

# recherche input d'un prénom pour avoir le nombre d'occurence + sa courbe dans le temps
st.write("### Tendance et occurrence d'un prénom")

name_input = st.text_input(label="Inscrire un prénom 👇")
if name_input :
    result = find_name_query(birth_load, name_input)
    print(result)
    st.metric("Nombre total d'occurrences détectées", result["total_occurence"])
    df_linechart = result["occurence_by_time"].reset_index()
    df_linechart.columns = ["annee", "naissances"]
    st.line_chart(df_linechart, x="annee", y="naissances")


# comparaison entre 2 prénoms

## indicateurs
st.divider()
st.markdown("""### 3. Quelques indicateurs de records""")

# records de prénoms le plus données coté fille et coté garçon
st.markdown("""#### a. Records des prénoms""")
name = top_name_by_genre(dataset=birth_load)
boy, girl = st.columns(2)

with boy:
    st.metric("👨Top prénom Homme",
              value=name["male"])
with girl:
    st.metric("👩 Top prénom Femme",
              value=name["female"])

# record de naissances, naissances la plus basse
st.markdown("""
<strong><span style="font-size:25px;">b. Records des naissances</span>
<span style="font-size:12px;"> avec valeur totale</span></strong>
""", unsafe_allow_html=True)



result = top_or_down_birth(birth_load)
top, down = st.columns(2)

with top:
    st.metric("📊 Année la plus haute (total)",
              value=result["all"]["highest_year"]["year"],
              delta=result["all"]["highest_year"]["value"],
              delta_color="off")

    top_female, top_male = st.columns(2)

    with top_female:
        st.metric("♀️ Féminin",
                  value=result["female"]["highest_year"]["year"],
                  delta=result["female"]["highest_year"]["value"],
                  delta_color="off")

    with top_male:
        st.metric("♂️ Masculin",
                  value=result["male"]["highest_year"]["year"],
                  delta=result["male"]["highest_year"]["value"],
                  delta_color="off")

with down:
    st.metric("📉 Année la plus basse (total)",
              result["all"]["lowest_year"]["year"],
              delta=result["all"]["lowest_year"]["value"],
              delta_color="off")

    top_female2, top_male2 = st.columns(2)

    with top_female2:
        st.metric("♀️ Féminin",
                  result["female"]["lowest_year"]["year"],
                  delta=result["female"]["lowest_year"]["value"],
                  delta_color="off")

    with top_male2:
        st.metric("♂️ Masculin",
                  result["male"]["lowest_year"]["year"],
                  delta=result["male"]["lowest_year"]["value"],
                  delta_color="off")