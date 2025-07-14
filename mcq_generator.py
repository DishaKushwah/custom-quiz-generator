import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import pipeline

class AdvancedMCQGenerator:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        # Initialize NLP models
        self.qa_pipeline = pipeline("question-answering")
        self.stop_words = set(stopwords.words('english'))

    def extract_key_concepts(self, context):
        """Extract key concepts and important phrases"""
        # Tokenize sentences
        sentences = sent_tokenize(context)
        
        # Extract potential key concepts
        key_concepts = []
        for sentence in sentences:
            # Look for sentences with unique, meaningful content
            words = word_tokenize(sentence)
            filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in self.stop_words and len(word) > 2]
            # Prioritize sentences with named entities or specific concepts
            if len(filtered_words) > 3:
                key_concepts.append(sentence)
        return key_concepts[:5]  # Return top 5 key concepts

    def generate_intelligent_question(self, concept, context):
        """Generate a more nuanced and contextually relevant question"""
        question_templates = [
            f"What is the primary significance of {concept}?",
            f"How does {concept} impact the broader context?",
            f"What key role does {concept} play in the narrative?",
            f"Explain the importance of {concept} in this context.",
            f"What makes {concept} crucial to understanding the situation?"
        ]
        
        return random.choice(question_templates)

    def generate_contextual_distractors(self, correct_answer, context):
        """Create semantically related but incorrect distractors"""
        sentences = sent_tokenize(context)
        distractors = []
        
        potential_distractors = [sent for sent in sentences if correct_answer.lower() not in sent.lower() and len(sent.split()) > 3]
        
        # Generating diverse distractors
        while len(distractors) < 3:
            if potential_distractors:
                # Choose a unique distractor
                distractor = random.choice(potential_distractors)
                potential_distractors.remove(distractor)
                words = word_tokenize(distractor)
                key_phrase = ' '.join([word for word in words if word.lower() not in self.stop_words and len(word) > 2][:3])
                distractors.append(key_phrase)
            else:
                fallback_distractors = ["A partially related historical context","An alternative interpretation","A peripheral aspect of the main theme"]
                distractor = random.choice(fallback_distractors)
                distractors.append(distractor)
        return distractors

    def generate_mcq(self, context, num_questions=3):
        """Generate Multiple Choice Questions"""
        # Validate context
        if not context or len(context.split()) < 30:
            raise ValueError("Context is too short. Provide more detailed text.")
        
        # Generate questions
        mcq_questions = []
        key_concepts = self.extract_key_concepts(context)
        
        for concept in key_concepts[:num_questions]:
            try:
                question = self.generate_intelligent_question(concept, context)      # Generate question
                answer_result = self.qa_pipeline(question=question, context=context)      # Use QA pipeline to find the most relevant answer
                correct_answer = answer_result['answer']    # Get correct answer
                distractors = self.generate_contextual_distractors(correct_answer, context)     # Generate distractors
                all_options = [correct_answer] + distractors    # Combine options
                random.shuffle(all_options)
                correct_index = all_options.index(correct_answer)       # Determine correct option index
                mcq_questions.append({"question": question,"options": all_options,"correct_answer": correct_index})     # Create MCQ
            except Exception as e:
                print(f"Error generating question: {e}")
        return mcq_questions
def main():
    # Create generator instance
    generator = AdvancedMCQGenerator()
    context = input("Enter context text: ")
    num_questions = int(input("How many questions do you want? "))
    questions = generator.generate_mcq(context, num_questions)
    
    # Display and solve quiz
    print("\n--- Quiz Started ---")
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{chr(65+j)}. {option}")
        
        while True:
            user_answer = input("\nYour Answer (A/B/C/D): ").upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            print("Invalid input. Please enter A, B, C, or D.")
        
        user_index = ord(user_answer) - 65
        if user_index == q['correct_answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer was: {chr(65 + q['correct_answer'])}")
    print(f"\nFinal Score: {score}/{len(questions)}")

if __name__ == "__main__":
    main()
