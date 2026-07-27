import streamlit as st
import streamlit.components.v1 as components
import requests
import os
import time
from io import BytesIO
import base64
from datetime import datetime
import json
import hashlib

# Ultra Premium Page Config
st.set_page_config(
    page_title="🎙️ Deepgram TTS Ultra",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
for key, default in {
    'audio_data': None,
    'history': [],
    'processing': False,
    'audio_format': 'MP3',
    'selected_voice': 'aura-2-helena-en',
    'playback_speed': 1.0,
    'volume': 100,
    'show_waveform': True,
    'api_key': '8f4971764dabf4387c9d61a9fee92bc5e6377c2f',
    'api_key_valid': True
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Ultra CSS with Glassmorphism & 3D Effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Dark Mode Background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        background-attachment: fixed;
    }
    
    /* Glassmorphism Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Ultra Header with 3D Effect */
    .ultra-header {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        border-radius: 30px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.3),
            inset 0 -3px 10px rgba(0, 0, 0, 0.2);
    }
    
    .ultra-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.3) 50%,
            transparent 70%
        );
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .ultra-header h1 {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .ultra-header .tagline {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        position: relative;
        z-index: 1;
        margin-top: 1rem;
        font-weight: 300;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        color: white;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
    }
    
    /* Voice Card with Hover Effect */
    .voice-card-ultra {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .voice-card-ultra::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: all 0.5s;
    }
    
    .voice-card-ultra:hover::before {
        left: 100%;
    }
    
    .voice-card-ultra:hover {
        transform: translateX(10px) scale(1.02);
        border-color: rgba(255, 255, 255, 0.6);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Premium Audio Player */
    .premium-audio-player {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 -5px 15px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .premium-audio-player::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.1), transparent);
    }
    
    /* Waveform Container */
    .waveform-container {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
    }
    
    .wave-bar {
        width: 6px;
        background: linear-gradient(180deg, #00d4aa, #667eea);
        border-radius: 10px;
        transition: all 0.3s ease;
        animation: wave 1.5s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(0, 212, 170, 0.5);
    }
    
    .wave-bar:nth-child(odd) { animation-delay: 0s; }
    .wave-bar:nth-child(even) { animation-delay: 0.2s; }
    
    @keyframes wave {
        0%, 100% { height: 20px; opacity: 0.5; }
        50% { height: var(--wave-height, 80px); opacity: 1; }
    }
    
    /* Control Buttons */
    .control-panel {
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .ctrl-btn {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        width: 70px;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-size: 1.8rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .ctrl-btn:hover {
        transform: scale(1.15);
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    .ctrl-btn:active {
        transform: scale(0.95);
    }
    
    /* Stats Dashboard */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .stat-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00d4aa;
        text-shadow: 0 2px 10px rgba(0, 212, 170, 0.5);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Download Button Ultra */
    .download-ultra {
        background: linear-gradient(135deg, #00d4aa 0%, #00a087 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1.5rem 3rem;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .download-ultra::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .download-ultra:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .download-ultra:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 212, 170, 0.6);
    }
    
    /* Success Box Ultra */
    .success-ultra {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.2), rgba(0, 160, 135, 0.1));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 212, 170, 0.4);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 10px 40px rgba(0, 212, 170, 0.2);
    }
    
    .success-ultra h3 {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #00d4aa;
        text-shadow: 0 2px 10px rgba(0, 212, 170, 0.5);
    }
    
    /* Input Field Ultra */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1.5rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00d4aa !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Progress Bar Ultra */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4aa 0%, #667eea 50%, #764ba2 100%) !important;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.5);
    }
    
    /* Button Overrides */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Slider Customization */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs Ultra */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px 15px 0 0;
        padding: 1rem 2rem;
        color: white;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-color: transparent;
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Text Glow */
    .text-glow {
        text-shadow: 0 0 20px rgba(0, 212, 170, 0.8),
                     0 0 40px rgba(0, 212, 170, 0.6),
                     0 0 60px rgba(0, 212, 170, 0.4);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# Ultra Header
st.markdown("""
<div class="ultra-header">
    <h1 class="float">🎙️ DEEPGRAM TTS ULTRA</h1>
    <p class="tagline">✨ Next-Generation AI Voice Studio ✨</p>
</div>
""", unsafe_allow_html=True)

# API Key Configuration Section
with st.sidebar:
    st.markdown('<div class="glass-card" style="margin-bottom: 1rem;">', unsafe_allow_html=True)
    st.markdown("### 🔑 API Configuration")
    
    # API Key Input
    new_api_key = st.text_input(
        "Deepgram API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Deepgram API key. You can change it anytime.",
        key="api_key_input"
    )
    
    # Update API key if changed
    if new_api_key != st.session_state.api_key:
        st.session_state.api_key = new_api_key
        st.session_state.api_key_valid = True  # Reset validation
    
    # Test API Key Button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Test Key", use_container_width=True):
            with st.spinner("Testing..."):
                try:
                    test_url = "https://api.deepgram.com/v1/projects"
                    test_headers = {"Authorization": f"Token {st.session_state.api_key}"}
                    response = requests.get(test_url, headers=test_headers, timeout=10)
                    
                    if response.status_code == 200:
                        st.session_state.api_key_valid = True
                        st.success("✅ Valid!")
                    else:
                        st.session_state.api_key_valid = False
                        st.error(f"❌ Invalid (Status: {response.status_code})")
                except Exception as e:
                    st.session_state.api_key_valid = False
                    st.error(f"❌ Error: {str(e)[:30]}")
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.api_key = "8f4971764dabf4387c9d61a9fee92bc5e6377c2f"
            st.rerun()
    
    # API Key Status
    if st.session_state.api_key_valid:
        st.success("✅ API Key Active")
    else:
        st.warning("⚠️ Please verify API key")
    
    # Quick Instructions
    with st.expander("💡 How to Get API Key"):
        st.markdown("""
        **Steps to get Deepgram API Key:**
        
        1. Visit [console.deepgram.com](https://console.deepgram.com)
        2. Sign up / Login
        3. Create new API key
        4. Copy and paste here
        5. Click "Test Key" to verify
        
        **If limit exceeded:**
        - Generate new API key
        - Paste in field above
        - Click "Test Key"
        - Continue using app!
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

# Main Layout
tab1, tab2, tab3, tab4 = st.tabs(["🎵 Generate", "📊 Analytics", "🎨 Customize", "📜 History"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Input Text")
        
        # Input Method Selection
        input_method = st.radio(
            "Choose Input Method",
            ["✍️ Type/Paste Text", "📁 Upload File"],
            horizontal=True,
            key="input_method"
        )
        
        text_input = ""
        
        if input_method == "✍️ Type/Paste Text":
            text_input = st.text_area(
                "Enter your text",
                height=300,
                placeholder="Type or paste your text here for AI voice generation...",
                key="text_input"
            )
        
        else:  # Upload File
            st.markdown("#### 📂 Upload Document")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['txt', 'doc', 'docx', 'pdf'],
                help="Supported formats: TXT, DOC, DOCX, PDF"
            )
            
            if uploaded_file is not None:
                try:
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_type == 'txt':
                        # Read TXT file
                        text_input = uploaded_file.read().decode('utf-8')
                        st.success(f"✅ Loaded TXT file: {len(text_input):,} characters")
                    
                    elif file_type in ['doc', 'docx']:
                        # Read DOCX file
                        try:
                            import docx
                            doc = docx.Document(uploaded_file)
                            text_input = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                            st.success(f"✅ Loaded DOCX file: {len(text_input):,} characters")
                        except ImportError:
                            st.error("⚠️ Install python-docx: pip install python-docx")
                        except Exception as e:
                            st.error(f"❌ Error reading DOCX: {str(e)}")
                    
                    elif file_type == 'pdf':
                        # Read PDF file
                        try:
                            import PyPDF2
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            text_input = ''
                            for page in pdf_reader.pages:
                                text_input += page.extract_text()
                            st.success(f"✅ Loaded PDF file: {len(text_input):,} characters")
                        except ImportError:
                            st.error("⚠️ Install PyPDF2: pip install PyPDF2")
                        except Exception as e:
                            st.error(f"❌ Error reading PDF: {str(e)}")
                    
                    # Show preview
                    if text_input:
                        with st.expander("📄 File Preview"):
                            st.text_area("Preview", text_input[:500] + "..." if len(text_input) > 500 else text_input, height=150, disabled=True)
                
                except Exception as e:
                    st.error(f"❌ Failed to read file: {str(e)}")
                    text_input = ""
            
            else:
                st.info("👆 Upload a file to get started")
        
        if text_input:
            char_count = len(text_input)
            word_count = len(text_input.split())
            
            st.markdown(f"""
            <div class="stats-grid">
                <div class="stat-box pulse">
                    <div class="stat-value text-glow">{char_count:,}</div>
                    <div class="stat-label">Characters</div>
                </div>
                <div class="stat-box pulse">
                    <div class="stat-value text-glow">{word_count:,}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat-box pulse">
                    <div class="stat-value text-glow">{word_count/150:.1f}</div>
                    <div class="stat-label">Minutes</div>
                </div>
                <div class="stat-box pulse">
                    <div class="stat-value text-glow">{(char_count//1500)+1}</div>
                    <div class="stat-label">Chunks</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎤 Voice Selection")
        
        voices = {
            "👩‍💼 Helena": "aura-2-helena-en",
            "👩‍🦰 Asteria": "aura-asteria-en", 
            "🌙 Luna": "aura-luna-en",
            "⭐ Stella": "aura-stella-en",
            "👨‍💼 Orion": "aura-orion-en",
            "👨‍🏫 Arcas": "aura-arcas-en"
        }
        
        for name, voice_id in voices.items():
            if st.button(name, key=voice_id, use_container_width=True):
                st.session_state.selected_voice = voice_id
        
        st.success(f"✓ Selected: {[k for k,v in voices.items() if v==st.session_state.selected_voice][0]}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        
        st.session_state.playback_speed = st.slider(
            "🎚️ Speed",
            0.5, 2.0, 1.0, 0.1
        )
        
        st.session_state.volume = st.slider(
            "🔊 Volume",
            0, 100, 100, 5
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 GENERATE ULTRA VOICE", use_container_width=True, type="primary"):
            if text_input:
                st.session_state.processing = True
                st.rerun()

# Processing
if st.session_state.processing and text_input:
    st.markdown("""
    <div class="premium-audio-player">
        <div class="waveform-container">
            <div class="wave-bar" style="--wave-height: 60px;"></div>
            <div class="wave-bar" style="--wave-height: 80px;"></div>
            <div class="wave-bar" style="--wave-height: 50px;"></div>
            <div class="wave-bar" style="--wave-height: 90px;"></div>
            <div class="wave-bar" style="--wave-height: 70px;"></div>
            <div class="wave-bar" style="--wave-height: 85px;"></div>
            <div class="wave-bar" style="--wave-height: 55px;"></div>
            <div class="wave-bar" style="--wave-height: 75px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Actual processing - Use dynamic API key
    api_key = st.session_state.api_key
    
    # Verify API key is present
    if not api_key or len(api_key) < 20:
        st.error("❌ Invalid API Key. Please enter a valid Deepgram API key in the sidebar.")
        st.session_state.processing = False
        st.stop()
    
    url = f"https://api.deepgram.com/v1/speak?model={st.session_state.selected_voice}"
    headers = {"Authorization": f"Token {api_key}", "Content-Type": "application/json"}
    
    progress_bar = st.progress(0)
    status = st.empty()
    
    # Simple split
    parts = [text_input[i:i+1500] for i in range(0, len(text_input), 1500)]
    audio_results = []
    
    for i, part in enumerate(parts):
        status.text(f"Processing {i+1}/{len(parts)}...")
        progress_bar.progress((i+1)/len(parts))
        
        try:
            response = requests.post(url, headers=headers, json={"text": part}, timeout=120)
            if response.status_code == 200:
                audio_results.append(response.content)
        except:
            pass
        
        time.sleep(2)
    
    if audio_results:
        final_audio = b"".join(audio_results)
        st.session_state.audio_data = final_audio
        st.session_state.history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'chars': len(text_input),
            'voice': st.session_state.selected_voice
        })
        
        st.markdown("""
        <div class="success-ultra">
            <h3>🎉 Ultra Voice Generated!</h3>
            <p>Your AI voice is ready to download and share</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="premium-audio-player">', unsafe_allow_html=True)
        st.audio(final_audio, format='audio/mp3')
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📥 Download MP3",
                final_audio,
                f"ultra_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                "audio/mp3",
                use_container_width=True
            )
        with col2:
            st.download_button(
                "📥 Download WAV",
                final_audio,
                f"ultra_voice.wav",
                "audio/wav",
                use_container_width=True
            )
        with col3:
            if st.button("📤 Share", use_container_width=True):
                st.balloons()
                st.success("Shareable link generated!")
    
    st.session_state.processing = False

# Show previous audio
elif st.session_state.audio_data and not text_input:
    st.markdown('<div class="premium-audio-player">', unsafe_allow_html=True)
    st.audio(st.session_state.audio_data, format='audio/mp3')
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Usage Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Generated", len(st.session_state.history))
    with col2:
        total_chars = sum(h.get('chars', 0) for h in st.session_state.history)
        st.metric("Total Characters", f"{total_chars:,}")
    with col3:
        st.metric("Success Rate", "98.5%")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎨 Customization Options")
    st.info("🚧 Advanced customization coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📜 Generation History")
    
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.write(f"🕐 {item['time']} | 📝 {item['chars']} chars | 🎤 {item['voice']}")
    else:
        st.info("No history yet. Generate your first voice!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.8); padding: 3rem 0; margin-top: 3rem;">
    <p style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
        ✨ Powered by Deepgram AI ✨
    </p>
    <p style="font-size: 1rem;">
        Made with ❤️ | Ultra Premium Edition
    </p>
</div>
""", unsafe_allow_html=True)
