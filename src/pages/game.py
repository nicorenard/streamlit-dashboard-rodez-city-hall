import random
import streamlit as st
from src.utils import find_better_name_game, find_name_query, dataset_load, questions, calculate_score, PERIODES, \
    stats_period
from src.utils.mystery_game import generate_text

# header
left, right = st.columns([1, 4])
logo = left.image(image="src/static/rodez_logo_propre.png", width=150)
right.title("Exploration ludique des jeux de données!")

st.write(""" L'objectif de cette page est de 'jouer' avec les données et de voir d'autres possibilités d'exploitation sur des dataset même léger.""")
st.divider()
# data
birth_load = dataset_load("liste_des_naissances.csv")

# Naissance

st.write("### 1.  💪 Versus 💪!")
st.info("Objectif : Découvrez quel prénom a été le plus populaire sur la période 1981-2016 ! 😎")

left, right = st.columns(2)

with left:
    name1 = st.text_input("Inscrire un 1er prénom  👇", key="prenom1")
with right:
    name2 = st.text_input("Inscrire un 2ème prénom 👇", key="prenom2")

if name1 and name2:
    result = find_better_name_game(birth_load, name1, name2)
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


st.divider()
st.write("### 2.  🤔 Quiz Général sur les données du site !")
st.info("Objectif : Découvrez votre score en répondant à ces 6 questions ! 🤓")

if st.button(label="🔄 Relancer le quiz"):
    st.session_state.clear()
    st.rerun()

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

def next_question():
    selected = st.session_state[f"answer_{st.session_state.current_question}"]
    st.session_state.user_answers.append(selected)
    st.session_state.current_question += 1

if st.session_state.current_question < len(questions):
    q = questions[st.session_state.current_question]
    st.write(f"**Question {st.session_state.current_question + 1}**: {q['question']}")
    st.radio("Choisissez une réponse :", q["options"], key=f"answer_{st.session_state.current_question}")
    st.button("Suivant", on_click=next_question)
else:
    # Quiz terminé : calculer le score
    score, results = calculate_score(st.session_state.user_answers)
    st.write("### Résultat du quiz :")
    for i, r in enumerate(results):
        if r["is_correct"]:
            st.success(f"Question {i+1}: ✅ Correct = {r['user_answer']}")
        else:
            st.error(f"Question {i+1}: ❌ Incorrect = {r['user_answer']} - La bonne réponse était : {r['correct_answer']}")
    st.write(f"**Votre score final : {score}/{len(questions)}**")



st.divider()
st.write("## 3. 🎭 Profil mystère !")
st.info(
    "Objectif : Trouver la période ou cette personne 'fictive' aurait pu naitre ! 🤗"
)

if st.button("Rejouer !"):
    del st.session_state.period
    del st.session_state.stats
    del st.session_state.text
    st.rerun()


if "period" not in st.session_state:
    st.session_state.period = random.choice(list(PERIODES.keys()))
    starting_date, final_date = PERIODES[st.session_state.period]
    st.session_state.stats = stats_period(starting_date, final_date)
    st.session_state.text = generate_text(st.session_state.stats)


st.markdown(st.session_state.text, unsafe_allow_html=True)

response = st.radio(
    "À quelle période cette personne aurait pu naître ?",
    list(PERIODES.keys())
)

if st.button("Valider"):
    if response == st.session_state.period:
        st.success("Bonne réponse !")
    else:
        st.error(
            f"Mauvaise réponse. La bonne période était **{st.session_state.period}**."
        )
