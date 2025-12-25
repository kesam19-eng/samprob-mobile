import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np

# ==============================================================================
# 1. UI DESIGN "DEEP BLACK OLED" (Fidèle aux Maquettes)
# ==============================================================================
st.set_page_config(page_title="SAMProb OS v5", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* BOUTONS NAVIGATION (Mode GO/DOCK/STATION) - Style Maquette Dashboard */
    div.stButton > button {
        background-color: #1a1a1a;
        border: 1px solid #333;
        color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        font-size: 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        text-align: left; /* Alignement comme sur la maquette */
        display: flex;
        align-items: center;
    }
    div.stButton > button:hover {
        border-color: #00ADB5; /* Cyan Médical */
        background-color: #0f1f22;
        color: #00ADB5;
    }
    
    /* ALERT BOXES (IA DIAGNOSIS) */
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
    
    /* PROBE STATUS (Badge) */
    .probe-badge {
        background-color: #00ADB5;
        color: black;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        float: right;
    }

    /* SLIDERS CUSTOM */
    div.stSlider > div[data-baseweb="slider"] > div { background-color: #00ADB5; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SYSTÈME DE GESTION DES SONDES (PROBE MANAGER)
# ==============================================================================
if 'active_probe' not in st.session_state: st.session_state.active_probe = "None"
if 'scan_mode' not in st.session_state: st.session_state.scan_mode = "2D" # 2D, Volumetric, Photoacoustic

def sidebar_probe_manager():
    with st.sidebar:
        st.markdown("### 🔌 PROBE MANAGER")
        
        # Style visuel comme l'image "Probe Manager"
        col_p1, col_p2 = st.columns([1, 4])
        with col_p1: st.image("https://img.icons8.com/ios/50/00ADB5/ultrasound.png", width=40)
        with col_p2: 
            p1 = st.toggle("Cardiovascular Probe", value=True)
            if p1: st.session_state.active_probe = "Cardio"
            st.caption("Bluetooth • Connected")
            
        st.divider()
        
        col_p3, col_p4 = st.columns([1, 4])
        with col_p3: st.image("https://img.icons8.com/ios/50/aaaaaa/ultrasound.png", width=40)
        with col_p4: 
            p2 = st.toggle("Abdominal Probe", value=False)
            if p2: st.session_state.active_probe = "Abdo"
            st.caption("Calibration Required")
            
        st.divider()
        st.caption(f"ACTIVE: **{st.session_state.active_probe.upper()}**")

# ==============================================================================
# 3. CERVEAU IA (ANALYSE IMAGE ET SPECTRE)
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

    def analyze(self, prompt, context):
        if not self.connected: return "⚠️ SYSTEM OFFLINE: Connect Neural Key in Sidebar."
        try:
            full_prompt = f"CONTEXT: {context}. ROLE: Medical Imaging AI. TASK: {prompt}"
            return self.model.generate_content(full_prompt).text
        except: return "Error processing data."

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. NAVIGATION PRINCIPALE (DASHBOARD)
# ==============================================================================
sidebar_probe_manager()

# Clé API (Cachée en bas de sidebar)
with st.sidebar:
    st.divider()
    k = st.text_input("🔑 NEURAL KEY", type="password")
    if k and st.session_state.brain.connect(k): st.success("ONLINE")

# Sélecteur de Pages (Menu caché)
if 'page' not in st.session_state: st.session_state.page = "DASHBOARD"

# --- PAGE 1: DASHBOARD (SÉLECTEUR DE MODE) ---
if st.session_state.page == "DASHBOARD":
    st.image("https://img.icons8.com/ios-filled/100/ffffff/heart-monitor.png", width=80)
    st.title("SAMProb OS")
    st.markdown("Select Operational Mode")
    
    st.write("") # Spacer
    
    # REPLIQUE EXACTE DE L'IMAGE 6 (Select Mode)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📱 SAMProb GO\nPortable Use"):
            st.session_state.page = "SCAN"
            st.session_state.mode = "GO"
            st.rerun()
            
        if st.button("💻 SAMProb DOCK\nDesktop Use"):
            st.session_state.page = "SCAN"
            st.session_state.mode = "DOCK"
            st.rerun()
            
        if st.button("🏥 SAMProb STATION\nCart Use"):
            st.session_state.page = "SCAN"
            st.session_state.mode = "STATION"
            st.rerun()

# --- PAGE 2: SCAN INTERFACE (PRE-SCAN & LIVE) ---
elif st.session_state.page == "SCAN":
    # HEADER AVEC BOUTON RETOUR
    col_h1, col_h2 = st.columns([1, 10])
    with col_h1:
        if st.button("←"): 
            st.session_state.page = "DASHBOARD"
            st.rerun()
    with col_h2:
        st.markdown(f"**{st.session_state.mode} MODE** | PROBE: {st.session_state.active_probe}")

    # CONFIGURATION DU SCAN (IMAGE 7 & 8)
    col_settings, col_viz = st.columns([1, 3])
    
    with col_settings:
        st.markdown("### PRE-SCAN")
        
        # SÉLECTEUR DE TYPE DE SCAN (Boutons segmentés simulés)
        scan_type = st.radio("SCAN MODE", ["2D", "Volumetric 3D", "Photoacoustic"], label_visibility="collapsed")
        st.session_state.scan_mode = scan_type
        
        st.markdown(f"**MODE: {scan_type}**")
        
        # SLIDERS (Comme Image 7)
        depth = st.slider("DEPTH (cm)", 2, 20, 12)
        
        st.markdown("GAIN")
        cg1, cg2, cg3 = st.columns(3)
        with cg1: st.button("Low")
        with cg2: st.button("Normal", type="primary") # Simule la sélection
        with cg3: st.button("High")
        
        st.selectbox("PRESET", ["General", "Cardio", "OB/GYN", "Vascular"])
        
        st.divider()
        
        if st.button("🔵 START SCAN", use_container_width=True):
            st.toast("Initialization des cristaux piézoélectriques...")
            time.sleep(1)

    with col_viz:
        # ZONE DE VISUALISATION (DEPEND DU MODE)
        st.markdown("### LIVE VIEW")
        
        if scan_type == "2D":
            # Image 1 Simulation (Echo classique + AI)
            st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", caption="Live 2D Feed", use_column_width=True)
            
            # AI OVERLAY (Comme Image 1)
            st.markdown("""
            <div class="suspicious-mass">
            ⚠️ SUSPICIOUS MASS DETECTED (89%)
            <br><span style="font-size:12px; color:white;">Location: Left Ventricle Wall</span>
            </div>
            """, unsafe_allow_html=True)
            
        elif scan_type == "Volumetric 3D":
            # Image 2 Simulation (Cœur 3D)
            st.info("Rendering VoluScan 3D™...")
            # Ici on mettrait une image 3D ou un objet PyDeck si on avait les données
            st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", caption="VoluScan 3D Reconstruction", use_column_width=True)
            st.metric("Volume Mass", "4.2 cm³", "High Density")

        elif scan_type == "Photoacoustic":
            # Image 5 Simulation (Spectrale)
            st.warning("LASER ACTIVE - Photoacoustic Imaging")
            
            c_img, c_graph = st.columns(2)
            with c_img:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Hb/Oxy Heatmap")
            
            with c_graph:
                st.markdown("**Spectral View (nm)**")
                # Simulation données graphe Image 5
                chart_data = pd.DataFrame(
                    np.random.randn(20, 2) + [10, 5],
                    columns=['Hb', 'HbO2']
                )
                st.line_chart(chart_data)

    # BARRE D'ACTION BAS DE PAGE (IMAGE 1: Measure, Analyze, Report)
    st.divider()
    ca1, ca2, ca3 = st.columns(3)
    with ca1: st.button("📏 MEASURE", use_container_width=True)
    with ca2: 
        if st.button("🤖 AI ANALYZE", use_container_width=True):
            res = st.session_state.brain.analyze(f"Analyze mass in {scan_type} mode with depth {depth}cm", st.session_state.mode)
            st.info(res)
    with ca3: 
        if st.button("📄 REPORT (PACS)", use_container_width=True):
            st.success("DICOM Sent to PACS [Coyah P.D. ID: 350742]") # Ref image 4
