import html
import random
import requests # for making API requests
import streamlit as st

# --- Page Config --- #

st.set_page_config(page_title="Trivia Woohoo", layout="centered")

# --- API --- #

# triv_categ_url = 
# triv_ques_url =

# --- Q dictionary --- #

Questions = [
    {
        "question": "How many continents are there in the world?",
        "correct_answer": "7",
        "incorrect_answers": ["6", "8", "9"],
    },
    {
        "question": "",
        "correct_answer": "",
        "incorrect_answers": [],
    },
    {
        "question": "",
        "correct_answer": "",
        "incorrect_answers": [],
    },
]

# --- Session STate --- #

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = ""

# --- Functions --- #

def start_game() -> None:
    """Fetch questions and start the game."""
    st.session_state.game_started = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answer_submitted = True
    st.session_state.selected_answer = ""
    # st.rerun()

    st.subheader("Begin!")
    current_questions = Questions[st.session_state.question_index]

    if st.session_state.question_index < len(current_questions):
        st.write(
            f"Question # {st.session_state.question_index + 1} of {len(current_questions)}"
        )
        st.write(
            f"Score: {st.session_state.score}"
        )
        st.subheader(current_questions["question"])
    # chosen = next(
    #     (
    #         category
    #         for category in st.session_state.categories
    #         if category["name"] == st.session_state.category_choice
    #     ),
    #     None,
    # )

    # if chosen is None:
    #     st.error("Invalid category selected")

# --- UI --- #

if not st.session_state.game_started:
    st.title("🌎 Geography Trivia Game")
    st.write("Answer 6 or 7 questions correctly and you get bragging rights")
    st.button("Let's Go!", on_click=start_game)


