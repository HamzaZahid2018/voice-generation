import streamlit as st
import requests
import os
import time
from io import BytesIO
import base64
from datetime import datetime
import json

# Page config with custom theme
st.set_page_config(
    page_title="Deepgram TTS Premium",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #00d4aa;
        --error-color: #ff6b6b;
    }
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header */
    .premium-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .premium-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .premium-header p {
        font-size: 1.3rem;
        margin-top: 0.5rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Voice Card */
    .voice-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .voice-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border-color: var(--primary-color);
    }
    
    /* Audio Player Custom */
    .audio-player-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    .audio-player-container audio {
        width: 100%;
        border-radius: 50px;
    }
    
    /* Download Button Enhanced */
    .download-btn-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .download-btn {
        flex: 1;
        min-width: 200px;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .download-btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .download-btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .download-btn-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    .download-btn-secondary:hover {
        background: #667eea;
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Success Box */
    .success-box {
        padding: 2rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    .success-box h3 {
        color: #155724;
        margin-bottom: 1rem;
    }
    
    /* Stats Card */
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Waveform Animation */
    .waveform {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        height: 60px;
        margin: 1rem 0;
    }
    
    .waveform-bar {
        width: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        animation: wave 1s ease-in-out infinite;
    }
    
    .waveform-bar:nth-child(1) { animation-delay: 0s; height: 20px; }
    .waveform-bar:nth-child(2) { animation-delay: 0.1s; height: 35px; }
    .waveform-bar:nth-child(3) { animation-delay: 0.2s; height: 50px; }
    .waveform-bar:nth-child(4) { animation-delay: 0.3s; height: 35px; }
    .waveform-bar:nth-child(5) { animation-delay: 0.4s; height: 20px; }
    
    @keyframes wave {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(1.5); }
    }
    
    /* Format Selector */
    .format-selector {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .format-option {
        flex: 1;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .format-option:hover {
        border-color: #667eea;
        background: #f5f7ff;
    }
    
    .format-option.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Audio Controls */
    .audio-controls {
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
        margin: 1.5rem 0;
    }
    
    .control-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .control-btn:hover {
        background: #667eea;
        color: white;
        transform: scale(1.1);
    }
    
    /* Tabs Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        background: rgba(255, 255, 255, 0.7);
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Input Fields */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'audio_format' not in st.session_state:
    st.session_state.audio_format = 'MP3'

# Header
st.markdown("""
<div class="premium-header">
    <h1>🎙️ Deepgram TTS Premium</h1>
    <p>✨ AI-Powered Voice Generation with Studio Quality ✨</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key = st.text_input(
        "🔑 API Key",
        type="password",
        value=os.getenv("DEEPGRAM_API_KEY", "8f4971764dabf4387c9d61a9fee92bc5e6377c2f")
    )
    
    st.divider()
    
    # Voice Selection with Preview
    st.markdown("### 🎤 Voice Selection")
    
    voice_categories = {
        "👩 Female Voices": {
            "aura-2-helena-en": {"name": "Helena", "desc": "Professional & Clear", "emoji": "👩‍💼"},
            "aura-asteria-en": {"name": "Asteria", "desc": "Warm & Friendly", "emoji": "👩‍🦰"},
            "aura-luna-en": {"name": "Luna", "desc": "Soft & Calm", "emoji": "👩‍🎤"},
            "aura-stella-en": {"name": "Stella", "desc": "Bright & Energetic", "emoji": "👩‍🚀"},
        },
        "👨 Male Voices": {
            "aura-orion-en": {"name": "Orion", "desc": "Deep & Authoritative", "emoji": "👨‍💼"},
            "aura-arcas-en": {"name": "Arcas", "desc": "Professional", "emoji": "👨‍🏫"},
            "aura-perseus-en": {"name": "Perseus", "desc": "Young & Dynamic", "emoji": "👨‍💻"},
            "aura-angus-en": {"name": "Angus", "desc": "Casual & Relaxed", "emoji": "👨‍🎨"},
        }
    }
    
    category = st.selectbox("Category", list(voice_categories.keys()))
    
    voices = voice_categories[category]
    
    for voice_id, info in voices.items():
        if st.button(f"{info['emoji']} {info['name']}", key=voice_id, use_container_width=True):
            st.session_state.selected_voice = voice_id
        st.caption(info['desc'])
    
    if 'selected_voice' not in st.session_state:
        st.session_state.selected_voice = "aura-2-helena-en"
    
    st.success(f"Selected: {voices.get(st.session_state.selected_voice, {}).get('name', 'Helena')}")
    
    st.divider()
    
    # Advanced Settings
    with st.expander("🎛️ Advanced Settings"):
        chunk_size = st.slider("Chunk Size", 500, 2500, 1500, 100)
        max_retries = st.slider("Max Retries", 1, 10, 5)
        timeout = st.slider("Timeout (s)", 30, 180, 120, 10)
    
    st.divider()
    
    # Stats
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Generated", len(st.session_state.history))
    with col2:
        total_chars = sum(h.get('chars', 0) for h in st.session_state.history)
        st.metric("Characters", f"{total_chars:,}")

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Text Input")
    
    # Input Method Selection
    input_method = st.radio(
        "Input Method",
        ["✍️ Type/Paste", "📁 Upload File", "📋 Templates"],
        horizontal=True
    )
    
    text_input = ""
    
    if input_method == "✍️ Type/Paste":
        text_input = st.text_area(
            "Enter your text",
            height=300,
            placeholder="Type or paste your text here...",
            help="Maximum recommended: 5000 characters per generation"
        )
    
    elif input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload text file",
            type=['txt', 'md', 'doc', 'docx'],
            help="Supported formats: TXT, MD, DOC, DOCX"
        )
        if uploaded_file:
            try:
                text_input = uploaded_file.read().decode('utf-8')
                st.success(f"✓ Loaded {len(text_input):,} characters")
            except:
                st.error("Failed to read file")
    
    elif input_method == "📋 Templates":
        templates = {
            "🎬 Movie Trailer": "In a world where artificial intelligence meets human creativity, one voice will change everything. Coming soon to a device near you.",
            "📢 Announcement": "Attention all team members. We are pleased to announce our latest achievement. Thank you for your dedication and hard work.",
            "📚 Audiobook Sample": "Chapter One. It was a bright cold day in April, and the clocks were striking thirteen. The story begins here.",
            "🎤 Podcast Intro": "Welcome back to another episode. Today we have an amazing guest who will share incredible insights. Let's dive right in.",
            "🎓 Educational": "In this lesson, we will explore the fundamental concepts that shape our understanding. Pay close attention to the following key points.",
        }
        
        selected_template = st.selectbox("Choose Template", list(templates.keys()))
        text_input = templates[selected_template]
        st.text_area("Preview", text_input, height=150, disabled=True)
    
    # Text Stats
    if text_input:
        char_count = len(text_input)
        word_count = len(text_input.split())
        est_duration = word_count / 150  # ~150 words per minute
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{char_count:,}</div>
                <div class="stats-label">Characters</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{word_count:,}</div>
                <div class="stats-label">Words</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{est_duration:.1f}</div>
                <div class="stats-label">Minutes</div>
            </div>
            """, unsafe_allow_html=True)
        with col_d:
            chunks = (char_count // chunk_size) + 1
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{chunks}</div>
                <div class="stats-label">Chunks</div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎨 Output Options")
    
    # Format Selection
    st.markdown("#### Audio Format")
    formats = {
        "MP3": {"icon": "🎵", "desc": "Universal compatibility"},
        "WAV": {"icon": "🎼", "desc": "Studio quality"},
        "OGG": {"icon": "🎹", "desc": "Open source"}
    }
    
    for fmt, info in formats.items():
        if st.button(f"{info['icon']} {fmt}", key=f"fmt_{fmt}", use_container_width=True):
            st.session_state.audio_format = fmt
        st.caption(info['desc'])
    
    st.success(f"Format: {st.session_state.audio_format}")
    
    st.divider()
    
    # Quality Settings
    st.markdown("#### Quality Settings")
    quality = st.select_slider(
        "Bitrate",
        options=["64 kbps", "128 kbps", "192 kbps", "256 kbps", "320 kbps"],
        value="192 kbps"
    )
    
    st.divider()
    
    # Quick Actions
    st.markdown("#### Quick Actions")
    if st.button("🗑️ Clear Text", use_container_width=True):
        text_input = ""
        st.rerun()
    
    if st.button("📋 Copy to Clipboard", use_container_width=True):
        if text_input:
            st.toast("Text copied!")

# Generate Section
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate_btn = st.button(
        "🎵 GENERATE SPEECH",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.processing or not text_input or not api_key
    )

# Processing Logic
if generate_btn:
    st.session_state.processing = True
    
    def split_text(text, max_length):
        sentences = text.replace('\n', ' ').split('. ')
        parts = []
        current_part = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if not sentence.endswith('.'):
                sentence += '.'
            if len(current_part) + len(sentence) > max_length and current_part:
                parts.append(current_part.strip())
                current_part = sentence
            else:
                current_part += " " + sentence if current_part else sentence
        if current_part.strip():
            parts.append(current_part.strip())
        return parts
    
    def get_audio_chunk(url, headers, text_part, retries):
        payload = {"text": text_part}
        for attempt in range(retries):
            try:
                response = requests.post(
                    url, headers=headers, json=payload,
                    timeout=(15, timeout)
                )
                if response.status_code == 200:
                    return response.content, None
                time.sleep(3)
            except:
                if attempt < retries - 1:
                    time.sleep(3)
        return None, "Failed"
    
    # Setup
    url = f"https://api.deepgram.com/v1/speak?model={st.session_state.selected_voice}"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    
    text_parts = split_text(text_input, chunk_size)
    total_parts = len(text_parts)
    
    # Waveform Animation
    st.markdown("""
    <div class="waveform">
        <div class="waveform-bar"></div>
        <div class="waveform-bar"></div>
        <div class="waveform-bar"></div>
        <div class="waveform-bar"></div>
        <div class="waveform-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔄 Generating Audio...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        success_metric = st.empty()
    with col2:
        failed_metric = st.empty()
    with col3:
        time_metric = st.empty()
    
    audio_results = {}
    start_time = time.time()
    
    for i, part in enumerate(text_parts, 1):
        elapsed = time.time() - start_time
        progress_bar.progress(i / total_parts)
        status_text.text(f"Processing part {i}/{total_parts}")
        
        audio_data, error = get_audio_chunk(url, headers, part, max_retries)
        
        if audio_data:
            audio_results[i] = audio_data
        
        success_metric.metric("✅ Success", f"{len(audio_results)}/{total_parts}")
        failed_metric.metric("❌ Failed", f"{total_parts - len(audio_results)}/{total_parts}")
        time_metric.metric("⏱️ Time", f"{int(elapsed)}s")
        
        if i < total_parts:
            time.sleep(2)
    
    # Results
    if audio_results:
        audio_chunks = [audio_results[i] for i in sorted(audio_results.keys())]
        final_audio = b"".join(audio_chunks)
        st.session_state.audio_data = final_audio
        
        # Save to history
        st.session_state.history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'chars': len(text_input),
            'parts': len(audio_chunks),
            'voice': st.session_state.selected_voice,
            'size': len(final_audio)
        })
        
        # Success Message
        st.markdown(f"""
        <div class="success-box">
            <h3>🎉 Audio Generated Successfully!</h3>
            <p><strong>Size:</strong> {len(final_audio)/1024/1024:.2f} MB</p>
            <p><strong>Duration:</strong> ~{len(text_input.split())/150:.1f} minutes</p>
            <p><strong>Parts:</strong> {len(audio_chunks)}/{total_parts}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio Player
        st.markdown('<div class="audio-player-container">', unsafe_allow_html=True)
        st.audio(final_audio, format='audio/mp3')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Options
        st.markdown("### 📥 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download MP3",
                data=final_audio,
                file_name=f"deepgram_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                mime="audio/mp3",
                use_container_width=True
            )
        
        with col2:
            # Generate shareable link (base64)
            b64 = base64.b64encode(final_audio).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="audio.mp3" class="download-btn download-btn-secondary">🔗 Generate Link</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col3:
            if st.button("📊 View Analytics", use_container_width=True):
                st.balloons()
                st.info(f"""
                **Generation Stats:**
                - Processing Time: {int(time.time() - start_time)}s
                - Success Rate: {len(audio_chunks)/total_parts*100:.1f}%
                - Average Speed: {len(text_input)/(time.time() - start_time):.0f} chars/sec
                """)
        
    else:
        st.error("❌ Generation failed. Please try again.")
    
    st.session_state.processing = False

# Show previous audio if exists
elif st.session_state.audio_data:
    st.markdown("### 🎵 Previous Generation")
    st.audio(st.session_state.audio_data, format='audio/mp3')
    
    st.download_button(
        label="📥 Download Previous Audio",
        data=st.session_state.audio_data,
        file_name="previous_audio.mp3",
        mime="audio/mp3",
        use_container_width=True
    )

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p style="font-size: 1.1rem;"><strong>✨ Deepgram TTS Premium</strong></p>
    <p>Powered by AI | Made with ❤️ using Streamlit & Deepgram API</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        <a href="https://deepgram.com" target="_blank" style="color: #667eea; text-decoration: none;">Get API Key</a> | 
        <a href="#" style="color: #667eea; text-decoration: none;">Documentation</a> | 
        <a href="#" style="color: #667eea; text-decoration: none;">Support</a>
    </p>
</div>
""", unsafe_allow_html=True)
