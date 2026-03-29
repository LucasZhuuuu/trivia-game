import html
import random
import requests # for making API requests
import streamlit as st

# --- Page Config --- #

st.set_page_config(page_title="Trivia Woohoo", layout="centered")

# --- API --- #

TRIVIA_API_URL = "https://opentdb.com/api.php"
DIFFICULTY_OPTIONS = ["easy", "medium", "hard"]

# --------------------------------------------------
# Helper function: get questions from API
# --------------------------------------------------
def get_questions(difficulty: str, amount: int = 10) -> list[dict]:
    """Fetch multiple-choice questions from The Trivia API."""

    params = {
        "amount": amount,
        "category" : "22",
        "difficulty" : difficulty,
        "type" : "multiple",
    }




    response = requests.get(TRIVIA_API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    questions = []

    for item in data.get("results", []):

        # if str(item.get("category", "")).lower() != "geography":
        #     continue

        question_text = html.unescape(item.get("question", ""))
        correct = html.unescape(item.get("correct_answer", ""))
        incorrect = [html.unescape(ans) for ans in item.get("incorrect_answers", [])]

        # Pad incorrect answers to 3 if less than 3
        if not correct or not question_text or not len(incorrect) != 3:
            incorrect.append("Option X")  # placeholder text

        options = incorrect + [correct]  # ensure 3 incorrect + 1 correct
        random.shuffle(options)

        questions.append(
            {
                "question": question_text,
                "correct_answer": correct,
                "options": options,
                "difficulty": str(item.get("difficulty", difficulty)).title(),
            }
        )

    return questions

# --- Session STate --- #

if "page" not in st.session_state:
    st.session_state.page = "menu"

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = ""

if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = "medium"


# --- Functions --- #

def start_game() -> None:
    """Fetch questions and start the game."""
    try:
        questions = get_questions(
            difficulty=st.session_state.selected_difficulty,
            amount=10
        )
    except requests.RequestException:
        st.error("Could not load questions from the Trivia API.")
        return
    if not questions:
        st.error("No questions were found try another difficulty.")
        return
    
    st.session_state.questions = questions
    st.session_state.current_q = 0
    st.session_state.game_started = True
    st.session_state.answered =False
    st.session_state.score = 0
    st.session_state.answer_submitted = None
    st.session_state.selected_answer = None
    st.session_state.page = "game"


def submit_answer() -> None:
    """Check the current selected answer."""
    pass


def next_question() -> None:
    """Move to the next question."""
    pass


def back_to_menu() -> None:
    """Return to main menu and reset game data."""
    pass


def replay_same_settings() -> None:
    """Start a fresh game with the same category and difficulty."""
    pass


# --- UI --- #
# --------------------------------------------------
# Main menu screen
# --------------------------------------------------
if not st.session_state.game_started and st.session_state.page == "menu":
    st.title("🌎 Geography Trivia Game")
    st.write("Answer 6 or 7 questions correctly and you get bragging rights")

    chosen_difficulty = st.selectbox(
        "Choose a difficulty:", 
        DIFFICULTY_OPTIONS
    )
    st.session_state.selected_difficulty = chosen_difficulty

    st.write(f"Difficulty: **{st.session_state.selected_difficulty.title()}**")

    st.button("Let's Go!", on_click=start_game)

# --------------------------------------------------
# Game screen
# --------------------------------------------------
else:
    st.subheader("Begin!")
    total_questions = len(st.session_state.questions)
    current_index = st.session_state.current_q

    if current_index < total_questions:
        current_question = st.session_state.questions[current_index]
        st.write(
            f"Question # {st.session_state.current_q + 1} of {total_questions}"
        )
        st.write(
            f"Score: {st.session_state.score}"
        )

        st.progress((current_index + 1) / total_questions)
        st.markdown(f" ### {current_question["question"]}")

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
    # pass
# --------------------------------------------------
# Game over screen
# --------------------------------------------------
