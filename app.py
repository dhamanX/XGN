import streamlit as st
from tavily import TavilyClient
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="XGN by Gravtian", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #000000; color: #ffffff; }
.main { background-color: #000000; }
.block-container { padding-top: 2rem; max-width: 780px; }
.stTextInput > div > div > input {
    background-color: #0d0d0d;
    border: 0.5px solid #2a2a2a;
    border-radius: 50px;
    color: #ffffff;
    padding: 1rem 1.5rem;
    font-size: 15px;
}
.stTextInput > div > div > input:focus { border-color: #555; }
.stTextInput > div > div > input::placeholder { color: #444; }
.xgn-logo { text-align: center; font-size: 56px; font-weight: 700; letter-spacing: 0.2em; color: #ffffff; margin-bottom: 4px; margin-top: 2rem; }
.xgn-tagline { text-align: center; font-size: 10px; letter-spacing: 0.3em; color: #333; margin-bottom: 2rem; }
.xgn-cats { display: flex; justify-content: center; gap: 8px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.xgn-cat { border: 0.5px solid #222; color: #555; font-size: 12px; padding: 5px 16px; border-radius: 20px; display: inline-block; cursor: pointer; }
.suggest-label { font-size: 10px; color: #333; letter-spacing: 0.15em; margin: 1.5rem 0 0.5rem; }
.suggest-item { background: #0d0d0d; border: 0.5px solid #1a1a1a; border-radius: 10px; padding: 10px 16px; font-size: 13px; color: #666; margin-bottom: 8px; cursor: pointer; }
.answer-label { font-size: 10px; color: #333; letter-spacing: 0.15em; margin: 1.5rem 0 0.5rem; }
.answer-box { background: #0d0d0d; border: 0.5px solid #1e1e1e; border-radius: 14px; padding: 20px 24px; font-size: 14px; line-height: 1.9; color: #cccccc; }
.action-row { display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap; }
.action-btn { border: 0.5px solid #222; background: none; color: #555; font-size: 12px; padding: 6px 16px; border-radius: 20px; cursor: pointer; display: inline-block; }
.sources-label { font-size: 10px; color: #333; letter-spacing: 0.15em; margin: 1.5rem 0 0.5rem; }
.source-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
.source-card { background: #0d0d0d; border: 0.5px solid #1a1a1a; border-radius: 10px; padding: 12px 14px; }
.source-title { font-size: 12px; color: #888; margin-bottom: 4px; font-weight: 500; }
.source-url { font-size: 11px; color: #333; }
.footer { text-align: center; font-size: 10px; color: #222; letter-spacing: 0.2em; margin-top: 3rem; padding-top: 1rem; border-top: 0.5px solid #111; padding-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="xgn-logo">XGN</div>', unsafe_allow_html=True)
st.markdown('<div class="xgn-tagline">UNDERSTAND THE INTELLIGENCE</div>', unsafe_allow_html=True)

st.markdown("""
<div class="xgn-cats">
    <span class="xgn-cat">Startups</span>
    <span class="xgn-cat">Finance</span>
    <span class="xgn-cat">Technology</span>
    <span class="xgn-cat">Market</span>
    <span class="xgn-cat">Research</span>
</div>
""", unsafe_allow_html=True)

query = st.text_input("", placeholder="What do you want to know?", label_visibility="collapsed")

if not query:
    st.markdown('<div class="suggest-label">TRY ASKING</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="suggest-item">💡 What are the biggest mistakes founders make when raising pre-seed?</div>
    <div class="suggest-item">📈 What are the top AI startups to watch in 2026?</div>
    <div class="suggest-item">🎯 How do I find product-market fit for a B2B SaaS?</div>
    """, unsafe_allow_html=True)

if query:
    with st.spinner(""):
        results = tavily.search(query=query, max_results=5)
        sources = results["results"]
        context = "\n\n".join([f"Source: {s['url']}\n{s['content']}" for s in sources])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are XGN, an AI research engine by Gravtian. Answer clearly, concisely and intelligently based on the sources provided. Format your answer in clean paragraphs."},
                {"role": "user", "content": f"Sources:\n{context}\n\nQuestion: {query}"}
            ]
        )
        answer = response.choices[0].message.content

        st.markdown('<div class="answer-label">ANSWER</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="action-row">
            <span class="action-btn" onclick="navigator.clipboard.writeText(`{answer[:100]}`)">📋 Copy</span>
            <span class="action-btn">👍 Like</span>
            <span class="action-btn">👎 Dislike</span>
            <span class="action-btn">🔗 Share</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sources-label">SOURCES</div>', unsafe_allow_html=True)
        source_cards = ""
        for s in sources:
            source_cards += f"""
            <div class="source-card" onclick="window.open('{s['url']}', '_blank')" style="cursor:pointer;">
                <div class="source-title">{s['title'][:50]}...</div>
                <div class="source-url" style="color:#555;">{s['url'][:40]}...</div>
            </div>"""
        st.markdown(f'<div class="source-grid">{source_cards}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">POWERED BY GRAVTIAN</div>', unsafe_allow_html=True)