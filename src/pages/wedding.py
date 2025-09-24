"""
Nombre de mariages par année/mois.
Mariages par saison (printemps/été/automne/hiver).
Âge moyen au mariage (par sexe, par décennie).
Professions les plus fréquentes au mariage (nuage ou histogramme).
"""

import streamlit as st
import altair as alt
import streamlit_shadcn_ui as ui
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from src.utils import (
    dataset_load,
    aggregate_by_year,
    top_year_and_down_year,
    wedding_by_month_chart,
    wedding_by_season_month,
    wedding_type_gender,
    wordcloud_jobs,
    average_wedding_age,
)

# data
wedding_set = dataset_load("liste_des_mariages.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/assets/rodez_logo_propre.png", width=150)
right.title("Statistique et exploration des mariages")

st.write("""Le dataset des mariages propose des données plutôt parcellaire parfois ( de l'ordre ~ 10%) mais qui mérite 
que l'on si interesse.""")

st.divider()
st.markdown("""### 1. Timelines et indicateurs""")

st.markdown("""#### a. Indicateurs clés""")
df = top_year_and_down_year(wedding_set)
top, down = st.columns(2)

with top:
    ui.metric_card(
        title=" 💐 Année la plus haute",
        content=df["highest_year"]["year"],
        description=f"{df['highest_year']['value']} marriages",
    )


with down:
    ui.metric_card(
        title="🤍Année la plus basse",
        content=df["lowest_year"]["year"],
        description=f"{df['lowest_year']['value']} décès",
    )


st.markdown("""#### b. Timeline globale sur la période 1981-2016""")
df2 = aggregate_by_year(wedding_set)
with st.container():
    st.bar_chart(df2, x_label="Années", y_label="Nombre de mariages total")

st.divider()
st.markdown("""### 2. Répartitions temporelles""")

st.write(
    """ L'analyse de ces données est très utile quand à la saisonnalité des mariages sur la période au complet"""
)

st.markdown("""#### a. Histogramme des mariages par mois entre 1981-2016""")
df_plot = wedding_by_month_chart(wedding_set).reset_index()
df_plot.columns = ["Mois", "Mariages"]

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
        y=alt.Y("Mariages:Q", title="Nombre de mariages"),
        tooltip=["Mois", "Mariages"],
    )
)

st.altair_chart(chart, use_container_width=True)

st.markdown("""#### b.Heatmap des mariages par saison et par année""")
df_season = wedding_by_season_month(wedding_set)

figure, axis = plt.subplots(figsize=(10, 5))
sns.heatmap(
    df_season,
    annot=False,  # pas de label de chiffre
    fmt="d",  # entier pas float
    cmap="YlOrRd",
    cbar_kws={"label": "Nombre de mariages"},
    ax=axis,
)
axis.set_title("Nombre de mariages par saison et année")
axis.set_xlabel("Années")
axis.set_ylabel("Saison")
st.pyplot(figure)


st.divider()

st.info("""On notera ici que les analyses suivants portent sur des données plutôt pauvres, elles représentent 
environ ~10% du dataset et donc l'analyse ne peut être étendue sur la période complete.""")

st.markdown("""### 3. Dimensions démographique""")
st.markdown(
    """#### a. Histogramme du dénombrement des types de couples pour les années post années 2010"""
)


st.write("""##### Note
On prendra une référence proche de 2013 car à cette date, la loi du mariage pour tous à été promue et donc officiellement
, on peut relever une apparition de ce type de données concernant le mariage de couples LGBT""")

type_gender = wedding_type_gender(wedding_set)
if "inconnu" in type_gender.columns:
    type_gender = type_gender.drop(columns=["inconnu"])
df_filtered = type_gender[type_gender["annee"] >= 2013]

df_filtered = df_filtered.rename(columns={"hetero": "Couples Hétérosexuel", "lgbt": "Couples LGBT"})
fig = go.Figure()

# Couples Hétéro
fig.add_trace(
    go.Bar(
        x=df_filtered["annee"],
        y=df_filtered["Couples Hétérosexuel"],
        name="Couples Hétérosexuel",
        marker_color="blue",
    )
)
# Couples LGBT
fig.add_trace(
    go.Bar(
        x=df_filtered["annee"],
        y=df_filtered["Couples LGBT"],
        name="Couples LGBT",
        marker_color="purple",
    )
)

# Mise en forme
fig.update_layout(
    barmode="group",
    title="Évolution des types de couple depuis 2010",
    xaxis_title="Années",
    yaxis_title="Pourcentage de mariages",
    template="plotly_white",
)

st.plotly_chart(fig)
st.markdown("""#### b. Nuage de mots des professions""")

job_epoux, job_epouse = st.columns(2)

wc = wordcloud_jobs(wedding_set, "profession_epoux")
fig_wc, axis_wc = plt.subplots(figsize=(10, 5))
axis_wc.imshow(wc, interpolation="bilinear")
axis_wc.axis("off")
job_epoux.pyplot(fig_wc)
job_epoux.write("Profession des 'époux'")

wc2 = wordcloud_jobs(wedding_set, "profession_epouse")
fig_wc2, axis_wc2 = plt.subplots(figsize=(10, 5))
axis_wc2.imshow(wc2, interpolation="bilinear")
axis_wc2.axis("off")
job_epouse.pyplot(fig_wc2)
job_epouse.write("Profession des 'épouses'")

st.divider()
st.markdown("""### 4. Quelques indicateurs optionnels""")


# age moyen au mariage ( homme versus femme)
avg_age = average_wedding_age(wedding_set)
fig_avg_age = go.Figure()

# epoux
fig_avg_age.add_trace(
    go.Bar(
        x=avg_age["annee"],
        y=avg_age["age_moyen_epoux"],
        name="Age moyen des 'époux'",
        marker_color="blue",
    )
)
# epouse
fig_avg_age.add_trace(
    go.Bar(
        x=avg_age["annee"],
        y=avg_age["age_moyen_epouse"],
        name="Age moyen des 'épouses'",
        marker_color="pink",
    )
)

# Mise en forme
fig_avg_age.update_layout(
    barmode="group",
    title="Évolution de l'age moyen au mariages en fonction des époux/épouses",
    xaxis_title="Années",
    yaxis_title="Age moyen",
    template="plotly_white",
)

st.plotly_chart(fig_avg_age)
# histogramme des ages H/F
# distribution des écarts d'age entre conjoints
