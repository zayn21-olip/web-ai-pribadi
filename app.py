import streamlit as st
from google import genai

# 1. Konfigurasi tampilan halaman Web AI
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. SUNTIKAN KODE CSS UNTUK EFEK LIQUID GLASS BIRU 💎
st.markdown("""
<style>
    /* Mengubah warna latar belakang utama (Deep Liquid Blue Theme) */
    .stApp {
        background: linear-gradient(135deg, #02011a 0%, #050c2d 100%);
        color: #ffffff;
    }
    
    /* EFEK LIQUID GLASS PADA BALON CHAT 💧 */
    .stChatMessage {
        border-radius: 20px !important;
        margin-bottom: 15px !important;
        background-color: rgba(0, 160, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 15px rgba(0, 160, 255, 0.1) !important;
        overflow: hidden !important;
    }

    /* Gradient kilau kaca di balon chat assistant */
    .stChatMessage:nth-child(even) {
        background: linear-gradient(135deg, rgba(0, 160, 255, 0.1) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
        border: 1px solid rgba(0, 160, 255, 0.2) !important;
    }

    /* EFEK LIQUID GLASS PADA KOTAK INPUT 🧊 */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid rgba(0, 160, 255, 0.5) !important;
        background-color: rgba(22, 20, 38, 0.7) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        box-shadow: 0 4px 15px rgba(0, 160, 255, 0.2) !important;
        background-image: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%) !important;
    }
    
    /* Mempercantik tampilan block teks markdown di dalam chat */
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #ffffff !important;
    }
    
    /* Warna teks di input container agar tetap terbaca */
    .stChatInputContainer input {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Judul Utama Aplikasi dengan Identitas Anda
st.title("👾 cvAI4 Assistant • By Zayn")
st.caption("Lab cvAI4 Aktif • Created by -Oxy-")

# Mengambil API Key dengan aman dari fitur rahasia (Secrets) Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key tidak ditemukan! Silakan masukkan 'GEMINI_API_KEY' di bagian Advanced Settings > Secrets di Streamlit Cloud.")
    st.stop()

# Inisialisasi AI Client
client = genai.Client(api_key=api_key)

# Membuat memori penyimpanan chat di browser agar AI ingat konteks
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat yang sudah ada di layar dengan Avatar Keren (Biru)
for message in st.session_state.messages:
    avatar_icon = "👨‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Kotak input obrolan untuk pengguna
if user_input := st.chat_input("Ketik pesan Anda di sini, Tuan Zayn..."):
    # Tampilkan pesan pengguna di layar
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_input)
        
    # Simpan pesan ke riwayat memori
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Gabungkan riwayat chat agar AI paham konteks obrolan dari atas
    konteks_obrolan = []
    for msg in st.session_state.messages:
        role_name = "User" if msg["role"] == "user" else "Model"
        konteks_obrolan.append(f"{role_name}: {msg['content']}")
        
    prompt_lengkap = "\n".join(konteks_obrolan)
    
    # Ambil respons dari model AI Gemini
    with st.chat_message("assistant", avatar="🤖"):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_lengkap,
            )
            st.markdown(response.text)
            # Simpan respons AI ke riwayat memori
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Gagal mengambil respons dari AI: {e}")
    
