import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==============================================================================
# 1. CONFIGURATION & DESIGN
# ==============================================================================
st.set_page_config(page_title="SAMProb Expert", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; font-size: 18px !important; color: #1e1e1e !important; }
    .stApp { background-color: #f8f9fa; }
    h1 { color: #2e7d32 !important; font-size: 2.2rem !important; border-bottom: 2px solid #2e7d32; text-transform: uppercase; }
    .ai-box { background-color: #ffffff; border-left: 5px solid #2e7d32; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .stButton>button { height: 3.5em !important; font-size: 20px !important; border-radius: 8px !important; background-color: #2e7d32; color: white; width: 100%; border: none; }
    
    /* Bouton spécifique pour éteindre (Rouge) */
    .stop-btn>button { background-color: #c62828 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SÉCURITÉ
# ==============================================================================
if 'auth_sam' not in st.session_state: st.session_state.auth_sam = False

if not st.session_state.auth_sam:
    st.markdown("<br><h1 style='text-align:center'>🧬 SAMProb</h1><h3 style='text-align:center'>IDENTIFICATION</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("CODE D'ACTIVATION", type="password")
        if st.button("INITIALISER"):
            if pwd == "SAMPROB2025":
                st.session_state.auth_sam = True
                st.rerun()
            else: st.error("⛔ CODE INCORRECT")
    st.stop()

# ==============================================================================
# 3. CERVEAU IA
# ==============================================================================
class Brain:
    def __init__(self):
        self.model = None
        self.api_valid = False

    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.api_valid = True
            return True
        except: return False

    def analyze(self, prompt, images=None):
        if not self.api_valid: return "⚠️ ERREUR : Connectez la clé API dans CONFIG."
        sys_prompt = "Tu es SAMProb, assistant expert en Chirurgie et Urgences. Structure ta réponse : 1. OBSERVATION, 2. HYPOTHÈSES, 3. CONDUITE À TENIR. Sois concis."
        try:
            content = [sys_prompt, prompt]
            if images: content.extend(images)
            response = self.model.generate_content(content)
            return response.text
        except Exception as e: return f"Erreur IA : {e}"

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. APPLICATION
# ==============================================================================
with st.sidebar:
    st.title("🧬 SAMProb V3.1")
    st.caption("Dr. SAMAKÉ")
    menu = st.radio("MENU", ["💬 AVIS MÉDICAL", "👁️ VISION (MULTI)", "🧮 SCORES", "⚡ URGENCES", "⚙️ CONFIG"])
    if st.button("🔒 SORTIR"):
        st.session_state.auth_sam = False
        st.rerun()

# --- MODULE AVIS ---
if menu == "💬 AVIS MÉDICAL":
    st.title("CONSULTATION IA")
    if 'history' not in st.session_state: st.session_state.history = []
    
    for msg in st.session_state.history:
        style = "background:#e3f2fd;padding:15px;border-radius:
