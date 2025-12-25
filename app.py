import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import random

# ==============================================================================
# 1. INTERFACE TACTIQUE "TITANIUM GRADE"
# ==============================================================================
st.set_page_config(page_title="AEGIS OS v4.0", page_icon="☢️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 1. TYPOGRAPHIE INDUSTRIELLE */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; font-size: 20px !important; }
    
    /* 2. BARRE D'ÉTAT (BATTERIE / SATELLITE) */
    .status-bar {
        background-color: #111; color: #00ffcc; padding: 10px;
        border-bottom: 2px solid #00ffcc; font-size: 16px;
        display: flex; justify-content: space-between;
    }
    
    /* 3. BOUTONS HAPTIQUES */
    div.stButton > button {
        height: 85px; width: 100%; font-size: 24px !important; font-weight: 800 !important;
        border: 1px solid #444; background-color: #222; color: white;
        border-radius: 4px; transition: 0.2s;
        text-transform: uppercase; letter-spacing: 2px;
    }
    div.stButton > button:hover { border-color: #00ffcc; color: #00ffcc; }
    
    /* 4. TERMINAL DE DIAGNOSTIC */
    .terminal-output {
        background-color: #0a0a0a; border: 1px solid #333; color: #0f0;
        font-family: 'Courier New', monospace; padding: 15px; border-radius: 5px;
        margin-top: 10px; font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SEQUENCE DE DÉMARRAGE (BIOS CHECK)
# ==============================================================================
if 'boot_check' not in st.session_state:
    st.session_state.boot_check = True
    
# Barre d'état persistante (Simule le Hardware Unit-01)
st.markdown("""
<div class="status-bar">
    <span>UNIT-01 | EXYNOS MEDICAL 3nm | NPU: 50 TOPS</span>
    <span>SAT: IRIDIUM [ON] | BATT: SOLID-STATE 98% (SOLAR ACTIVE)</span>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. LE CERVEAU AEGIS (AWARENESS INDUSTRIEL)
# ==============================================================================
class Brain:
    def __init__(self):
        self.model = None
        self.connected = False
    
    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-pro') # Upgrade vers Pro pour la logique complexe
            self.connected = True
            return True
        except: return False

    def triage(self, texte, images=None, mode_actif="GO", hardware_context=""):
        if not self.connected: return "⚠️ ERREUR : LIAISON NEURALE INACTIVE."
        
        # --- DEFINITION DES SPÉCIFICATIONS INGÉNIERIE ---
        specs_techniques = f"""
        TU ES L'OS DU SAMProb™ UNIT-01.
        
        TES CAPACITÉS MATÉRIELLES (HARDWARE AWARENESS) :
        1.  **VISION :** ISOCELL HP5 (200MP) pour la dermatologie de précision + FLIR Boson+ (Thermique) pour l'inflammation + LiDAR (Profondeur plaies).
        2.  **CALCUL :** SoC Exynos Medical (NPU 50 TOPS). Tu peux analyser des images en temps réel sans Cloud.
        3.  **IMAGERIE LOURDE (Si connecté) :** SAMTum™ (Scanner Quantique). Capteurs NV Centers (Diamant). Sensibilité Femtotesla.
        4.  **WEARABLES :** Tu reçois les flux de la Galaxy Watch Medical (Spectrométrie SWIR Glucose/Lactate) et du Ring Life (Température 0.01°C).
        
        CONTEXTE OPÉRATIONNEL : {mode_actif}
        {hardware_context}
        """
        
        system_prompt = f"""
        {specs_techniques}
        
        INSTRUCTIONS DE TRAITEMENT :
        - Analyse les données entrantes (Texte/Image/Signes Vitaux).
        - Si Mode STATION + SAMTum™ activé : Simule une analyse quantique des tissus (Détection champs magnétiques neuronaux ou tumoraux).
        - Si Mode TERRAIN (GO) : Utilise les données FLIR/LiDAR pour évaluer la plaie/trauma.
        
        FORMAT DE SORTIE (STRICT) :
        [SYSTEM] : État des capteurs utilisés (ex: "FLIR: Hotspot détecté", "SAMTum: Séquence Q-MRI terminée").
        [DIAGNOSTIC] : Analyse probabiliste basée sur la fusion de capteurs.
        [ACTION] : Protocole recommandé.
        [PATIENT] : Explication vulgarisée.
        """
        
        try:
            content = [system_prompt, f"DONNÉES ENTRÉE : {texte}"]
            if images: content.extend(images)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur IA : {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. MENU SYSTÈME (SIDEBAR)
# ==============================================================================
if 'page' not in st.session_state: st.session_state.page = "HOME"

with st.sidebar:
    st.title("AEGIS OS™")
    st.caption("v4.0 | KERNEL: ANDROMED 16")
    
    st.divider()
    
    # SÉLECTEUR DE MODE (Conforme Dossier Premium) [cite: 140]
    st.subheader("MODE OPÉRATIONNEL")
    mode_aegis = st.radio(
        "Configuration Chassis :",
        [
            "AEGIS GO (Terrain/Sat)", 
            "AEGIS DOCK (Clinique)", 
            "AEGIS STATION (Hôpital/Bloc)"
        ],
        index=0
    )
    
    # SÉLECTEUR DE PÉRIPHÉRIQUES (Nouveau !)
    st.subheader("PÉRIPHÉRIQUES EXTERNES")
    periph_watch = st.checkbox("Galaxy Watch Medical (SWIR)", value=True)
    periph_ring = st.checkbox("Galaxy Ring Life", value=True)
    
    if "STATION" in mode_aegis:
        periph_samtum = st.checkbox("SAMTum™ (Quantum MRI)", value=False)
        st.caption("*Nécessite alimentation 220V*")
    else:
        periph_samtum = False

    st.divider()
    key = st.text_input("CLÉ NEURALE (API)", type="password")
    if key and st.session_state.brain.connect(key):
        st.success("CORTEX EN LIGNE")

# ==============================================================================
# 5. DASHBOARD PRINCIPAL
# ==============================================================================
if st.session_state.page == "HOME":
    st.title(f"INTERFACE : {mode_aegis.split('(')[0]}")
    
    # Affichage des Wearables (Si connectés)
    if periph_watch or periph_ring:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("GLUCOSE (SWIR)", "98 mg/dL", "-2")
        with c2: st.metric("LACTATE", "1.1 mmol/L", "Normal")
        with c3: st.metric("TEMP (RING)", "37.02 °C", "+0.01")
        st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔴 TRAUMA & \nURGENCES"):
            st.session_state.page = "RED"
            st.rerun()
    with col2:
        if st.button("🟡 IMAGERIE \nMULTIMODALE"):
            st.session_state.page = "YELLOW"
            st.rerun()
    with col3:
        if st.button("🟢 ARCHIVES \nQUANTIQUE"):
            st.session_state.page = "GREEN"
            st.rerun()

# ==============================================================================
# PAGE JAUNE : IMAGERIE AVANCÉE (SAMTum & CAPTEURS)
# ==============================================================================
elif st.session_state.page == "YELLOW":
    st.title("🟡 IMAGERIE & FUSION CAPTEURS")
    
    # 1. MODE QUANTUM (Si STATION + SAMTum activé)
    if periph_samtum and "STATION" in mode_aegis:
        st.markdown("""
        <div class="terminal-output">
        >>> PÉRIPHÉRIQUE DÉTECTÉ : SAMTum™ QUANTUM IMAGER
        >>> MATRICE : 10 240 NV CENTERS (DIAMOND)
        >>> ÉTAT : PRÊT (T < 1W)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("LANCER SÉQUENCE Q-MRI (NEURO/CORPS)"):
            with st.spinner("ACQUISITION FEMTOTESLA EN COURS..."):
                time.sleep(2) # Simulation scan
                res = st.session_state.brain.triage(
                    "Séquence Q-MRI complétée. Recherche anomalie champ magnétique tissulaire.", 
                    mode_actif="STATION",
                    hardware_context="INPUT: SAMTum MRI. Sensibilité détection: Métabolisme cellulaire."
                )
                st.markdown(f"<div class='terminal-output'>{res}</div>", unsafe_allow_html=True)
    
    # 2. MODE TERRAIN (Capteurs Dorsaux Unit-01)
    else:
        st.info(f"CAPTEURS ACTIFS : ISOCELL HP5 (200MP) | FLIR BOSON+ | LiDAR")
        
        tab1, tab2 = st.tabs(["📸 OPTIQUE / DERMATO", "🔥 THERMIQUE / TRAUMA"])
        
        with tab1:
            st.write("Acquisition Macro (200MP)")
            img_input = st.camera_input("Scanner Lésion")
        
        with tab2:
            st.write("Acquisition Thermique (FLIR)")
            if st.button("ACTIVER VUE INFRAROUGE"):
                st.image("https://upload.wikimedia.org/wikipedia/commons/9/96/Thermal_image_of_hand.jpg", caption="FLIR BOSON+ SIMULATION", width=300)

        # ANALYSE IA GÉNÉRIQUE
        if st.button("ANALYSE FUSION (LIDAR + OPTIQUE)"):
             if 'img_input' in locals() and img_input:
                # Analyse de l'image
                res = st.session_state.brain.triage(
                    "Analyse de lésion cutanée. Utilise LiDAR pour profondeur et FLIR pour inflammation.", 
                    images=[Image.open(img_input)],
                    mode_actif=mode_aegis
                )
                st.markdown(f"<div class='terminal-output'>{res}</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE ROUGE : URGENCES (AVEC WEARABLES)
# ==============================================================================
elif st.session_state.page == "RED":
    st.title("🔴 URGENCES & SIGNES VITAUX")
    
    col_wear, col_act = st.columns([1, 2])
    
    with col_wear:
        st.subheader("SENTINELLES (WEARABLES)")
        # Simulation flux continu
        st.metric("ECG (WATCH)", "Sinusal Regular")
        st.metric("SpO2", "99%", "Stable")
        st.metric("LACTATE (SWIR)", "2.5 mmol/L", "High") # Simulation stress
    
    with col_act:
        st.subheader("ACTION TACTIQUE")
        st.warning("ALERTE : NIVEAU LACTATE ÉLEVÉ DÉTECTÉ PAR LA MONTRE")
        if st.button("GÉNÉRER PROTOCOLE DE CHOC"):
            res = st.session_state.brain.triage(
                "Alerte Wearable : Lactate 2.5 mmol/L. Patient conscient. Demande protocole.",
                mode_actif=mode_aegis
            )
            st.markdown(f"<div class='terminal-output'>{res}</div>", unsafe_allow_html=True)

# ==============================================================================
# BOUTON RETOUR
# ==============================================================================
if st.button("RETOUR ACCUEIL"):
    st.session_state.page = "HOME"
    st.rerun()
