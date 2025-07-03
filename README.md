# 🧠 AI-Powered Custom Quiz Generator

Generate personalized questions using Hugging Face Transformers and Streamlit UI.

## 💡 Features
- T5-based question generator
- Streamlit frontend
- Cosine Similarity & BLEU Evaluation
- Simulated RLHF via user feedback

## 🚀 How to Run

```bash
git clone https://github.com/YOUR_USERNAME/custom-quiz-generator.git
cd custom-quiz-generator
python -m venv venv #run this command if u want to work in a virtual env
source venv\Scripts\activate #run this command if u want to work in a virtual env
pip install -r requirements.txt #to install all the required packages and libraries

#Repo Struture
custom-quiz-generator/
│
├── app.py                        # Streamlit frontend
├── model_utils.py               # Model loading, prompt creation, generation
├── evaluation.py                # Cosine similarity & BLEU score calculations
├── fine_tune.py                 # (Optional) fine-tuning script (even mock)
├── feedback_log.csv             # Simulated RLHF storage
├── requirements.txt             # All dependencies
├── README.md                    # Project overview and usage guide
│
├── data/
│   └── sample_qa_dataset.csv    # A small quiz dataset for testing/fine-tuning
│
├── outputs/
│   └── generated_questions.csv  # Store generated questions if needed
│
├── models/                      # (Optional) Store custom fine-tuned models
│
└── assets/                      # Images/screenshots for README/demo
