import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(page_title="oXy AI • By Zayn", page_icon="💧", layout="centered")

# 2. CSS RESET & ULTRA iPHONE GLASS GEN Z STYLING
st.markdown("""
<style>
    /* Latar Belakang Aplikasi Ultra Biru Gelap Cyber */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* Hilangkan Header & Footer Bawaan Streamlit */
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

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
    
    /* KOTAK INPUT UTAMA NEON GLASS EFFECT */
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.3), 
                    inset 0 1px 1px 0 rgba(255, 255, 255, 0.2) !important;
        padding: 4px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* STRUCTURE ALIGNMENT CHAT (KANAN & KIRI) */
    .chat-container-block {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        margin-bottom: 22px !important;
    }
    .align-user { align-items: flex-end !important; }
    .align-ai { align-items: flex-start !important; }

    /* LABEL DI ATAS BALON CHAT (NAMA + AVATAR EMOJI) */
    .ai-name-tag {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 12px !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        margin-left: 8px !important;
        margin-bottom: 6px !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .user-name-tag {
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        font-size: 12px !important;
        color: #a7f3d0 !important;
        font-weight: 700 !important;
        margin-right: 8px !important;
        margin-bottom: 6px !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* USER BUBBLE: GRADIENT iPHONE STYLE */
    .iphone-user {
        background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 12px 18px !important;
        border-radius: 20px 20px 4px 20px !important;
        max-width: 80% !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
    }

    /* AI BUBBLE: LIQUID GLASS DENGAN PENDARAN NEON */
    .iphone-ai {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 10px 20px !important;
        border-radius: 4px 20px 20px 20px !important;
        max-width: 90% !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
                    0 0 15px rgba(56, 189, 248, 0.15), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.2) !important;
    }

    /* Memperbaiki Pewarnaan Teks di Code Block agar Kontras */
    .iphone-ai code, .iphone-ai pre {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* JUDUL GLOW LIQUID EFFECT */
    .liquid-title {
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(to right, #ffffff, #38bdf8, #a7f3d0);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0px 4px 12px rgba(56, 189, 248, 0.4));
        margin-bottom: 2px !important;
    }
    .custom-caption { color: #7dd3fc !important; font-weight: 500; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT ENGINE (Penjaga Background Transparan di Mobile)
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
st.markdown('<p class="custom-caption">Lab cvAI4 Aktif • Powered by OpenRouter Free Engine</p>', unsafe_allow_html=True)

# Ambil Token OpenRouter dari Secrets
or_api_key = st.secrets.get("OPENROUTER_API_KEY")
if not or_api_key:
    st.error("⚠️ Token OPENROUTER_API_KEY tidak ditemukan di menu Secrets Streamlit Anda.")
    st.stop()

# Hubungkan Klien OpenAI ke Server OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=or_api_key
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. RENDER UTAMA HISTORI CHAT DARI MEMORI
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.html(f'<div class="chat-container-block align-user"><div class="user-name-tag">Tuan Gigs 👨‍💻</div><div class="iphone-user">{msg["content"]}</div></div>')
    else:
        st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI • By Zayn</div><div class="iphone-ai">')
        st.markdown(msg["content"])
        st.html('</div></div>')

# INPUT FIELD CHAT UTAMA
if user_input := st.chat_input("Tanyakan sesuatu, Tuan Gigs..."):
    # Tampilkan pesan user instan di layar
    st.html(f'<div class="chat-container-block align-user"><div class="user-name-tag">Tuan Gigs 👨‍💻</div><div class="iphone-user">{user_input}</div></div>')
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Tembak API OpenRouter menggunakan jalur model gratisan otomatis
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": user_input}]
        )
        full_response = response.choices[0].message.content
        
        # Munculkan wadah balon chat AI kustom
        st.html('<div class="chat-container-block align-ai"><div class="ai-name-tag">🤖 oXy AI • By Zayn</div><div class="iphone-ai">')
        
        # EFEK KETIKAN BERJALAN PREMIUM (STREAMING TEXT EFFECT)
        placeholder = st.empty()
        displayed_text = ""
        for word in full_response.split(" "):
            displayed_text += word + " "
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.03)
        placeholder.markdown(full_response)
        st.html('</div></div>')
        
        # Amankan pesan ke dalam memori session_state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Waduh Tuan, ada kendala pada server OpenRouter: {e}")
        
