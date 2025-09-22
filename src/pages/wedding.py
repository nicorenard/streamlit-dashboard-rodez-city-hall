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

from src.utils import (
    dataset_load,
    aggregate_by_year,
    top_year_and_down_year,
    wedding_by_month_chart,
    weeding_by_season_month,
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
        title=" Année la plus haute",
        content=df["highest_year"]["year"],
        description=f"{df['highest_year']['value']} marriages",
    )


with down:
    ui.metric_card(
        title=" Année la plus basse",
        content=df["lowest_year"]["year"],
        description=f"{df['lowest_year']['value']} décès",
    )


# nombre de mariage total
st.markdown("""#### b. Timeline""")
df2 = aggregate_by_year(wedding_set)
with st.container():
    st.bar_chart(df2, x_label="Années", y_label="Nombre de mariages total")

st.divider()
st.markdown("""### 2. Répartitions temporelles""")
# section2 : repartition temporelle
# histogramme par mois
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
# heatmap des saisons
st.markdown("""#### b.Heatmap des mariages par saison et par année""")
df_season = weeding_by_season_month(wedding_set)

fig, axis = plt.subplots(figsize=(10, 5))
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
st.pyplot(fig)


st.divider()
st.markdown("""### 3. Dimensions démographique""")
st.write("""On notera ici que les données étant pauvres, elle représente environ ~10% du dataset au complet et donc 
l'analyse ne peut être étendu sur la pèriode complete.""")

# genre epoux/epouse
# profession dans un tables ou un nuage de mot ?
st.divider()
st.markdown("""### 4. Quelques indicateurs optionnels""")
st.write(
    """On notera ici que les données étant pauvres, elle représente aussi environ ~10% du dataset au complet."""
)

# age moyen au mariage ( homme versus femme)
# histogramme des ages H/F
# distribution des écarts d'age entre conjoints
