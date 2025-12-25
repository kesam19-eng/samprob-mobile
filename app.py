import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. CONFIGURATION VISUELLE "SAMPROB OLED DARK"
# ==============================================================================
st.set_page_config(page_title="SAMProb Neuro-OS v10", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap');
    
    /* THEME GLOBAL NOIR OLED */
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* LOGIN SCREEN */
    .login-box { border: 1px solid #333; padding: 50px; border-radius: 20px; text-align: center; max-width: 450px; margin: auto; background: #0a0a0a; box-shadow: 0 10px 30px rgba(0,255,255,0.05); }
    
    /* HUB BUTTONS (Select Mode) - Inspiré de tes screens */
    .hub-btn {
        border: 2px solid #222; border-radius: 16px; padding: 25px; 
        text-align: center; cursor: pointer; transition: 0.3s; background: #111; height: 100%;
    }
    .hub-btn:hover { border-color: #00ADB5; background: #051a1c; transform: translateY(-5px); }
    
    /* TABS NAVIGATION */
    div[data-testid="stTabs"] button { font-size: 18px; padding: 12px; border-radius: 8px; margin: 0 5px; }
    div[data-testid="stTabs"] button[aria-selected="true"] { 
        background-color: #00ADB5 !important; color: #000 !important; font-weight: bold; 
    }
    
    /* WIDGETS IMAGERIE */
    .param-box { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .scan-screen { border: 2px solid #333; border-radius: 10px; overflow: hidden; position: relative; }
    
    /* ALERTES IA */
    .ai-heatmap-alert {
        background: rgba(255, 0, 0, 0.15); border: 2px dashed #ff4444; 
        color: #ff4444; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;
    }
    
    /* BARRE LATÉRALE PROBES */
    .probe-card {
        background: #151515; border-radius: 10px; padding: 10px; margin-bottom: 8px; 
        display: flex; align-items: center; border-left: 4px solid #333;
    }
    .probe-card.active { border-left: 4px solid #00ADB5; background: #0f1f22; }
    
    /* RESULTATS ANALYSE */
    .report-paper { background: #fff; color: #000; padding: 20px; border-radius: 5px; font-family: 'Times New Roman'; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LOGIQUE SYSTÈME (SESSION STATE)
# ==============================================================================
if 'step' not in st.session_state: st.session_state.step = 'LOGIN'
if 'mode' not in st.session_state: st.session_state.mode = None
if 'active_probe' not in st.session_state: st.session_state.active_probe = "Linear"

# ==============================================================================
# 3. CERVEAU IA (GEMINI)
# ==============================================================================
class NeuralCore:
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

    def analyze(self, prompt, images, context):
        if not self.connected: return "⚠️ IA HORS-LIGNE. Veuillez connecter la clé API."
        
        system_prompt = f"""
        TU ES : SAMProb OS (Version 10.0).
        CONTEXTE : {context}.
        
        INSTRUCTIONS :
        1. Analyse les images fournies (Radios, Photos lésions, ECG).
        2. Analyse le texte clinique.
        3. Génère une réponse structurée médicale.
        
        Si Mode GO (Terrain) : Sois concis, focus urgence et évacuation.
        Si Mode DOCK (Cabinet) : Analyse détaillée, diagnostics différentiels, bibliographie.
        Si Mode STATION (Bloc) : Focus signes vitaux, interaction médicamenteuse, court et précis.
        """
        try:
            content = [system_prompt, f"DONNÉES : {prompt}"]
            if images: content.extend(images)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur IA : {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = NeuralCore()

# ==============================================================================
# ÉCRAN 1 : LOGIN (SÉCURITÉ)
# ==============================================================================
if st.session_state.step == 'LOGIN':
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("""
        <div class='login-box'>
            <h1 style='color:#00ADB5'>SAMProb OS</h1>
            <p style='color:#888'>Biometric Authentication</p>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Enter Passcode", type="password", label_visibility="collapsed")
        
        if st.button("UNLOCK DEVICE", use_container_width=True):
            if pwd == "SAMPROB2025":
                st.session_state.step = 'HUB'
                st.rerun()
            else: st.error("ACCESS DENIED")

# ==============================================================================
# ÉCRAN 2 : LE HUB CENTRAL (SÉLECTEUR DE MODE)
# ==============================================================================
elif st.session_state.step == 'HUB':
    st.markdown("<h1 style='text-align:center; margin-bottom:40px;'>SELECT OPERATIONAL MODE</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='hub-btn'><h3>📱 GO</h3><p>Rural & Emergency<br>Low Power Mode</p></div>""", unsafe_allow_html=True)
        if st.button("LAUNCH GO", use_container_width=True):
            st.session_state.mode = "GO"
            st.session_state.step = 'WORKSPACE'
            st.rerun()
            
    with col2:
        st.markdown("""<div class='hub-btn'><h3>💻 DOCK</h3><p>Clinic & Office<br>Full Analytics</p></div>""", unsafe_allow_html=True)
        if st.button("LAUNCH DOCK", use_container_width=True):
            st.session_state.mode = "DOCK"
            st.session_state.step = 'WORKSPACE'
            st.rerun()
            
    with col3:
        st.markdown("""<div class='hub-btn'><h3>🏥 STATION</h3><p>Hospital & OR<br>Sensor Fusion</p></div>""", unsafe_allow_html=True)
        if st.button("LAUNCH STATION", use_container_width=True):
            st.session_state.mode = "STATION"
            st.session_state.step = 'WORKSPACE'
            st.rerun()

# ==============================================================================
# ÉCRAN 3 : WORKSPACE (L'INTERFACE INTELLIGENTE)
# ==============================================================================
elif st.session_state.step == 'WORKSPACE':
    
    # --- TOP BAR ---
    c_back, c_info, c_status = st.columns([1, 6, 2])
    with c_back:
        if st.button("⬅ HUB"):
            st.session_state.step = 'HUB'
            st.rerun()
    with c_info:
        st.markdown(f"### SAMProb **{st.session_state.mode}** <span style='font-size:14px; color:#888'>| Dr. Samaké</span>", unsafe_allow_html=True)
    with c_status:
        # Simulation icônes statut (Batt, Wifi)
        net = "5G" if st.session_state.mode == "GO" else "ETH"
        st.caption(f"🔋 92% • 📶 {net} • ☁️ PACS")

    # --- SIDEBAR (PROBE MANAGER) ---
    with st.sidebar:
        st.markdown("### 🔌 PROBES")
        
        # Carte Sonde Cardio
        if st.button("Cardio (Phased)", use_container_width=True): st.session_state.active_probe = "Cardio"
        cls = "active" if st.session_state.active_probe == "Cardio" else ""
        st.markdown(f"<div class='probe-card {cls}'>💙 Cardio <span style='margin-left:auto; font-size:10px'>CONNECTED</span></div>", unsafe_allow_html=True)
        
        # Carte Sonde Abdo
        if st.button("Abdo (Curved)", use_container_width=True): st.session_state.active_probe = "Abdo"
        cls = "active" if st.session_state.active_probe == "Abdo" else ""
        st.markdown(f"<div class='probe-card {cls}'>🟠 Abdo <span style='margin-left:auto; font-size:10px'>READY</span></div>", unsafe_allow_html=True)
        
        # Carte Sonde Lineaire
        if st.button("Linear (Vascular)", use_container_width=True): st.session_state.active_probe = "Linear"
        cls = "active" if st.session_state.active_probe == "Linear" else ""
        st.markdown(f"<div class='probe-card {cls}'>📏 Linear <span style='margin-left:auto; font-size:10px'>ACTIVE</span></div>", unsafe_allow_html=True)

        st.divider()
        k = st.text_input("🔑 NEURAL KEY", type="password")
        if k and st.session_state.brain.connect(k): st.success("GEMINI ONLINE")

    # --- MAIN TABS ---
    tab_img, tab_med, tab_admin = st.tabs(["📡 IMAGERIE", "🧠 ASSISTANT", "📂 DOSSIERS"])

    # ==========================================================================
    # ONGLET 1 : IMAGERIE (CONTEXT-AWARE)
    # ==========================================================================
    with tab_img:
        col_controls, col_screen, col_actions = st.columns([1, 3, 1])

        # --- CONTROLES (GAUCHE) ---
        with col_controls:
            st.markdown("###### PARAMETERS")
            if st.session_state.mode == "GO":
                st.button("⚡ FAST EXAM")
                st.slider("Gain", 0, 100, 60)
                st.slider("Depth", 2, 20, 10)
                st.selectbox("Preset", ["Trauma (eFAST)", "OB 1st Trim", "Lung"])
            
            elif st.session_state.mode == "DOCK":
                st.button("🧊 3D RENDER")
                st.selectbox("Harmonics", ["Low", "High", "Pulse"])
                st.slider("Focus Pos", 1, 10, 5)
                st.toggle("AI Speckle Reduc.", value=True)

            elif st.session_state.mode == "STATION":
                st.button("🔴 PHOTOACOUSTIC")
                st.slider("Laser Power", 0, 100, 80)
                st.selectbox("Wavelength", ["700nm (Hb)", "850nm (HbO2)"])
                st.toggle("Fusion Overlay", value=True)

        # --- ECRAN (CENTRE) ---
        with col_screen:
            st.markdown(f"<div class='scan-screen'>", unsafe_allow_html=True)
            
            # Affichage Simulé selon le Mode
            if st.session_state.mode == "GO":
                st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", use_column_width=True)
                st.caption("Live 2D | 34 fps | MI 0.8")
            
            elif st.session_state.mode == "DOCK":
                st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", use_column_width=True)
                st.markdown("<div class='ai-heatmap-alert'>⚠️ SUSPICIOUS MASS DETECTED (89%)</div>", unsafe_allow_html=True)
            
            elif st.session_state.mode == "STATION":
                c1, c2 = st.columns(2)
                with c1: st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Hb Map")
                with c2: st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['O2', 'Hb']))
            
            st.markdown("</div>", unsafe_allow_html=True)

        # --- ACTIONS (DROITE) ---
        with col_actions:
            st.markdown("###### TOOLS")
            st.button("📸 CAPTURE")
            st.button("❄️ FREEZE")
            st.button("📏 MEASURE")
            if st.session_state.mode != "GO":
                st.button("🤖 AI ANALYZE")

    # ==========================================================================
    # ONGLET 2 : ASSISTANT MÉDICAL (LA GEMME)
    # ==========================================================================
    with tab_med:
        c_chat, c_data = st.columns([1, 1])
        
        with c_data:
            st.markdown("### 📥 DONNÉES PATIENT")
            
            # Entrée multimodale
            txt = st.text_area("Notes Cliniques / Anamnèse", height=100)
            
            # Camera Integration (comme demandé)
            img_cam = st.camera_input("Scanner Lésion / Document")
            
            # Upload (comme demandé)
            files = st.file_uploader("Importer DICOM/PDF/JPG", accept_multiple_files=True)
            
            imgs_to_process = []
            if img_cam: imgs_to_process.append(Image.open(img_cam))
            if files: 
                for f in files: imgs_to_process.append(Image.open(f))
            
            if st.button("🚀 LANCER ANALYSE SAMPROB", use_container_width=True):
                if txt or imgs_to_process:
                    with st.spinner("Analyse Neurale en cours..."):
                        res = st.session_state.brain.analyze(txt, imgs_to_process, st.session_state.mode)
                        st.session_state.ai_response = res
                else: st.warning("Données manquantes.")

        with c_chat:
            st.markdown("### 💡 RÉSULTATS IA")
            if 'ai_response' in st.session_state:
                st.markdown(f"<div class='param-box'>{st.session_state.ai_response}</div>", unsafe_allow_html=True)
            else:
                st.info("En attente de données...")
            
            # Outils spécifiques au mode
            st.divider()
            if st.session_state.mode == "GO":
                with st.expander("🚨 PROTOCOLES URGENCE (OFFLINE)"):
                    st.write("**ACR:** Adré 1mg/4min.")
                    st.write("**PALU GRAVE:** Artésunate IV.")
            elif st.session_state.mode == "STATION":
                st.markdown("**MONITORING BLOC**")
                k1, k2, k3 = st.columns(3)
                k1.metric("FC", "72")
                k2.metric("SpO2", "99%")
                k3.metric("TA", "120/80")

    # ==========================================================================
    # ONGLET 3 : ADMINISTRATIF & RAPPORTS
    # ==========================================================================
    with tab_admin:
        st.markdown(f"### 📝 BUREAU ({st.session_state.mode})")
        
        col_form, col_view = st.columns(2)
        
        with col_form:
            pat_name = st.text_input("Patient Name")
            exam_type = st.selectbox("Exam Type", ["Echography", "Consultation", "Surgery"])
            findings = st.text_area("Findings (Dictation)", height=150)
            
            if st.button("📄 GENERATE REPORT"):
                report_text = f"""
                SAMProb REPORT | Mode: {st.session_state.mode}
                Date: {datetime.date.today()}
                Patient: {pat_name}
                --------------------------------
                EXAM: {exam_type}
                
                FINDINGS:
                {findings}
                
                CONCLUSION:
                Consistent with clinical data.
                
                Signed: Dr. Samaké
                Generated by SAMProb OS
                """
                st.session_state.final_report = report_text

        with col_view:
            if 'final_report' in st.session_state:
                st.markdown(f"<div class='report-paper'><pre>{st.session_state.final_report}</pre></div>", unsafe_allow_html=True)
                st.download_button("
