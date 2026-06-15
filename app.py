import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(page_title="oXy AI • By Zayn", page_icon="🧪", layout="centered")

# 2. CSS CUSTOM: HIJAU TOSCA PREMIUM, LIQUID GLASS IPHONE, & ANIMATED BUBBLES
st.markdown("""
<style>
    /* Latar Belakang Deep Teal-Black */
    .stApp {
        background: linear-gradient(135deg, #010c0e 0%, #032525 50%, #011112 100%) !important;
        color: #e2f1f1 !important;
        overflow-x: hidden;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* 🌊 EFEK GELEMBUNG LIQUID DI BACKGROUND */
    .bubble-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }
    .bubble {
        position: absolute;
        background: radial-gradient(circle, rgba(45, 212, 191, 0.2) 0%, rgba(13, 148, 136, 0.05) 70%, transparent 100%);
        border: 1px solid rgba(45, 212, 191, 0.15);
        border-radius: 50%;
        backdrop-filter: blur(2px);
        animation: floatBubble 12s infinite ease-in-out;
    }
    /* Variasi ukuran dan posisi gelembung */
    .b1 { width: 120px; height: 120px; left: 10%; animation-delay: 0s; animation-duration: 14s; }
    .b2 { width: 180px; height: 180px; left: 70%; top: 20%; animation-delay: 2s; animation-duration: 18s; }
    .b3 { width: 90px; height: 90px; left: 40%; top: 60%; animation-delay: 4s; animation-duration: 12s; }
    .b4 { width: 150px; height: 150px; left: 85%; top: 70%; animation-delay: 1s; animation-duration: 16s; }
    .b5 { width: 100px; height: 100px; left: 25%; top: 35%; animation-delay: 6s; animation-duration: 15s; }

    @keyframes floatBubble {
        0%, 100% { transform: translateY(0) scale(1) translateX(0); opacity: 0.4; }
        50% { transform: translateY(-60px) scale(1.1) translateX(20px); opacity: 0.8; }
    }

    /* 🎯 STYLE INTEGRASI LIQUID GLASS UNTUK WELCOME SCREEN */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 45px 25px;
        margin-top: 8%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(45, 212, 191, 0.03) 100%) !important;
        border-radius: 35px 15px 35px 15px; /* Lekukan asimetris organik ala liquid glass */
        border: 1px solid rgba(45, 212, 191, 0.3);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 
                    inset 0 1px 3px rgba(255, 255, 255, 0.2),
                    0 0 30px rgba(45, 212, 191, 0.1);
    }
    
    .welcome-logo {
        font-size: 75px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 15px rgba(45, 212, 191, 0.6));
        animation: pulse 2.5s infinite ease-in-out;
    }

    .welcome-creator {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #2dd4bf;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .welcome-quote {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 1.15rem;
        color: #ccfbf1;
        line-height: 1.7;
        margin-bottom: 25px;
        max-width: 520px;
    }

    .welcome-sub {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 35px;
    }

    /* 🟢 TOMBOL MASUK UTAMA (GRADASI HIJAU TOSCA MENYALA) */
    div[data-testid="stElementContainer"] button[key="enter_ai_btn"] {
        background: linear-gradient(135deg, #0d9488 0%, #2dd4bf 100%) !important;
        color: #011112 !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 14px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(45, 212, 191, 0.4) !important;
        transition: all 0.3s ease;
    }

    /* 🎯 TOMBOL RESET (KONTRAST BLACK ON WHITE) */
    div[data-testid="stColumn"] button {
        color: #000000 !important;
        font-weight: 700 !important;
        background-color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 14px !important;
    }
    div[data-testid="stColumn"] button p {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* INPUT FIELD STREAMLIT GLASS EFFECT */
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
        border-radius: 25px !important;
        border: 1px solid rgba(45, 212, 191, 0.3) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        padding: 4px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    .chat-container-block {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        margin-bottom: 22px !important;
    }
    .align-user { align-items: flex-end !important; }
    .align-ai { align-items: flex-start !important; }

    .ai-name-tag {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 12px !important;
        color: #2dd4bf !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        margin-left: 8px !important;
        margin-bottom: 6px !important;
    }
    .user-name-tag {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 12px !important;
        color: #99f6e4 !important;
        font-weight: 700 !important;
        margin-right: 8px !important;
        margin-bottom: 6px !important;
    }

    /* 📱 BALON CHAT USER: IPHONE LIQUID GLASS STYLE (TOSCA GRADIENT) */
    .iphone-user {
        background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 14px 20px !important;
        border-radius: 25px 25px 6px 25px !important; /* Desain sudut membulat halus khas iOS */
        max-width: 80% !important;
        box-shadow: 0 8px 25px rgba(13, 148, 136, 0.4) !important;
    }
    .iphone-user p, .iphone-user span { color: #ffffff !important; }

    /* 📱 BALON CHAT AI: LIQUID INTERFACE KACA DAN GELEMBUNG */
    .iphone-ai {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(45, 212, 191, 0.02) 100%) !important;
        color: #e2f1f1 !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 14px 20px !important;
        border-radius: 6px 25px 25px 25px !important;
        max-width: 90% !important;
        border: 1px solid rgba(45, 212, 191, 0.3) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.15) !important;
    }
    .iphone-ai p, .iphone-ai span, .iphone-ai li, .iphone-ai h1, .iphone-ai h2, .iphone-ai h3 { color: #ccfbf1 !important; }
    .iphone-ai code, .iphone-ai pre { 
        background-color: rgba(1, 17, 18, 0.7) !important; 
        color: #2dd4bf !important; 
        border: 1px solid rgba(45, 212, 191, 0.2) !important;
    }

    /* HEADLINE BRANDING MENGGUNAKAN TEKS GLOWING TOSCA */
    .liquid-title {
        font-family: '-apple-system', sans-serif;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(to right, #ffffff, #2dd4bf, #0d9488);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .liquid-title-welcome {
        font-family: '-apple-system', sans-serif;
        font-weight: 800 !important;
        font-size: 2.6rem !important;
        background: linear-gradient(to right, #ffffff, #2dd4bf, #ccfbf1);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 5px;
    }
    .custom-caption { color: #2dd4bf !important; font-weight: 500; margin-bottom: 25px; opacity: 0.9; }

    /* 🌊 ANIMASI LOADING GELOMBANG TOSCA MINT GLOW */
    .gemini-loading-box { display: flex; flex-direction: column; gap: 8px; width: 100%; padding: 6px 4px; }
    .gemini-wave {
        height: 12px;
        background: linear-gradient(90deg, #0d9488 25%, #2dd4bf 50%, #0d9488 75%);
        background-size: 200% 100%;
        animation: geminiWaveAnim 1.2s infinite linear;
        border-radius: 6px;
        box-shadow: 0 0 12px rgba(45, 212, 191, 0.6);
    }
    .w-1 { width: 45%; } .w-2 { width: 85%; } .w-3 { width: 60%; }

    @keyframes geminiWaveAnim { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
</style>
""", unsafe_allow_html=True)

