import streamlit as st
from google import genai

# Konfigurasi tampilan halaman Web AI
st.set_page_config(page_title="Chatbot AI Saya", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot AI Pribadi Saya")
st.caption("Web AI ini terhubung langsung ke repositori GitHub dan Gemini API")

# Mengambil API Key dengan aman dari fitur rahasia (Secrets) Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key tidak ditemukan! Silakan masukkan 'GEMINI_API_KEY' di bagian Advanced Settings > Secrets di Dashboard Streamlit Anda.")
    st.stop()

# Inisialisasi AI Client
client = genai.Client(api_key=api_key)

# Membuat memori penyimpanan chat di browser agar AI ingat konteks
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat yang sudah ada di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input obrolan untuk pengguna
if user_input := st.chat_input("Ketik pesan Anda di sini..."):
    # Tampilkan pesan pengguna di layar
    with st.chat_message("user"):
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
    with st.chat_message("assistant"):
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
          
