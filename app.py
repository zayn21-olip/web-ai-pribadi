import streamlit as st
from google import genai

# 1. Konfigurasi Halaman & Favicon Ikon Tetesan Air
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS LIQUID GLASS iPHONE & BIRU ULTRA HD (Membersihkan Putih di Bawah)
st.markdown("""
<style>
    /* Mengubah warna latar belakang global ke Biru Gelap HD */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #e0f2fe !important;
    }
    
    /* MENYAPU BERSIH WARNA PUTIH DI BAGIAN BAWAH */
    div[data-testid="stBottom"], 
    div[data-testid="stBottomBlockContainer"],
    .stChatInputContainer {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    /* EFEK LIQUID GLASS iPHONE PADA KOTAK INPUT CHAT */
    .stChatInputContainer {
        border-radius: 30px !important;
        /* Menggunakan border semi-transparan putih di atas & kiri untuk efek kilauan kaca iPhone */
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 162, 255, 0.3), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
        padding: 4px !important;
    }
    
    /* Warna teks di dalam kotak ketik agar putih bersih */
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }
    
    /* EFEK LIQUID GLASS iPHONE PADA BALON OBROLAN (CHAT BUBBLES) */
    .stChatMessage {
        border-radius: 24px !important;
        margin-bottom: 16px !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.2) !important;
    }

    /* Balon chat asisten AI dengan kilauan kaca Biru HD yang tebal */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(0, 162, 255, 0.25) 0%, rgba(56, 189, 248, 0.05) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 162, 255, 0.25), 
                    inset 0 1px 3px rgba(255, 255, 255, 0.5) !important;
    }
    
    /* EFEK LIQUID GLASS iPHONE PADA TULISAN JUDUL (cvAI4 Assistant) */
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

# 3. KONTEN UTAMA APLIKASI DENGAN TAMPILAN LIQUID GLASS
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

# Menampilkan Riwayat Obrolan
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
            
