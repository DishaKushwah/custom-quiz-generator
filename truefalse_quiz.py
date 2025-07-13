import random
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize

# Download required tokenizer
nltk.download('punkt_tab', quiet=True)

# Load NLI model
nli = pipeline("text-classification", model="facebook/bart-large-mnli")

# Input validation
def validate_inputs(context, num_questions, difficulty):
    if not context.strip():
        raise ValueError("Context cannot be empty.")
    sentences = sent_tokenize(context)
    if len(sentences) < num_questions:
        raise ValueError(f"Context has only {len(sentences)} sentences, but {num_questions} questions requested.")
    if difficulty not in ["easy", "medium", "hard"]:
        raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'.")
    return sentences

# Difficulty-based sentence modifier
def apply_noise(sentence: str, level: str) -> str:
    if level == "easy":
        return sentence
    elif level == "medium":
        if "Sun" in sentence:
            return sentence.replace("Sun", "Moon")
        return sentence.replace("is", "is not") if "is" in sentence else sentence
    elif level == "hard":
        if "eight" in sentence:
            return sentence.replace("eight", "ten")
        return sentence.replace("planets", "stars") if "planets" in sentence else sentence
    return sentence

# Statement generator
def generate_statements(context, n, difficulty, sentences):
    random.seed(42)
    selected = random.sample(sentences, min(n * 2, len(sentences)))
    final = []
    for s in selected:
        clean = s.strip()
        modified = apply_noise(clean, difficulty)
        label = "ENTAILMENT" if clean == modified else "CONTRADICTION"
        final.append((modified, label))
        if len(final) >= n:
            break
    return final

# Get valid user answer
def get_user_answer():
    while True:
        user = input("True or False? ").strip().lower()
        if user in ["true", "false"]:
            return user
        print("Please enter 'true' or 'false'.")

# Main logic
try:
    context = input(">> Enter context text: ")
    num_questions = int(input("\n>> How many questions do you want to generate? "))
    difficulty = input("\n>> Enter difficulty level (easy/medium/hard): ").strip().lower()
    
    sentences = validate_inputs(context, num_questions, difficulty)
    questions = generate_statements(context, num_questions, difficulty, sentences)
    
    if len(questions) < num_questions:
        print(f"Warning: Only {len(questions)} questions generated due to limited context.")
    
    print("\n--- QUIZ STARTS ---\n")
    score = 0
    
    for idx, (statement, actual_label) in enumerate(questions, 1):
        print(f"Q{idx}: {statement}")
        user = get_user_answer()
        
        # Format input for facebook/bart-large-mnli
        input_text = f"{context} [SEP] {statement}"
        result = nli(input_text)[0]
        if result["label"] == "neutral":
            print("Skipping ambiguous statement.\n")
            continue
        model_label = "ENTAILMENT" if result["label"] == "entailment" else "CONTRADICTION"
        
        if model_label == "ENTAILMENT" and user == "true":
            print("Correct!\n")
            score += 1
        elif model_label == "CONTRADICTION" and user == "false":
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! (Correct answer: {'True' if model_label == 'ENTAILMENT' else 'False'})\n")
    
    print(f"\n--- Final Score: {score}/{len(questions)} ---")

except ValueError as e:
    print(f"Error: {e}")