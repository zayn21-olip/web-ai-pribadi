import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# Konfigurasi Halaman
st.set_page_config(page_title="oXy AI • Core", page_icon="💧", layout="centered")

# CSS DETAIL: PURPLE CYBERPUNK - oXy AI EDITION
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }

    .stApp {
        background: radial-gradient(circle at 50% 15%, #18102c 0%, #090612 70%, #040308 100%) !important;
        color: #e2dcf0 !important;
    }

    /* ORB CORE - oXy Style */
    .cyber-core {
        width: 140px; height: 140px; border-radius: 50%;
        background: radial-gradient(circle, #2dd4bf 0%, #0d9488 40%, #115e59 80%, transparent 100%);
        border: 2px solid rgba(45, 212, 191, 0.4);
        box-shadow: 0 0 40px rgba(45, 212, 191, 0.5);
        margin: 0 auto 15px auto;
        animation: pulseCore 3s infinite ease-in-out;
    }
    @keyframes pulseCore {
        0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(45, 212, 191, 0.5); }
        50% { transform: scale(1.03); box-shadow: 0 0 55px rgba(45, 212, 191, 0.7); }
    }

    .oxy-title {
        text-align: center; font-weight: 800 !important; font-size: 2.8rem !important;
        background: linear-gradient(to right, #ffffff 40%, #5eead4 70%, #2dd4bf 100%);
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    }
    
    .creator-tag {
        text-align: center; color: #5eead4 !important; font-size: 0.9rem;
        margin-bottom: 30px !important; letter-spacing: 2px; text-transform: uppercase;
    }

    .welcome-card-cyber {
        background: rgba(20, 13, 38, 0.5) !important;
        border-radius: 24px !important; border: 1px solid rgba(45, 212, 191, 0.2) !important;
        padding: 30px; text-align: center; margin: 20px auto; max-width: 500px;
    }

    .cyber-user-bubble {
        background: rgba(43, 29, 74, 0.4) !important; color: #f1f0f5 !important;
        padding: 13px 22px !important; border-radius: 20px !important;
        border: 1px solid rgba(45, 212, 191, 0.3) !important;
    }

    .ai-mini-orb {
        width: 22px; height: 22px; border-radius: 50%;
        background: radial-gradient(circle, #5eead4 0%, #0d9488 70%);
        box-shadow: 0 0 10px rgba(45, 212, 191, 0.8);
    }
    
    /* Code Block Styling */
    pre { background-color: #06040a !important; border: 1px solid rgba(45, 212, 191, 0.3) !important; border-radius: 16px !important; }
</style>
""", unsafe_allow_html=True)

# LOGIKA APP
if "sudah_masuk" not in st.session_state:
    st.session_state.sudah_masuk = False

if not st.session_state.sudah_masuk:
    st.markdown('<div class="cyber-core"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title">oXy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="creator-tag">CREATED BY ZAYN</p>', unsafe_allow_html=True)
    
    st.html('<div class="welcome-card-cyber"><h3>Apa yang bisa oXy bantu hari ini?</h3><p>Asisten AI pintar untuk pengembangan perangkat lunak.</p></div>')
    
    if st.button("Mulai Sesi 💧", use_container_width=True):
        st.session_state.sudah_masuk = True
        st.rerun()

else:
    # Interface Chat
    st.markdown('<h2 style="text-align:center;">oXy AI Core</h2>', unsafe_allow_html=True)
    
    or_api_key = st.secrets.get("OPENROUTER_API_KEY")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=or_api_key)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.html(f'<div style="display:flex; justify-content:flex-end;"><div class="cyber-user-bubble">{msg["content"]}</div></div><br>')
        else:
            st.html('<div style="display:flex; align-items:center; gap:10px;"><div class="ai-mini-orb"></div><b>oXy AI</b></div>')
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask to oXy..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(model="openrouter/free", messages=st.session_state.messages)
        ans = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()
        
