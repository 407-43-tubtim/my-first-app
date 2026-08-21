import time
import random
import streamlit as st

st.set_page_config(page_title="เกมเติมศัพท์จับเวลา", page_icon="⏱️")

st.title("⏱️ เกมเติมศัพท์จับเวลา")
st.write("เติมตัวอักษรที่หายไปให้ถูกต้องภายใน 30 วินาที 🎯")


# =====================================================
# 📚 คลังคำศัพท์
# =====================================================

vocabulary = {
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
        ("💡", "Bulb"),
    ]
}


# =====================================================
# 🔀 สร้างโจทย์
# =====================================================

all_words = []

for category, words in vocabulary.items():
    for emoji, word in words:
        all_words.append({
            "category": category,
            "emoji": emoji,
            "word": word
        })


def make_question(word):
    """
    สุ่มตำแหน่งตัวอักษรที่จะหายไป
    """
    letters = list(word)

    # เลือกเฉพาะตัวอักษรภาษาอังกฤษ
    positions = [
        i for i, char in enumerate(letters)
        if char.isalpha()
    ]

    if len(positions) < 2:
        return word

    # หาย 1-2 ตัว
    num_missing = min(2, len(positions) // 2)

    missing_positions = random.sample(
        positions,
        num_missing
    )

    for pos in missing_positions:
        letters[pos] = "_"

    return " ".join(letters)


# =====================================================
# 🔄 เริ่มเกมใหม่
# =====================================================

def reset_game():

    selected_words = random.sample(
        all_words,
        min(4, len(all_words))
    )

    st.session_state.questions = selected_words

    st.session_state.answers = [""] * len(selected_words)

    st.session_state.start = time.time()

    st.session_state.is_ended = False

    st.session_state.game_started = True


# =====================================================
# 📊 แสดงผล
# =====================================================

@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog():

    score = 0

    st.balloons()

    for i, question in enumerate(st.session_state.questions):

        user_answer = st.session_state.answers[i].strip().lower()

        correct_answer = question["word"].lower()

        if user_answer == correct_answer:

            st.success(
                f"ข้อ {i + 1}: ✅ ถูกต้อง — {question['word']}"
            )

            score += 1

        else:

            st.error(
                f"ข้อ {i + 1}: ❌ ผิด "
                f"(คำตอบที่ถูกคือ {question['word']})"
            )

    total = len(st.session_state.questions)

    st.info(
        f"🏆 ได้คะแนน {score} / {total} คะแนน"
    )

    if score == total:
        st.success("🎉 You Win! เก่งมาก!")
    else:
        st.error("💀 You Lose! ลองใหม่อีกครั้ง")


# =====================================================
# 🎮 ปุ่มเริ่มเกม
# =====================================================

if st.button("🎮 เริ่มเล่นเกม", use_container_width=True):

    reset_game()
    st.rerun()


# =====================================================
# ⏱️ ระบบจับเวลา
# =====================================================

if st.session_state.get("game_started", False):

    if not st.session_state.get("is_ended", False):

        elapsed = time.time() - st.session_state.start

        time_left = int(30 - elapsed)

        if time_left > 0:

            st.error(
                f"⏳ เหลือเวลา: {time_left} วินาที"
            )

        else:

            st.session_state.is_ended = True

            st.rerun()


st.divider()


# =====================================================
# 📝 แสดงคำถาม
# =====================================================

if st.session_state.get("game_started", False):

    if not st.session_state.get("is_ended", False):

        for i, question in enumerate(
            st.session_state.questions
        ):

            masked_word = make_question(
                question["word"]
            )

            # เก็บโจทย์ไว้ ไม่ให้เปลี่ยนทุกครั้งที่ rerun
            if "masked_questions" not in st.session_state:

                st.session_state.masked_questions = []

            if len(st.session_state.masked_questions) < len(
                st.session_state.questions
            ):

                st.session_state.masked_questions = [
                    make_question(q["word"])
                    for q in st.session_state.questions
                ]

            masked_word = st.session_state.masked_questions[i]

            st.write(
                f"### ข้อ {i + 1}"
            )

            st.write(
                f"{question['emoji']} "
                f"`{masked_word}`"
            )

            answer = st.text_input(
                "เติมคำศัพท์:",
                key=f"answer_{i}"
            )

            st.session_state.answers[i] = answer


        st.divider()

        # =================================================
        # 📥 ส่งคำตอบ
        # =================================================

        if st.button(
            "📥 ส่งคำตอบ",
            use_container_width=True
        ):

            st.session_state.is_ended = True

            st.rerun()


        # =================================================
        # 🔄 ทำให้นาฬิกานับต่อ
        # =================================================

        time.sleep(1)

        st.rerun()


# =====================================================
# 📊 เปิดผลคะแนน
# =====================================================

if st.session_state.get("is_ended", False):

    show_result_dialog()       

st.divider()
st.write("นางสาว ทับทิม คำป้อ เลขที่ 43 ม.4/7")
