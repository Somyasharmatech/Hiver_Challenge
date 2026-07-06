import streamlit as st
import json
import time
import os
import plotly.express as px
from utils import load_custom_css, generate_diff_html, create_radar_chart, create_gauge_chart
from generator import AIGenerator
from evaluator import Evaluator

st.set_page_config(page_title="AI Email Response Intelligence", layout="wide")

# Load CSS
load_custom_css()

# Initialize AI & Evaluator
@st.cache_resource
def load_ai_models():
    return AIGenerator(), Evaluator()

ai_gen, evaluator = load_ai_models()

# Load Dataset
@st.cache_data
def load_dataset():
    if os.path.exists('dataset.json'):
        with open('dataset.json', 'r') as f:
            return json.load(f)
    return []

dataset = load_dataset()

# Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'current_eval' not in st.session_state:
    st.session_state.current_eval = None
if 'coach_feedback' not in st.session_state:
    st.session_state.coach_feedback = None

# Sidebar Dashboard
with st.sidebar:
    st.markdown("<h2 class='text-gradient'>🧠 AI Dashboard</h2>", unsafe_allow_html=True)
    if not dataset:
        st.warning("Dataset not found. Run `dataset_generator.py`")
    
    # Analytics if history exists
    if st.session_state.history:
        avg_score = sum([h['eval']['Overall Score'] for h in st.session_state.history]) / len(st.session_state.history)
        st.metric("Avg AI Score", f"{avg_score:.1f}%")
        st.metric("Total Analyzed", len(st.session_state.history))
    
    st.markdown("---")
    if st.button("🔄 Clear History"):
        st.session_state.history = []
        st.session_state.current_analysis = None
        st.session_state.current_eval = None
        st.session_state.coach_feedback = None
        st.rerun()

# Main Header
st.markdown("<h1 class='text-gradient' style='text-align: center;'>AI Email Response Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A1A1AA; font-size: 1.2rem; margin-bottom: 2rem;'>Generate professional replies and auto-evaluate using advanced NLP metrics.</p>", unsafe_allow_html=True)

