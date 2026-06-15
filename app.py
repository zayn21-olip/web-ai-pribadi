import streamlit as st
import streamlit.components.v1 as components
from google import genai

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS UTAMA & STYLING BALON CHAT (Aman dari Reset)
st.markdown("""
<style>
    /* Latar Belakang Aplikasi Ultra Biru HD */
    .stApp {
        background: linear-gradient(135deg, #02081e 0%, #051642 100%) !important;
        color: #ffffff !important;
    }
    
    /* Menghilangkan Header Default */
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden !important; }

    /* RESTRUKTURISASI CONTAINER CHAT AGAR BISA KANAN-KIRI */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px 0px !important;
        width: 100% !important;
        display: flex !important;
    }
    
    /* Pengguna (User) Dipaksa Rapat Kanan */
    div[data-testid="stChatMessageUser"] {
        flex-direction: row-reverse !important;
    }
    
    /* Asisten (AI) Dipaksa Rapat Kiri */
    div[data-testid="stChatMessageAssistant"] {
        flex-direction: row !important;
    }

    /* BALON CHAT USER: LIQUID GLASS iPHONE BIRU GLOSSY */
    div[data-testid="stChatMessageUser"] div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(0, 140, 255, 0.45) 0%, rgba(0, 90, 255, 0.25) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
        border-radius: 20px 20px 4px 20px !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 24px rgba(0, 114, 255, 0.3), 
                    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        max-width: 75% !important;
    }

    /* BALON CHAT AI: LIQUID GLASS iPHONE FROSTY WHITE */
    div[data-testid="stChatMessageAssistant"] div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px 20px 20px 4px !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 
                    inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        max-width: 75% !important;
    }

    /* Memaksa Semua Teks di Dalam Balon Berwarna Putih Terang */
    div[data-testid="stChatMessageContent"] p, 
    div[data-testid="stChatMessageContent"] span, 
    div[data-testid="stChatMessageContent"] div {
        color: #ffffff !important;
    }

    /* Avatar bulat estetik */
    div[data-testid="stChatMessageAvatar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* JUDUL DENGAN LIQUID GLASS STYLE iPHONE */
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

# 3. JAVASCRIPT INJECTION (Menghancurkan Sisa Putih di Bawah Secara Paksa)
components.html("""
<script>
    function fixStreamlitTheme() {
        // 1. Cari container paling bawah tempat input berada
        const bottomContainers = window.parent.document.querySelectorAll('div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"], .stChatInputContainer');
        bottomContainers.forEach(el => {
            el.style.setProperty('background-color', 'transparent', 'important');
            el.style.setProperty('background', 'transparent', 'important');
            el.style.setProperty('box-shadow', 'none', 'important');
            el.style.setProperty('border', 'none', 'important');
        });

        // 2. Ubah Kotak Input Utama Menjadi Efek Kaca iPhone Semu
        const inputForm = window.parent.document.querySelector('div[data-testid="stChatInputContainer"] > div');
        if (inputForm) {
            inputForm.style.setProperty('background', 'rgba(255, 255, 255, 0.1)', 'important');
            inputForm.style.setProperty('backdrop-filter', 'blur(20px)', 'important');
            inputForm.style.setProperty('-webkit-backdrop-filter', 'blur(20px)', 'important');
            inputForm.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.25)', 'important');
            inputForm.style.setProperty('border-radius', '30px', 'important');
            inputForm.style.setProperty('box-shadow', '0 4px 20px rgba(0,0,0,0.3), inset 0 1px 1px rgba(255,255,255,0.3)', 'important');
        }

        // 3. Pastikan Textarea Pengguna Berwarna Putih Bersih
        const textarea = window.parent.document.querySelector('div[data-testid="stChatInputContainer"] textarea');
        if (textarea) {
            textarea.style.setProperty('color', '#ffffff', 'important');
        }
    }

    // Jalankan berulang-ulang agar ketika user ngetik, warna putihnya tidak balik lagi
    setInterval(fixStreamlitTheme, 100);
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
            
