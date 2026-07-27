import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from data import message

# Load API key from environment variable for security
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "8f4971764dabf4387c9d61a9fee92bc5e6377c2f")

SELECTED_MODEL = "aura-2-helena-en"  # aura-2-orion-en #aura-2-pluto-en

DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={SELECTED_MODEL}"

print("DEEPGRAM_API_KEY =", DEEPGRAM_API_KEY[:10] + "..." if DEEPGRAM_API_KEY else "None")

if DEEPGRAM_API_KEY:
    print("Key Length:", len(DEEPGRAM_API_KEY))
else:
    print("API Key is NOT loaded!")
    exit(1)
    
headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}


def split_text(text, max_length=960):
    """Split the text into chunks of `max_length` characters or less"""
    parts = []
    while len(text) > max_length:
        # Find the last space within the max_length to avoid cutting words in half
        split_pos = text.rfind(" ", 0, max_length)
        
        # If no space found, force split at max_length
        if split_pos == -1:
            split_pos = max_length
            
        parts.append(text[:split_pos].strip())
        text = text[split_pos:].strip()
    
    if text:  # Only append if there's remaining text
        parts.append(text)
    
    return parts

def get_deepgram_audio(DEEPGRAM_URL, text_part, part_num, max_retries=5):
    """Get audio from Deepgram API for a text chunk with robust retry logic"""
    payload = {
        "text": text_part
    }
    
    for attempt in range(max_retries):
        try:
            # Progressive timeout increase with each retry
            timeout_seconds = 90 + (attempt * 30)  # 90s, 120s, 150s, 180s, 210s
            
            response = requests.post(
                DEEPGRAM_URL, 
                headers=headers, 
                json=payload, 
                timeout=(15, timeout_seconds),  # (connection timeout, read timeout)
                stream=False  # Don't stream for better reliability
            )
            
            # Check response status
            if response.status_code == 200:
                return (part_num, response.content)
            elif response.status_code == 429:  # Rate limit
                print(f"⚠ Rate limited on part {part_num}, waiting...")
                time.sleep(10)
                continue
            else:
                print(f"✗ API Error on part {part_num}: Status {response.status_code}")
                print(f"Response: {response.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    return (part_num, None)
                
        except requests.exceptions.Timeout:
            print(f"⚠ Part {part_num}: Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                wait_time = min((attempt + 1) * 3, 15)  # Max 15s wait
                print(f"   Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"✗ Part {part_num}: Failed after {max_retries} attempts")
                return (part_num, None)
                
        except requests.exceptions.ConnectionError:
            print(f"⚠ Part {part_num}: Connection error on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                wait_time = min((attempt + 1) * 5, 20)
                print(f"   Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"✗ Part {part_num}: Connection failed")
                return (part_num, None)
                
        except Exception as e:
            print(f"⚠ Part {part_num}: Unexpected error - {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                return (part_num, None)
    
    return (part_num, None)

if __name__ == "__main__":
    try:
        text_parts = split_text(message)
        total_parts = len(text_parts)
        print(f"📝 Total text parts to process: {total_parts}")
        print(f"📊 Total characters: {len(message):,}")
        print(f"⏳ Estimated time: {total_parts * 2}-{total_parts * 4} minutes\n")
        
        file_path = "output.mp3"
        
        # Process parts sequentially with robust error handling
        print("🎵 Generating audio from Deepgram...\n")
        audio_results = {}
        successful = 0
        failed = 0
        
        for i, part in enumerate(text_parts, 1):
            print(f"[{i}/{total_parts}] Processing... ({len(part)} chars)", end=" ", flush=True)
            
            result = get_deepgram_audio(DEEPGRAM_URL, part, i)
            part_num, audio_data = result
            
            if audio_data:
                audio_results[part_num] = audio_data
                successful += 1
                print(f"✓ ({len(audio_data) / 1024:.1f} KB)")
            else:
                failed += 1
                print(f"✗ Failed")
            
            # Delay between requests to avoid rate limiting
            if i < total_parts:
                time.sleep(2)
        
        print(f"\n{'='*50}")
        print(f"✓ Successful: {successful}/{total_parts}")
        if failed > 0:
            print(f"✗ Failed: {failed}/{total_parts}")
        print(f"{'='*50}\n")
        
        if not audio_results:
            print("❌ No audio chunks generated. Please check:")
            print("   1. Internet connection")
            print("   2. API key validity")
            print("   3. Deepgram service status")
            exit(1)
        
        # Combine audio chunks in order
        print("🔄 Combining audio chunks...")
        audio_chunks = [audio_results[i] for i in sorted(audio_results.keys())]
        audio_bytes = b"".join(audio_chunks)
        
        # Save to file
        print(f"💾 Saving to {file_path}...")
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        
        file_size_mb = len(audio_bytes) / 1024 / 1024
        print(f"\n{'='*50}")
        print(f"🎉 SUCCESS!")
        print(f"{'='*50}")
        print(f"✓ File: {file_path}")
        print(f"✓ Size: {file_size_mb:.2f} MB")
        print(f"✓ Parts: {len(audio_chunks)}/{total_parts}")
        print(f"{'='*50}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)