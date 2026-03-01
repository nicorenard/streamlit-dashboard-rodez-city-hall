"""
Évolution démographique : naissances vs décès → tendance naturelle de croissance/déclin.
Âge au mariage par cohorte (ex. génération née dans les années 1920 → mariée en moyenne à 25 ans).
Espérance de vie moyenne par cohorte (décès − naissance).
Impact des événements historiques : guerres mondiales, baby-boom, crises sanitaires → mise en évidence des variations.
Comparaison inter-périodes : avant/après-guerre, baby-boom, crises.
"""

import plotly.express as px
import streamlit as st
import pandas as pd
import altair as alt
from src.utils import dataset_load, multiple_event_by_year, multiple_aggregate_by_year

# data
birth_load = dataset_load("liste_des_naissances.csv")
death_load = dataset_load("liste_des_deces.csv")
wedding_load = dataset_load("liste_des_mariages.csv")

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/static/rodez_logo_propre.png", width=150)
right.title("Explorations temporelles transversale")

st.write("""L'objectif de cette page est de mettre en avant les données des 3 datasets et d'analyser d'un point de 
vue historique, démographique les données. Le but est de comparer les tendances et les interactions temporelles.""")

st.divider()
st.markdown("""### 1. Volumétries annuelles""")
st.write(
    "Le but de cette analyse est permettre l'identification rapide des tendances synchrones (croissance, stagnation, chutes)"
    "ainsi que les ruptures (pics, creux, croisements)"
)


radar_df = multiple_event_by_year(birth_load, death_load, wedding_load)
years_choices = radar_df.index.tolist()
selected_years = st.multiselect(
    "Sélectionnez les années à comparer :", options=years_choices, default=[years_choices[50]]
)

# Préparation des données pour Plotly radar
if selected_years:
    radar_data = (
        radar_df.loc[selected_years]
        .reset_index()
        .melt(id_vars="annee", var_name="Événement", value_name="Valeur")
    )
    radar_data.rename(columns={"annee": "Années"}, inplace=True)

    # Radar chart
    fig = px.line_polar(
        radar_data, r="Valeur", theta="Événement", color="Années", line_close=True, markers=True
    )
    fig.update_traces(fill="toself")  # for polygons
    st.plotly_chart(fig, use_container_width=True)


st.divider()
st.markdown("### 2. Indicateurs dynamiques")
st.markdown(
    "Les indicateurs combinent naissances, mariages et décès pour analyser "
    "les dynamiques démographiques et sociales au fil du temps."
)

# --- Préparation timeline ---
timeline = multiple_aggregate_by_year(
    birth_load,
    death_load,
    wedding_load
)

timeline = timeline.sort_values("annee").copy()

# colonne affichage pour éviter 1,950
timeline["annee_label"] = timeline["annee"].astype(str)

# --- Slider temporel ---
year_min = int(timeline["annee"].min())
year_max = int(timeline["annee"].max())

