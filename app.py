import streamlit as st
from mcq_generator import AdvancedMCQGenerator
from short_answer_generator import QuestionGenerator
from truefalse_quiz import generate_true_false
import io

# Set page config at the top
st.set_page_config(page_title="QuizCraft AI", layout="centered")

# App title and intro
st.title("🎓 QuizCraft AI")
st.markdown("Generate intelligent quizzes from any context using AI. Choose the type, level, and number of questions!")

# Input section
context = st.text_area("📜 Enter your context/text here:", height=100)

col1, col2 = st.columns(2)
question_type = col1.selectbox("Question Type", ["Multiple Choice", "Short Answer", "True/False"])
difficulty = col2.selectbox("Difficulty", ["easy", "medium", "hard"])

num_questions = st.slider("🔢 Number of Questions", min_value=1, max_value=10, value=3)
#<<<<<<< main
#=======

#>>>>>>> main

# Generate button
if st.button("⚡ Generate Quiz"):
    if not context.strip():
        st.warning("Please enter some context/text to generate questions.")
    else:
        with st.spinner("Generating quiz..."):
            output = io.StringIO()  # For optional export
            questions = []

            if question_type == "Multiple Choice":
                generator = AdvancedMCQGenerator()
                try:
                    questions = generator.generate_mcq(context, num_questions=num_questions, difficulty=difficulty)
                    st.subheader("📘 Multiple Choice Questions")
                    for idx, q in enumerate(questions, 1):
                        st.markdown(f"**Q{idx}: {q['question']}**")
                        for i, option in enumerate(q['options']):
                            st.markdown(f"- {chr(65+i)}. {option}")
                        st.markdown(f"🟢 **Answer:** {chr(65 + q['correct_answer'])}\n\n---")

                        # Export text
                        output.write(f"Q{idx}: {q['question']}\n")
                        for i, option in enumerate(q['options']):
                            output.write(f"  {chr(65+i)}. {option}\n")
                        output.write(f"Answer: {chr(65 + q['correct_answer'])}\n\n")
                except Exception as e:
                    st.error(f"❌ Failed to generate MCQs: {str(e)}")

            elif question_type == "Short Answer":
                try:
                    generator = QuestionGenerator()
                    questions = generator.generate_questions(context, num_questions=num_questions, difficulty=difficulty)
                    st.subheader("📝 Short Answer Questions")
                    for idx, q in enumerate(questions, 1):
                        st.markdown(f"**Q{idx}: {q['question']}**")
                        st.markdown(f"🟢 **Expected Keyword:** {q['answer']}")
                        st.markdown("---")

                        # Export text
                        output.write(f"Q{idx}: {q['question']}\nExpected keyword: {q['answer']}\n\n")
                except Exception as e:
                    st.error(f"❌ Failed to generate short answer questions: {str(e)}")

            elif question_type == "True/False":
                try:
                    st.subheader("✅ True/False Questions")
                    tf_generator = generate_true_false()  # Initialize the class
                    sentences = tf_generator.validate_inputs(context, num_questions, difficulty)
                    questions = tf_generator.generate_statements(context, num_questions, difficulty, sentences)
                    
                    for idx, (statement, label) in enumerate(questions, 1):
                        st.markdown(f"**Q{idx}: {statement}**")
                        st.markdown(f"🟢 **Answer:** {'True' if label == 'ENTAILMENT' else 'False'}")
                        st.markdown("---")

                        # Export text
                        output.write(f"Q{idx}: {statement}\nAnswer: {'True' if label == 'ENTAILMENT' else 'False'}\n\n")
                except Exception as e:
                    st.error(f"❌ Failed to generate true/false questions: {str(e)}")


            # Download button if questions were generated
            if questions:
                st.download_button("⬇️ Download Quiz as PDF", output.getvalue(), file_name="quizcraft_quiz.pdf")

#<<<<<<< main

#=======
#>>>>>>> main
