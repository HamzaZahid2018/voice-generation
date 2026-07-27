# 🚀 How to Run Streamlit App

## Step 1: Install Requirements

```bash
pip install -r requirements.txt
```

## Step 2: Run the App

```bash
streamlit run app.py
```

## Step 3: Open in Browser

App will automatically open at: `http://localhost:8501`

---

## Features

### 🎨 Beautiful UI
- Modern gradient design
- Real-time progress tracking
- Live audio preview
- Download functionality

### ⚙️ Customizable Settings
- Multiple voice models (13+ options)
- Adjustable chunk size
- API key configuration

### 📊 Real-time Monitoring
- Progress bar with ETA
- Success/failure metrics
- Detailed processing logs
- Live time tracking

### 📤 Multiple Input Options
- Direct text input
- File upload (.txt, .md)
- Sample text loading
- Character & word count

### 🎵 Audio Features
- In-browser audio player
- Download as MP3
- Combine multiple chunks
- Automatic retry on failure

---

## Voice Models Available

1. **Helena** (Recommended) - Clear, professional
2. **Asteria** - Warm, friendly
3. **Luna** - Soft, calm
4. **Stella** - Bright, energetic
5. **Athena** - Strong, confident
6. **Hera** - Elegant, mature
7. **Orion** - Deep male voice
8. **Arcas** - Professional male
9. **Perseus** - Young male
10. **Angus** - Casual male
11. **Orpheus** - Artistic male
12. **Helios** - Powerful male
13. **Zeus** - Authoritative male

---

## Troubleshooting

### App not starting?
```bash
# Check if streamlit is installed
streamlit --version

# Reinstall if needed
pip install --upgrade streamlit
```

### Port already in use?
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### API errors?
- Verify your API key at https://console.deepgram.com
- Check internet connection
- Try a different voice model

---

## Tips for Best Results

✅ Use **chunk size 1500** for most texts  
✅ Choose **Helena model** for clarity  
✅ For long texts, be patient (2-3 min per 1000 words)  
✅ Enable **processing log** to monitor progress  
✅ Download immediately after generation  

---

## Keyboard Shortcuts (in app)

- `Ctrl + R` - Rerun app
- `Ctrl + Shift + R` - Clear cache & rerun
- `ESC` - Stop running script

---

Made with ❤️
