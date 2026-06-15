import streamlit as st
from google import genai

# 1. Konfigurasi Halaman & Favicon Ikon Tetesan Air
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. STYLING LIQUID GLASS iPHONE & CHAT ALIGNMENT SPECIALIST
st.markdown("""
<style>
    /* Mengubah warna latar belakang global ke Biru Gelap Ultra HD */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* 1. MENGHILANGKAN TOTAL KOTAK PUTIH DI AREA BAWAH MOBILE */
    footer {visibility: hidden !important;}
    header[data-testid="stHeader"] { background: transparent !important; }
    
    /* Memaksa transparan mutlak pada pembungkus bawah Streamlit */
    div[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stChatInputContainer"],
    .stChatInput,
    form, 
    div[class^="ststChatInput"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* 2. KOTAK KETIK INPUT CHAT DENGAN REAL iPHONE GLASS EFFECT */
    div[data-testid="stChatInputContainer"] > div {
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.25), 
                    inset 0 1px 1px 0 rgba(255, 255, 255, 0.3) !important;
        padding: 4px !important;
    }
    
    /* Memastikan teks yang diketik berwarna putih bersih kontras tinggi */
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* 3. RESTRUKTURISASI BALON CHAT: KANAN DAN KIRI */
    /* Mengubah container chat utama agar fleksibel */
    div[data-testid="stChatMessage"] {
        display: flex !important;
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin-bottom: 20px !important;
    }
    
    /* PENGGUNA (USER) DIPAKSA DI SEBELAH KANAN */
    div[data-testid="stChatMessageUser"] {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    
    /* ASISTEN (AI) TETAP DI SEBELAH KIRI */
    div[data-testid="stChatMessageAssistant"] {
        flex-direction: row !important;
        text-align: left !important;
    }
    
    /* Memaksa seluruh elemen teks di dalam chat berwarna putih HD */
    .stMarkdown, .stMarkdown p, p, span, h1, h2, h3 {
        color: #ffffff !important;
    }

    /* 4. BALON CHAT SPESIFIK DENGAN LIQUID GLASS iPHONE STYLE */
    /* Tampilan Isi Obrolan Pengguna (Kanan - Kaca Glossy Kebiruan) */
    div[data-testid="stChatMessageUser"] > div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(0, 162, 255, 0.25) 0%, rgba(56, 189, 248, 0.15) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px 20px 4px 20px !important; /* Sudut melengkung khas iPhone chat */
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 114, 255, 0.2),
                    inset 0 1px 2px 0 rgba(255, 255, 255, 0.4) !important;
        padding: 12px 18px !important;
        max-width: 80% !important;
        display: inline-block !important;
    }
    
    /* Tampilan Isi Obrolan AI (Kiri - Kaca Frosty Putih) */
    div[data-testid="stChatMessageAssistant"] > div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px 20px 20px 4px !important; /* Sudut melengkung khas iPhone chat */
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3),
                    inset 0 1px 1px 0 rgba(255, 255, 255, 0.2) !important;
        padding: 12px 18px !important;
        max-width: 80% !important;
        display: inline-block !important;
    }
    
    /* Menambahkan jarak halus pada avatar chat */
    div[data-testid="stChatMessageAvatar"] {
        margin-left: 10px !important;
        margin-right: 10px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 50% !important;
    }

    /* 5. TULISAN JUDUL METALLIC GLOW */
    .liquid-title {
        color: #00d2ff !important;
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        background: linear-gradient(to bottom, #ffffff 20%, #38bdf8 60%, #0072ff 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0px 4px 10px rgba(56, 189, 248, 0.5));
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

# Menampilkan Riwayat Obrolan dengan Layout Posisi Baru
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
        
