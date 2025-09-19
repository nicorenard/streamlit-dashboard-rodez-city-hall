"""
Configuration générale
    Définir le titre global de ton app (ex. "Explorateur démographique de Rodez").
    Eventuellement configurer le layout (large ou centré).
Page d’introduction
    Présenter ton projet en quelques lignes (but, description rapide des datasets).
    Ajouter un lien vers la documentation officielle des données (source mairie).
Infos pratiques
    Indiquer que la navigation se fait via la barre latérale (les autres pages sont dans pages/).
    Mettre éventuellement un logo, une image d’illustration, ou un petit encart "À propos".

"""

import streamlit as st



# navigatioon
home = st.Page("src/pages/home.py", title="Acceuil", icon=":material/home:", default=True)
birth = st.Page("src/pages/birth.py", title="Les Naissances", icon=":material/child_care:")
death = st.Page("src/pages/death.py", title="Les Déces", icon=":material/deceased:")
wedding = st.Page("src/pages/wedding.py", title="Les Mariages", icon=":material/partner_heart:")
exploration = st.Page ("src/pages/temporal_exploration.py", title="Exploration générationnelle", icon=":material/data_exploration:")
ad_analysis = st.Page("src/pages/advanced_analysis.py", title="Analyses Avancées", icon=":material/search_insights:")
game = st.Page("src/pages/game.py", title="Let's play !", icon=":material/joystick:")

pg = st.navigation(pages=[home,birth,death,wedding,exploration,ad_analysis,game], position="top")
pg.run()
