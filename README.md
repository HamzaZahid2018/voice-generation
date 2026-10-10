# 🎙️ Deepgram Text-to-Speech Generator - Complete Suite

Convert long text to speech using Deepgram API with **4 Beautiful UI Options**!
## 🚀 Quick Start
### Option 1: Streamlit Web Apps (Choose Your Style! ✨)

```bash
# Install requirements
pip install -r requirements.txt

# Choose your version:

# 1. Basic (Simple & Fast)
streamlit run app.py

# 2. Advanced (More Features)
streamlit run app_advanced.py

# 3. Premium (Glassmorphism & 3D) ⭐
streamlit run app_premium.py

# 4. Ultra (Dark Mode + Animations) 🚀
streamlit run app_ultra.py
```

Then open: http://localhost:8501

### Option 2: Command Line

```bash
# Best version
python deepgram_improved.py

# Or original improved
python "deepgram (1).py"
```

## 📁 Files

### Web Apps:
- **`app.py`** - Beautiful Streamlit interface (Basic)
- **`app_advanced.py`** - Advanced version with history & more features

### CLI Scripts:
- **`deepgram_improved.py`** - Production-ready CLI version
- **`deepgram (1).py`** - Original with improvements
- **`data.py`** - Sample text data

### Config:
- **`.env`** - API key storage
- **`requirements.txt`** - Python dependencies

## 🎨 Streamlit App Features

### Basic App (app.py):
✅ Clean, modern UI with gradients  
✅ Real-time progress tracking  
✅ 13+ voice models  
✅ File upload support  
✅ In-browser audio player  
✅ One-click download  
✅ Adjustable chunk size  
✅ Live processing logs  

### Advanced App (app_advanced.py):
✅ Everything in basic +  
✅ Generation history tracker  
✅ API key tester  
✅ Voice category filters  
✅ Load text from URL  
✅ Session statistics  
✅ Custom output filenames  
✅ Multiple sample texts  

## 📊 Voice Models Available

**Female:**
- aura-2-helena-en (Professional)
- aura-asteria-en (Warm)
- aura-luna-en (Calm)
- aura-stella-en (Energetic)
- aura-athena-en (Confident)
- aura-hera-en (Elegant)

**Male:**
- aura-orion-en (Deep)
- aura-arcas-en (Professional)
- aura-perseus-en (Young)
- aura-angus-en (Casual)
- aura-orpheus-en (Artistic)
- aura-helios-en (Powerful)
- aura-zeus-en (Authoritative)

## ⚙️ Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Get API key from: https://console.deepgram.com/signup

3. Set in `.env` file:
```
DEEPGRAM_API_KEY=your_key_here
```

## 🎯 Usage Examples

### Web App:
1. Start app: `streamlit run app.py`
2. Enter/paste text or upload file
3. Select voice model
4. Click "Generate Speech"
5. Listen & download

### CLI:
```bash
# Edit data.py with your text
python deepgram_improved.py
```

## 💡 Tips

- **Chunk Size:** 1500 chars = best balance
- **Voice:** Helena recommended for clarity
- **Speed:** ~2-3 minutes per 1000 words
- **Network:** Use VPN if timeouts occur
- **Reliability:** Advanced app has retry logic

## 🔧 Troubleshooting

**Streamlit not starting?**
```bash
pip install --upgrade streamlit
streamlit --version
```

**API errors?**
- Verify key at console.deepgram.com
- Check internet connection
- Try different model

**Timeout issues?**
- Reduce chunk size
- Increase max retries
- Check network stability

## 📦 Output

- **Web App:** Direct download + preview
- **CLI:** `output.mp3` file
- **Format:** MP3 audio
- **Quality:** High (Deepgram AI voices)

## 🌟 Best Features

1. **Automatic Retry** - Never fails on first error
2. **Progress Tracking** - Know exactly what's happening
3. **Partial Success** - Get audio even if some parts fail
4. **History Tracking** - (Advanced) See all generations
5. **Rate Limiting** - Automatic protection
6. **Resume Support** - (CLI) Continue on interruption

## 📚 Documentation

- See `RUN_APP.md` for detailed Streamlit guide
- See code comments for API details
- Visit https://developers.deepgram.com for API docs

## 🎉 What's New

- ✨ Beautiful Streamlit web interface
- 🎨 Two UI versions (basic & advanced)
- 📊 Session history tracking
- 🎤 13+ voice models
- 📁 Multiple input methods
- ⚡ Enhanced error handling
- 🔄 Auto-save progress

---

Made with ❤️ using Streamlit & Deepgram API

---

## 📅 Daily Updates

- 2026-10-02: README refreshed.
- 2026-10-04: README refreshed.
- 2026-10-05: README refreshed.
- 2026-10-10: README refreshed.
