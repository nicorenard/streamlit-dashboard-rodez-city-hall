import streamlit as st
from src.config import VERSION


def render_footer():
    st.html(f"""
    <div class="footer">
        <div class="footer-section">
            <h4>Crédits</h4>
            <p>Auteur : Nicolas Renard</p>
            <p>Version application: {VERSION}</a></p>
            <p><a href="https://github.com/nicorenard/streamlit-dashboard-rodez-city-hall" target="_blank">Github</a></p>
        </div>
        <div class="footer-section">
            <h4>Informations</h4>
            <p><a href="https://www.data.gouv.fr/datasets/population-mariages-deces-naissances-1/" target="_blank">Source datasets</a></p>
            <p>Dernière mise à jour : 17-10-2016</p>
        </div>
        <div class="footer-section">
            <h4></h4>
            <p>/p>
            <p></p>
            <p></p>
        </div>
        <div class="footer-divider"></div>
        <div class="footer-bottom">
            © 2025 - Tous droits réservés - Nicolas Renard
        </div>
    </div>
    """)
