import streamlit as st
from google import genai

# 1. Konfigurasi Halaman & Favicon Ikon Tetesan Air
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS ANTI-WHITE CONTAINER & TEKS ULTRA KONTRAST HD
st.markdown("""
<style>
    /* Mengubah warna latar belakang global ke Biru Gelap HD */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* MENYAPU BERSIH WARNA PUTIH DI SELURUH AREA BAWAH STREAMLIT */
    footer {visibility: hidden !important;}
    header[data-testid="stHeader"] { background: transparent !important; }
    
    /* Menembus paksa semua lapisan container pembungkus bawah */
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
    
    /* KOTAK INPUT CHAT LIQUID GLASS iPHONE ASLI */
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 162, 255, 0.4), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
        padding: 4px !important;
    }
    
    /* Warna teks di dalam kotak ketik (saat mengetik) agar putih bersih */
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* MEMAKSA TEKS CHAT PENGGUNA & AI AGAR KELIHAN JELAS (WARNA PUTIH) */
    .stChatMessage, .stMarkdown, .stMarkdown p, p, span, div {
        color: #ffffff !important;
    }
    
    /* BALON OBROLAN (CHAT BUBBLES) LIQUID GLASS */
    .stChatMessage {
        border-radius: 24px !important;
        margin-bottom: 16px !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.3) !important;
    }

    /* Balon chat milik AI dibuat bercahaya Biru Neon HD */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(0, 162, 255, 0.3) 0%, rgba(56, 189, 248, 0.08) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 162, 255, 0.3), 
                    inset 0 1px 3px rgba(255, 255, 255, 0.6) !important;
    }
    
    /* EFEK LIQUID GLASS PADA TULISAN JUDUL UTAMA */
    .liquid-title {
        color: #00d2ff !important;
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 800 !important;
        font-size: 2.6rem !important;
        background: linear-gradient(to bottom, #ffffff 30%, #38bdf8 70%, #0072ff 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0px 4px 12px rgba(56, 189, 248, 0.6));
        margin-bottom: 2px !important;
    }
    
    .custom-caption {
        color: #7dd3fc !important;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# 3. KONTEN UTAMA APLIKASI
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

# Menampilkan Riwayat Obrolan (Teks dipastikan Kontras Tinggi)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Kotak Input Tempat Mengetik Pesan
if user_input := st.chat_input("Tanyakan sesuatu, Tuan Zayn..."):
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant", avatar="🤖"):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            