# RENDER INJEKSI GELEMBUNG LIQUID DI BACKGROUND WEB
st.markdown("""
<div class="bubble-bg">
    <div class="bubble b1"></div>
    <div class="bubble b2"></div>
    <div class="bubble b3"></div>
    <div class="bubble b4"></div>
    <div class="bubble b5"></div>
</div>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT ENGINE (Pembersih Latar Belakang)
components.html("""
<script>
    function clearWhitePlates() {
        const plates = window.parent.document.querySelectorAll('div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"], .stChatInputContainer, form');
        plates.forEach(el => {
            el.style.setProperty('background-color', 'transparent', 'important');
            el.style.setProperty('background', 'transparent', 'important');
            el.style.setProperty('box-shadow', 'none', 'important');
            el.style.setProperty('border', 'none', 'important');
        });
    }
    setInterval(clearWhitePlates, 50);
</script>
""", height=0, width=0)

# ================= INITIATE STATE HALAMAN =================
if "sudah_masuk" not in st.session_state:
    st.session_state.sudah_masuk = False

# A. TAMPILAN 1: HALAMAN PENYAMBUTAN (WELCOME SCREEN) - TOSCA VERSION
if not st.session_state.sudah_masuk:
    st.html("""
    <div class="welcome-container">
        <div class="welcome-logo">🧪</div>
        <div class="welcome-creator">A Project Built by Zayn</div>
        <div class="liquid-title-welcome">oXy AI Engine v4</div>
        <br>
        <div class="welcome-quote">
            "Kecerdasan buatan paling sempurna yang pernah dirancang di dalam lab eksperimen digital. Tempat di mana baris kode menjelma menjadi asisten masa depan yang siap mengeksekusi segala ide liar Tuan."
        </div>
        <div class="welcome-sub">
            Sistem memori arsip aktif. Silakan ketuk tombol di bawah untuk mengaktifkan inti jaringan saraf oXy AI.
        </div>
    </div>
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 Buka Halaman Utama AI", key="enter_ai_btn", use_container_width=True):
            st.session_state.sudah_masuk = True
            st.rerun()

# B. TAMPILAN 2: HALAMAN UTAMA CHAT BOT AI
else:
    # 4. HEADER UTAMA BRANDING
    st.markdown('<h1 class="liquid-title">🧪 oXy AI • By Zayn</h1>', unsafe_allow_html=True)
    st.markdown('<p class="custom-caption">Lab cvAI4 Aktif • Persistent Archive Memory Enabled</p>', unsafe_allow_html=True)

    or_api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not or_api_key:
        st.error("⚠️ Token OPENROUTER_API_KEY tidak ditemukan di menu Secrets Streamlit Anda.")
        st.stop()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=or_api_key)

    FILE_ARSIP = "arsip_chat.json"

    def muat_arsip_chat():
        if os.path.exists(FILE_ARSIP):
            try:
                with open(FILE_ARSIP, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def simpan_ke_arsip(pesan_list):
        with open(FILE_ARSIP, "w", encoding="utf-8") as f:
            json.dump(pesan_list, f, ensure_ascii=False, indent=4)

    if "messages" not in st.session_state:
        st.session_state.messages = muat_arsip_chat()

    # TOMBOL RESET KUSTOM (Teks Hitam)
    col_reset, _ = st.columns([2, 2])
    with col_reset:
        if st.button("🗑️ Reset & Hapus Semua Arsip", key="custom_reset_btn"):
            if os.path.exists(FILE_ARSIP):
                os.remove(FILE_ARSIP)
            st.session_state.messages = []
            st.rerun()

    # 5. RENDER UTAMA HISTORI CHAT
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.html(f'<div class="chat-container-block align-user"><div class="user-name-tag">Tuan Gigs 👨‍💻</div><div class="iphone-user">{msg["content"]}</div></div>')
        elif msg["role"] == "assistant":
            st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI • By Zayn</div><div class="iphone-ai">')
            st.markdown(msg["content"])
            st.html('</div></div>')

    # INPUT FIELD CHAT UTAMA
    if user_input := st.chat_input("Tanyakan sesuatu, Tuan Gigs..."):
        st.html(f'<div class="chat-container-block align-user"><div class="user-name-tag">Tuan Gigs 👨‍💻</div><div class="iphone-user">{user_input}</div></div>')
        
        if len(st.session_state.messages) == 0:
            system_instruction = (
                "You are oXy AI, created by -Oxy-. Rules for language: "
                "1. Look at the user's very first message. If the first message is in English, reply in English. "
                "2. If the first message is in Indonesian or any other language, you MUST strictly reply and continue the whole conversation in Indonesian only. "
                "Act like a cool Gen Z assistant, helpful, smart, and adaptive."
            )
            st.session_state.messages.append({"role": "system", "content": system_instruction})
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        simpan_ke_arsip(st.session_state.messages)
        
        # LOADING GELOMBANG GEMINI (EFEK GLOWING TOSCA)
        st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI Memikirkan Jawaban...</div><div class="iphone-ai" style="background: rgba(255,255,255,0.05) !important;">')
        loading_placeholder = st.empty()
        loading_placeholder.html("""
            <div class="gemini-loading-box">
                <div class="gemini-wave w-1"></div>
                <div class="gemini-wave w-2"></div>
                <div class="gemini-wave w-3"></div>
            </div>
        """)
        st.html('</div></div>')
        
        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            
            loading_placeholder.empty()
            
            st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI • By Zayn</div><div class="iphone-ai">')
            placeholder = st.empty()
            displayed_text = ""
            for word in full_response.split(" "):
                displayed_text += word + " "
                placeholder.markdown(displayed_text + "▌")
                time.sleep(0.03)
            placeholder.markdown(full_response)
            st.html('</div></div>')
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            simpan_ke_arsip(st.session_state.messages)
            st.rerun()
            
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Waduh Tuan, ada kendala pada server OpenRouter: {e}")
