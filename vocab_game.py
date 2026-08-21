import time
import random
import streamlit as st


# =========================================================
# ⚙️ ตั้งค่าหน้าเว็บ
# =========================================================

st.set_page_config(
    page_title="เกมเติมศัพท์จับเวลา",
    page_icon="⏱️",
    layout="centered"
)

st.title("⏱️ เกมเติมศัพท์จับเวลา")
st.write("เติมคำศัพท์ภาษาอังกฤษให้ถูกต้องภายใน 30 วินาที 🎯")


# =========================================================
# 📚 คลังคำศัพท์
# =========================================================

VOCABULARY = {
    "Fruits": [
        ("🍎", "Apple"),
        ("🍏", "Green Apple"),
        ("🍌", "Banana"),
        ("🍊", "Orange"),
        ("🍋", "Lemon"),
        ("🍇", "Grapes"),
        ("🍓", "Strawberry"),
        ("🫐", "Blueberry"),
        ("🍉", "Watermelon"),
        ("🍍", "Pineapple"),
        ("🥭", "Mango"),
        ("🍑", "Peach"),
        ("🍒", "Cherry"),
        ("🥥", "Coconut"),
        ("🥑", "Avocado"),
    ],

    "Objects & Supplies": [
        ("✏️", "Pencil"),
        ("🖊️", "Pen"),
        ("📏", "Ruler"),
        ("📚", "Books"),
        ("✂️", "Scissors"),
        ("🎒", "Backpack"),
        ("👓", "Glasses"),
        ("🔑", "Key"),
        ("⏰", "Alarm Clock"),
        ("🚗", "Car"),
        ("🎈", "Balloon"),
        ("🎁", "Gift"),
        ("📱", "Phone"),
        ("💻", "Laptop"),
        ("💡", "Light Bulb"),
    ]
}


# =========================================================
# 🔤 รวมคำศัพท์ทั้งหมด
# =========================================================

ALL_WORDS = []

for category, words in VOCABULARY.items():

    for emoji, word in words:

        ALL_WORDS.append({
            "category": category,
            "emoji": emoji,
            "word": word
        })


# =========================================================
# 🧠 ฟังก์ชันสร้างคำที่มีช่องว่าง
# =========================================================

