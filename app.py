import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==============================================================================
# 1. CONFIGURATION & DESIGN
# ==============================================================================
st.set_page_config(page_title="SAMProb Expert", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

# Design Médical Vert
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; font-size: 18px !important; color: #1e1e1e !important; }
    .stApp { background-color: #f8f9fa; }
    h1 { color: #2e7d32 !important; font-size: 2.5rem !important; border-bottom: 2px solid #2e7d32; text-transform: uppercase; }
    h2, h3 { color: #1b5e20 !important; }
    .ai-box { background-color: #ffffff; border-left: 5px solid #2e7d32; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .stButton>button { height: 3.5em !important; font-size: 20px !important; border-radius: 8px !important; background-color: #2e7d32; color: white; width: 100%; border: none; }
    .urgence-box { background-color: #ffebee; border: 2px solid #c62828; color: #c62828; padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SÉCURITÉ ROBUSTE (Correction du Bug)
# ==============================================================================
if 'auth_sam' not in st.session_state:
    st.session_state.auth_sam = False

# Si pas connecté, on affiche l'écran de login et ON ARRÊTE le reste du script
if not st.session_state.auth_sam:
    st.markdown("<br><br><h1 style='text-align:center'>🧬 SAMProb</h1><h3 style='text-align:center'>IDENTIFICATION REQUISE</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Méthode directe sans callback complexe
        pwd = st.text_input("CODE D'ACTIVATION", type="password")
        
        if st.button("INITIALISER LE SYSTÈME"):
            if pwd == "SAMPROB2025":
                st.session_state.auth_sam = True
                st.rerun() # On recharge la page pour entrer
            else:
                st.error("⛔ CODE INCORRECT")
    
    st.stop() # Empêche l'exécution du reste du code tant que pas connecté

# ==============================================================================
# 3. MOTEUR INTELLIGENCE
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

    def analyze(self, prompt, image=None):
        if not self.api_valid: return "⚠️ ERREUR : Clé API non connectée (Voir Menu Config)."
        sys_prompt = "Tu es SAMProb, assistant expert en Chirurgie et Urgences. Structure ta réponse : 1. HYPOTHÈSES, 2. BILAN, 3. TRAITEMENT. Sois concis."
        try:
            content = [sys_prompt, prompt]
            if image: content.append(image)
            response = self.model.generate_content(content)
            return response.text
        except Exception as e: return f"Erreur réseau : {e}"

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. APPLICATION PRINCIPALE
# ==============================================================================
with st.sidebar:
    st.title("🧬 SAMProb V2")
    st.caption("Dr. SAMAKÉ")
    st.write("---")
    menu = st.radio("MODULES", ["💬 AVIS MÉDICAL", "👁️ VISION", "🧮 SCORES", "⚡ URGENCES", "⚙️ CONFIG"])
    st.write("---")
    if st.button("🔒 DÉCONNEXION"):
        st.session_state.auth_sam = False
        st.rerun()

# --- MODULES ---
if menu == "💬 AVIS MÉDICAL":
    st.title("CONSULTATION IA")
    if 'history' not in st.session_state: st.session_state.history = []
    
    for msg in st.session_state.history:
        style = "background:#e3f2fd;padding:15px;border-radius:10px;text-align:right" if msg['role']=='user' else "background:white;border-left:5px solid #2e7d32;padding:15px"
        st.markdown(f"<div style='{style}'><b>{'Dr. Samaké' if msg['role']=='user' else 'SAMProb'} :</b><br>{msg['text']}</div><br>", unsafe_allow_html=True)
            
    user_input = st.chat_input("Décrivez le cas clinique...")
    if user_input:
        st.session_state.history.append({"role": "user", "text": user_input})
        with st.spinner("Analyse..."):
            resp = st.session_state.brain.analyze(user_input)
            st.session_state.history.append({"role": "ai", "text": resp})
        st.rerun()

elif menu == "👁️ VISION":
    st.title("ANALYSE VISUELLE")
    src = st.radio("Source", ["Caméra", "Fichier"], horizontal=True)
    img_file = st.camera_input("Photo") if src == "Caméra" else st.file_uploader("Upload")
    if img_file and st.button("ANALYSER"):
        with st.spinner("Lecture..."):
            res = st.session_state.brain.analyze("Analyse cette image médicale (Plaie/Radio/ECG).", Image.open(img_file))
            st.markdown(f"<div class='ai-box'>{res}</div>", unsafe_allow_html=True)

elif menu == "🧮 SCORES":
    st.title("CALCULATEURS")
    t1, t2 = st.tabs(["GLASGOW", "WELLS"])
    with t1:
        y = st.selectbox("Yeux", [4,3,2,1], format_func=lambda x: f"{x} - {'Spontané' if x==4 else 'Voix' if x==3 else 'Douleur' if x==2 else 'Nul'}")
        v = st.selectbox("Verbal", [5,4,3,2,1], format_func=lambda x: f"{x} - {'Orienté' if x==5 else 'Confus' if x==4 else 'Inapproprié' if x==3 else 'Incompréhensible' if x==2 else 'Nul'}")
        m = st.selectbox("Moteur", [6,5,4,3,2,1], format_func=lambda x: f"{x} - {'Ordre' if x==6 else 'Orienté' if x==5 else 'Evitement' if x==4 else 'Flexion' if x==3 else 'Extension' if x==2 else 'Nul'}")
        sc = y+v+m
        st.metric("GLASGOW", f"{sc}/15")
        if sc<=8: st.error("COMA GRAVE")
    with t2:
        st.write("Cochez si présent (+1 point chaque):")
        s = sum([st.checkbox(l) for l in ["Cancer actif", "Paralysie/Plâtre", "Alitement >3j", "Douleur trajet veineux", "Oedème membre complet", "Oedème mollet >3cm"]])
        st.metric("WELLS", s)
        if s>=2: st.error("RISQUE ÉLEVÉ TVP")

elif menu == "⚡ URGENCES":
    st.title("PROTOCOLES VITAUX")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("❤️ ARRÊT CARDIAQUE"):
            st.error("MCE 30:2 | Adrénaline 1mg/4min | Choc si FV")
    with c2:
        if st.button("💉 CHOC ANAPHYLACTIQUE"):
            st.warning("Adrénaline IM 0.5mg | Remplissage | Corticoïdes")

elif menu == "⚙️ CONFIG":
    st.title("RÉGLAGES")
    key = st.text_input("CLÉ API GOOGLE", type="password")
    if key and st.button("CONNECTER"):
        if st.session_state.brain.connect(key): st.success("CONNECTÉ")
        else: st.error("ERREUR CLÉ")
