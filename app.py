import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="oXy AI • Core", page_icon="🌐", layout="centered")

# 2. INJEKSI CSS STRUKTUR: DEEP PURPLE CYBER INTERFACE & PLANET BUMI CAIRAN KACA 3D
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Background Deep Nebula */
    .stApp {
        background: radial-gradient(circle at 50% 15%, #0e0a21 0%, #06040d 70%, #020105 100%) !important;
        color: #e2dcf0 !important;
        overflow-x: hidden;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* 🌐 ANIMATED CYBER EARTH PLANET (BIRU MUDA + LIQUID GLASS PUTIH HD) */
    .cyber-core-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5%;
        margin-bottom: 25px;
    }
    
    .cyber-planet {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        position: relative;
        /* Tekstur Dasar: Biru muda dengan lapisan liquid glass putih */
        background: radial-gradient(circle at 30% 30%, #ffffff 0%, #a5f3fc 25%, #38bdf8 60%, #0369a1 100%);
        box-shadow: 
            0 0 20px rgba(56, 189, 248, 0.4),
            0 0 50px rgba(14, 165, 233, 0.6),
            inset -10px -10px 30px rgba(3, 105, 161, 0.7),
            inset 15px 15px 25px rgba(255, 255, 255, 0.9);
        overflow: hidden;
        animation: rotatePlanet 12s linear infinite;
    }

    /* Efek Lubang-Lubang Kawah & Kontur Lapisan Kaca Bumi */
    .cyber-planet::before {
        content: '';
        position: absolute;
        width: 200%;
        height: 100%;
        background-image: 
            /* Pola lubang-lubang bulat transparan/kawah */
            radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.4) 8%, transparent 9%),
            radial-gradient(circle at 35% 70%, rgba(2, 132, 199, 0.5) 12%, transparent 13%),
            radial-gradient(circle at 60% 40%, rgba(255, 255, 255, 0.5) 6%, transparent 7%),
            radial-gradient(circle at 75% 75%, rgba(2, 132, 199, 0.4) 10%, transparent 11%),
            radial-gradient(circle at 90% 25%, rgba(255, 255, 255, 0.3) 14%, transparent 15%),
            /* Aliran Liquid Glass Putih */
            linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 20%, rgba(255,255,255,0.6) 40%, transparent 60%);
        background-size: 50% 100%;
        animation: moveClouds 6s linear infinite;
    }

    /* Efek Atmosfer Kaca Glossy Mengkilap diluar Planet */
    .cyber-planet::after {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, transparent 50%, rgba(0,0,0,0.3) 100%);
        pointer-events: none;
    }

    @keyframes rotatePlanet {
        0% { transform: rotate(0deg); box-shadow: 0 0 40px rgba(56, 189, 248, 0.5); }
        50% { box-shadow: 0 0 55px rgba(14, 165, 233, 0.7); }
        100% { transform: rotate(360deg); box-shadow: 0 0 40px rgba(56, 189, 248, 0.5); }
    }

    @keyframes moveClouds {
        0% { background-position: 0px 0px; }
        100% { background-position: 140px 0px; }
    }

    /* TEKS UTAMA BRANDING */
    .oxy-title {
        text-align: center;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        background: linear-gradient(to right, #ffffff 40%, #bae6fd 70%, #38bdf8 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .oxy-sub {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 1.1rem;
        margin-bottom: 30px !important;
    }

    /* 📱 KARTU BANNER PERTAMA - PERBAIKAN: HALO SAYA oXy */
    .welcome-card-cyber {
        background: rgba(15, 23, 42, 0.5) !important;
        border-radius: 28px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        padding: 40px 30px;
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
    }
    .welcome-h1 { 
        font-size: 2.2rem !important; 
        font-weight: 800 !important; 
        color: #38bdf8 !important; 
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    .welcome-p { 
        font-size: 1.1rem; 
        color: #e2e8f0; 
        line-height: 1.7; 
        font-weight: 500;
    }

    /* BUTTON TO ENTER CORE */
    div[data-testid="stElementContainer"] button[key="enter_cyber_btn"] {
        background: #0284c7 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 14px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
    }

    /* 🏷️ SEKSI TENTANG SAYA DI BAGIAN BAWAH */
    .about-section-container {
        text-align: center;
        margin-top: 60px;
        margin-bottom: 20px;
    }
    .about-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        margin-bottom: 30px;
    }
    .about-profile-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        border: 2px solid #0284c7;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
        margin: 0 auto 25px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(15, 23, 42, 0.6);
    }
    .about-profile-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    /* Deskripsi Penjelasan oXy AI */
    .about-description-box {
        max-width: 500px;
        margin: 0 auto 60px auto;
        padding: 0 20px;
        text-align: center;
    }
    .about-text-p {
        font-size: 1rem;
        color: #94a3b8;
        line-height: 1.7;
        margin-bottom: 15px;
    }
    .about-highlight {
        color: #7dd3fc !important;
        font-weight: 600;
    }

    /* CHAT CORE LAYOUT & GELEMBUNG INPUT */
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        background: rgba(10, 15, 30, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        padding: 6px 14px !important;
    }
    
    /* 💬 Gelembung User */
    .cyber-user-bubble {
        background: rgba(14, 165, 233, 0.25) !important;
        color: #f8fafc !important;
        padding: 13px 22px !important;
        border-radius: 20px 20px 4px 20px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        max-width: 85% !important;
    }
    
    /* 🔮 Gelembung AI */
    .cyber-ai-bubble-box {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 4px 20px 20px 20px !important;
        padding: 18px 22px !important;
        margin-bottom: 25px !important;
        max-width: 85% !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .ai-header-inline { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
    .ai-mini-orb {
        width: 18px; height: 18px; border-radius: 50%;
        background: radial-gradient(circle, #ffffff 0%, #38bdf8 60%, #0284c7 100%);
        border: 1px solid rgba(56, 189, 248, 0.5);
    }
    .cyber-ai-content-flow { color: #e2e8f0 !important; line-height: 1.7 !important; }
    
    div[data-testid="stMarkdownContainer"] pre {
        background-color: #020617 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
    }

    /* 🟢 ANIMASI GELEMBUNG PEMIKIR */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 5px 10px;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #38bdf8;
        border-radius: 50%;
        animation: cyberBlink 1.4s infinite both;
    }
    .typing-dot:nth-child(2) { animation-delay: .2s; background-color: #7dd3fc; }
    .typing-dot:nth-child(3) { animation-delay: .4s; background-color: #bae6fd; }

    @keyframes cyberBlink {
        0%, 100% { transform: scale(0.8); opacity: 0.4; }
        50% { transform: scale(1.2); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# 3. FIX OVERLAY INTERFACE & JAVASCRIPT AUTO-SCROLL LOADER
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
    
    function scrollToBottom() {
        window.parent.scrollTo({
            top: window.parent.document.body.scrollHeight,
            behavior: 'smooth'
        });
    }

    setInterval(fixInputStyle, 50);
    setInterval(scrollToBottom, 400);
</script>
""", height=0, width=0)

# ================= MANAJEMEN HALAMAN APP =================
if "sudah_masuk" not in st.session_state:
    st.session_state.sudah_masuk = False

# 🏠 HALAMAN 1: WELCOME SCREEN (BUMI CYBER BERPUTAR + HALO SAYA oXy)
if not st.session_state.sudah_masuk:
    st.markdown('<div class="cyber-core-container"><div class="cyber-planet"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title">oXy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="oxy-sub">Apa yang bisa saya bantu?</p>', unsafe_allow_html=True)
    
    st.html("""
    <div class="welcome-card-cyber">
        <div class="welcome-h1">Halo, Saya oXy</div>
        <div class="welcome-p">
            Seorang <strong>Asisten Kecerdasan Buatan</strong> yang siap membantumu kapan saja.
        </div>
    </div>
    """)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Masuk ke Core Core 🔮", key="enter_cyber_btn", use_container_width=True):
            st.session_state.sudah_masuk = True
            st.rerun()
            
    st.html("""
    <div class="about-section-container">
        <div class="about-title">Tentang Kreator</div>
        <div class="about-profile-circle">
            <div class="about-profile-text">Zayn Profile</div>
        </div>
    </div>
    <div class="about-description-box">
        <p class="about-text-p">
            <span class="about-highlight">oXy AI</span> adalah entitas sistem kecerdasan buatan siber mutakhir yang dirancang khusus oleh <span class="about-highlight">Zayn</span> untuk membantu mempercepat alur kerja pengembangan perangkat lunak, perakitan skrip kode, dan manajemen logika komputasi secara cerdas.
        </p>
    </div>
    """)

# 💬 HALAMAN 2: INTERFACE CHAT CORE UTAMA (GRATIS & STABLE)
else:
    st.markdown('<div class="cyber-core-container" style="margin-top:2%;"><div class="cyber-planet" style="width:70px; height:70px; box-shadow: 0 0 25px rgba(56,189,248,0.5);"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title" style="font-size: 1.8rem !important;">oXy AI Core</h1>', unsafe_allow_html=True)
    st.markdown('<p class="oxy-sub" style="font-size: 0.85rem; margin-bottom: 20px !important;">Created by Zayn • Powered by OpenRouter</p>', unsafe_allow_html=True)

    openrouter_key = st.secrets.get("OPENROUTER_API_KEY")
    if not openrouter_key:
        st.error("⚠️ Token OPENROUTER_API_KEY tidak ditemukan di dashboard Streamlit Secrets.")
        st.stop()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key
    )
    FILE_ARSIP = "arsip_chat.json"

    if "messages" not in st.session_state:
        if os.path.exists(FILE_ARSIP):
            try:
                with open(FILE_ARSIP, "r", encoding="utf-8") as f: st.session_state.messages = json.load(f)
            except: st.session_state.messages = []
        else:
            st.session_state.messages = []

    col_reset, _ = st.columns([2, 2])
    with col_reset:
        if st.button("🗑️ Kosongkan Sesi oXy", key="cyber_reset"):
            if os.path.exists(FILE_ARSIP): os.remove(FILE_ARSIP)
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.html(f'<div style="display:flex; justify-content:flex-end; margin-bottom:20px;"><div class="cyber-user-bubble">{msg["content"]}</div></div>')
        elif msg["role"] == "assistant":
            with st.container():
                st.html('<div style="display:flex; justify-content:flex-start;"><div class="cyber-ai-bubble-box"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div style="font-weight:700; color:#fff; font-size:0.95rem;">oXy AI</div></div><div class="cyber-ai-content-flow">')
                st.markdown(msg["content"])
                st.html('</div></div></div>')

    if user_input := st.chat_input("Ask to oXy..."):
        st.html(f'<div style="display:flex; justify-content:flex-end; margin-bottom:20px;"><div class="cyber-user-bubble">{user_input}</div></div>')
        
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({
                "role": "system", 
                "content": "You are oXy AI, a highly advanced artificial intelligence developed by Zayn. Always assist users professionally and use code blocks when delivering scripts."
            })
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with open(FILE_ARSIP, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
            
        try:
            placeholder_loading = st.empty()
            with placeholder_loading.container():
                st.html("""
                <div style="display:flex; justify-content:flex-start;">
                    <div class="cyber-ai-bubble-box" style="margin-bottom:10px;">
                        <div class="ai-header-inline">
                            <div class="ai-mini-orb"></div>
                            <div style="font-weight:700; color:#fff; font-size:0.95rem;">oXy AI berpikir...</div>
                        </div>
                        <div class="typing-indicator">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
                """)
            
            response_stream = client.chat.completions.create(
                model="openrouter/auto", 
                messages=st.session_state.messages,
                stream=True
            )
            
            placeholder_loading.empty()
            
            def generate_stream_data():
                for chunk in response_stream:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            yield delta.content

            with st.container():
                st.html('<div style="display:flex; justify-content:flex-start;"><div class="cyber-ai-bubble-box"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div style="font-weight:700; color:#fff; font-size:0.95rem;">oXy AI</div></div><div class="cyber-ai-content-flow">')
                full_response = st.write_stream(generate_stream_data)
                st.html('</div></div></div>')
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            with open(FILE_ARSIP, "w", encoding="utf-8") as f:
                json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
            st.rerun()
            
        except Exception as e:
            placeholder_loading.empty()
            st.error(f"Gagal mengambil respons OpenRouter: {e}")
    
