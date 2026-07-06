# AI Email Response Intelligence 🧠✉️

A production-ready, AI-powered Customer Email Response System designed for the Hiver AI Internship Open Challenge. This application leverages the Gemini API to analyze customer intents, generate empathetic replies, and rigorously evaluate the response quality using advanced NLP metrics (BLEU, ROUGE, BERTScore, Cosine Similarity) inside a premium, glassmorphism-styled SaaS dashboard.

## 🚀 Features

- **Programmatic Dataset Generation:** Deterministically generates 100 realistic customer support emails across 20 categories (no Gemini hallucination for data).
- **AI Reasoning Pipeline:** Extracts Intent → Emotion → Urgency → Required Action before drafting any reply.
- **Explainable Evaluation (Explainable AI):** Calculates quantitative (BLEU, ROUGE, Cosine Sim, Readability) and qualitative (Empathy, Professionalism) scores, providing a transparent reason for *every* score.
- **Enterprise Analytics Dashboard:** Built with Plotly, featuring Gauge charts and Radar charts.
- **AI Coach (Iterative Improvement):** Suggests improvements for any generated reply and outputs an enhanced version.
- **Premium SaaS UI:** Custom CSS hides default Streamlit styling in favor of modern glassmorphism, animated buttons, and gradient text.
- **Semantic Diff Comparison:** GitHub-style side-by-side highlighting of differences between the Expected baseline and the AI Generated reply.

## 📁 Project Structure

```text
Hiver_Challenge/
├── app.py                 # Main Streamlit Application UI
├── generator.py           # Gemini API logic for Reasoning & Generation
├── evaluator.py           # NLP Metrics & Scoring Logic
├── dataset_generator.py   # Python script to programmatically build the dataset
├── dataset.json           # The generated 100-email training/testing set
├── prompts.py             # System prompts for Analysis, Reply, and Coach
├── config.py              # Configuration & Environment Variables
├── utils.py               # Custom UI Components (CSS, Plotly, Diff)
├── requirements.txt       # Project Dependencies
├── .env.example           # Environment variables template
└── README.md              # Project Documentation
```

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key.

### 2. Installation

Clone the repository and install the dependencies:
```bash
git clone https://github.com/Somyasharmatech/Hiver_Challenge.git
cd Hiver_Challenge
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Gemini API Key:
```bash
cp .env.example .env
```
Edit `.env` and set `GEMINI_API_KEY=your_key_here`.

### 4. Running the Application

First, (optional) re-generate the dataset if you want fresh data:
```bash
python dataset_generator.py
```

Then, launch the Streamlit app:
```bash
streamlit run app.py
```

## 📊 Evaluation Metrics Used

1. **BLEU & ROUGE:** For structural and phrasing overlap with expected responses.
2. **Cosine Similarity (SentenceTransformers):** For semantic meaning comparison (`all-MiniLM-L6-v2`).
3. **Flesch Reading Ease:** To ensure responses are accessible to all customers.
4. **Professionalism, Empathy, Grammar, Completeness:** Graded via an LLM-as-a-judge (Gemini 1.5) with reasoning attached.

## 🤝 Architecture & Design Philosophy
This project was built to mimic a real-world enterprise product. It separates concerns (Prompts, UI, Evaluator, Generator) and completely revamps Streamlit's default UI to look like a modern AI SaaS tool (similar to Notion AI or Vercel).

---
*Created by [somyasharmatech](https://github.com/somyasharmatech)*
