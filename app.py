import streamlit as st


# navigation

home = st.Page("src/pages/home.py", title="Acceuil", icon=":material/home:", default=True)
birth = st.Page("src/pages/birth.py", title="Les Naissances", icon=":material/child_care:")
death = st.Page("src/pages/death.py", title="Les Déces", icon=":material/deceased:")
wedding = st.Page("src/pages/wedding.py", title="Les Mariages", icon=":material/partner_heart:")
exploration = st.Page(
    "src/pages/temporal_exploration.py",
    title="Exploration générationnelle",
    icon=":material/data_exploration:",
)
game = st.Page("src/pages/game.py", title="Let's play !", icon=":material/joystick:")
st.set_page_config(layout="wide")

pg = st.navigation(pages=[home, birth, death, wedding, exploration, game])
pg.run()
