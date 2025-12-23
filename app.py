import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from PIL import Image

# --- CONFIGURATION CLOUD ---
st.set_page_config(page_title="SAMProb Cloud", page_icon="☁️", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MOBILE ---
st.markdown("""
    <style>
    .stApp {background-color: #fafafa;}
    .stButton>button {height: 3.5em; border-radius: 12px; font-weight: bold; width: 100%; border: none;}
    .chat-bubble {padding: 15px; border-radius: 15px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
    .user-msg {background-color: #e3f2fd; border-right: 5px solid #2196f3; text-align: right;}
    .ai-msg {background-color: #ffffff; border-left: 5px solid #4caf50;}
    </style>
""", unsafe_allow_html=True)

# --- CERVEAU ---
class CloudBrain:
    def __init__(self):
        self.model = None
    def connect(self, key):
        try:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            return True
        except: return False
    def ask(self, prompt, image=None):
        if not self.model: return "⚠️ Clé API non connectée."
        try:
            content = ["Tu es SAMProb, assistant médical expert. Sois concis.", prompt]
            if image: content.append(image)
            return self.model.generate_content(content).text
        except Exception as e: return f"Erreur: {str(e)}"

if 'brain' not in st.session_state: st.session_state.brain = CloudBrain()
if 'history' not in st.session_state: st.session_state.history = []

# --- INTERFACE ---
with st.sidebar:
    st.title("☁️ SAMProb")
    key = st.text_input("Clé API Google", type="password")
    if key and st.session_state.brain.connect(key): st.success("Connecté")

st.title("SAMProb Mobile")

tabs = st.tabs(["💬 CHAT", "📸 VISION", "⚡ URGENCES"])

with tabs[0]:
    for msg in st.session_state.history:
        role = "user-msg" if msg['role'] == "user" else "ai-msg"
        st.markdown(f"<div class='chat-bubble {role}'>{msg['content']}</div>", unsafe_allow_html=True)
    
    user_input = st.chat_input("Cas clinique...")
    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.spinner("Analyse..."):
            resp = st.session_state.brain.ask(user_input)
            st.session_state.history.append({"role": "assistant", "content": resp})
        st.rerun()

with tabs[1]:
    img = st.camera_input("Scanner")
    if img and st.button("Analyser"):
        with st.spinner("Vision..."):
            # Conversion pour compatibilité Cloud
            img_pil = Image.open(img)
            resp = st.session_state.brain.ask("Analyse cette image médicale.", img_pil)
            st.info(resp)

with tabs[2]:
    st.error("PROTOCOLES VITAUX")
    if st.button("❤️ ARRÊT CARDIAQUE"):
        st.code("MCE 30:2\nAdrénaline 1mg / 4min", language="text")
    if st.button("⚡ CHOC ANAPHYLACTIQUE"):
        st.code("Adrénaline IM: 0.01 mg/kg\nRemplissage 20ml/kg", language="text")