# Main Container
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📥 Customer Email")
    
    # Sample selection
    selected_sample = None
    is_benchmark_mode = False
    if dataset:
        sample_options = ["✍️ Custom Email (Real-world Mode)"] + [f"📄 Sample {i+1}: {d['category']} (Benchmark Mode)" for i, d in enumerate(dataset)]
        selection = st.selectbox("📂 Choose Input Source", sample_options)
        
        if selection != "✍️ Custom Email (Real-world Mode)":
            idx = int(selection.split(":")[0].replace("📄 Sample ", "")) - 1
            selected_sample = dataset[idx]
            is_benchmark_mode = True
    
    default_text = selected_sample['email_body'] if selected_sample else ""
    email_input = st.text_area("Paste customer email here", value=default_text, height=200, label_visibility="collapsed")
    
    expected_reply_input = ""
    if is_benchmark_mode and selected_sample:
        expected_reply_input = selected_sample['expected_reply']
        st.markdown("###### Expected Reply (For Evaluation Benchmark)")
        st.info(expected_reply_input[:100] + "...")
        
    if st.button("✨ Analyze & Generate Reply"):
        if not email_input.strip():
            st.error("Please enter an email.")
        else:
            with st.spinner("Pipeline Running..."):
                # 1. Reasoning Pipeline
                st.toast("Reading Email & Detecting Intent...")
                analysis = ai_gen.analyze_email(email_input)
                
                if "error" in analysis:
                    st.error(f"Reasoning Failed: {analysis['error']}")
                    st.stop()
                
                # 2. Reply Generation
                st.toast("Generating Professional Response...")
                gen_result = ai_gen.generate_reply(email_input, analysis)
                
                if "error" in gen_result:
                    st.error(f"Generation Failed: {gen_result['error']}")
                    st.stop()
                
                # 3. Qualitative Eval
                st.toast("Evaluating with NLP Metrics...")
                qual_metrics = ai_gen.evaluate_qualitative(email_input, expected_reply_input, gen_result['reply'])
                
                if "error" in qual_metrics:
                    st.error(f"Evaluation Failed: {qual_metrics['error']}")
                    st.stop()
                
                # 4. Final NLP Scoring
                if is_benchmark_mode:
                    eval_result = evaluator.run_full_evaluation(expected_reply_input, gen_result['reply'], qual_metrics)
                else:
                    eval_result = evaluator.run_realworld_evaluation(gen_result['reply'], qual_metrics)
                
                # Save to state
                st.session_state.current_analysis = {
                    "email": email_input,
                    "expected": expected_reply_input,
                    "analysis": analysis,
                    "generated": gen_result['reply'],
                    "time": gen_result['duration'],
                    "tokens": gen_result['tokens'],
                    "is_benchmark": is_benchmark_mode
                }
                st.session_state.current_eval = eval_result
                st.session_state.coach_feedback = None # Reset coach
                
                st.session_state.history.append({
                    "analysis": st.session_state.current_analysis,
                    "eval": st.session_state.current_eval
                })
    st.markdown("</div>", unsafe_allow_html=True)

    # AI Reasoning Chips
    if st.session_state.current_analysis:
        an = st.session_state.current_analysis['analysis']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🧠 AI Reasoning")
        st.markdown(f"""
        <div class='metric-chip'>Intent <span>{an.get('intent', 'N/A')}</span></div>
        <div class='metric-chip'>Emotion <span>{an.get('emotion', 'N/A')}</span></div>
        <div class='metric-chip'>Urgency <span>{an.get('urgency', 'N/A')}</span></div>
        <div class='metric-chip'>Confidence <span>{an.get('confidence', 'N/A')}%</span></div>
        """, unsafe_allow_html=True)
        st.caption(f"**Keywords:** {', '.join(an.get('keywords', []))}")
        st.caption(f"**Missing Information:** {', '.join(an.get('missing_information', ['None']))}")
        st.caption(f"**Summary:** {an.get('summary', 'N/A')}")
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if st.session_state.current_analysis and st.session_state.current_eval:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        eval_data = st.session_state.current_eval
        
        st.markdown(f"### {eval_data['Recommendation']} {eval_data['Stars']}")
        
        # Display Generated Reply
        st.markdown("###### ✉️ Generated AI Reply")
        st.success(st.session_state.current_analysis['generated'])
        
        c1, c2 = st.columns(2)
        c1.caption(f"⏱️ Time: {st.session_state.current_analysis['time']:.2f}s")
        c2.caption(f"🪙 Tokens: ~{st.session_state.current_analysis['tokens']}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Dashboard
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Explainable Evaluation Dashboard")
        
        g1, g2 = st.columns([1, 1])
        with g1:
            st.plotly_chart(create_gauge_chart(eval_data['Overall Score']), use_container_width=True)
        with g2:
            st.plotly_chart(create_radar_chart(eval_data['Metrics']), use_container_width=True)
        
        # Metric Grid
        metrics = eval_data['Metrics']
        cols = st.columns(3)
        keys = list(metrics.keys())
        for i, key in enumerate(keys):
            with cols[i % 3]:
                st.markdown(f"**{key}**: {metrics[key]['score']}")
                st.markdown(f"<div class='score-reason'>{metrics[key]['reason']}</div>", unsafe_allow_html=True)
                st.write("")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Expected vs Generated Diff (Only in Benchmark Mode)
        if st.session_state.current_analysis.get('is_benchmark', False):
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🔍 Semantic Comparison (Expected vs Generated)")
            diff_html = generate_diff_html(st.session_state.current_analysis['expected'], st.session_state.current_analysis['generated'])
            st.markdown(f"<div style='line-height: 1.6; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px;'>{diff_html}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # AI Coach Feature
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🎓 AI Coach (Iterative Improvement)")
        if not st.session_state.coach_feedback:
            if st.button("Review & Improve Reply"):
                with st.spinner("AI Coach analyzing..."):
                    feedback = ai_gen.get_coach_feedback(
                        st.session_state.current_analysis['email'],
                        st.session_state.current_analysis['expected'],
                        st.session_state.current_analysis['generated'],
                        eval_data['Overall Score']
                    )
                    st.session_state.coach_feedback = feedback
                    st.rerun()
        else:
            fb = st.session_state.coach_feedback
            if "error" in fb:
                st.error(f"Coach Failed: {fb['error']}")
            else:
                st.success(f"**Expected Score:** {fb.get('Expected_Score', 'N/A')}% (Up from {eval_data['Overall Score']}%)")
                st.markdown("###### ✅ Strengths:")
                for s in fb.get('Strengths', []):
                    st.markdown(f"- {s}")
                st.markdown("###### 🎯 Weaknesses:")
                for w in fb.get('Weaknesses', []):
                    st.markdown(f"- {w}")
                st.markdown("###### ✨ Improved Reply:")
                st.info(fb.get('Improved_Reply', ''))
        st.markdown("</div>", unsafe_allow_html=True)
