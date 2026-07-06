# AI Email Response Intelligence 🧠✉️

[![Live Demo](https://img.shields.io/badge/Live_Demo-Play_Now-000000?style=for-the-badge&logo=streamlit&logoColor=white)](https://hiverchallenge-8ckxvrgahym4aom73qwjch.streamlit.app/)
[![Video Walkthrough](https://img.shields.io/badge/Video_Walkthrough-Watch_Now-red?style=for-the-badge&logo=youtube&logoColor=white)](https://drive.google.com/file/d/15nBNhfxoPhafSAhKKa4qb0gMwdp8TGNw/view?usp=sharing&t=26.544)

> [!IMPORTANT]  
> 🎥 **Recruiters & Reviewers:** Please [watch the full video walkthrough here](https://drive.google.com/file/d/15nBNhfxoPhafSAhKKa4qb0gMwdp8TGNw/view?usp=sharing&t=26.544) to see the system's end-to-end reasoning pipeline, dual-mode operation, and explainable AI dashboard in action!

A production-ready, highly robust Customer Email Response System designed for the Hiver AI Internship Open Challenge. This application leverages the Gemini API to analyze customer intents, generate empathetic replies, and rigorously evaluate the response quality using advanced NLP metrics inside a premium, glassmorphism-styled SaaS dashboard.

## 🚀 Features

- **Dual-Mode Operation:** 
  - *Benchmark Mode:* Tests the model against a pre-generated dataset of 100 realistic customer support emails to compute full NLP and Qualitative metrics.
  - *Real-world Mode:* Allows you to paste any custom email to get an instant reply, evaluated qualitatively.
> **Note for Reviewers:** This live demo runs on the **Gemini Free Tier API**. Because our pipeline rigorously evaluates multiple metrics in the background, you may encounter a temporary "Quota Exceeded" error if you click the generate button rapidly. If this happens, simply wait 60 seconds and try again!
- **Strict Sequential Reasoning Pipeline:** Extracts Intent → Emotion → Urgency → Confidence before drafting any reply. Built with rigorous `try-except` error handling that halts on failure rather than hallucinating placeholder values.
- **Explainable Evaluation Dashboard:** Calculates quantitative (BLEU, ROUGE, Cosine Sim, Readability) and qualitative (Empathy, Professionalism, Completeness, Helpfulness, Grammar, Hallucination Risk) scores, providing a transparent reason for *every* score.
- **AI Coach (Iterative Improvement):** Suggests improvements for any generated reply, outputs an enhanced version, and projects the expected score increase based on identified strengths and weaknesses.
- **Premium SaaS UI:** Custom CSS hides default Streamlit styling in favor of modern glassmorphism, animated buttons, dynamic charts (Plotly), and gradient text.
- **Comprehensive Logging:** Background file logging for generation speeds, tokens, successful evaluations, and captured stack traces.

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
- A Google Gemini API Key

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

First, ensure NLTK packages are downloaded:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

Then, launch the Streamlit app:
```bash
streamlit run app.py
```

## 📊 Evaluation Metrics Used

1. **BLEU & ROUGE:** For structural and phrasing overlap with expected responses.
2. **Cosine Similarity (SentenceTransformers):** For semantic meaning comparison (`all-MiniLM-L6-v2`).
3. **Flesch Reading Ease:** To ensure responses are accessible to all customers.
4. **Qualitative Metrics:** Professionalism, Empathy, Grammar, Completeness, Helpfulness, and Hallucination Risk (Graded via LLM-as-a-judge with reasoning attached).

## 🤝 Architecture & Design Philosophy
This project was built to mimic a real-world enterprise product. It separates concerns (Prompts, UI, Evaluator, Generator), utilizes strict JSON parsing with automatic retry logic, and completely revamps Streamlit's default UI to look like a modern AI SaaS tool.

---
*Created by [somyasharmatech](https://github.com/somyasharmatech)*
