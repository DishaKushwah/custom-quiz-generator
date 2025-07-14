import streamlit as st
import time
st.title("AI Custom Quiz Generator")
st.markdown("""
Welcome to the AI-Powered Quiz Generator!  
Enter your preferences below to generate personalized quizzes based on your topic, difficulty level, and question type.
""")
topic = st.text_input("Enter Topic :")
difficulty = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])
q_type = st.selectbox("Question Type:", ["MCQ", "True/False", "Short Answer"])
num_questions = st.slider("Number of Questions:", 1, 20, 5)
if st.button("🚀 Generate Quiz"):
    if topic.strip() == "":
        st.warning("Please enter a topic before generating the quiz.")
    else:
        with st.spinner("Generating your quiz... Please wait..."):
            time.sleep(2) 
        st.success("Quiz generated!")