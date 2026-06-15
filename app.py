import streamlit as st
import streamlit.components.v1 as components
from google import genai

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS RESET & ULTRA iPHONE GLASS STYLING
st.markdown("""
<style>
    /* Latar Belakang Aplikasi Ultra Biru Gelap */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* Hilangkan Header & Footer */
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
    
    /* KOTAK INPUT UTAMA GLASS iPHONE EFFECT */
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
    .chat-row {
        display: flex !important;
        width: 100% !important;
        margin-bottom: 18px !important;
    }
    .align-user { justify-content: flex-end !important; }
    .align-ai { justify-content: flex-start !important; }

    /* USER BUBBLE: BIRU CERAH iPHONE */
    .iphone-user {
        background: #1aa1e2 !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 12px 18px !important;
        border-radius: 20px 20px 4px 20px !important;
        max-width: 80% !important;
        box-shadow: 0 4px 15px rgba(26, 161, 226, 0.3) !important;
    }

    /* AI BUBBLE: REAL LIQUID GLASS iPHONE (FROSTY DARK) */
    .iphone-ai {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, sans-serif;
        padding: 6px 18px !important;
        border-radius: 20px 20px 20px 4px !important;
        max-width: 90% !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    }

    /* Mencegah Teks Code Block Menjadi Putih Rusak */
    .iphone-ai code, .iphone-ai pre {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* JUDUL GLOW METALLIC */
    .liquid-title {
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 800 !important;
        font-size: 2.3rem !important;
        background: linear-gradient(to bottom, #ffffff 10%, #38bdf8 60%, #0072ff 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0px 4px 8px rgba(56, 189, 248, 0.5));
        margin-bottom: 2px !important;
    }
    .custom-caption { color: #7dd3fc !important; font-weight: 500; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT BACKGROUND ENGINE (Pembersih Kotak Putih Mobile)
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

# 4. HEADER UTAMA
st.markdown('<h1 class="liquid-title">💧 cvAI4 Assistant • By Zayn</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-caption">Lab cvAI4 Aktif • Created by -Oxy-</p>', unsafe_allow_html=True)

# API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key tidak ditemukan di Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. RENDER CHAT DENGAN STYLING KANAN-KIRI TANPA MERUSAK MARKDOWN
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.html(f'<div class="chat-row align-user"><div class="iphone-user">{msg["content"]}</div></div>')
    else:
        # Menggunakan st.html gabungan untuk mengisolasi bubble custom tanpa merusak isi markdown internal
        st.html('<div class="chat-row align-ai"><div class="iphone-ai">')
        st.markdown(msg["content"])
        st.html('</div></div>')

# INPUT FIELD CHAT
if user_input := st.chat_input("Tanyakan sesuatu, Tuan Gigs..."):
    st.html(f'<div class="chat-row align-user"><div class="iphone-user">{user_input}</div></div>')
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=user_input)
        
        st.html('<div class="chat-row align-ai"><div class="iphone-ai">')
        st.markdown(response.text)
        st.html('</div></div>')
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
        
