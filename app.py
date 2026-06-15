import streamlit as st
from google import genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="cvAI4 Assistant", page_icon="💧", layout="centered")

# 2. CSS Liquid Glass Biru Muda (Semua jadi Biru, Putih-putih hilang)
st.markdown("""
<style>
    /* Paksa semua latar belakang jadi biru tua dan transparan */
    .stApp, .stAppHeader, div[data-testid="stBottom"] {
        background: linear-gradient(135deg, #061033 0%, #0b2466 100%) !important;
    }
    
    /* Hilangkan background putih header & footer */
    header, footer, .stAppHeader, div[data-testid="stBottom"] {
        background: transparent !important;
    }

    /* Efek Liquid Glass untuk Input Chat */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid rgba(56, 189, 248, 0.7) !important;
        background-color: rgba(6, 16, 51, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.3) !important;
    }
    
    /* Balon Chat Glass */
    .stChatMessage {
        border-radius: 20px !important;
        background-color: rgba(56, 189, 248, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        color: #e0f2fe !important;
    }

    h1, h2, h3 { color: #38bdf8 !important; text-shadow: 0 0 15px #38bdf8; }
    .stMarkdown, p, div { color: #e0f2fe !important; }
</style>
""", unsafe_allow_html=True)

# 3. Konten Aplikasi
st.title("💧 cvAI4 Assistant • By Zayn")
st.caption("Lab cvAI4 Aktif • Created by -Oxy-")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key tidak ditemukan! Masukkan di Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

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
            
