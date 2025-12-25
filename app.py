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
        style = "background:#e3f2fd;padding:15px;border-radius:10px;text-align:right" if msg['role']=='user' else "background:white;border-left:5px solid #2e7d32;padding:15px"
        st.markdown(f"<div style='{style}'><b>{'Moi' if msg['role']=='user' else 'SAMProb'} :</b><br>{msg['text']}</div><br>", unsafe_allow_html=True)
            
    user_input = st.chat_input("Cas clinique...")
    if user_input:
        st.session_state.history.append({"role": "user", "text": user_input})
        with st.spinner("Réflexion..."):
            resp = st.session_state.brain.analyze(user_input)
            st.session_state.history.append({"role": "ai", "text": resp})
        st.rerun()

# --- MODULE VISION (AVEC BOUTON ON/OFF) ---
elif menu == "👁️ VISION (MULTI)":
    st.title("ANALYSE D'IMAGES")
    
    # Gestion de l'état de la caméra (ON/OFF)
    if 'cam_active' not in st.session_state:
        st.session_state.cam_active = False

    st.info("Importez des fichiers ou activez la caméra.")

    # 1. BOUTON D'ACTIVATION CAMÉRA
    if not st.session_state.cam_active:
        if st.button("📸 ALLUMER LA CAMÉRA"):
            st.session_state.cam_active = True
            st.rerun()
    else:
        # Caméra active -> On affiche le widget ET le bouton pour éteindre
        st.markdown("<div class='stop-btn'>", unsafe_allow_html=True)
        if st.button("❌ ÉTEINDRE LA CAMÉRA (Économie Batterie)"):
            st.session_state.cam_active = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        img_cam = st.camera_input("PRENDRE PHOTO")

    # 2. UPLOAD MULTIPLE
    uploaded_files = st.file_uploader("📂 FICHIERS (GALERIE)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    
    # Rassemblement des images
    images_to_analyze = []
    
    # Récupération photo caméra (si active et prise)
    if st.session_state.cam_active and 'img_cam' in locals() and img_cam:
        st.image(img_cam, caption="Photo Caméra", width=150)
        images_to_analyze.append(Image.open(img_cam))
    
    # Récupération fichiers uploadés
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} fichiers importés :**")
        cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            img = Image.open(file)
            images_to_analyze.append(img)
            cols[i].image(img, use_container_width=True)

    # BOUTON ANALYSE
    if images_to_analyze:
        if st.button(f"LANCER L'ANALYSE ({len(images_to_analyze)} images)"):
            with st.spinner("Analyse groupée en cours..."):
                prompt_text = "Analyse ces images médicales. Décris les lésions, fractures ou anomalies visibles sur l'ensemble des clichés."
                res = st.session_state.brain.analyze(prompt_text, images=images_to_analyze)
                st.markdown(f"<div class='ai-box'>{res}</div>", unsafe_allow_html=True)

# --- AUTRES MODULES ---
elif menu == "🧮 SCORES":
    st.title("SCORES")
    t1, t2 = st.tabs(["GLASGOW", "WELLS"])
    with t1:
        y = st.selectbox("YEUX", [4,3,2,1], format_func=lambda x: f"{x}-Spontané" if x==4 else f"{x}-Voix" if x==3 else f"{x}-Douleur" if x==2 else f"{x}-Nul")
        v = st.selectbox("VERBAL", [5,4,3,2,1], format_func=lambda x: f"{x}-Orienté" if x==5 else f"{x}-Confus" if x==4 else f"{x}-Inapp" if x==3 else f"{x}-Incomp" if x==2 else f"{x}-Nul")
        m = st.selectbox("MOTEUR", [6,5,4,3,2,1], format_func=lambda x: f"{x}-Ordre" if x==6 else f"{x}-Orienté" if x==5 else f"{x}-Evit" if x==4 else f"{x}-Flex" if x==3 else f"{x}-Ext" if x==2 else f"{x}-Nul")
        st.metric("TOTAL", y+v+m)
    with t2:
        s = sum([st.checkbox(l) for l in ["Cancer", "Immobilisation", "Alitement", "Douleur Veine", "Oedème Global", "Oedème >3cm"]])
        st.metric("TOTAL", s)

elif menu == "⚡ URGENCES":
    st.title("URGENCES")
    if st.button("❤️ ACR (Arrêt Cardiaque)"): st.error("MCE 30:2 | Adré 1mg/4min")
    if st.button("💉 CHOC ANAPHYLACTIQUE"): st.warning("Adré IM 0.01mg/kg | Remplissage")

elif menu == "⚙️ CONFIG":
    st.title("CONFIG")
    k = st.text_input("CLÉ API", type="password")
    if st.button("CONNECTER") and k:
        if st.session_state.brain.connect(k): st.success("OK")
        else: st.error("ERREUR")
