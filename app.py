import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. CONFIGURATION VISUELLE "SAMPROB OLED"
# ==============================================================================
st.set_page_config(page_title="SAMProb OS v9", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* THEME GLOBAL */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* PAGE LOGIN */
    .login-container { border: 1px solid #333; padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; margin: auto; background: #111; }
    
    /* BOUTONS HUB (Sélecteur Mode) */
    .mode-btn {
        border: 2px solid #333; border-radius: 15px; padding: 30px; 
        text-align: center; cursor: pointer; transition: 0.3s; background: #1a1a1a;
    }
    .mode-btn:hover { border-color: #00ADB5; background: #0f1f22; transform: scale(1.02); }
    
    /* ONGLETS */
    div[data-testid="stTabs"] button { font-size: 20px; padding: 15px; width: 100%; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #00ADB5 !important; border-bottom: 3px solid #00ADB5 !important; }

    /* ELEMENTS SPECIFIQUES STATION (BLOC OP) */
    .vital-monitor { background: #000; border: 1px solid #333; color: #0f0; font-family: 'Courier New'; padding: 10px; border-radius: 5px; text-align: center; }
    
    /* RESULTATS IA */
    .ai-box { background-color: #002626; border-left: 5px solid #00ADB5; padding: 20px; border-radius: 5px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. GESTION D'ÉTAT (SESSION STATE)
# ==============================================================================
if 'step' not in st.session_state: st.session_state.step = 'LOGIN' # LOGIN -> HUB -> WORKSPACE
if 'active_mode' not in st.session_state: st.session_state.active_mode = None

# ==============================================================================
# 3. LE CERVEAU IA (BACKEND)
# ==============================================================================
class NeuralBrain:
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

    def assistant_multimodal(self, texte, images, mode):
        if not self.connected: return "⚠️ IA HORS-LIGNE. Veuillez connecter la clé dans la Sidebar."
        
        # Adaptation du prompt selon le mode choisi
        contexte_specifique = ""
        if mode == "GO":
            contexte_specifique = "CONTEXTE: TERRAIN / RURAL. Priorité: Triage, Urgence, Moyens limités. Sois concis."
        elif mode == "DOCK":
            contexte_specifique = "CONTEXTE: CABINET / CLINIQUE. Priorité: Diagnostic complet, Rédaction rapport, Analyse fine."
        elif mode == "STATION":
            contexte_specifique = "CONTEXTE: BLOC OPÉRATOIRE. Priorité: Signes vitaux, Complications chirurgicales, Réponses immédiates."

        system_prompt = f"""
        TU ES : SAMProb, Assistant Médical Expert.
        {contexte_specifique}
        
        TACHE : Analyse les données (Texte + Images).
        FORMAT DE RÉPONSE :
        1. 👁️ OBSERVATION (Ce que tu vois sur l'image/le cas).
        2. 🩺 DIAGNOSTIC (Hypothèses pondérées).
        3. 💡 RECOMMANDATION (Adaptée au contexte {mode}).
        """
        try:
            content = [system_prompt, f"DONNÉES : {texte}"]
            if images: content.extend(images)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur : {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = NeuralBrain()

# ==============================================================================
# ÉTAPE 1 : LOGIN (SÉCURITÉ)
# ==============================================================================
if st.session_state.step == 'LOGIN':
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div class='login-container'>
            <h1>🔒 SAMProb OS</h1>
            <p>Biometric / Passcode Entry</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            if pwd == "SAMPROB2025": # Mot de passe hardcodé pour démo
                st.session_state.step = 'HUB'
                st.rerun()
            else:
                st.error("ACCESS DENIED")

# ==============================================================================
# ÉTAPE 2 : LE HUB (SÉLECTION DES 3 MODES)
# ==============================================================================
elif st.session_state.step == 'HUB':
    st.markdown("<h1 style='text-align:center'>SELECT OPERATIONAL MODE</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_go, col_dock, col_stat = st.columns(3)
    
    with col_go:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/ambulance.png", width=80)
        if st.button("GO (TERRAIN)\nRural & Urgences", use_container_width=True):
            st.session_state.active_mode = "GO"
            st.session_state.step = 'WORKSPACE'
            st.rerun()
            
    with col_dock:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/doctor-male.png", width=80)
        if st.button("DOCK (CLINIQUE)\nConsultation & Bureau", use_container_width=True):
            st.session_state.active_mode = "DOCK"
            st.session_state.step = 'WORKSPACE'
            st.rerun()
            
    with col_stat:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/surgery.png", width=80)
        if st.button("STATION (BLOC)\nChirurgie & Monitoring", use_container_width=True):
            st.session_state.active_mode = "STATION"
            st.session_state.step = 'WORKSPACE'
            st.rerun()

# ==============================================================================
# ÉTAPE 3 : WORKSPACE (L'INTERFACE SPÉCIFIQUE)
# ==============================================================================
elif st.session_state.step == 'WORKSPACE':
    
    # --- HEADER & RETOUR ---
    c_back, c_title = st.columns([1, 8])
    with c_back:
        if st.button("⬅ HUB"):
            st.session_state.step = 'HUB'
            st.rerun()
    with c_title:
        st.markdown(f"## SAMProb **{st.session_state.active_mode}**")

    # --- SIDEBAR COMMUNE ---
    with st.sidebar:
        st.title(f"MODE {st.session_state.active_mode}")
        # Gestion Clé API
        k = st.text_input("🔑 CLÉ NEURALE", type="password")
        if k and st.session_state.brain.connect(k): st.success("ONLINE")
        
        st.divider()
        st.write("🔌 **SONDES**")
        if st.session_state.active_mode == "GO":
            st.info("Sonde Portable : ACTIVE")
        elif st.session_state.active_mode == "DOCK":
            st.info("Sonde Abdo/Cardio : STANDBY")
        else:
            st.info("Matrice Photoacoustique : READY")

    # --- ONGLETS PRINCIPAUX ---
    tab_img, tab_assist = st.tabs(["📡 IMAGERIE AVANCÉE", "🧠 ASSISTANT MÉDICAL (GEMME)"])

    # ==========================================================================
    # ONGLET IMAGERIE (VARIE SELON LE MODE)
    # ==========================================================================
    with tab_img:
        
        # --- CAS 1 : MODE GO (TERRAIN) ---
        if st.session_state.active_mode == "GO":
            st.markdown("### 📱 POCUS (Point-of-Care Ultrasound)")
            c_view, c_ctrl = st.columns([3, 1])
            with c_view:
                st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", caption="Scan Rapide 2D", use_column_width=True)
            with c_ctrl:
                st.button("FREEZE")
                st.button("SAVE JPEG")
                st.slider("Gain", 0, 100, 50)
            st.warning("⚠️ Mode Optimisé pour Batterie & Rapidité")

        # --- CAS 2 : MODE DOCK (CABINET) ---
        elif st.session_state.active_mode == "DOCK":
            st.markdown("### 🖥️ WORKSTATION ANALYTICS")
            c_view, c_data = st.columns([2, 1])
            with c_view:
                st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", caption="Reconstruction 3D Haute Déf", use_column_width=True)
            with c_data:
                st.write("**Mesures Automatiques**")
                st.metric("Volume VG", "120 ml")
                st.metric("FEVG", "55 %")
                st.button("EXPORT PACS")
                st.button("IMPRIMER RAPPORT")

        # --- CAS 3 : MODE STATION (BLOC OP) ---
        elif st.session_state.active_mode == "STATION":
            st.markdown("### 🏥 SURGICAL MONITORING & FUSION")
            
            # Simulation Monitoring Vitaux
            col_v1, col_v2, col_v3, col_v4 = st.columns(4)
            col_v1.markdown("<div class='vital-monitor'>FC<br><b>88</b></div>", unsafe_allow_html=True)
            col_v2.markdown("<div class='vital-monitor'>SpO2<br><b>99%</b></div>", unsafe_allow_html=True)
            col_v3.markdown("<div class='vital-monitor'>PNI<br><b>120/80</b></div>", unsafe_allow_html=True)
            col_v4.markdown("<div class='vital-monitor'>Temp<br><b>37.2°C</b></div>", unsafe_allow_html=True)
            
            st.divider()
            
            c_view, c_spectre = st.columns(2)
            with c_view:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Guidage Photoacoustique Temps Réel")
            with c_spectre:
                st.line_chart(pd.DataFrame(np.random.randn(50, 2), columns=['Hb', 'O2']))
                st.caption("Spectroscopie Tissulaire")

    # ==========================================================================
    # ONGLET ASSISTANT MÉDICAL (LA GEMME - COMMUN MAIS ADAPTÉ)
    # ==========================================================================
    with tab_assist:
        st.markdown(f"### 🧬 CORTEX CLINIQUE ({st.session_state.active_mode})")
        
        # Division en 2 colonnes : INPUTS vs OUTPUTS
        col_in, col_out = st.columns([1, 1])
        
        with col_in:
            st.markdown("#### 1. ACQUISITION DONNÉES")
            
            # A. TEXTE
            symptomes = st.text_area("Observations / Constantes / Anamnèse", height=100)
            
            # B. CAMERA (La fonction "Appareil Photo" demandée)
            cam_pic = st.camera_input("📸 Prendre photo (Lésion, Document
