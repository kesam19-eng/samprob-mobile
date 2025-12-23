import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="SAMProb Mobile", page_icon="⚕️", layout="wide", initial_sidebar_state="collapsed")

# --- CORRECTION COULEURS (Haut Contraste) ---
st.markdown("""
    <style>
    /* On force le fond blanc ET le texte noir pour éviter le bug */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Style des boutons et zones de texte */
    .stButton>button {
        height: 3.5em; 
        border-radius: 12px; 
        font-weight: bold; 
        width: 100%; 
        border: 1px solid #ddd;
        color: #000000 !important; /* Texte bouton noir */
        background-color: #f0f2f6;
    }
    
    /* Bulles de discussion */
    .chat-bubble {
        padding: 15px; 
        border-radius: 15px; 
        margin-bottom: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: #000000 !important; /* Texte bulle noir */
    }
    .user-msg {background-color: #e3f2fd; border-right: 5px solid #2196f3; text-align: right;}
    .ai-msg {background-color: #f1f8e9; border-left: 5px solid #4caf50;}
    
    /* Titres et textes */
    h1, h2, h3, p, label, .stMarkdown {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CERVEAU ---
class CloudBrain:
    def __init__(self):
        self.model = None
    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            return True
        except: return False
    def ask(self, prompt, image=None):
        if not self.model: return "⚠️ Clé API non connectée. Entrez-la dans le menu."
        try:
            content = ["Tu es SAMProb, assistant médical expert. Sois concis.", prompt]
            if image: content.append(image)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur: {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = CloudBrain()
if 'history' not in st.session_state: st.session_state.history = []

# --- INTERFACE ---
with st.sidebar:
    st.title("⚙️ Réglages")
    key = st.text_input("Clé API Google", type="password")
    if key and st.session_state.brain.connect(key): st.success("Connecté ✅")

st.title("SAMProb Mobile")

tabs = st.tabs(["💬 CHAT", "📸 VISION", "⚡ URGENCES"])

with tabs[0]:
    # Affichage historique
    for msg in st.session_state.history:
        role = "user-msg" if msg['role'] == "user" else "ai-msg"
        st.markdown(f"<div class='chat-bubble {role}'><b>{'Moi' if msg['role']=='user' else 'SAMProb'} :</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Zone de saisie
    user_input = st.chat_input("Décrivez le cas clinique...")
    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.spinner("Analyse en cours..."):
            resp = st.session_state.brain.ask(user_input)
            st.session_state.history.append({"role": "assistant", "content": resp})
        st.rerun()

with tabs[1]:
    st.info("Prenez une photo de la lésion ou du document.")
    img = st.camera_input("Scanner")
    if img:
        st.image(img)
        if st.button("Lancer l'analyse visuelle"):
            with st.spinner("Vision par ordinateur..."):
                img_pil = Image.open(img)
                resp = st.session_state.brain.ask("Analyse cette image médicale (Radio, Plaie ou Bilan). Donne les anomalies visibles.", img_pil)
                st.success(resp)

with tabs[2]:
    st.error("PROTOCOLES VITAUX (Mode Réflexe)")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("❤️ ARRÊT CARDIAQUE"):
            st.info("MCE 30:2 | 100-120 bpm\nAdrénaline 1mg / 4min")
    with c2:
        if st.button("⚡ CHOC ANAPHYLACTIQUE"):
            st.warning("Adrénaline IM: 0.01 mg/kg\nRemplissage 20ml/kg")
