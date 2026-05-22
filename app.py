import streamlit as st
from tavily import TavilyClient
from groq import Groq

# API Keys
import os
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Setup
tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = Groq(api_key=GROQ_API_KEY)

# Page config
st.set_page_config(page_title="XGN by Gravtian", page_icon="⚡", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .main { background-color: #0a0a0a; }
    .block-container { padding-top: 4rem; max-width: 800px; }
    
    h1 {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: 0.3rem;
        text-align: center;
        color: #ffffff;
    }
    .subtitle {
        text-align: center;
        color: #555555;
        font-size: 0.8rem;
        letter-spacing: 0.2rem;
        margin-bottom: 2rem;
    }
    .powered {
        text-align: center;
        color: #333333;
        font-size: 0.7rem;
        letter-spacing: 0.15rem;
        margin-bottom: 3rem;
    }
    .stTextInput > div > div > input {
        background-color: #111111;
        border: 1px solid #222222;
        border-radius: 12px;
        color: #ffffff;
        padding: 1rem 1.5rem;
        font-size: 1rem;
    }
    .answer-box {
        background-color: #111111;
        border: 1px solid #1e1e1e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        line-height: 1.8;
        color: #e0e0e0;
    }
    .source-item {
        color: #444444;
        font-size: 0.8rem;
        margin: 0.3rem 0;
    }
    .source-item a { color: #555555; text-decoration: none; }
    .source-item a:hover { color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>XGN</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">UNDERSTAND THE INTELLIGENCE</p>', unsafe_allow_html=True)
st.markdown('<p class="powered">POWERED BY GRAVTIAN</p>', unsafe_allow_html=True)

# Search
query = st.text_input("", placeholder="Ask anything...")

if query:
    with st.spinner(""):
        results = tavily.search(query=query, max_results=5)
        sources = results["results"]
        context = "\n\n".join([f"Source: {s['url']}\n{s['content']}" for s in sources])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are XGN, an AI research engine by Gravtian. Answer clearly, concisely and intelligently based on sources provided."},
                {"role": "user", "content": f"Sources:\n{context}\n\nQuestion: {query}"}
            ]
        )

        answer = response.choices[0].message.content

        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="source-item">Sources</p>', unsafe_allow_html=True)
        for s in sources:
            st.markdown(f'<p class="source-item">→ <a href="{s["url"]}" target="_blank">{s["title"]}</a></p>', unsafe_allow_html=True)