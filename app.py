import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time
import os
import json

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(page_title="oXy AI • By Zayn", page_icon="💧", layout="centered")

# 2. CSS RESET, KHUSUS TOMBOL TEKS HITAM, & NEON GEMINI WAVE LOADING
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* 🎯 FIX TOMBOL RESET: PAKSA TEKS WARNA HITAM PEKAT */
    div[data-testid="stColumn"] button {
        color: #000000 !important;
        font-weight: 700 !important;
        background-color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 12px !important;
    }
    
    div[data-testid="stColumn"] button p {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* MEMBERSIHKAN CONTAINER INPUT BAWAH STREAMLIT */
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
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.3) !important;
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
        color: #38bdf8 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        margin-left: 8px !important;
        margin-bottom: 6px !important;
    }
    
    .user-name-tag {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 12px !important;
        color: #a7f3d0 !important;
        font-weight: 700 !important;
        margin-right: 8px !important;
        margin-bottom: 6px !important;
    }

    /* 💧 KEMBALI KE ORIGINAL BALON CHAT USER (TEKS PUTIH ESTETIK) */
    .iphone-user {
        background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 12px 18px !important;
        border-radius: 20px 20px 4px 20px !important;
        max-width: 80% !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
    }
    .iphone-user p, .iphone-user span { color: #ffffff !important; }

    /* 💧 KEMBALI KE ORIGINAL BALON CHAT AI GLASS EFFECT (TEKS PUTIH ESTETIK) */
    .iphone-ai {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 12px 20px !important;
        border-radius: 4px 20px 20px 20px !important;
        max-width: 90% !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.2) !important;
    }
    .iphone-ai p, .iphone-ai span, .iphone-ai li, .iphone-ai h1, .iphone-ai h2, .iphone-ai h3 { 
        color: #ffffff !important; 
    }

    .iphone-ai code, .iphone-ai pre {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .liquid-title {
        font-family: '-apple-system', sans-serif;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(to right, #ffffff, #38bdf8, #a7f3d0);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .custom-caption { color: #7dd3fc !important; font-weight: 500; margin-bottom: 25px; }

    /* 🌊 ANIMASI LOADING GELOMBANG GEMINI CYAN MINT GLOW */
    .gemini-loading-box {
        display: flex;
        flex-direction: column;
        gap: 8px;
        width: 100%;
        padding: 6px 4px;
    }
    .gemini-wave {
        height: 12px;
        background: linear-gradient(90deg, #38bdf8 25%, #a7f3d0 50%, #38bdf8 75%);
        background-size: 200% 100%;
        animation: geminiWaveAnim 1.2s infinite linear;
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
    }
    .w-1 { width: 45%; }
    .w-2 { width: 85%; }
    .w-3 { width: 60%; }

    @keyframes geminiWaveAnim {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
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

# 4. HEADER UTAMA BRANDING
st.markdown('<h1 class="liquid-title">💧 oXy AI • By Zayn</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-caption">Lab cvAI4 Aktif • Persistent Archive Memory Enabled</p>', unsafe_allow_html=True)

or_api_key = st.secrets.get("OPENROUTER_API_KEY")
if not or_api_key:
    st.error("⚠️ Token OPENROUTER_API_KEY tidak ditemukan di menu Secrets Streamlit Anda.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=or_api_key)

# ==================== SISTEM ARSIP MEMORI FILE Teks ====================
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
# ======================================================================

if "messages" not in st.session_state:
    st.session_state.messages = muat_arsip_chat()

# TOMBOL RESET KUSTOM (Ditembak pakai CSS khusus teks hitam)
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
    
    # LOADING GELOMBANG GEMINI GLOWING
    st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI Memikirkan Jawaban...</div><div class="iphone-ai" style="background: rgba(255,255,255,0.1) !important;">')
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
            messages=[m for m in st.session_state.messages if m["role"] != "system"]
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
        
