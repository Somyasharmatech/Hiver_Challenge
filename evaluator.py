import os
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
from textstat import flesch_reading_ease
import textstat
import textwrap

# Download nltk requirements safely
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class Evaluator:
    def __init__(self):
        # We load a small fast sentence transformer for cosine similarity
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

    def calculate_bleu(self, expected, generated):
        reference = [nltk.word_tokenize(expected.lower())]
        candidate = nltk.word_tokenize(generated.lower())
        smoothie = SmoothingFunction().method4
        score = sentence_bleu(reference, candidate, smoothing_function=smoothie)
        
        # Explainability
        if score > 0.4: reason = "Strong phrasing overlap with expected reply."
        elif score > 0.2: reason = "Moderate overlap in vocabulary."
        else: reason = "Low exact phrase matching (may still be semantically correct)."
        
        return {"score": round(score * 100, 1), "reason": reason}

    def calculate_rouge(self, expected, generated):
        scores = self.rouge.score(expected, generated)
        rouge_l = scores['rougeL'].fmeasure
        
        if rouge_l > 0.6: reason = "Excellent structural similarity and term recall."
        elif rouge_l > 0.4: reason = "Good coverage of key concepts."
        else: reason = "Missing several key concepts from the expected reply."
        
        return {"score": round(rouge_l * 100, 1), "reason": reason}

    def calculate_cosine_similarity(self, expected, generated):
        emb1 = self.embedding_model.encode(expected, convert_to_tensor=True)
        emb2 = self.embedding_model.encode(generated, convert_to_tensor=True)
        cosine_scores = util.cos_sim(emb1, emb2)
        score = cosine_scores.item()
        
        if score > 0.85: reason = "Very high semantic equivalence."
        elif score > 0.65: reason = "Captures the core meaning well."
        else: reason = "Diverges significantly in meaning."
        
        return {"score": round(score * 100, 1), "reason": reason}
        
    def calculate_readability(self, generated):
        score = flesch_reading_ease(generated)
        # Flesch reading ease: 0-100 (higher is easier)
        # We normalize to 100 max
        norm_score = min(max(score, 0), 100)
        
        if norm_score > 60: reason = "Clear and easy to read for most customers."
        else: reason = "A bit complex, consider simpler wording."
        
        return {"score": round(norm_score, 1), "reason": reason}

    def run_full_evaluation(self, expected, generated, qual_metrics):
        """Combines quantitative NLP metrics with qualitative Gemini metrics."""
        
        # Quantitative
        bleu = self.calculate_bleu(expected, generated)
        rouge = self.calculate_rouge(expected, generated)
        cosine = self.calculate_cosine_similarity(expected, generated)
        readability = self.calculate_readability(generated)
        
        length_diff = abs(len(expected.split()) - len(generated.split()))
        
        # Map Qualitative Metrics (from Gemini JSON)
        prof_score = qual_metrics.get("Professionalism", {}).get("score", 7) * 10
        emp_score = qual_metrics.get("Empathy", {}).get("score", 7) * 10
        gram_score = qual_metrics.get("Grammar", {}).get("score", 7) * 10
        comp_score = qual_metrics.get("Completeness", {}).get("score", 7) * 10
        
        prof_reason = qual_metrics.get("Professionalism", {}).get("reason", "Standard tone.")
        emp_reason = qual_metrics.get("Empathy", {}).get("reason", "Acceptable empathy.")
        gram_reason = qual_metrics.get("Grammar", {}).get("reason", "No major issues.")
        comp_reason = qual_metrics.get("Completeness", {}).get("reason", "Addressed main points.")
        hallu_reason = qual_metrics.get("Hallucination Risk", {}).get("reason", "Low risk.")

        # Compute Overall Score (Weighted)
        # NLP metrics: 40%, Qual Metrics: 60%
        overall = (
            (bleu["score"] * 0.10) +
            (rouge["score"] * 0.15) +
            (cosine["score"] * 0.15) +
            (prof_score * 0.20) +
            (emp_score * 0.15) +
            (gram_score * 0.10) +
            (comp_score * 0.15)
        )
        overall = min(round(overall, 1), 100)
        
        # Stars
        stars_num = max(1, min(5, int(overall / 20) + (1 if overall % 20 > 10 else 0)))
        stars_str = "⭐" * stars_num
        
        # Recommendation
        if overall >= 90:
            recommendation = "✅ Safe to Send"
        elif overall >= 70:
            recommendation = "⚠ Needs Review"
        else:
            recommendation = "❌ Poor Reply"
            
        return {
            "Overall Score": overall,
            "Stars": stars_str,
            "Recommendation": recommendation,
            "Metrics": {
                "BLEU": bleu,
                "ROUGE": rouge,
                "Cosine Similarity": cosine,
                "Readability": readability,
                "Professionalism": {"score": prof_score, "reason": prof_reason},
                "Empathy": {"score": emp_score, "reason": emp_reason},
                "Grammar": {"score": gram_score, "reason": gram_reason},
                "Completeness": {"score": comp_score, "reason": comp_reason},
                "Hallucination Risk": {"score": qual_metrics.get("Hallucination Risk", {}).get("score", 10)*10, "reason": hallu_reason}
            }
        }
