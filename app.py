import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ==============================================================================
# 1. CONFIGURATION & STYLE (INTERFACE ÉPURÉE)
# ==============================================================================
st.set_page_config(page_title="SAMProb Final", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* POLICE ET BASE */
    html, body, [class*="css"] { font-family: 'Helvetica', sans-serif; font-size: 18px !important; }
    
    /* BOUTONS D'ACCUEIL GÉANTS */
    .big-btn {
        width: 100%;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* COULEURS SPÉCIFIQUES */
    .red-zone { background-color: #d32f2f; border: 2px solid #b71c1c; }
    .yellow-zone { background-color: #fbc02d; color: black !important; border: 2px solid #f9a825; }
    .green-zone { background-color: #388e3c; border: 2px solid #2e7d32; }

    /* BOUTONS STREAMLIT CLASSIQUES */
    .stButton>button { height: 3.5em !important; font-size: 20px !important; border-radius: 8px !important; width: 100%; }
    
    /* BOUTON RETOUR MAISON */
    .home-btn>button { background-color: #607d8b; color: white; }
    
    /* CONTENEUR IA */
    .ai-result { background-color: #fff; border-left: 6px solid #fbc02d; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SÉCURITÉ
# ==============================================================================
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><h1 style='text-align:center'>🧬 SAMProb</h1><h3 style='text-align:center'>INITIALISATION</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        pwd = st.text_input("CODE D'ACTIVATION", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == "SAMPROB2025":
                st.session_state.auth = True
                st.rerun()
            else: st.error("⛔ CODE INCORRECT")
    st.stop()

# ==============================================================================
# 3. CERVEAU IA (ANALYSE GLOBALE)
# ==============================================================================
class Brain:
    def __init__(self):
        self.model = None
        self.connected = False
    
    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.connected = True
            return True
        except: return False

    def triage(self, texte, images=None):
        if not self.connected: return "⚠️ ERREUR : VEUILLEZ CONNECTER LA CLÉ API DANS 'CONFIG'."
        
        prompt = """
        Tu es SAMProb, un système expert de triage hospitalier.
        Analyse les données fournies (Symptômes, Constantes, et potentiellement Images Radio/Bio/Plaie).
        
        TA RÉPONSE DOIT SUIVRE CE FORMAT STRICT :
        1. 🏥 SPÉCIALITÉ CONCERNÉE : (Ex: Cardiologie, Orthopédie, Chirurgie Viscérale...)
        2. 🚨 NIVEAU D'URGENCE : (Absolue / Relative / Différée)
        3. 🔬 ANALYSE DES SIGNES/IMAGES : (Ce que tu vois sur les images ou dans le texte)
        4. 📝 HYPOTHÈSES DIAGNOSTIQUES : (Liste probable)
        5. 💊 PRISE EN CHARGE IMMÉDIATE : (Examens à faire + Traitement d'attaque)
        """
        
        try:
            content = [prompt, f"DONNÉES PATIENT : {texte}"]
            if images: content.extend(images)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur IA : {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = Brain()

# ==============================================================================
# 4. GESTION DE LA NAVIGATION (PAGES)
# ==============================================================================
if 'page' not in st.session_state: st.session_state.page = "HOME"

def go_home(): st.session_state.page = "HOME"
def go_red(): st.session_state.page = "RED"
def go_yellow(): st.session_state.page = "YELLOW"
def go_green(): st.session_state.page = "GREEN"
def go_config(): st.session_state.page = "CONFIG"

# ==============================================================================
# 5. PAGE D'ACCUEIL (LES 3 BOUTONS)
# ==============================================================================
if st.session_state.page == "HOME":
    st.title("CENTRE DE COMMANDE")
    
    # Bouton ROUGE
    st.markdown('<div class="big-btn red-zone">1. URGENCES VITALES<br><span style="font-size:16px">Protocoles Réanimation & Déchocage</span></div>', unsafe_allow_html=True)
    if st.button("ACCÉDER AUX URGENCES (ROUGE)", key="btn_red"): go_red(); st.rerun()

    # Bouton JAUNE
    st.markdown('<div class="big-btn yellow-zone">2. ANALYSE & ADMISSION<br><span style="font-size:16px">Diagnostic IA Temps Réel (Symptômes + Imagerie)</span></div>', unsafe_allow_html=True)
    if st.button("NOUVELLE ADMISSION (JAUNE)", key="btn_yellow"): go_yellow(); st.rerun()
    
    # Bouton VERT
    st.markdown('<div class="big-btn green-zone">3. DOSSIERS & RAPPORTS<br><span style="font-size:16px">Comptes-Rendus Automatiques & Archives</span></div>', unsafe_allow_html=True)
    if st.button("GESTION DOSSIERS (VERT)", key="btn_green"): go_green(); st.rerun()
    
    st.markdown("---")
    if st.button("⚙️ CONFIGURATION CLÉ API"): go_config(); st.rerun()

# ==============================================================================
# PAGE ROUGE : URGENCES VITALES
# ==============================================================================
elif st.session_state.page == "RED":
    st.markdown("<div class='home-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR ACCUEIL"): go_home(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#d32f2f !important'>🚨 PROTOCOLES URGENCES</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.error("❤️ ARRÊT CARDIO-RESPIRATOIRE")
        st.write("""
        **1. MCE** : 100-120/min (30 compressions / 2 insufflations)
        **2. DÉFIBRILLATION** : Si FV/TV sans pouls -> Choc 200J Biphasique.
        **3. ADRÉNALINE** : 1mg IVD toutes les 4 min.
        **4. AMIODARONE** : 300mg IVD après le 3ème choc.
        """)
        
        st.error("🩸 CHOC HÉMORRAGIQUE")
        st.write("""
        **1. HÉMOSTASE** : Compression / Garrot / Pansement compressif.
        **2. REMPLISSAGE** : NaCl 0.9% ou Ringer (Objectif PAM > 65).
        **3. ACIDE TRANEXAMIQUE** : 1g IV lent sur 10 min.
        **4. TRANSFUSION** : CGR O-négatif si urgence absolue.
        """)

    with c2:
        st.error("🐝 CHOC ANAPHYLACTIQUE")
        st.write("""
        **1. ADRÉNALINE IM** (Cuisse) : 
           - Adulte : 0.5 mg
           - Enfant : 0.01 mg/kg
        **2. OXYGÈNE** : Masque haute concentration.
        **3. REMPLISSAGE** : 20ml/kg si hypotension.
        """)
        
        st.error("🧠 COMA / HYPOGLYCÉMIE")
        st.write("""
        **1. GLYCÉMIE CAPILLAIRE** : Si < 0.6 g/l -> G30% IVD.
        **2. PROTECTION VA** : PLS ou Intubation si GCS < 8.
        """)

# ==============================================================================
# PAGE JAUNE : NOUVELLE ADMISSION (LE CERVEAU IA)
# ==============================================================================
elif st.session_state.page == "YELLOW":
    st.markdown("<div class='home-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR ACCUEIL"): go_home(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#fbc02d !important'>🧬 DIAGNOSTIC TEMPS RÉEL</h1>", unsafe_allow_html=True)
    st.info("Remplissez les signes cliniques et ajoutez les examens (Photos/PDF) pour déterminer la spécialité.")

    # 1. DONNÉES CLINIQUES
    col_input, col_file = st.columns(2)
    with col_input:
        st.subheader("1. Signes & Symptômes")
        texte_clinique = st.text_area("Anamnèse, Constantes, Plaintes...", height=150, placeholder="Ex: Homme 45 ans, douleur thoracique irradiant bras gauche, TA 16/9, Sueurs...")
    
    # 2. GESTION FICHIERS (CORRIGÉE)
    with col_file:
        st.subheader("2. Imagerie & Bio")
        
        # Interrupteur Caméra
        if 'cam_on' not in st.session_state: st.session_state.cam_on = False
        
        if not st.session_state.cam_on:
            if st.button("📸 OUVRIR CAMÉRA"): st.session_state.cam_on = True; st.rerun()
        else:
            if st.button("❌ FERMER CAMÉRA"): st.session_state.cam_on = False; st.rerun()
            img_cam = st.camera_input("Prendre photo")
        
        # Upload Multiple
        uploaded = st.file_uploader("📂 OU CHARGER FICHIERS", type=['png','jpg','jpeg'], accept_multiple_files=True)
        
        # Rassemblement des images
        images_analyse = []
        if st.session_state.cam_on and 'img_cam' in locals() and img_cam: images_analyse.append(Image.open(img_cam))
        if uploaded: 
            for f in uploaded: images_analyse.append(Image.open(f))
            st.success(f"✅ {len(images_analyse)} fichiers prêts à l'analyse.")

    # 3. BOUTON ACTION
    st.markdown("---")
    if st.button("🚀 LANCER L'ANALYSE DIAGNOSTIQUE COMPLÈTE"):
        if not texte_clinique and not images_analyse:
            st.error("⚠️ Veuillez entrer du texte ou une image.")
        else:
            with st.spinner("🧠 SAMProb analyse les symptômes, les radios et les constantes..."):
                resultat = st.session_state.brain.triage(texte_clinique, images_analyse)
                st.markdown(f"<div class='ai-result'>{resultat}</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE VERTE : GESTION DOSSIERS
# ==============================================================================
elif st.session_state.page == "GREEN":
    st.markdown("<div class='home-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR ACCUEIL"): go_home(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='color:#2e7d32 !important'>📂 DOSSIERS & RAPPORTS</h1>", unsafe_allow_html=True)
    
    st.subheader("Générateur de Compte-Rendu")
    
    c1, c2 = st.columns(2)
    with c1:
        nom = st.text_input("Nom Patient")
        diag = st.text_input("Diagnostic Retenu")
        acte = st.text_input("Acte / Traitement réalisé")
    
    with c2:
        type_rap = st.selectbox("Type de Rapport", ["Compte-Rendu d'Hospitalisation", "Ordonnance de Sortie", "Lettre de liaison"])
        chir = st.text_input("Médecin Responsable", "Dr. SAMAKÉ")
    
    if st.button("GÉNÉRER LE DOCUMENT"):
        date = time.strftime("%d/%m/%Y")
        rapport = f"""
        CHU DONKA - SERVICE D'URGENCE ET CHIRURGIE
        ------------------------------------------------
        DATE : {date}
        TYPE : {type_rap}
        MÉDECIN : {chir}
        
        PATIENT : {nom}
        DIAGNOSTIC : {diag}
        
        HISTOIRE DE LA MALADIE :
        Patient admis ce jour pour {diag}.
        
        PRISE EN CHARGE :
        {acte}
        
        CONCLUSION :
        État stable. Sortie autorisée avec ordonnance.
        """
        st.text_area("Aperçu du Document", rapport, height=300)
        st.download_button("📥 TÉLÉCHARGER LE RAPPORT", rapport, file_name=f"Rapport_{nom}.txt")

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
elif st.session_state.page == "CONFIG":
    st.title("RÉGLAGES SYSTÈME")
    key = st.text_input("CLÉ API GOOGLE GEMINI", type="password")
    if st.button("CONNECTER"):
        if st.session_state.brain.connect(key):
            st.success("✅ CONNEXION RÉUSSIE. RETOURNEZ À L'ACCUEIL.")
            time.sleep(1)
            go_home(); st.rerun()
        else:
            st.error("❌ CLÉ INVALIDE")
    
    if st.button("⬅️ RETOUR SANS SAUVEGARDER"): go_home(); st.rerun()
