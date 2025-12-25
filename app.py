import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. ARCHITECTURE VISUELLE "DEEP BLACK OLED" (Base du Code 2)
# ==============================================================================
st.set_page_config(page_title="SAMProb Fusion OS", page_icon="💠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* IMPORT FONT TECHNOLOGIQUE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* GLOBAL DARK THEME */
    .stApp {
        background-color: #050505; /* Noir Profond OLED */
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* HEADERS */
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -0.5px; }
    
    /* NAVIGATION DU HAUT (TABS) */
    div[data-testid="stTabs"] button {
        font-size: 18px;
        font-weight: bold;
        color: #888;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #00ADB5 !important;
        border-bottom-color: #00ADB5 !important;
    }

    /* BOUTONS SCANNER (Style Code 2) */
    .btn-scan {
        border-radius: 12px;
        padding: 10px;
        font-weight: 600;
    }

    /* BOUTONS TACTIQUES (Style Code 1 - Adapté au Dark Mode) */
    div.stButton > button {
        background-color: #1a1a1a;
        border: 1px solid #333;
        color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        font-size: 20px;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        border-color: #00ADB5;
        background-color: #0f1f22;
        color: #00ADB5;
        transform: translateY(-2px);
    }
    
    /* ALERTS & RESULTATS IA */
    .ai-result {
        background-color: #002626; 
        border-left: 4px solid #00ADB5; 
        padding: 20px; 
        border-radius: 5px; 
        color: #e0e0e0;
        margin-top: 15px;
        font-family: 'Courier New', monospace;
    }
    
    .suspicious-mass {
        border: 2px dashed #ff4b4b;
        background-color: rgba(255, 75, 75, 0.1);
        padding: 15px;
        border-radius: 8px;
        color: #ff4b4b;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* PROBE STATUS */
    .probe-badge {
        background-color: #00ADB5; color: black; padding: 4px 12px; border-radius: 20px; font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SÉCURITÉ (Code 1)
# ==============================================================================
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br><h1 style='text-align:center'>🔒 SÉCURITÉ SAMPROB</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        pwd = st.text_input("CODE D'ACCÈS", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == "SAMPROB2025":
                st.session_state.auth = True
                st.rerun()
            else: st.error("CODE ERRONÉ")
    st.stop()

# ==============================================================================
# 3. CERVEAU IA UNIFIÉ (Code 1 + Code 2 Logic)
# ==============================================================================
class Brain:
    def __init__(self):
        self.connected = False
        self.model = None

    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.connected = True
            return True
        except: return False

    # Logique du Code 1 (Triage Médical)
    def triage_clinique(self, texte, contexte):
        if not self.connected: return "⚠️ IA HORS-LIGNE. Connectez la clé."
        
        system_prompt = f"""
        TU ES : SAMProb, assistant médical expert.
        CONTEXTE : {contexte} (Adapte tes réponses : Si Rural -> Solutions simples. Si Urbain -> Examens de pointe).
        
        TACHE : Analyse clinique.
        FORMAT DE RÉPONSE :
        A. SYNTHÈSE & RED FLAGS
        B. DIAGNOSTIC PROBABLE
        C. PLAN D'ACTION (Examens + Traitement adapté au contexte {contexte})
        D. EXPLICATION PATIENT
        """
        try:
            return self.model.generate_content([system_prompt, f"CAS : {texte}"]).text
        except Exception as e: return f"Erreur : {str(e)}"

    # Logique du Code 2 (Analyse Image)
    def analyse_image(self, prompt, context, images=None):
        if not self.connected: return "⚠️ IA HORS-LIGNE."
        try:
            full_prompt = [f"ROLE: Medical Imaging AI. CONTEXT: {context}. TASK: {prompt}"]
            if images: full_prompt.extend(images)
            return self.model.generate_content(full_prompt).text
        except: return "Erreur d'analyse."

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. BARRE LATÉRALE (FUSION : PROBES + CONTEXTE)
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/00ADB5/ultrasound.png", width=60)
    st.title("SAMProb OS")
    st.caption("v7.0 Ultimate Fusion")
    
    st.divider()
    
    # --- LOGIQUE CODE 1 : CONTEXTE ---
    st.subheader("📍 CONTEXTE (Code 1)")
    contexte_medical = st.radio(
        "Zone d'intervention :",
        ["Urbain (CHU/Plateau Technique)", "Rural (CS/Ressources Limitées)"],
        index=0
    )
    
    st.divider()

    # --- LOGIQUE CODE 2 : PROBES ---
    st.subheader("🔌 SONDES (Code 2)")
    p1 = st.toggle("Cardio Probe", value=True)
    p2 = st.toggle("Abdo Probe", value=False)
    
    active_probe = "Cardio" if p1 else ("Abdo" if p2 else "None")
    st.caption(f"Active: **{active_probe}**")
    
    st.divider()
    
    # --- SECURITE ---
    k = st.text_input("🔑 CLÉ NEURALE", type="password")
    if k and st.session_state.brain.connect(k): 
        st.success("CORTEX EN LIGNE")
        
    if st.button("🔒 VERROUILLER"):
        st.session_state.auth = False
        st.rerun()

# ==============================================================================
# 5. NAVIGATION PRINCIPALE (ONGLÉTS)
# ==============================================================================
# C'est ici que la fusion opère : On sépare l'Imagerie (Code 2) de l'Assistant (Code 1)
tab_scan, tab_assistant, tab_admin = st.tabs(["📡 IMAGERIE (SCAN)", "👨‍⚕️ ASSISTANT (TRIAGE)", "📝 DOCUMENTS"])

# ==============================================================================
# ONGLET 1 : L'INTERFACE D'IMAGERIE (CODE 2 PUR)
# ==============================================================================
with tab_scan:
    # REPLIQUE DU CODE 2 (Interface Scan)
    col_settings, col_viz = st.columns([1, 3])
    
    with col_settings:
        st.markdown("### ⚙️ RÉGLAGES")
        st.info(f"Mode : **{contexte_medical.split(' ')[0]}**")
        
        # Sélecteur Scan (Code 2)
        scan_type = st.radio("MODE D'IMAGE", ["2D Standard", "Volumetric 3D", "Photoacoustic"], label_visibility="collapsed")
        
        st.markdown("**PARAMÈTRES**")
        depth = st.slider("Profondeur (cm)", 2, 25, 12)
        gain = st.select_slider("Gain (dB)", options=["Low", "Med", "High"], value="Med")
        
        st.divider()
        if st.button("🔵 FREEZE", use_container_width=True):
            st.toast("Image Gelée")

    with col_viz:
        st.markdown("### 🖥️ TEMPS RÉEL")
        
        # Visualisation Simulée (Code 2)
        if scan_type == "2D Standard":
            st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", caption="Flux 2D Live", use_column_width=True)
            st.markdown("<div class='suspicious-mass'>⚠️ SUSPICIOUS MASS (89%)</div>", unsafe_allow_html=True)
            
        elif scan_type == "Volumetric 3D":
            st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", caption="Reconstruction 3D", use_column_width=True)
            
        elif scan_type == "Photoacoustic":
            c_img, c_graph = st.columns(2)
            with c_img:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Hb/Oxy Heatmap")
            with c_graph:
                st.line_chart(pd.DataFrame(np.random.randn(20, 2) + [10, 5], columns=['Hb', 'HbO2']))

    # Analyse IA Image
    if st.button("🤖 ANALYSER L'IMAGE (IA)"):
        res = st.session_state.brain.analyse_image(f"Analyse image {scan_type}", context=contexte_medical)
        st.info(res)

# ==============================================================================
# ONGLET 2 : L'ASSISTANT MÉDICAL (CODE 1 PUR)
# ==============================================================================
with tab_assistant:
    # REPLIQUE DU CODE 1 (Les 3 boutons et la logique Triage)
    
    st.markdown("### 🚑 TRIAGE & URGENCES")
    
    col_urg, col_consul = st.columns([1, 2])
    
    with col_urg:
        # BOUTON ROUGE (CODE 1)
        if st.button("🔴 URGENCES VITALES\n(Protocoles)"):
            st.session_state.sub_mode = "RED"
        
        # Affichage des protocoles si cliqué
        if 'sub_mode' in st.session_state and st.session_state.sub_mode == "RED":
            st.error("PROTOCOLES HORS-LIGNE")
            with st.expander("❤️ ARRÊT CARDIAQUE (ACR)", expanded=True):
                st.write("- MCE 100-120 bpm")
                st.write("- Adrénaline 1mg / 4 min")
            with st.expander("🐝 CHOC ANAPHYLACTIQUE"):
                st.write("- Adrénaline IM 0.5mg")
                st.write("- Remplissage 20ml/kg")
    
    with col_consul:
        # BOUTON JAUNE (CODE 1) - LA CONSULTATION IA
        st.markdown("#### 🧠 IA CLINIQUE")
        txt_input = st.text_area("Symptômes / Cas Clinique", height=100, placeholder="Ex: Douleur thoracique atypique, troponine négative...")
        
        if st.button("🟡 ANALYSE DIAGNOSTIQUE (IA)"):
            if txt_input:
                with st.spinner(f"Analyse contextuelle ({contexte_medical})..."):
                    rep = st.session_state.brain.triage_clinique(txt_input, contexte_medical)
                    st.markdown(f"<div class='ai-result'>{rep}</div>", unsafe_allow_html=True)
            else:
                st.warning("Veuillez décrire le cas.")

# ==============================================================================
# ONGLET 3 : ADMINISTRATIF (CODE 1 - PARTIE VERTE)
# ==============================================================================
with tab_admin:
    # REPLIQUE DU CODE 1 (Bouton Vert / Rapports)
    st.markdown("### 🟢 GESTION DOSSIERS")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Générateur de Rapport")
        pat = st.text_input("Patient")
        diag = st.text_input("Diagnostic Final")
        traitement = st.text_area("Conduite à Tenir")
        
        if st.button("GÉNÉRER DOCUMENT PDF"):
            doc = f"""
            SAMProb REPORT - {contexte_medical}
            Date: {datetime.date.today()}
            --------------------------------
            PATIENT : {pat}
            DIAGNOSTIC : {diag}
            
            TRAITEMENT :
            {traitement}
            
            Dr. SAMAKÉ
            """
            st.session_state.last_doc = doc
            st.success("Rapport généré !")
            
    with c2:
        if 'last_doc' in st.session_state:
            st.text_area("Aperçu", st.session_state.last_doc, height=300)
            st.download_button("📥 TÉLÉCHARGER", st.session_state.last_doc)