def create_question(word):

    letters = list(word)

    # ตำแหน่งที่เป็นตัวอักษร
    positions = [
        i for i, char in enumerate(letters)
        if char.isalpha()
    ]

    # ถ้าคำสั้นมาก
    if len(positions) <= 2:
        missing_count = 1

    else:
        missing_count = min(
            2,
            max(1, len(positions) // 3)
        )

    # สุ่มตำแหน่งที่จะหาย
    missing_positions = random.sample(
        positions,
        missing_count
    )

    for position in missing_positions:
        letters[position] = "_"

    # ใส่ช่องว่างระหว่างตัวอักษร
    return " ".join(letters)


# =========================================================
# 🔄 สร้าง Session State
# =========================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_ended" not in st.session_state:
    st.session_state.game_ended = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "masked_questions" not in st.session_state:
    st.session_state.masked_questions = []


# =========================================================
# 🎮 ฟังก์ชันเริ่มเกม
# =========================================================

def start_game():

    # สุ่มคำศัพท์ 4 ข้อ
    selected_words = random.sample(
        ALL_WORDS,
        4
    )

    # บันทึกโจทย์ไว้ใน session_state
    st.session_state.questions = selected_words

    # สร้างโจทย์แบบเติมคำ
    st.session_state.masked_questions = [
        create_question(item["word"])
        for item in selected_words
    ]

    # เตรียมคำตอบ
    st.session_state.answers = [
        ""
        for _ in selected_words
    ]

    # เริ่มจับเวลา
    st.session_state.start_time = time.time()

    # สถานะเกม
    st.session_state.game_started = True
    st.session_state.game_ended = False


# =========================================================
# 🔄 ฟังก์ชันเริ่มเกมใหม่
# =========================================================

def reset_game():

    start_game()


# =========================================================
# 📊 ฟังก์ชันตรวจคำตอบ
# =========================================================

def calculate_score():

    score = 0

    for index, question in enumerate(
        st.session_state.questions
    ):

        correct_answer = (
            question["word"]
            .strip()
            .lower()
        )

        user_answer = (
            st.session_state.answers[index]
            .strip()
            .lower()
        )

        if user_answer == correct_answer:
            score += 1

    return score


# =========================================================
# 📊 Dialog แสดงผลคะแนน
# =========================================================

@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog():

    score = calculate_score()

    total = len(
        st.session_state.questions
    )

    st.balloons()

    st.subheader(
        f"🏆 คะแนน {score} / {total}"
    )

    st.divider()

    # แสดงผลแต่ละข้อ
    for index, question in enumerate(
        st.session_state.questions
    ):

        user_answer = (
            st.session_state.answers[index]
            .strip()
        )

        correct_answer = question["word"]

        if user_answer.lower() == correct_answer.lower():

            st.success(
                f"ข้อ {index + 1} ✅ ถูกต้อง — {correct_answer}"
            )

        else:

            if user_answer == "":
                display_answer = "ไม่ได้ตอบ"
            else:
                display_answer = user_answer

            st.error(
                f"ข้อ {index + 1} ❌ "
                f"คุณตอบ: {display_answer} "
                f"| คำตอบที่ถูก: {correct_answer}"
            )

    st.divider()

    # สรุปผล
    if score == total:

        st.success(
            "🎉 You Win! เก่งมาก ถูกทุกข้อเลย!"
        )

    elif score >= 2:

        st.warning(
            "👏 Almost there! ลองอีกครั้งเพื่อทำคะแนนให้เต็ม!"
        )

    else:

        st.error(
            "💀 You Lose! ลองใหม่อีกครั้งนะ"
        )


# =========================================================
# 🎮 ปุ่มเริ่มเกม
# =========================================================

if not st.session_state.game_started:

    st.info(
        "กดปุ่มด้านล่างเพื่อเริ่มเกม "
        "ระบบจะสุ่มคำศัพท์ให้ 4 ข้อ"
    )

    if st.button(
        "🎮 เริ่มเล่นเกม",
        use_container_width=True
    ):

        start_game()

        st.rerun()


# =========================================================
# ⏱️ ระบบจับเวลา
# =========================================================

if (
    st.session_state.game_started
    and not st.session_state.game_ended
):

    elapsed_time = (
        time.time()
        - st.session_state.start_time
    )

    time_left = max(
        0,
        30 - int(elapsed_time)
    )

    # แสดงเวลาที่เหลือ
    st.error(
        f"⏳ เหลือเวลา: {time_left} วินาที"
    )

    # Progress Bar
    progress = max(
        0,
        min(
            1,
            time_left / 30
        )
    )

    st.progress(progress)

    # หมดเวลา
    if time_left <= 0:

        st.session_state.game_ended = True

        st.rerun()


# =========================================================
# 📝 แสดงโจทย์
# =========================================================

if (
    st.session_state.game_started
    and not st.session_state.game_ended
):

    st.divider()

    st.subheader("📝 เติมคำศัพท์ให้ถูกต้อง")

    for index, question in enumerate(
        st.session_state.questions
    ):

        st.markdown(
            f"### ข้อ {index + 1}"
        )

        # Emoji
        st.markdown(
            f"<div style='font-size:55px; text-align:center;'>"
            f"{question['emoji']}"
            f"</div>",
            unsafe_allow_html=True
        )

        # ประเภทคำศัพท์
        st.caption(
            f"หมวด: {question['category']}"
        )

        # คำที่มีช่องว่าง
        st.markdown(
            f"### `{st.session_state.masked_questions[index]}`"
        )

        # ช่องตอบ
        answer = st.text_input(
            f"✏️ คำตอบข้อ {index + 1}",
            key=f"answer_{index}"
        )

        # บันทึกคำตอบ
        st.session_state.answers[index] = answer

        st.divider()


# =========================================================
# 📥 ปุ่มส่งคำตอบ
# =========================================================

if (
    st.session_state.game_started
    and not st.session_state.game_ended
):

    if st.button(
        "📥 ส่งคำตอบ",
        use_container_width=True
    ):

        st.session_state.game_ended = True

        st.rerun()


# =========================================================
# 🔄 ปุ่มเล่นใหม่
# =========================================================

if st.session_state.game_ended:

    if st.button(
        "🔄 เล่นเกมใหม่",
        use_container_width=True
    ):

        reset_game()

        st.rerun()

    # แสดงผล
    show_result_dialog()


# =========================================================
# ⏱️ ทำให้ Timer ทำงานต่อเนื่อง
# =========================================================

if (
    st.session_state.game_started
    and not st.session_state.game_ended
):

    time.sleep(1)

    st.rerun()

st.divider()
st.write("นางสาว ทับทิม คำป้อ เลขที่ 43 ม.4/7")
