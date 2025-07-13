import torch
import random
import nltk
import re
from transformers import (pipeline, AutoModelForQuestionAnswering, AutoTokenizer)
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any
nltk.download('punkt')
nltk.download('stopwords')

class AdvancedMCQGenerator:
    def __init__(self):
        """Advanced Multiple Choice Question Generator with Intelligent Distractor Strategy"""
        # Question Answering Model
        qa_model_name = "deepset/roberta-base-squad2"
        self.qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
        self.qa_pipeline = pipeline("question-answering", model=qa_model_name,device=0 if torch.cuda.is_available() else -1)
        self.sentence_embedder = SentenceTransformer('all-mpnet-base-v2')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.sentence_tokenizer = nltk.sent_tokenize
        self.generated_questions = set()

    def _extract_context_features(self, context: str) -> Dict[str, Any]:
        """Advanced context feature extraction"""
        sentences = self.sentence_tokenizer(context)
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            top_keywords = []
            for i, sentence in enumerate(sentences):
                feature_indices = tfidf_matrix[i].nonzero()[1]                # Get top TF-IDF scores for each sentence
                top_sentence_keywords = [feature_names[idx] for idx in feature_indices][:3]
                top_keywords.extend(top_sentence_keywords)
            return {'sentences': sentences,'keywords': list(set(top_keywords)),'total_sentences': len(sentences)}
        except Exception as e:
            print(f"Context feature extraction error: {e}")
            return {'sentences': sentences,'keywords': context.split()[:10],'total_sentences': len(sentences)}

    def _generate_smart_distractors(self, correct_answer: str, context_features: Dict[str, Any], num_distractors: int = 3) -> List[str]:
        """Intelligent Distractor Generation Strategy"""
        distractors = []
        used_options = set([correct_answer.lower()])
        sentences = context_features['sentences']
        keywords = context_features['keywords']
        # Semantic similarity-based distractor generation
        for _ in range(num_distractors):
            try:
                semantic_candidates = [sent for sent in sentences if sent.lower() not in used_options and len(sent.split()) > 3]
                if semantic_candidates:
                    candidate_similarities = [(sent, self._calculate_semantic_similarity(correct_answer, sent)) for sent in semantic_candidates]
                    candidate_similarities.sort(key=lambda x: abs(0.5 - x[1]))
                    if candidate_similarities:
                        best_distractor = candidate_similarities[0][0]
                        distractors.append(best_distractor)
                        used_options.add(best_distractor.lower())
                        continue
                
                if keywords:
                    keyword_distractor = f"A key aspect related to {random.choice(keywords)}"
                    distractors.append(keyword_distractor)
                    used_options.add(keyword_distractor.lower())
                    continue
                fallback_distractors = ["A related contextual detail","An alternative interpretation","A supplementary concept"]
                distractor = random.choice(fallback_distractors)
                distractors.append(distractor)
                used_options.add(distractor.lower())
            
            except Exception as e:
                print(f"Distractor generation error: {e}")
                distractors.append("A contextual detail")
        return distractors[:num_distractors]

    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            # Embed texts
            embedding1 = self.sentence_embedder.encode(text1)
            embedding2 = self.sentence_embedder.encode(text2)
            
            # Calculate cosine similarity
            similarity = torch.nn.functional.cosine_similarity(torch.tensor(embedding1), torch.tensor(embedding2)).item()
            return abs(similarity)
        except Exception:
            return 0.0

    def generate_mcq(self, context: str, num_questions: int = 5, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """
        Generate Multiple Choice Questions
        """
        context = self._preprocess_context(context)        # Preprocess context
        context_features = self._extract_context_features(context)        # Extract context features
        self.generated_questions.clear()        # Reset generated questions
        mcq_questions = []
        
        for _ in range(num_questions):
            try:
                keywords = context_features['keywords']
                subject = random.choice(keywords)
                        # Question templates
                templates = [f"What is the significance of {subject} in this context?",f"Explain the role of {subject}.",f"How does {subject} contribute to the overall understanding?"]
                question = random.choice(templates)
                answer_result = self.qa_pipeline(question=question, context=context)      # Extract answer using QA pipeline
                correct_answer = answer_result['answer']       # Get correct answer
                distractors = self._generate_smart_distractors(correct_answer, context_features)      # Generate contextually relevant distractors
                all_options = [correct_answer] + distractors                # Combine options
                random.shuffle(all_options)
                correct_index = all_options.index(correct_answer)                # Determine correct option index
                mcq_questions.append({"question": question,"options": all_options,"correct_answer": correct_index,"explanation": f"Correct answer based on the context: {correct_answer}"})
            except Exception as e:
                print(f"MCQ generation error: {e}")
        return mcq_questions

    def _preprocess_context(self, context: str) -> str:
        """Advanced context preprocessing"""
        context = re.sub(r'\s+', ' ', context).strip()        # Remove extra whitespaces and special characters
        context = ''.join(char for char in context if char.isprintable())        # Remove non-printable characters
        if len(context.split()) < 20:        # Append context if too short
            context += " Additional context to enhance question generation."
        return context

def main():
    generator = AdvancedMCQGenerator()
    print(" -------------Multiple Choice Question Generator-------------")
    context = input("\n>> Enter context text: ")
    while True:
        try:
            num_questions = int(input("\n>> How many questions do you want to generate? "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        difficulty = input("\n>> Enter difficulty level (easy/medium/hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            break
        print("Invalid difficulty level. Please choose easy, medium, or hard.")
    questions = generator.generate_mcq(context, num_questions, difficulty)
    if questions:
        print("\n--- Multiple Choice Quiz ---")
        correct_answers = 0        # Simple score tracking
        total_questions = len(questions)

        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q['question']}")
            print("Options:")
            for j, option in enumerate(q['options']):
                print(f"{chr(65+j)}. {option}")
            
            while True:
                user_input = input("\nYour Answer (A/B/C/D): ").upper()
                if user_input in ['A', 'B', 'C', 'D']:
                    break
                print("Invalid input. Please enter A, B, C, or D.")
            
            user_answer_index = ord(user_input) - 65
            if user_answer_index == q['correct_answer']:
                print("✅ Correct!")
                correct_answers += 1
            else:
                print(f"❌ Incorrect. Correct Answer: {chr(65+q['correct_answer'])}")
        
        # Simple score display
        print(f"\n-----Score: {correct_answers}/{total_questions}-----")

    else:
        print("\nNo multiple choice questions were generated.")

if __name__ == "__main__":
    main()
# SAMPLE CONTEXT- The French Revolution began in 1789 and marked a significant turning point in European history. It was fueled by widespread social inequality, financial crisis, and the rise of Enlightenment ideas. The French monarchy was overthrown, and King Louis XVI was executed. The revolution introduced the ideals of liberty, equality, and fraternity. It led to the rise of Napoleon Bonaparte and had a lasting impact on modern democracy and human rights movements around the world.
