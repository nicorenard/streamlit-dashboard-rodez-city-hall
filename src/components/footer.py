import streamlit as st
from src.config import VERSION


def render_footer():
    st.markdown("""---""")
    st.html(f"""
    <div class="footer-bottom">
        <p>Auteur : Nicolas Renard | Version application: {VERSION} | <a href="https://github.com/nicorenard/streamlit-dashboard-rodez-city-hall" target="_blank">Source projet - Github</a></p>
        <p><a href="https://www.data.gouv.fr/datasets/population-mariages-deces-naissances-1/" target="_blank">Source des datasets</a> | Dernière mise à jour : 17-10-2016</p>
    </div>
    <div class="footer-bottom">
        © 2025 - Tous droits réservés - Nicolas Renard
    </div>
    """)
