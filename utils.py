import streamlit as st
import difflib
import plotly.graph_objects as go
import plotly.express as px

def load_custom_css():
    st.markdown("""
    <style>
    /* Hide Streamlit default UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Fonts & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #09090B !important;
        color: #FFFFFF !important;
    }
    
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: rgba(24, 24, 27, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(124, 58, 237, 0.3);
    }
    
    /* Gradients */
    .text-gradient {
        background: linear-gradient(90deg, #7C3AED, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Primary Button Animation */
    .stButton>button {
        background: linear-gradient(90deg, #7C3AED, #3B82F6);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5);
        color: white;
    }
    
    /* Metrics / Chips */
    .metric-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-right: 8px;
        margin-bottom: 8px;
        color: #A1A1AA;
    }
    .metric-chip span {
        color: white;
        font-weight: 600;
        margin-left: 4px;
    }
    
    /* Diff Highlight */
    .diff-del { background-color: rgba(239, 68, 68, 0.2); color: #FCA5A5; text-decoration: line-through; }
    .diff-add { background-color: rgba(16, 185, 129, 0.2); color: #6EE7B7; }
    
    /* Score box */
    .score-reason {
        font-size: 12px;
        color: #9CA3AF;
        margin-top: 4px;
    }
    
    </style>
    """, unsafe_allow_html=True)

def generate_diff_html(expected, generated):
    d = difflib.ndiff(expected.split(), generated.split())
    html = []
    for word in d:
        if word.startswith("- "):
            html.append(f'<span class="diff-del">{word[2:]}</span>')
        elif word.startswith("+ "):
            html.append(f'<span class="diff-add">{word[2:]}</span>')
        elif word.startswith("  "):
            html.append(word[2:])
    return " ".join(html)

def create_radar_chart(metrics_dict):
    categories = list(metrics_dict.keys())
    values = [metrics_dict[cat]["score"] for cat in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values + [values[0]],
      theta=categories + [categories[0]],
      fill='toself',
      line=dict(color='#7C3AED'),
      fillcolor='rgba(124, 58, 237, 0.2)'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], color='#FFFFFF'),
        angularaxis=dict(color='#FFFFFF')
      ),
      paper_bgcolor='rgba(0,0,0,0)',
      plot_bgcolor='rgba(0,0,0,0)',
      showlegend=False,
      margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

def create_gauge_chart(score):
    if score >= 90:
        color = "#10B981" # Green
    elif score >= 70:
        color = "#F59E0B" # Yellow
    else:
        color = "#EF4444" # Red
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Quality", 'font': {'color': 'white', 'size': 20}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 70], 'color': "rgba(239,68,68,0.2)"},
                {'range': [70, 90], 'color': "rgba(245,158,11,0.2)"},
                {'range': [90, 100], 'color': "rgba(16,185,129,0.2)"}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
