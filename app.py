import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="oXy AI • Core", page_icon="💧", layout="centered")

# 2. INJEKSI CSS STRUKTUR: CYBERPUNK DEEP PURPLE INTERFACE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Latar Belakang Gradasi Radial Ungu Gelap Sesuai Screenshot */
    .stApp {
        background: radial-gradient(circle at 50% 15%, #18102c 0%, #090612 70%, #040308 100%) !important;
        color: #e2dcf0 !important;
        overflow-x: hidden;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* 🔮 ORB CYBER CORE BULAT BERGERAK/BERDENYUT (ANIMATED ORB) */
    .cyber-core-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5%;
        margin-bottom: 15px;
    }
    .cyber-core {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, #a855f7 0%, #6b21a8 40%, #1e1b4b 80%, transparent 100%);
        border: 2px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 0 40px rgba(168, 85, 247, 0.5),
                    inset 0 0 25px rgba(168, 85, 247, 0.4);
        position: relative;
        animation: pulseCore 3s infinite ease-in-out;
    }
    .cyber-core::after {
        content: '';
        position: absolute;
        top: 25%; left: 25%; width: 50%; height: 50%;
        border-radius: 50%;
        background: radial-gradient(circle, #ffffff 0%, #d8b4fe 50%, transparent 100%);
        filter: blur(2px);
    }
    @keyframes pulseCore {
        0%, 100% { transform: scale(1); box-shadow: 0 0 35px rgba(168, 85, 247, 0.5); }
        50% { transform: scale(1.05); box-shadow: 0 0 55px rgba(168, 85, 247, 0.7), 0 0 20px rgba(139, 92, 246, 0.3); }
    }

    /* 🎯 SEKSI BRANDING TEKS GRADASI */
    .oxy-title {
        text-align: center;
        font-weight: 800 !important;
        font-size: 2.6rem !important;
        background: linear-gradient(to right, #ffffff 40%, #d8b4fe 70%, #a855f7 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 2px !important;
    }
    .creator-tag {
        text-align: center;
        color: #c084fc !important;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 35px !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* WELCOME CARD ELEMEN */
    .welcome-card-cyber {
        background: rgba(20, 13, 38, 0.5) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 35px 25px;
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
    }
    .welcome-h1 { font-size: 1.7rem !important; font-weight: 800 !important; color: #e9d5ff !important; margin-bottom: 15px; }
    .welcome-p { font-size: 0.98rem; color: #94a3b8; line-height: 1.6; }

    /* BUTTON MANAGEMENT */
    div[data-testid="stElementContainer"] button[key="enter_cyber_btn"] {
        background: #7c3aed !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 35px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4) !important;
    }
    div[data-testid="stColumn"] button {
        color: #ffffff !important;
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 12px !important;
    }

    /* INPUT FIELD UTAMA BENTUK KAPSUL LONJONG */
    div[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stChatInputContainer"],
    .stChatInput,
    form {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        background: rgba(13, 9, 24, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.7) !important;
        padding: 6px 14px !important;
    }
    .stChatInputContainer textarea { color: #ffffff !important; background-color: transparent !important; }

    /* BALON USER GLASS TRANSPARAN */
    .chat-container-block { display: flex !important; flex-direction: column !important; width: 100% !important; margin-bottom: 26px !important; }
    .align-user { align-items: flex-end !important; }
    .align-ai { align-items: flex-start !important; }

    .cyber-user-bubble {
        background: rgba(43, 29, 74, 0.4) !important;
        color: #f1f0f5 !important;
        padding: 13px 22px !important;
        border-radius: 20px !important;
        max-width: 85% !important;
        border: 1px solid rgba(168, 85, 247, 0.25) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }

    /* RESPONSIVE CHAT FLOW ALIRAN AI */
    .ai-header-inline { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; margin-left: 4px; }
    .ai-mini-orb {
        width: 20px; height: 20px; border-radius: 50%;
        background: radial-gradient(circle, #c084fc 0%, #6b21a8 70%);
        border: 1px solid rgba(168, 85, 247, 0.5);
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.7);
    }
    .ai-name-tag-inline { font-size: 1.05rem !important; color: #ffffff !important; font-weight: 700 !important; }
    .cyber-ai-content-flow { width: 100% !important; padding-left: 32px !important; color: #dbd5ea !important; line-height: 1.7 !important; }

    /* PREMIUM CODE BLOCK LOG MATRIX */
    div[data-testid="stMarkdownContainer"] pre, .stMarkdown pre {
        background-color: #06040a !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.8) !important;
    }
    div[data-testid="stMarkdownContainer"] code, .stMarkdown code {
        color: #d8b4fe !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* LOADING ANIMATION EMBED */
    .cyber-loading-box { display: flex; flex-direction: column; gap: 8px; width: 60%; padding-left: 32px; }
    .cyber-wave { height: 9px; background: linear-gradient(90deg, #3b1754 25%, #a855f7 50%, #3b1754 75%); background-size: 200% 100%; animation: cyberWaveAnim 1.2s infinite linear; border-radius: 5px; }
    .w-1 { width: 35%; } .w-2 { width: 80%; } .w-3 { width: 55%; }
    @keyframes cyberWaveAnim { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
</style>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT FIXED FOR FLOATING LAYERS
components.html("""
<script>
    function fixInputStyle() {
        const plates = window.parent.document.querySelectorAll('div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"], .stChatInputContainer, form');
        plates.forEach(el => {
            el.style.setProperty('background-color', 'transparent', 'important');
            el.style.setProperty('background', 'transparent', 'important');
            el.style.setProperty('box-shadow', 'none', 'important');
            el.style.setProperty('border', 'none', 'important');
        });
    }
    setInterval(fixInputStyle, 50);
</script>
""", height=0, width=0)

# ================= APP LIFECYCLE MANAGEMENT =================
if "sudah_masuk" not in st.session_state:
    st.session_state.sudah_masuk = False

# HALAMAN 1: WELCOME INITIAL SCREEN
if not st.session_state.sudah_masuk:
    st.markdown('<div class="cyber-core-container"><div class="cyber-core"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title">oXy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="creator-tag">CREATED BY ZAYN</p>', unsafe_allow_html=True)
    
    st.html("""
    <div class="welcome-card-cyber">
        <div class="welcome-h1">Halo, Saya oXy AI</div>
        <div class="welcome-p">
            Asisten sistem kecerdasan buatan siber buatan Zayn, dirancang khusus untuk memenuhi instruksi Tuan Gigs secara optimal.
        </div>
    </div>
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Masuk Sesi Inti 💧", key="enter_cyber_btn", use_container_width=True):
            st.session_state.sudah_masuk = True
            st.rerun()

# HALAMAN 2: UTAMA CHAT PANEL (MEMPERBAIKI MASALAH KOSONG DI GAMBAR 84618.png)
else:
    # 🔮 RENDER BULATAN ORB BERGERAK DI CHAT CORE (Menghilangkan kekosongan atas)
    st.markdown('<div class="cyber-core-container" style="margin-top:2%;"><div class="cyber-core" style="width:75px; height:75px; box-shadow: 0 0 25px rgba(168,85,247,0.45);"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title" style="font-size: 1.8rem !important;">oXy AI Core</h1>', unsafe_allow_html=True)
    st.markdown('<p class="creator-tag" style="font-size: 0.75rem; margin-bottom: 20px !important;">By Zayn • Lab System Active</p>', unsafe_allow_html=True)

    or_api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not or_api_key:
        st.error("⚠️ Token OPENROUTER_API_KEY tidak terdeteksi.")
        st.stop()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=or_api_key)
    FILE_ARSIP = "arsip_chat.json"

    def muat_arsip_chat():
        if os.path.exists(FILE_ARSIP):
            try:
                with open(FILE_ARSIP, "r", encoding="utf-8") as f: return json.load(f)
            except: return []
        return []

    def simpan_ke_arsip(pesan_list):
        with open(FILE_ARSIP, "w", encoding="utf-8") as f: json.dump(pesan_list, f, ensure_ascii=False, indent=4)

    if "messages" not in st.session_state:
        st.session_state.messages = muat_arsip_chat()

    col_reset, _ = st.columns([2, 2])
    with col_reset:
        if st.button("🗑️ Kosongkan Sesi oXy", key="cyber_reset"):
            if os.path.exists(FILE_ARSIP): os.remove(FILE_ARSIP)
            st.session_state.messages = []
            st.rerun()

    # Log Histori Obrolan
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.html(f'<div class="chat-container-block align-user"><div class="cyber-user-bubble">{msg["content"]}</div></div>')
        elif msg["role"] == "assistant":
            st.html('<div class="chat-container-block align-ai"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div class="ai-name-tag-inline">oXy AI</div></div><div class="cyber-ai-content-flow">')
            st.markdown(msg["content"])
            st.html('</div></div>')

    # Input Box Kapsul Utama
    if user_input := st.chat_input("Ask to oXy..."):
        st.html(f'<div class="chat-container-block align-user"><div class="cyber-user-bubble">{user_input}</div></div>')
        
        if len(st.session_state.messages) == 0:
            system_instruction = (
                "You are oXy AI, a highly advanced artificial intelligence created by Zayn. "
                "Always serve Tuan Gigs with maximum efficiency. Reply in Indonesian with a sharp, cool tech vibe."
            )
            st.session_state.messages.append({"role": "system", "content": system_instruction})
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        simpan_ke_arsip(st.session_state.messages)
        
        # Animasi Loading
        st.html('<div class="chat-container-block align-ai"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div class="ai-name-tag-inline">oXy AI Merakit Data...</div></div></div>')
        loading_placeholder = st.empty()
        loading_placeholder.html("""
            <div class="cyber-loading-box">
                <div class="cyber-wave w-1"></div>
                <div class="cyber-wave w-2"></div>
                <div class="cyber-wave w-3"></div>
            </div>
        """)
        
        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            loading_placeholder.empty()
            
            st.html('<div class="chat-container-block align-ai"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div class="ai-name-tag-inline">oXy AI</div></div><div class="cyber-ai-content-flow">')
            placeholder = st.empty()
            displayed_text = ""
            for word in full_response.split(" "):
                displayed_text += word + " "
                placeholder.markdown(displayed_text + "▌")
                time.sleep(0.015)
            placeholder.markdown(full_response)
            st.html('</div></div>')
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            simpan_ke_arsip(st.session_state.messages)
            st.rerun()
            
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Koneksi oXy Core Terputus: {e}")
                
