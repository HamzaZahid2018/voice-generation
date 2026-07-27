import streamlit as st
import requests
import os
import time
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Deepgram Text-to-Speech",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .success-box {
        padding: 1.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎵 Deepgram Text-to-Speech Generator</h1>
    <p>Convert your text to natural-sounding speech</p>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    api_key = st.text_input(
        "Deepgram API Key",
        type="password",
        value=os.getenv("DEEPGRAM_API_KEY", "8f4971764dabf4387c9d61a9fee92bc5e6377c2f"),
        help="Get your free API key from https://console.deepgram.com"
    )
    
    model = st.selectbox(
        "Voice Model",
        [
            "aura-2-helena-en",
            "aura-asteria-en",
            "aura-luna-en",
            "aura-stella-en",
            "aura-athena-en",
            "aura-hera-en",
            "aura-orion-en",
            "aura-arcas-en",
            "aura-perseus-en",
            "aura-angus-en",
            "aura-orpheus-en",
            "aura-helios-en",
            "aura-zeus-en"
        ],
        help="Select the voice model for speech generation"
    )
    
    chunk_size = st.slider(
        "Chunk Size (characters)",
        min_value=500,
        max_value=2000,
        value=1500,
        step=100,
        help="Smaller chunks = more reliable, but slower"
    )
    
    st.divider()
    
    st.markdown("### 📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Max Retries", "5")
    with col2:
        st.metric("Timeout", "120s")
    
    st.divider()
    
    st.markdown("### 💡 Tips")
    st.info("""
    - Use shorter chunks for unstable connections
    - Helena model is recommended for clarity
    - Processing takes ~2-3 min per 1000 words
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Input Text")
    text_input = st.text_area(
        "Enter your text here",
        height=300,
        placeholder="Type or paste your text here...",
        help="Enter the text you want to convert to speech"
    )
    
    # Character count
    char_count = len(text_input)
    word_count = len(text_input.split())
    st.caption(f"Characters: {char_count:,} | Words: {word_count:,} | Est. time: ~{word_count//150}-{word_count//100} minutes")

with col2:
    st.header("🎛️ Quick Actions")
    
    # Sample texts
    if st.button("📄 Load Sample Text", use_container_width=True):
        sample = "Hello! This is a sample text to test the Deepgram Text-to-Speech system. The quick brown fox jumps over the lazy dog. This technology is amazing!"
        text_input = sample
        st.rerun()
    
    if st.button("🗑️ Clear Text", use_container_width=True):
        text_input = ""
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📤 Quick Import")
    uploaded_file = st.file_uploader(
        "Upload text file",
        type=['txt', 'md'],
        help="Upload a .txt or .md file"
    )
    
    if uploaded_file:
        text_input = uploaded_file.read().decode('utf-8')
        st.success(f"✓ Loaded {len(text_input)} characters")


# Helper functions
def split_text(text, max_length):
    """Split text into chunks at sentence boundaries"""
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


def get_audio_chunk(url, headers, text_part, max_retries=5):
    """Get audio from Deepgram API with retry logic"""
    payload = {"text": text_part}
    
    for attempt in range(max_retries):
        try:
            timeout = 120 + (attempt * 30)
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=(15, timeout)
            )
            
            if response.status_code == 200:
                return response.content, None
            elif response.status_code == 429:
                time.sleep(10)
                continue
            else:
                if attempt == max_retries - 1:
                    return None, f"API Error: {response.status_code}"
                time.sleep(5)
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(min((attempt + 1) * 3, 15))
            else:
                return None, "Timeout"
                
        except Exception as e:
            if attempt == max_retries - 1:
                return None, str(e)[:100]
            time.sleep(3)
    
    return None, "Max retries exceeded"


# Generate button
st.divider()

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_btn = st.button(
        "🎵 Generate Speech",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.processing or not text_input or not api_key
    )

# Processing
if generate_btn:
    st.session_state.processing = True
    st.session_state.audio_data = None
    
    # Validation
    if not text_input.strip():
        st.error("❌ Please enter some text first!")
        st.session_state.processing = False
        st.stop()
    
    if not api_key:
        st.error("❌ Please provide your Deepgram API key in the sidebar!")
        st.session_state.processing = False
        st.stop()
    
    # Setup
    url = f"https://api.deepgram.com/v1/speak?model={model}"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    
    # Split text
    text_parts = split_text(text_input, chunk_size)
    total_parts = len(text_parts)
    
    # Progress UI
    st.markdown("---")
    st.subheader("🔄 Processing...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        success_metric = st.empty()
    with metrics_col2:
        failed_metric = st.empty()
    with metrics_col3:
        time_metric = st.empty()
    
    log_container = st.expander("📋 Processing Log", expanded=True)
    
    # Process
    audio_results = {}
    failed_parts = []
    start_time = time.time()
    
    for i, part in enumerate(text_parts, 1):
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = (total_parts - i) * avg_time
        
        # Update progress
        progress_bar.progress(i / total_parts)
        status_text.text(f"Processing part {i}/{total_parts} | ETA: {int(remaining/60)}m {int(remaining%60)}s")
        
        with log_container:
            st.write(f"[{i}/{total_parts}] Processing {len(part)} characters...")
        
        # Get audio
        audio_data, error = get_audio_chunk(url, headers, part)
        
        if audio_data:
            audio_results[i] = audio_data
            with log_container:
                st.success(f"✓ Part {i} complete ({len(audio_data)/1024:.1f} KB)")
        else:
            failed_parts.append((i, error))
            with log_container:
                st.error(f"✗ Part {i} failed: {error}")
        
        # Update metrics
        success_metric.metric("✓ Successful", f"{len(audio_results)}/{total_parts}")
        failed_metric.metric("✗ Failed", f"{len(failed_parts)}/{total_parts}")
        time_metric.metric("⏱️ Elapsed", f"{int(elapsed/60)}m {int(elapsed%60)}s")
        
        # Rate limiting
        if i < total_parts:
            time.sleep(2)
    
    # Complete
    total_time = time.time() - start_time
    progress_bar.progress(1.0)
    status_text.text("✅ Processing Complete!")
    
    # Results
    if audio_results:
        # Combine audio
        audio_chunks = [audio_results[i] for i in sorted(audio_results.keys())]
        final_audio = b"".join(audio_chunks)
        st.session_state.audio_data = final_audio
        
        # Success message
        st.markdown(f"""
        <div class="success-box">
            <h3>🎉 Success!</h3>
            <p><strong>File Size:</strong> {len(final_audio)/1024/1024:.2f} MB</p>
            <p><strong>Parts Generated:</strong> {len(audio_chunks)}/{total_parts}</p>
            <p><strong>Total Time:</strong> {int(total_time/60)}m {int(total_time%60)}s</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio player
        st.audio(final_audio, format='audio/mp3')
        
        # Download button
        st.download_button(
            label="📥 Download Audio (MP3)",
            data=final_audio,
            file_name="output.mp3",
            mime="audio/mp3",
            use_container_width=True
        )
        
    else:
        st.markdown("""
        <div class="error-box">
            <h3>❌ Generation Failed</h3>
            <p>No audio chunks were generated. Please check:</p>
            <ul>
                <li>Internet connection</li>
                <li>API key validity</li>
                <li>Deepgram service status</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.processing = False

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    Made with ❤️ using Streamlit & Deepgram API<br>
    <a href="https://deepgram.com" target="_blank">Get your free API key</a>
</div>
""", unsafe_allow_html=True)
