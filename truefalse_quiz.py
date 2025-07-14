import random
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize

# Download required tokenizer
nltk.download('punkt', quiet=True)

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
        return sentence.replace(" is ", " is not ") if " is " in sentence else sentence
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

# ✅ MAIN BACKEND FUNCTION
def generate_true_false(context, num_questions, difficulty):
    """
    Returns a list of (statement, label) pairs for Streamlit frontend.
    label: 'ENTAILMENT' (True) or 'CONTRADICTION' (False)
    """
    sentences = validate_inputs(context, num_questions, difficulty)
    questions = generate_statements(context, num_questions, difficulty, sentences)
    result = []

    for statement, _ in questions:
        input_text = f"{context} [SEP] {statement}"
        nli_result = nli(input_text)[0]
        label = "ENTAILMENT" if nli_result["label"] == "entailment" else "CONTRADICTION"
        result.append((statement, label))
    
    return result
