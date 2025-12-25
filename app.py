import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. ARCHITECTURE & DESIGN (NEURO-OS)
# ==============================================================================
st.set_page_config(page_title="SAMProb Neuro-OS", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* THEME SOMBRE PROFOND (OLED) */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* NAVIGATION */
    .nav-header { font-size: 14px; color: #888; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* BOUTONS SCAN (Mode Visuel) */
    .stButton>button { border-radius: 8px; font-weight: 600; }
    
    /* ZONES DE TEXTE (Mode Bureau) */
    .stTextArea>div>div>textarea { background-color: #1a1a1a; color: white; border: 1px solid #333; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border: 1px solid #333; }
    
    /* MESSAGES IA (Assistant) */
    .chat-user { background-color: #2b2b2b; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right; }
    .chat-ai { background-color: #003333; border-left: 4px solid #00ADB5; padding: 10px; border-radius: 10px; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LE CERVEAU CENTRAL (INTELLIGENCE UNIFIÉE)
# ==============================================================================
class NeuralCore:
    def __init__(self):
        self.model = None
        self.connected = False
        self.history = [] # Mémoire de conversation
    
    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.connected = True
            return True
        except: return False

    def assistant_clinique(self, user_input, context="General"):
        if not self.connected: return "⚠️ IA HORS-LIGNE. Veuillez connecter la clé neurale."
        
        system_prompt = f"""
        TU ES : L'Assistant Médical Intégré du SAMProb.
        CONTEXTE ACTUEL : {context}.
        
        TES CAPACITÉS :
        1. Aide au diagnostic (Symptômes -> Probabilités).
        2. Protocoles thérapeutiques (Posologies, Urgences).
        3. Rédaction médicale (Transformer des notes en rapports formels).
        
        STYLE DE RÉPONSE : Précis, Clinique, Structuré (Listes à puces).
        """
        full_query = f"{system_prompt}\n\nQUESTION DU MÉDECIN : {user_input}"
        try:
            response = self.model.generate_content(full_query).text
            return response
        except Exception as e: return f"Erreur cognitive : {str(e)}"

    def generer_rapport(self, type_doc, data):
        prompt = f"""
        RÉDIGE UN DOCUMENT MÉDICAL FORMEL.
        TYPE : {type_doc}
        DONNÉES BRUTES : {data}
        
        FORMAT : Professionnel, prêt à être imprimé ou envoyé au PACS.
        Inclus : En-tête, Anamnèse, Examen, Conclusion.
        """
        return self.assistant_clinique(prompt, context="SECRETARIAT MÉDICAL")

if 'core' not in st.session_state: st.session_state.core = NeuralCore()

# ==============================================================================
# 3. BARRE LATÉRALE : NAVIGATION & MATÉRIEL
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/50/00ADB5/dna-helix.png", width=50)
    st.markdown("## SAMProb OS™")
    st.caption("v6.0 | Unified Medical Platform")
    
    st.divider()
    
    # --- CENTRE DE NAVIGATION ---
    st.markdown("<p class='nav-header'>MODULES</p>", unsafe_allow_html=True)
    app_mode = st.radio("SÉLECTIONNER INTERFACE :", 
        ["📡 IMAGERIE (SCAN)", "🧠 ASSISTANT CLINIQUE", "📝 BUREAU & RAPPORTS"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # --- GESTION SONDES (Visible partout) ---
    st.markdown("<p class='nav-header'>ÉTAT MATÉRIEL</p>", unsafe_allow_html=True)
    st.info(f"Sonde Active : **Cardio (Phased Array)**")
    st.progress(88, text="Batterie Tablette")
    
    # Connexion IA
    with st.expander("🔐 CLÉ NEURALE"):
        k = st.text_input("API Key", type="password")
        if st.button("CONNECTER"):
            if st.session_state.core.connect(k): st.success("CORTEX ACTIF")

# ==============================================================================
# MODULE A : IMAGERIE (LE CORPS - TON CODE VISUEL)
# ==============================================================================
if app_mode == "📡 IMAGERIE (SCAN)":
    st.title("IMAGERIE HYBRIDE")
    
    # --- COMMANDES ---
    c_ctrl, c_view = st.columns([1, 3])
    
    with c_ctrl:
        st.markdown("### RÉGLAGES")
        mode_scan = st.selectbox("MODE D'ACQUISITION", ["2D Standard", "Doppler Couleur", "Photoacoustique (Hb)", "Fusion 3D"])
        
        st.slider("PROFONDEUR (cm)", 2, 25, 12)
        st.slider("GAIN (dB)", 0, 100, 60)
        st.slider("FOCUS", 1, 5, 2)
        
        st.divider()
        if st.button("❄️ FREEZE", type="primary", use_container_width=True):
            st.toast("Image Gelée")
        if st.button("📸 CAPTURE DICOM", use_container_width=True):
            st.toast("Sauvegardé dans PACS Local")

    # --- VISUALISATION ---
    with c_view:
        # Simulation d'écran d'échographie
        if mode_scan == "Photoacoustique (Hb)":
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Analyse Spectrale Tissulaire", use_column_width=True)
            # Graphe spectral
            chart_data = pd.DataFrame(np.random.randn(20, 2) + [5, 5], columns=['Oxy-Hb', 'Deoxy-Hb'])
            st.line_chart(chart_data, height=200)
            
        elif mode_scan == "Fusion 3D":
            st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", caption="Reconstruction Volumétrique Temps Réel", use_column_width=True)
            
        else:
            st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", caption="Flux 2D Temps Réel", use_column_width=True)

# ==============================================================================
# MODULE B : ASSISTANT CLINIQUE (L'ESPRIT - CHATBOT MÉDICAL)
# ==============================================================================
elif app_mode == "🧠 ASSISTANT CLINIQUE":
    st.title("ASSISTANT DIAGNOSTIC & THÉRAPEUTIQUE")
    st.caption("Interrogez SAMProb sur des cas complexes, des posologies ou des protocoles.")
    
    # Historique simulé pour l'exemple
    st.markdown("""
    <div class='chat-user'>Patient de 45 ans, douleur thoracique atypique, ECG normal. Troponine négative.</div>
    <div class='chat-ai'>
    <b>Analyse SAMProb :</b><br>
    Le risque coronarien semble faible (Score HEART bas).<br>
    <b>Diagnostics différentiels à évoquer :</b>
    <ul>
    <li>Douleur pariétale / Musculaire (Syndrome de Tietze)</li>
    <li>Reflux Gastro-Oesophagien (RGO)</li>
    <li>Péricardite débutante (À recontrôler écho)</li>
    </ul>
    <b>Conduite à tenir suggérée :</b><br>
    Traitement d'épreuve IPP + Antalgiques simples. Surveillance ambulatoire.
    </div>
    """, unsafe_allow_html=True)
    
    # Zone d'interaction réelle
    user_q = st.chat_input("Posez votre question clinique ici...")
    if user_q:
        st.markdown(f"<div class='chat-user'>{user_q}</div>", unsafe_allow_html=True)
        with st.spinner("Analyse clinique en cours..."):
            rep = st.session_state.core.assistant_clinique(user_q, context="Consultation Médecine Générale")
            st.markdown(f"<div class='chat-ai'>{rep}</div>", unsafe_allow_html=True)

# ==============================================================================
# MODULE C : BUREAU & RAPPORTS (LA STATION DE TRAVAIL)
# ==============================================================================
elif app_mode == "📝 BUREAU & RAPPORTS":
    st.title("STATION DE TRAVAIL ADMINISTRATIVE")
    
    tab1, tab2, tab3 = st.tabs(["📄 COMPTE-RENDU", "🌙 RAPPORT DE GARDE", "📋 STAFF/TRANSMISSION"])
    
    # --- GÉNÉRATEUR DE CR D'EXAMEN ---
    with tab1:
        st.subheader("Générateur de Compte-Rendu Automatique")
        col_form, col_res = st.columns(2)
        
        with col_form:
            pat_name = st.text_input("Nom Patient")
            exam_type = st.selectbox("Examen réalisé", ["Échographie Abdominale", "Échographie Cardiaque", "Consultation Standard"])
            observations = st.text_area("Notes brutes (ex: Foie normal, reins ok, pas de calculs)", height=150)
            
            if st.button("GÉNÉRER LE DOCUMENT OFFICIEL"):
                if observations:
                    with st.spinner("Rédaction formelle..."):
                        res_rapport = st.session_state.core.generer_rapport(f"Compte-Rendu {exam_type}", f"Patient: {pat_name}. Notes: {observations}")
                        st.session_state.last_report = res_rapport
                else: st.error("Notes manquantes")
        
        with col_res:
            if 'last_report' in st.session_state:
                st.text_area("Aperçu Document", st.session_state.last_report, height=400)
                st.download_button("📥 TÉLÉCHARGER PDF", st.session_state.last_report)

    # --- GESTION DE GARDE ---
    with tab2:
        st.subheader("Journal de Garde")
        st.info("Saisissez les événements de la nuit pour générer le rapport de transmission matinal.")
        
        evt_nuit = st.text_area("Événements marquants (ex: 2h00 Admission AVC, 4h00 Décès lit 3...)", height=100)
        if st.button("CRÉER RAPPORT DE TRANSMISSION"):
            with st.spinner("Synthèse..."):
                synthese = st.session_state.core.assistant_clinique(
                    f"Fais un rapport de transmission structuré pour l'équipe du matin basé sur : {evt_nuit}", 
                    context="RELÈVE DE GARDE HÔPITAL"
                )
                st.markdown(f"<div class='chat-ai'>{synthese}</div>", unsafe_allow_html=True)
    
    # --- STAFF ---
    with tab3:
        st.write("Gestion des dossiers difficiles et présentations staff.")
        st.text_input("Rechercher un dossier patient...")