year_range = st.slider(
    "Période d'analyse",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# filtrage sécurisé
filtered = timeline[
    (timeline["annee"] >= year_range[0]) &
    (timeline["annee"] <= year_range[1])
].copy()

# --- Choix indicateur ---
indicator = st.radio(
    "Indicateur",
    [
        "Solde naturel (Naissances - Décès)",
        "Mariages / Naissances",
        "Décès / Mariages"
    ],
    horizontal=True
)

if indicator == "Solde naturel (Naissances - Décès)":
    filtered["indicateur"] = filtered["Naissances"] - filtered["Décès"]
    label = "Solde naturel"

elif indicator == "Mariages / Naissances":
    filtered["indicateur"] = (
        filtered["Mariages"] / filtered["Naissances"].replace(0, None)
    )
    label = "Mariages / Naissances"

else:
    filtered["indicateur"] = (
        filtered["Décès"] / filtered["Mariages"].replace(0, None)
    )
    label = "Décès / Mariages"

# --- Metrics ---
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Moyenne", round(filtered["indicateur"].mean(), 2))

with c2:
    st.metric("Maximum", round(filtered["indicateur"].max(), 2))

with c3:
    st.metric("Minimum", round(filtered["indicateur"].min(), 2))

# --- Graphique ---
st.line_chart(
    filtered,
    x="annee_label",
    y="indicateur",
    y_label=label,
    x_label="Année"
)
st.markdown("### Comprendre le graphique")

if indicator == "Solde naturel (Naissances - Décès)":
    st.write(
        "Un solde positif indique une croissance naturelle de la population, "
        "un solde négatif un vieillissement ou une période de crise."
    )

elif indicator == "Mariages / Naissances":
    st.write(
        "Ce ratio reflète indirectement le contexte social et les comportements familiaux.\n"
        "Les analyses possibles:  \n"
        "- Ratio élevé = Mariages plus fréquents, Natalité plus tardive ou en baisse,\n"
        "- Ratio faible = Forte natalité avec de structures familiales plus traditionnelles ou plus jeunes"
    )

else:
    st.write(
        "L'Indicateur de stress démographique.\n "
        "Ce ratio est très sensible aux crises, un ratio élevé peut signaler une période de tension démographique ou sociale.\n"
        "Les analyses possibles:  \n"
        "- Ratio élevé : Moins de mariages, plus de décès, causes => Climat anxiogène (guerre, épidémie, crise économique)\n"
        "- Ratio faible : Société stable => Projection dans l’avenir (mariages nombreux)"
    )



st.divider()
st.markdown("""### 3. Décalages générationnels""")
st.write(
    "Le but de cette analyse est d'observer les cycles démographiques en alignant les naissances, "
    "mariages et décès d'une même génération."
)

timeline = multiple_aggregate_by_year(
    birth_load,
    death_load,
    wedding_load
).sort_values("annee")

timeline["annee"] = pd.to_numeric(timeline["annee"])
timeline = timeline.set_index("annee")
st.subheader("Paramètres d'analyse")

col1, col2, col3 = st.columns(3)

with col1:
    year_range = st.slider(
        "Période",
        int(timeline.index.min()),
        int(timeline.index.max()),
        (int(timeline.index.min()), int(timeline.index.max()))
    )

with col2:
    marriage_shift = st.slider(
        "Décalage naissance → mariage",
        15, 50, 30
    )

with col3:
    death_shift = st.slider(
        "Décalage naissance → décès",
        50, 110, 80
    )

mode = st.radio(
    "Mode d'affichage",
    ["Courbes originales", "Courbes alignées générationnellement"],
    horizontal=True
)

filtered = timeline.loc[year_range[0]:year_range[1]].copy()

if mode == "Courbes alignées générationnellement":
    filtered["Mariages"] = filtered["Mariages"].shift(-marriage_shift)
    filtered["Décès"] = filtered["Décès"].shift(-death_shift)

st.divider()
st.subheader("Événements alignés par génération")

filtered = filtered.copy()

# index numérique pour les calculs
filtered.index = filtered.index.astype(int)

# colonne texte pour l'affichage
filtered["annee_label"] = filtered.index.astype(str)

st.line_chart(
    filtered.set_index("annee_label")[["Naissances", "Mariages", "Décès"]],
    x_label="Année",
    y_label="Nombre d'événements",
    use_container_width=True
)

st.caption("Repères historiques démographiques")

periods = [
    ("Première Guerre mondiale", 1914, 1918),
    ("Grippe espagnole", 1918, 1919),
    ("Seconde Guerre mondiale", 1939, 1945),
    ("Baby boom", 1945, 1975),
]

for name, start, end in periods:
    if start >= year_range[0] and end <= year_range[1]:
        st.markdown(f"• {name} : {start}–{end}")

st.divider()
st.subheader("Indicateurs générationnels")

def safe_corr(a, b):
    aligned = pd.concat([a, b], axis=1).dropna()
    if len(aligned) < 2:
        return None
    return aligned.iloc[:, 0].corr(aligned.iloc[:, 1])

corr_birth_marriage = safe_corr(
    filtered["Naissances"],
    filtered["Mariages"]
)

corr_birth_death = safe_corr(
    filtered["Naissances"],
    filtered["Décès"]
)

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Corrélation Naissances → Mariages",
        None if corr_birth_marriage is None else round(corr_birth_marriage, 2)
    )

with c2:
    st.metric(
        "Corrélation Naissances → Décès",
        None if corr_birth_death is None else round(corr_birth_death, 2)
    )


st.divider()
st.markdown("""### 4. Focus historique""")
# selecteur de periode (menu deroulant, 14-18, 39-45, 68-75)
# graphique qui evolue et montre les valeurs de mariages, deces etc....

chart_data = chart_data[chart_data["annee"] >= 1981]
# ==============================
# 5. Domaine X = années réelles
# ==============================
year_min = int(chart_data["annee"].min())
year_max = int(chart_data["annee"].max())

# ==============================
# 6. Périodes historiques filtrées
# ==============================
periods = pd.DataFrame([
    {"start": 1914, "end": 1918, "label": "WW1"},
    {"start": 1918, "end": 1919, "label": "Grippe espagnole"},
    {"start": 1939, "end": 1945, "label": "WW2"},
    {"start": 1945, "end": 1975, "label": "Baby boom"},
    {"start": 2020, "end": 2022, "label": "COVID"},
])

periods = periods[
    (periods["end"] >= year_min) &
    (periods["start"] <= year_max)
]

# ==============================
# 7. Construction graphique
# ==============================
base = alt.Chart(chart_data).encode(
    x=alt.X(
        "annee:Q",
        title="Année",
        scale=alt.Scale(domain=[year_min, year_max], nice=False),
        axis=alt.Axis(format="d")   # indice brut
    )
)

birth_line = base.mark_line(size=2).encode(
    y="Naissances:Q"
)

marriage_line = base.mark_line(size=2).encode(
    y="Mariages_alignés:Q"
)

death_line = base.mark_line(size=2).encode(
    y="Décès_alignés:Q"
)

bands = alt.Chart(periods).mark_rect(opacity=0.15).encode(
    x="start:Q",
    x2="end:Q"
)

labels = alt.Chart(periods).mark_text(dy=-5).encode(
    x="start:Q",
    text="label:N"
)

chart = bands + birth_line + marriage_line + death_line + labels

st.altair_chart(chart, use_container_width=True)

# ==============================
# 8. Indicateurs générationnels
# ==============================
st.markdown("#### Lecture générationnelle")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Naissances moyennes", int(chart_data["Naissances"].mean()))

with col2:
    st.metric("Mariages alignés moyens", int(chart_data["Mariages_alignés"].mean()))

with col3:
    st.metric("Décès alignés moyens", int(chart_data["Décès_alignés"].mean()))

# ==============================
# 9. Interprétation automatique
# ==============================
birth_peak = int(chart_data.loc[chart_data["Naissances"].idxmax(), "annee"])

st.info(
    f"La génération née autour de {birth_peak} montre "
    f"un impact générationnel visible environ "
    f"{marriage_shift} ans plus tard sur les mariages "
    f"et {death_shift} ans plus tard sur la mortalité."
)