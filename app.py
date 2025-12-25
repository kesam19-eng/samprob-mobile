import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. ARCHITECTURE VISUELLE "DEEP BLACK OLED"
# ==============================================================================
st.set_page_config(page_title="SAMProb Neuro-OS v8", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* GLOBAL THEME */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* HEADERS */
    h1, h2, h3 { color: #ffffff; font-weight: 800; }
    
    /* ONGLETS MAJEURS (IMAGERIE vs ASSISTANT) */
    div[data-testid="stTabs"] button { font-size: 20px; font-weight: bold; padding: 15px; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #00ADB5 !important; border-bottom: 3px solid #00ADB5 !important; }

    /* BOUTONS TACTIQUES */
    div.stButton > button {
        background-color: #1a1a1a; border: 1px solid #333; color: white;
        border-radius: 10px; padding: 15px; font-weight: 600; width: 100%; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #00ADB5; color: #00ADB5; }

    /* ZONE URGENCES (ROUGE) */
    .emergency-box { border: 2px solid #d32f2f; background-color: #2b0e0e; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    
    /* ZONE IA (JAUNE) */
    .ai-box { border: 2px solid #fbc02d; background-color: #262002; padding: 20px; border-radius: 10px; }
    
    /* RESULTATS IA */
    .ai-output { background-color: #002626; border-left: 5px solid #00ADB5; padding: 20px; border-radius: 5px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CERVEAU IA (MULTIMODAL COMPLET)
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

    def analyse_complete(self, texte, images_list, contexte):
        if not self.connected: return "⚠️ IA HORS-LIGNE. Connectez la clé."
        
        system_prompt = f"""
        TU ES : SAMProb, l'Assistant Médical Avancé.
        CONTEXTE ACTUEL : {contexte}.
        
        TA MISSION :
        Analyser l'ensemble des données fournies (Symptômes + Images Cliniques + Résultat Labo/Radio).
        
        FORMAT DE RÉPONSE :
        1. 🔍 ANALYSE VISUELLE (Si images fournies) : Décris précisément les lésions ou anomalies.
        2. 🧠 SYNTHÈSE DIAGNOSTIQUE : Hypothèse principale et diagnostics différentiels.
        3. 💊 PLAN THÉRAPEUTIQUE : Traitement adapté au contexte ({contexte}).
        4. ⚠️ VIGILANCE : Signes de gravité à surveiller.
        """
        
        try:
            content = [system_prompt, f"DONNÉES PATIENT : {texte}"]
            if images_list: 
                content.append("CI-JOINT LES DONNÉES VISUELLES (Photos/Radios/ECG) :")
                content.extend(images_list)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur IA : {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 3. BARRE LATÉRALE (HARDWARE CONTEXT)
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/00ADB5/ultrasound.png", width=60)
    st.title("SAMProb OS")
    
    st.divider()
    
    # SÉLECTEUR DE MODE MATÉRIEL (Impacte l'onglet IMAGERIE)
    st.subheader("📍 MODE MATÉRIEL")
    mode_hardware = st.radio("Configuration :", ["GO (Terrain)", "DOCK (Cabinet)", "STATION (Hôpital)"])
    
    st.divider()
    
    # SÉCURITÉ
    k = st.text_input("🔑 CLÉ NEURALE", type="password")
    if k and st.session_state.brain.connect(k): 
        st.success("CORTEX EN LIGNE")

# ==============================================================================
# 4. NAVIGATION PRINCIPALE
# ==============================================================================
tab_imagerie, tab_assistant = st.tabs(["📡 IMAGERIE (SCAN)", "🧠 ASSISTANT (TRIAGE)"])

# ==============================================================================
# ONGLET A : IMAGERIE (S'ADAPTE AUX 3 MODES)
# ==============================================================================
with tab_imagerie:
    # ---------------- MODE GO (TERRAIN) ----------------
    if "GO" in mode_hardware:
        st.subheader("📱 MODE GO : POCUS & URGENCE")
        col_view, col_ctrl = st.columns([2, 1])
        
        with col_view:
            st.image("https://media.istockphoto.com/id/1145618475/photo/ultrasound-screen-with-fetal-heart.jpg?s=612x612&w=0&k=20&c=LwK-Tz7LhZ2C0sV-R2P-tS_eJd-xQyvR_k_r_z_x_y_=", caption="Vue Rapide 2D", use_column_width=True)
        
        with col_ctrl:
            st.info("Interface Simplifiée")
            st.button("🔵 FREEZE")
            st.button("💾 SAVE QUICK")
            st.slider("GAIN", 0, 100, 50)
            st.slider("DEPTH", 2, 20, 10)

    # ---------------- MODE DOCK (CABINET) ----------------
    elif "DOCK" in mode_hardware:
        st.subheader("💻 MODE DOCK : ANALYSE & RAPPORT")
        col_img, col_tools = st.columns([2, 1])
        
        with col_img:
            st.image("https://thumbs.dreamstime.com/b/human-heart-anatomy-cross-section-3d-rendering-human-heart-anatomy-cross-section-3d-rendering-white-background-116634898.jpg", caption="Reconstruction Volumétrique", use_column_width=True)
        
        with col_tools:
            st.write("### Outils d'Analyse")
            st.button("📐 MESURES AUTOMATIQUES")
            st.button("🧬 ANNOTATION IA")
            st.select_slider("Filtres", options=["Soft", "Hard", "Vascular"])
            st.multiselect("Overlay", ["Doppler", "Elasto", "Biometry"])

    # ---------------- MODE STATION (HÔPITAL) ----------------
    elif "STATION" in mode_hardware:
        st.subheader("🏥 MODE STATION : FUSION & SPECTROMÉTRIE")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**PHOTOACOUSTIC FUSION**")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Photoacoustic_imaging_principle.svg/1200px-Photoacoustic_imaging_principle.svg.png", caption="Hémoglobine / Oxygénation")
        with c2:
            st.markdown("**SPECTRAL ANALYSIS**")
            chart_data = pd.DataFrame(np.random.randn(50, 2) + [10, 5], columns=['Hb', 'HbO2'])
            st.line_chart(chart_data)
        
        st.divider()
        st.button("🚀 LANCER SÉQUENCE QUANTIQUE (SAMTum)")

# ==============================================================================
# ONGLET B : ASSISTANT TRIAGE (ROUGE / JAUNE / VERT)
# ==============================================================================
with tab_assistant:
    # Sous-onglets de couleur
    sub_red, sub_yellow, sub_green = st.tabs(["🔴 URGENCES", "🟡 ASSISTANT MÉDICAL (IA)", "🟢 DOCUMENTS"])
    
    # --- 1. ROUGE : URGENCES VITALES ---
    with sub_red:
        st.markdown("<div class='emergency-box'><h3>🚨 ZONE CRITIQUE</h3></div>", unsafe_allow_html=True)
        
        c_proto, c_calc = st.columns(2)
        with c_proto:
            st.markdown("#### PROTOCOLES IMMÉDIATS")
            with st.expander("❤️ ARRÊT CARDIAQUE", expanded=True):
                st.write("- **MCE** : 100-120/min")
                st.write("- **ADRÉ** : 1mg / 4min")
                st.write("- **CHOC** : Si FV/TV")
            with st.expander("🐝 CHOC ANAPHYLACTIQUE"):
                st.write("- **ADRÉ** : 0.5mg IM")
                st.write("- **REMPLISSAGE** : 20ml/kg")
        
        with c_calc:
            st.markdown("#### CALCULATEURS URGENCE")
            poids = st.number_input("Poids Patient (kg)", 5, 120, 70)
            st.metric("Adrénaline (ACR)", f"{1.0} mg")
            st.metric("Remplissage (Choc)", f"{poids * 20} ml")

    # --- 2. JAUNE : ASSISTANT MÉDICAL MULTIMODAL (LA GEMME) ---
    with sub_yellow:
        st.markdown("<div class='ai-box'><h3>🧠 IA DIAGNOSTIC & THÉRAPEUTIQUE</h3></div>", unsafe_allow_html=True)
        st.caption("Analysez texte, photos, radios et résultats labo simultanément.")
        
        col_input, col_res = st.columns([1, 1])
        
        with col_input:
            st.markdown("#### 1. DONNÉES CLINIQUES")
            anamnese = st.text_area("Symptômes & Histoire", height=150, placeholder="Décrivez le cas : Patient 45 ans, fièvre, toux...")
            
            st.markdown("#### 2. DONNÉES VISUELLES (MULTIMODAL)")
            
            # CAMERA
            cam_val = st.camera_input("📸 Prendre Photo (Lésion, Gorge, ECG...)")
            
            # UPLOAD MULTIPLE
            uploaded_files = st.file_uploader("📂 Charger Fichiers (Radio, PDF, Bio)", accept_multiple_files=True)
            
            # Consolidation des images
            image_payload = []
            if cam_val: image_payload.append(Image.open(cam_val))
            if uploaded_files:
                for f in uploaded_files:
                    image_payload.append(Image.open(f))
            
            if image_payload:
                st.success(f"{len(image_payload)} image(s) prête(s) pour analyse.")

            st.divider()
            analyze_btn = st.button("🚀 LANCER L'ANALYSE COMPLÈTE", use_container_width=True)

        with col_res:
            st.markdown("#### 3. RÉSULTAT SAMPROB")
            if analyze_btn:
                if not anamnese and not image_payload:
                    st.error("Veuillez fournir au moins du texte ou une image.")
                else:
                    with st.spinner("Fusion des données... Analyse sémantique et visuelle..."):
                        response = st.session_state.brain.analyse_complete(anamnese, image_payload, mode_hardware)
                        st.markdown(f"<div class='ai-output'>{response}</div>", unsafe_allow_html=True)

    # --- 3. VERT : ADMINISTRATIF ---
    with sub_green:
        st.markdown("<h3>📝 BUREAU & RAPPORTS</h3>", unsafe_allow_html=True)
        
        c_doc, c_arch = st.columns(2)
        with c_doc:
            st.subheader("Rédaction Automatique")
            pat_name = st.text_input("Nom Patient")
            notes_vrac = st.text_area("Notes en vrac (Dictée)", height=100)
            type_doc = st.selectbox("Type", ["Compte-Rendu Consult", "Lettre Confrère", "Ordonnance"])
            
            if st.button("GÉNÉRER DOCUMENT"):
                if notes_vrac:
                    doc_gen = f"""
                    HÔPITAL / CENTRE : {mode_hardware}
                    DOC : {type_doc.upper()}
                    PATIENT : {pat_name}
                    DATE : {datetime.date.today()}
                    --------------------------------
                    {notes_vrac}
                    --------------------------------
                    Signature Dr. Samaké
                    """
                    st.session_state.final_doc = doc_gen
        
        with c_arch:
            if 'final_doc' in st.session_state:
                st.text_area("Aperçu Final", st.session_state.final_doc, height=300)
                st.download_button("📥 TÉLÉCHARGER / IMPRIMER", st.session_state.final_doc)
