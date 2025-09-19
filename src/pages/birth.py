import streamlit as st
import plotly.graph_objects as go
import streamlit_shadcn_ui as ui

from src.utils import (
    dataset_load,
    aggregate_by_gender_and_by_year,
    top_or_down_birth,
    top_name_by_year_and_gender,
    aggregate_by_year,
    top_name_by_genre,
    find_name_query,
    name_vs_name,
)


# data
birth_load = dataset_load("liste_des_naissances.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/assets/rodez_logo_propre.png", width=150)
right.title("Exploration des naissances")

st.write(
    "Le dataset des naissances est plutôt léger en terme de richesse des données.\n\n"
    "On notera cependant les élements suivant qui permettent : \n\n"
    "1) D'explorer temporellement les naissances sur les années, d'avoir un focus sur certaines périodes traversées, quelques statistiques intéressantes\n"
    "2) D'effectuer une analyse des prénoms sous différents format ou comparaison \n"
    "3) D'avoir une focus sur certains indicateurs"
)

st.divider()

st.markdown("""### 1. Timelines""")

st.markdown("""#### a. Vue générale""")

df = aggregate_by_year(birth_load)
with st.container():
    st.bar_chart(df, x_label="Années", y_label="Nombre de naissances total")

st.markdown("""#### b. Vue par genres""")
dfg = aggregate_by_gender_and_by_year(birth_load).reset_index()

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
    "#### Note\n"
    "La chute de natalité pour les année 1982-1983 fait partie d'un ensemble de facteurs économiques, sociale "
    "et culturel dont une partie des réponses peut se retrouver comme expliqué "
    "dans cet article du Monde : https://www.lemonde.fr/archives/article/1983/10/05/la-natalite-continue-de-baisser-en"
    "-france-50-000-naissances-de-moins-en-1983_3077597_1819218.html"
)


st.divider()
st.markdown("""### 2. Focus sur les prénoms """)

st.write("#### a. Top prénoms par année et par genre")
result = top_name_by_year_and_gender(birth_load)
styled = result.style.set_table_styles(
    [
        {"selector": "th", "props": [("font-size", "16px"), ("text-align", "center")]},
        {"selector": "td", "props": [("font-size", "16px"), ("text-align", "center")]},
    ]
).map(lambda x: "background-color: #e6f2ff" if x else "")
st.dataframe(styled, use_container_width=True)


st.write("#### b. Tendance et occurrence d'un prénom")

name_input = st.text_input(label="Inscrire un prénom 👇")
if name_input:
    result = find_name_query(birth_load, name_input)
    st.metric("Nombre total d'occurrences détectées", result["total_occurence"])
    df_linechart = result["occurence_by_time"].reset_index()
    df_linechart.columns = ["annee", "naissances"]
    st.line_chart(
        df_linechart,
        x="annee",
        y="naissances",
        x_label="Années",
        y_label="Nombre de naissances",
    )


st.write("#### c. Versus !")
st.write("Petit comparatif rapide d'occurrence sur la période entre 2 prénoms")
left, right = st.columns(2)

with left:
    name1 = st.text_input("1er prénom ?  👇", key="prenom1")
with right:
    name2 = st.text_input("2ème prénom ? 👇", key="prenom2")

if name1 and name2:
    result = name_vs_name(birth_load, name1, name2)

    left.metric(name1, result[name1])
    right.metric(name2, result[name2])

    if result[name1] == result[name2]:
        st.success(f"{result['winner']}")
    else:
        st.balloons()
        st.success(f"🏆 Et le gagnant est : {result['winner']}")


st.divider()
st.markdown("""### 3. Quelques indicateurs de records""")

st.markdown("""#### a. Records des prénoms""")

name = top_name_by_genre(dataset=birth_load)
boy, girl = st.columns(2)

with boy:
    ui.metric_card(title="👨 Prénom masculin le plus fréquent", content=name["male"])

with girl:
    ui.metric_card(title="👩 Prénom féminin le plus fréquent", content=name["female"])


# record de naissances, naissances la plus basse
st.markdown("""#### b. Records des Naissances""")

result = top_or_down_birth(birth_load)
top, down = st.columns(2)

with top:
    ui.metric_card(
        title="📊 Année la plus haute (total)",
        content=result["all"]["highest_year"]["year"],
        description=f"{result['all']['highest_year']['value']} naissances",
    )

    top_female, top_male = st.columns(2)

    with top_female:
        ui.metric_card(
            title="♀️ Féminin",
            content=result["female"]["highest_year"]["year"],
            description=f"{result['female']['highest_year']['value']} naissances",
        )

    with top_male:
        ui.metric_card(
            title="♂️ Masculin",
            content=result["male"]["highest_year"]["year"],
            description=f"{result['male']['highest_year']['value']} naissances",
        )

with down:
    ui.metric_card(
        title="📉 Année la plus basse (total)",
        content=result["all"]["lowest_year"]["year"],
        description=f"{result['all']['lowest_year']['value']} naissances",
    )

    top_female2, top_male2 = st.columns(2)

    with top_female2:
        ui.metric_card(
            title="♀️ Féminin",
            content=result["female"]["lowest_year"]["year"],
            description=f"{result['female']['lowest_year']['value']} naissances",
        )

    with top_male2:
        ui.metric_card(
            title="♂️ Masculin",
            content=result["male"]["lowest_year"]["year"],
            description=f"{result['male']['lowest_year']['value']} naissances",
        )
