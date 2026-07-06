import json
import time
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from prompts import ANALYSIS_PROMPT, REPLY_PROMPT, EVALUATION_PROMPT, COACH_PROMPT
import re

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def clean_json_response(response_text):
    """Clean markdown formatting from Gemini JSON response."""
    cleaned = re.sub(r'```json\s*', '', response_text)
    cleaned = re.sub(r'```\s*', '', cleaned)
    return cleaned.strip()

class AIGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing. Check .env file.")
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        # For evaluation & coach, we might want lower temperature
        self.eval_model = genai.GenerativeModel(GEMINI_MODEL_NAME, generation_config={"temperature": 0.1})

    def analyze_email(self, email_body):
        """Step 1: AI Reasoning Pipeline - Extract intent, sentiment, etc."""
        prompt = ANALYSIS_PROMPT.format(email_body=email_body)
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            duration = time.time() - start_time
            
            cleaned_json = clean_json_response(response.text)
            analysis = json.loads(cleaned_json)
            analysis['duration'] = duration
            return analysis
        except Exception as e:
            print(f"Error in analyze_email: {e}")
            return {
                "intent": "Unknown", "emotion": "Neutral", "urgency": "Medium", 
                "required_action": "Review manually", "reason": "Failed to parse analysis.",
                "entities": [], "duration": 0
            }

    def generate_reply(self, email_body, analysis):
        """Step 2: Generate reply based on analysis."""
        prompt = REPLY_PROMPT.format(
            email_body=email_body,
            intent=analysis.get('intent', ''),
            emotion=analysis.get('emotion', ''),
            urgency=analysis.get('urgency', '')
        )
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            duration = time.time() - start_time
            
            # Simple token estimation (1 token approx 4 characters)
            token_usage = len(prompt + response.text) // 4
            
            return {
                "reply": response.text.strip(),
                "duration": duration,
                "tokens": token_usage
            }
        except Exception as e:
            print(f"Error in generate_reply: {e}")
            return {"reply": "Error generating reply.", "duration": 0, "tokens": 0}

    def evaluate_qualitative(self, email_body, expected_reply, generated_reply):
        """Step 3: Ask Gemini to evaluate qualitative metrics."""
        prompt = EVALUATION_PROMPT.format(
            email_body=email_body,
            expected_reply=expected_reply,
            generated_reply=generated_reply
        )
        try:
            response = self.eval_model.generate_content(prompt)
            cleaned_json = clean_json_response(response.text)
            return json.loads(cleaned_json)
        except Exception as e:
            print(f"Error in evaluate_qualitative: {e}")
            return {}

    def get_coach_feedback(self, email_body, expected_reply, generated_reply, score):
        """Step 4: AI Coach for continuous improvement."""
        prompt = COACH_PROMPT.format(
            email_body=email_body,
            expected_reply=expected_reply,
            generated_reply=generated_reply,
            score=score
        )
        try:
            response = self.eval_model.generate_content(prompt)
            cleaned_json = clean_json_response(response.text)
            return json.loads(cleaned_json)
        except Exception as e:
            print(f"Error in coach: {e}")
            return {
                "critique": "Failed to generate critique.",
                "improvement_suggestions": [],
                "improved_reply": generated_reply
            }
