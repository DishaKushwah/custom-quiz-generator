#<<<<<<< patch-1
import streamlit as st
import time
from io import StringIO

# Title and Description
st.set_page_config(page_title="AI Custom Quiz Generator", layout="centered")
st.title("🧠 AI Custom Quiz Generator")
st.markdown("""
Welcome to the AI-Powered Quiz Generator!  
Enter your preferences below to generate personalized quizzes based on your topic, difficulty level, and question type.
""")

# Input Section
with st.container():
    topic = st.text_input("📘 Enter Topic :")
    difficulty = st.selectbox("📊 Select Difficulty Level:", ["Easy", "Medium", "Hard"])
    q_type = st.selectbox("❓ Question Type:", ["MCQ", "True/False", "Short Answer"])
    num_questions = st.slider("🔢 Number of Questions:", 1, 20, 5)

# Placeholder for generated quiz
quiz_output = ""

# Generate Quiz Button
if st.button("🚀 Generate Quiz"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic before generating the quiz.")
    else:
        with st.spinner("🛠️ Generating your quiz... Please wait..."):
            try:
                time.sleep(2)

                # Fake quiz generation
                quiz_output = f"Topic: {topic}\nDifficulty: {difficulty}\nType: {q_type}\n\n"
                for i in range(1, num_questions + 1):
                    quiz_output += f"{i}. Sample question {i} on {topic} [{q_type} - {difficulty}]\n"

                st.success("✅ Quiz generated successfully!")
                st.text_area("📄 Your Quiz:", quiz_output, height=200)

                # Download button
                st.download_button(
                    label="⬇️ Download Quiz as .txt",
                    data=quiz_output,
                    file_name=f"{topic.lower().replace(' ', '_')}_quiz.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# Feedback Section
st.markdown("---")
st.subheader("💬 Feedback")
feedback = st.text_area("Let us know your thoughts or any issues you faced:")
if st.button("📩 Submit Feedback"):
    if feedback.strip() == "":
        st.info("✏️ Please write something before submitting.")
    else:
        st.success("🙌 Thank you for your feedback!")
