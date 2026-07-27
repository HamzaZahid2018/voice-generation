import streamlit as st
import requests
import os
import time
from io import BytesIO
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Deepgram TTS Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .success-box {
        padding: 1.5rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #28a745;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎙️ Deepgram TTS Professional</h1>
    <p style="font-size: 1.2rem;">Advanced Text-to-Speech with AI-Powered Voices</p>
</div>
""", unsafe_allow_html=True)

# Session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Settings
    with st.expander("🔑 API Settings", expanded=True):
        api_key = st.text_input(
            "API Key",
            type="password",
            value=os.getenv("DEEPGRAM_API_KEY", "8f4971764dabf4387c9d61a9fee92bc5e6377c2f")
        )
        
        test_api = st.button("Test API Key", use_container_width=True)
        if test_api:
            with st.spinner("Testing..."):
                try:
                    headers = {"Authorization": f"Token {api_key}"}
                    response = requests.get(
                        "https://api.deepgram.com/v1/projects",
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.success("✓ API Key Valid!")
                    else:
                        st.error(f"✗ Invalid (Status: {response.status_code})")
                except Exception as e:
                    st.error(f"✗ Error: {str(e)[:50]}")
    
    # Voice Settings
    with st.expander("🎤 Voice Settings", expanded=True):
        voice_category = st.selectbox(
            "Voice Category",
            ["Female Voices", "Male Voices", "All Voices"]
        )
        
        female_voices = [
            "aura-2-helena-en",
            "aura-asteria-en",
            "aura-luna-en",
            "aura-stella-en",
            "aura-athena-en",
            "aura-hera-en"
        ]
        
        male_voices = [
            "aura-orion-en",
            "aura-arcas-en",
            "aura-perseus-en",
            "aura-angus-en",
            "aura-orpheus-en",
            "aura-helios-en",
            "aura-zeus-en"
        ]
        
        if voice_category == "Female Voices":
            available_voices = female_voices
        elif voice_category == "Male Voices":
            available_voices = male_voices
        else:
            available_voices = female_voices + male_voices
        
        model = st.selectbox("Select Voice", available_voices)
        
        # Voice preview descriptions
        voice_descriptions = {
            "aura-2-helena-en": "Professional, clear, perfect for narration",
            "aura-asteria-en": "Warm, friendly, conversational",
            "aura-luna-en": "Soft, calm, soothing",
            "aura-stella-en": "Bright, energetic, upbeat",
            "aura-orion-en": "Deep, authoritative male",
            "aura-arcas-en": "Professional, business-like",
        }
        
        if model in voice_descriptions:
            st.info(f"💡 {voice_descriptions[model]}")
    
    # Processing Settings
    with st.expander("⚡ Processing Settings"):
        chunk_size = st.slider(
            "Chunk Size",
            500, 2500, 1500, 100,
            help="Characters per chunk"
        )
        
        max_retries = st.slider(
            "Max Retries",
            1, 10, 5,
            help="Retry attempts per chunk"
        )
        
        delay_between_chunks = st.slider(
            "Delay (seconds)",
            0, 5, 2,
            help="Wait time between API calls"
        )
    
    st.divider()
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Generated", len(st.session_state.history))
    with col2:
        total_chars = sum(h.get('chars', 0) for h in st.session_state.history)
        st.metric("Total Chars", f"{total_chars:,}")
    
    if st.button("Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🎵 Generate", "📜 History", "ℹ️ Info"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Text Input")
        
        input_method = st.radio(
            "Input Method",
            ["Type/Paste", "Upload File", "Load from URL"],
            horizontal=True
        )
        
        text_input = ""
        
        if input_method == "Type/Paste":
            text_input = st.text_area(
                "Enter your text",
                height=300,
                placeholder="Type or paste your text here..."
            )
        
        elif input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload text file",
                type=['txt', 'md', 'json']
            )
            if uploaded_file:
                try:
                    text_input = uploaded_file.read().decode('utf-8')
                    st.success(f"✓ Loaded {len(text_input):,} characters")
                except:
                    st.error("Failed to read file")
        
        elif input_method == "Load from URL":
            url = st.text_input("Enter URL")
            if st.button("Fetch") and url:
                with st.spinner("Fetching..."):
                    try:
                        response = requests.get(url, timeout=10)
                        text_input = response.text
                        st.success(f"✓ Loaded {len(text_input):,} characters")
                    except Exception as e:
                        st.error(f"Failed: {str(e)[:50]}")
        
        # Stats
        if text_input:
            char_count = len(text_input)
            word_count = len(text_input.split())
            est_time = word_count // 150
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Characters", f"{char_count:,}")
            with col_b:
                st.metric("Words", f"{word_count:,}")
            with col_c:
                st.metric("Est. Time", f"~{est_time} min")
    
    with col2:
        st.header("🎛️ Quick Actions")
        
        sample_texts = {
            "Short Test": "Hello! This is a quick test of the text to speech system.",
            "Medium Story": "Once upon a time, in a land far away, there lived a curious fox. The fox loved to explore the forest and meet new friends. One day, while wandering through the woods, the fox discovered a magical stream that could grant wishes. This discovery would change everything.",
            "Professional": "Welcome to our presentation on artificial intelligence and machine learning. Today, we will explore how these technologies are transforming industries and shaping the future of innovation."
        }
        
        selected_sample = st.selectbox("Load Sample", ["None"] + list(sample_texts.keys()))
        if selected_sample != "None" and st.button("Load Sample", use_container_width=True):
            text_input = sample_texts[selected_sample]
            st.rerun()
        
        st.divider()
        
        if st.button("🗑️ Clear All", use_container_width=True):
            text_input = ""
            st.rerun()
        
        st.divider()
        
        st.markdown("### 🎯 Output Options")
        output_format = st.selectbox("Format", ["MP3", "WAV"])
        output_name = st.text_input("Filename", "output")
    
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
    
    # Processing logic (same as before but enhanced)
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
                        timeout=(15, 120 + attempt * 30)
                    )
                    if response.status_code == 200:
                        return response.content, None
                    time.sleep(5)
                except:
                    if attempt < retries - 1:
                        time.sleep(3)
            return None, "Failed"
        
        # Setup
        url = f"https://api.deepgram.com/v1/speak?model={model}"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
        
        text_parts = split_text(text_input, chunk_size)
        total_parts = len(text_parts)
        
        st.markdown("---")
        st.subheader("🔄 Processing...")
        
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
            
            success_metric.metric("✓ Success", f"{len(audio_results)}/{total_parts}")
            failed_metric.metric("✗ Failed", f"{total_parts - len(audio_results)}/{total_parts}")
            time_metric.metric("⏱️ Time", f"{int(elapsed)}s")
            
            if i < total_parts:
                time.sleep(delay_between_chunks)
        
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
                'model': model,
                'size': len(final_audio)
            })
            
            st.success(f"🎉 Generated {len(final_audio)/1024/1024:.2f} MB audio!")
            
            st.audio(final_audio, format='audio/mp3')
            
            st.download_button(
                "📥 Download Audio",
                final_audio,
                f"{output_name}.mp3",
                "audio/mp3",
                use_container_width=True
            )
        else:
            st.error("❌ Generation failed. Please try again.")
        
        st.session_state.processing = False

with tab2:
    st.header("📜 Generation History")
    
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"#{len(st.session_state.history) - idx} - {item['timestamp']}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Characters", f"{item['chars']:,}")
                with col2:
                    st.metric("Parts", item['parts'])
                with col3:
                    st.metric("Model", item['model'].split('-')[1].title())
                with col4:
                    st.metric("Size", f"{item['size']/1024/1024:.2f} MB")
    else:
        st.info("No generation history yet. Start by generating your first audio!")

with tab3:
    st.header("ℹ️ Information")
    
    st.markdown("""
    ### About Deepgram TTS Professional
    
    This application uses Deepgram's state-of-the-art AI voices to convert text into natural-sounding speech.
    
    #### Features:
    - 🎤 13+ AI voices (male & female)
    - 📊 Real-time progress tracking
    - 🔄 Automatic retry on failures
    - 💾 Download as MP3
    - 📜 Generation history
    - ⚙️ Customizable settings
    
    #### Voice Models:
    - **Helena** - Professional narration
    - **Asteria** - Friendly conversations
    - **Orion** - Deep male voice
    - And many more!
    
    #### Tips:
    - Use chunk size 1500 for best results
    - Enable retries for unstable connections
    - Download audio immediately after generation
    
    ---
    
    Made with ❤️ using Streamlit & Deepgram
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <strong>Deepgram TTS Professional</strong> | 
    <a href="https://deepgram.com" target="_blank">Get API Key</a> | 
    <a href="https://developers.deepgram.com" target="_blank">Documentation</a>
</div>
""", unsafe_allow_html=True)
