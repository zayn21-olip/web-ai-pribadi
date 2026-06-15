import streamlit as st
from google import genai

# 1. Konfigurasi tampilan halaman Web AI
st.set_page_config(page_title="cvAI4 Assistant", page_icon="👾", layout="centered")

# 2. SUNTIKAN KODE CSS UNTUK MERUBAH TAMPILAN JADI TAMPAN ✨
st.markdown("""
<style>
    /* Mengubah warna latar belakang utama (Dark Space Theme) */
    .stApp {
        background: linear-gradient(135deg, #0b0914 0%, #110e25 100%);
        color: #f4f0ff;
    }
    
    /* Mempercantik kotak input chat di bagian bawah */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid #7f5af0 !important;
        background-color: #161426 !important;
        box-shadow: 0 4px 15px rgba(127, 90, 240, 0.2);
    }
    
    /* Memberikan efek neon pada judul utama */
    h1 {
        color: #a78bfa !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 800 !important;
        text-shadow: 0px 0px 15px rgba(167, 139, 250, 0.6);
        letter-spacing: 1px;
    }
    
    /* Mengubah dekorasi teks caption */
    .stCaption {
        color: #94a3b8 !important;
        font-style: italic;
    }
    
    /* Mempercantik tampilan block teks markdown di dalam chat */
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Judul Utama Aplikasi dengan Identitas Anda
st.title("👾 cvAI4 Assistant")
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

# Menampilkan riwayat chat yang sudah ada di layar dengan Avatar Keren
for message in st.session_state.messages:
    avatar_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Kotak input obrolan untuk pengguna
if user_input := st.chat_input("Ketik pesan Anda di sini, Tuan..."):
    # Tampilkan pesan pengguna di layar
    with st.chat_message("user", avatar="🧑‍💻"):
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
            
