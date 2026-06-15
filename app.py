import streamlit as st
import streamlit.components.v1 as components
from google import genai

# 1. Konfigurasi Halaman & Favicon Ikon Tetesan Air
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS UTAMA: MEMBERSIHKAN ELEMEN BAWAAN & BACKGROUND ULTRA BIRU HD
st.markdown("""
<style>
    /* Mengubah warna latar belakang global aplikasi */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* Menghilangkan Header & Footer Default Streamlit */
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* MENGHANCURKAN TOTAL WARNA PUTIH DI CONTAINER BAWAH */
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
    
    /* KOTAK KETIK INPUT CHAT GLASS iPHONE STYLE */
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
    
    /* Memastikan teks saat mengetik berwarna putih bersih */
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* 3. ARSITEKTUR BALON CHAT KUSTOM KANAN-KIRI (REKAYASA HTML) */
    .chat-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-bottom: 15px;
    }
    
    /* Baris Obrolan Pengguna (Mendorong ke Kanan) */
    .row-user {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-bottom: 12px;
    }
    
    /* Baris Obrolan AI (Mendorong ke Kiri) */
    .row-ai {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 12px;
    }
    
    /* BALON CHAT PENGGUNA: KANAN - BIRU CERAH iPHONE */
    .bubble-user {
        background: #1aa1e2 !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(26, 161, 226, 0.3) !important;
        word-wrap: break-word;
    }
    
    /* BALON CHAT AI: KIRI - GLASS FROSTY DARK/WHITE */
    .bubble-ai {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%) !important;
        color: #ffffff !important;
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        max-width: 85%;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        word-wrap: break-word;
    }

    /* KILAUAN TEKS JUDUL UTAMA */
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
    
    .custom-caption {
        color: #7dd3fc !important;
        font-weight: 500;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT ENGINE INJECTION (Pembersih Latar Putih Real-Time)
components.html("""
<script>
    function forceClearWhiteBoxes() {
        const targets = window.parent.document.querySelectorAll('div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"], .stChatInputContainer, form');
        targets.forEach(el => {
            el.style.setProperty('background-color', 'transparent', 'important');
            el.style.setProperty('background', 'transparent', 'important');
            el.style.setProperty('box-shadow', 'none', 'important');
            el.style.setProperty('border', 'none', 'important');
        });
    }
    setInterval(forceClearWhiteBoxes, 50);
</script>
""", height=0, width=0)

# 4. KONTEN UTAMA APLIKASI
st.markdown('<h1 class="liquid-title">💧 cvAI4 Assistant • By Zayn</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-caption">Lab cvAI4 Aktif • Created by -Oxy-</p>', unsafe_allow_html=True)

# Mengambil API Key dari Secrets Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key tidak ditemukan! Masukkan di Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. RENDER CHAT MENGGUNAKAN HTML KUSTOM (Anti Kotak Abu-Abu Kaku)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="row-user"><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="row-ai"><div class="bubble-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)

# Kotak Input Tempat Mengetik Pesan
if user_input := st.chat_input("Tanyakan sesuatu, Tuan Gigs..."):
    # Tampilkan chat user instan di sebelah kanan
    st.markdown(f'<div class="row-user"><div class="bubble-user">{user_input}</div></div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=user_input)
        # Tampilkan balasan AI instan di sebelah kiri dengan Liquid Glass
        st.markdown(f'<div class="row-ai"><div class="bubble-ai">{response.text}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
        
