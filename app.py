import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="oXy AI • Core", page_icon="🔮", layout="centered")

# 2. INJEKSI CSS STRUKTUR: DEEP PURPLE CYBER INTERFACE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Background Deep Nebula */
    .stApp {
        background: radial-gradient(circle at 50% 15%, #18102c 0%, #090612 70%, #040308 100%) !important;
        color: #e2dcf0 !important;
        overflow-x: hidden;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* 🔮 ANIMATED ORB UTAMA */
    .cyber-core-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5%;
        margin-bottom: 15px;
    }
    .cyber-core {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, #a855f7 0%, #6b21a8 40%, #1e1b4b 80%, transparent 100%);
        border: 2px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 0 45px rgba(168, 85, 247, 0.6);
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
        0%, 100% { transform: scale(1); box-shadow: 0 0 45px rgba(168, 85, 247, 0.6); }
        50% { transform: scale(1.04); box-shadow: 0 0 60px rgba(168, 85, 247, 0.8); }
    }

    /* TEKS UTAMA BRANDING */
    .oxy-title {
        text-align: center;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        background: linear-gradient(to right, #ffffff 40%, #d8b4fe 70%, #a855f7 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .oxy-sub {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 1.1rem;
        margin-bottom: 30px !important;
    }

    /* 📱 KARTU BANNER PERTAMA */
    .welcome-card-cyber {
        background: rgba(25, 18, 46, 0.6) !important;
        border-radius: 28px !important;
        border: 1px solid rgba(168, 85, 247, 0.25) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        padding: 40px 30px;
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
    }
    .welcome-h1 { 
        font-size: 2.2rem !important; 
        font-weight: 800 !important; 
        color: #d8b4fe !important; 
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    .welcome-p { 
        font-size: 1.1rem; 
        color: #c7d2fe; 
        line-height: 1.7; 
        font-weight: 500;
    }
    .welcome-p strong {
        color: #f3e8ff !important;
        font-weight: 700;
    }

    /* BUTTON TO ENTER CORE */
    div[data-testid="stElementContainer"] button[key="enter_cyber_btn"] {
        background: #8b5cf6 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 14px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
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
        color: #d8b4fe !important;
        margin-bottom: 30px;
    }
    .about-profile-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        border: 2px solid #8b5cf6;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
        margin: 0 auto 25px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(13, 9, 24, 0.6);
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
        color: #c084fc !important;
        font-weight: 600;
    }

    /* CHAT CORE LAYOUT & GELEMBUNG INPUT */
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        background: rgba(13, 9, 24, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        padding: 6px 14px !important;
    }
    
    /* 💬 Gelembung User */
    .cyber-user-bubble {
        background: rgba(43, 29, 74, 0.4) !important;
        color: #f1f0f5 !important;
        padding: 13px 22px !important;
        border-radius: 20px 20px 4px 20px !important;
        border: 1px solid rgba(168, 85, 247, 0.25) !important;
        max-width: 85% !important;
    }
    
    /* 🔮 Gelembung AI (oXy AI Bubble Container) */
    .cyber-ai-bubble-box {
        background: rgba(25, 18, 46, 0.5) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 4px 20px 20px 20px !important;
        padding: 18px 22px !important;
        margin-bottom: 25px !important;
        max-width: 85% !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .ai-header-inline { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
    .ai-mini-orb {
        width: 18px; height: 18px; border-radius: 50%;
        background: radial-gradient(circle, #c084fc 0%, #6b21a8 70%);
        border: 1px solid rgba(168, 85, 247, 0.5);
    }
    .cyber-ai-content-flow { color: #dbd5ea !important; line-height: 1.7 !important; }
    
    div[data-testid="stMarkdownContainer"] pre {
        background-color: #06040a !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 16px !important;
    }

    /* 🟢 ANIMASI GELEMBUNG PEMIKIR (GEMINI TYPING EFFECT) */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 5px 10px;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #a855f7;
        border-radius: 50%;
        animation: cyberBlink 1.4s infinite both;
    }
    .typing-dot:nth-child(2) { animation-delay: .2s; background-color: #c084fc; }
    .typing-dot:nth-child(3) { animation-delay: .4s; background-color: #d8b4fe; }

    @keyframes cyberBlink {
        0%, 100% { transform: scale(0.8); opacity: 0.4; }
        50% { transform: scale(1.2); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# 3. FIX OVERLAY INTERFACE JAVASCRIPT
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

# ================= MANAJEMEN HALAMAN APP =================
if "sudah_masuk" not in st.session_state:
    st.session_state.sudah_masuk = False

# 🏠 HALAMAN 1: WELCOME SCREEN
if not st.session_state.sudah_masuk:
    st.markdown('<div class="cyber-core-container"><div class="cyber-core"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title">oXy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="oxy-sub">Apa yang bisa saya bantu?</p>', unsafe_allow_html=True)
    
    st.html("""
    <div class="welcome-card-cyber">
        <div class="welcome-h1">Halo, Saya oXy</div>
        <div class="welcome-p">
            Seorang <strong>Pengembang Perangkat Lunak</strong> yang bersemangat menciptakan solusi inovatif.
        </div>
    </div>
    """)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Lihat Proyek Saya 🔮", key="enter_cyber_btn", use_container_width=True):
            st.session_state.sudah_masuk = True
            st.rerun()
            
    st.html("""
    <div class="about-section-container">
        <div class="about-title">Tentang Saya</div>
        <div class="about-profile-circle">
            <div class="about-profile-text">oXy Core</div>
        </div>
    </div>
    <div class="about-description-box">
        <p class="about-text-p">
            <span class="about-highlight">oXy AI</span> adalah entitas sistem kecerdasan buatan siber mutakhir yang dirancang khusus oleh <span class="about-highlight">Zayn</span> untuk membantu mempercepat alur kerja pengembangan perangkat lunak, perakitan skrip kode, dan manajemen logika komputasi secara cerdas.
        </p>
    </div>
    """)

# 💬 HALAMAN 2: INTERFACE CHAT CORE UTAMA (KONEKSI OPENROUTER)
else:
    st.markdown('<div class="cyber-core-container" style="margin-top:2%;"><div class="cyber-core" style="width:70px; height:70px; box-shadow: 0 0 25px rgba(168,85,247,0.4);"></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="oxy-title" style="font-size: 1.8rem !important;">oXy AI Core</h1>', unsafe_allow_html=True)
    st.markdown('<p class="oxy-sub" style="font-size: 0.85rem; margin-bottom: 20px !important;">Powered by OpenRouter • Lab Active</p>', unsafe_allow_html=True)

    # Membaca token OpenRouter dari secrets
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

    # Perulangan menampilkan chat history
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
                "content": "You are oXy AI, a highly advanced artificial intelligence developed by Zayn. Always assist Tuan Gigs professionally and use code blocks when delivering scripts."
            })
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with open(FILE_ARSIP, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
            
        try:
            # 🟢 PROSES PENAMPILAN GELEMBUNG LOADING MENGETIK KUSTOM
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
            
            # Request ke API dilakukan saat gelembung mengetik di atas menyala
            response = client.chat.completions.create(
                model="openrouter/auto", 
                messages=st.session_state.messages,
                stream=False
            )
            full_response = response.choices[0].message.content
            
            # Hapus gelembung loading, ganti dengan teks asli jawaban AI
            placeholder_loading.empty()
            
            with st.container():
                st.html('<div style="display:flex; justify-content:flex-start;"><div class="cyber-ai-bubble-box"><div class="ai-header-inline"><div class="ai-mini-orb"></div><div style="font-weight:700; color:#fff; font-size:0.95rem;">oXy AI</div></div><div class="cyber-ai-content-flow">')
                st.markdown(full_response)
                st.html('</div></div></div>')
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            with open(FILE_ARSIP, "w", encoding="utf-8") as f:
                json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
            st.rerun()
        except Exception as e:
            placeholder_loading.empty()
            st.error(f"Gagal mengambil respons OpenRouter: {e}")
