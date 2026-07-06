import json
import time
import os
import traceback
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from prompts import ANALYSIS_PROMPT, REPLY_PROMPT, EVALUATION_PROMPT, COACH_PROMPT
import re

# Setup logging
os.makedirs("logs", exist_ok=True)
def log_error(filename, error_msg, exception=None):
    with open(f"logs/{filename}", "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {error_msg}\n")
        if exception:
            f.write(traceback.format_exc() + "\n")

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def clean_json_response(response_text):
    """Clean markdown formatting from Gemini JSON response."""
    cleaned = re.sub(r'```json\s*', '', response_text)
    cleaned = re.sub(r'```\s*', '', cleaned)
    # find the first { and last } to handle trailing text
    start_idx = cleaned.find('{')
    end_idx = cleaned.rfind('}')
    if start_idx != -1 and end_idx != -1:
        cleaned = cleaned[start_idx:end_idx+1]
    return cleaned.strip()

class AIGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing. Check .env file.")
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        # For evaluation & coach, we might want lower temperature
        self.eval_model = genai.GenerativeModel(GEMINI_MODEL_NAME, generation_config={"temperature": 0.1})

    def _generate_with_retry(self, prompt, model_instance, retries=1):
        for attempt in range(retries + 1):
            try:
                response = model_instance.generate_content(prompt)
                return response
            except Exception as e:
                log_error("errors.log", f"Gemini API Error (Attempt {attempt+1}): {str(e)}", e)
                if attempt == retries:
                    raise e
                time.sleep(1)

    def analyze_email(self, email_body):
        """Step 1: AI Reasoning Pipeline - Extract intent, sentiment, etc."""
        prompt = ANALYSIS_PROMPT.format(email_body=email_body)
        try:
            start_time = time.time()
            response = self._generate_with_retry(prompt, self.model)
            duration = time.time() - start_time
            
            cleaned_json = clean_json_response(response.text)
            try:
                analysis = json.loads(cleaned_json)
            except json.JSONDecodeError as e:
                log_error("errors.log", f"JSON Parse Error in analyze_email: {response.text}", e)
                # Retry once for JSON parse error
                response = self._generate_with_retry(prompt, self.model)
                cleaned_json = clean_json_response(response.text)
                analysis = json.loads(cleaned_json)
                
            analysis['duration'] = duration
            
            with open("logs/generation.log", "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] analyze_email success. Duration: {duration:.2f}s\n")
            return analysis
        except Exception as e:
            error_msg = f"Generation Failed: {str(e)}"
            log_error("errors.log", f"Failed analyze_email completely: {str(e)}", e)
            return {"error": error_msg}

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
            response = self._generate_with_retry(prompt, self.model)
            duration = time.time() - start_time
            
            # Simple token estimation (1 token approx 4 characters)
            token_usage = len(prompt + response.text) // 4
            
            with open("logs/generation.log", "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] generate_reply success. Tokens: {token_usage}\n")
            
            return {
                "reply": response.text.strip(),
                "duration": duration,
                "tokens": token_usage
            }
        except Exception as e:
            error_msg = f"Generation Failed: {str(e)}"
            log_error("errors.log", f"Failed generate_reply completely: {str(e)}", e)
            return {"error": error_msg}

    def evaluate_qualitative(self, email_body, expected_reply, generated_reply):
        """Step 3: Ask Gemini to evaluate qualitative metrics."""
        prompt = EVALUATION_PROMPT.format(
            email_body=email_body,
            expected_reply=expected_reply,
            generated_reply=generated_reply
        )
        try:
            response = self._generate_with_retry(prompt, self.eval_model)
            cleaned_json = clean_json_response(response.text)
            try:
                res_json = json.loads(cleaned_json)
            except json.JSONDecodeError as e:
                log_error("errors.log", f"JSON Parse Error in evaluate_qualitative: {response.text}", e)
                response = self._generate_with_retry(prompt, self.eval_model)
                cleaned_json = clean_json_response(response.text)
                res_json = json.loads(cleaned_json)
                
            with open("logs/evaluation.log", "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] evaluate_qualitative success.\n")
            return res_json
        except Exception as e:
            error_msg = f"Evaluation Failed: {str(e)}"
            log_error("errors.log", f"Failed evaluate_qualitative completely: {str(e)}", e)
            return {"error": error_msg}

    def get_coach_feedback(self, email_body, expected_reply, generated_reply, score):
        """Step 4: AI Coach for continuous improvement."""
        prompt = COACH_PROMPT.format(
            email_body=email_body,
            expected_reply=expected_reply,
            generated_reply=generated_reply,
            score=score
        )
        try:
            response = self._generate_with_retry(prompt, self.eval_model)
            cleaned_json = clean_json_response(response.text)
            try:
                res_json = json.loads(cleaned_json)
            except json.JSONDecodeError as e:
                log_error("errors.log", f"JSON Parse Error in coach: {response.text}", e)
                response = self._generate_with_retry(prompt, self.eval_model)
                cleaned_json = clean_json_response(response.text)
                res_json = json.loads(cleaned_json)
                
            with open("logs/evaluation.log", "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] coach feedback success.\n")
            return res_json
        except Exception as e:
            error_msg = f"Coach Failed: {str(e)}"
            log_error("errors.log", f"Failed get_coach_feedback completely: {str(e)}", e)
            return {"error": error_msg}
