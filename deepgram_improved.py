import requests
import os
import time
from data import message

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "8f4971764dabf4387c9d61a9fee92bc5e6377c2f")

# Multiple model options - if one fails, try another
MODELS = [
    "aura-2-helena-en",
    "aura-asteria-en",
    "aura-luna-en",
    "aura-stella-en"
]

SELECTED_MODEL = MODELS[0]

print(f"🔑 API Key: {DEEPGRAM_API_KEY[:10]}..." if DEEPGRAM_API_KEY else "❌ No API Key")

if not DEEPGRAM_API_KEY:
    print("❌ API Key is NOT loaded!")
    exit(1)

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}


def split_text(text, max_length=2000):
    """Split text into chunks at sentence boundaries"""
    sentences = text.replace('\n', ' ').split('. ')
    parts = []
    current_part = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Add period back if not the last sentence
        if not sentence.endswith('.'):
            sentence += '.'
        
        # If adding this sentence exceeds max_length, save current part
        if len(current_part) + len(sentence) > max_length and current_part:
            parts.append(current_part.strip())
            current_part = sentence
        else:
            current_part += " " + sentence if current_part else sentence
    
    # Add the last part
    if current_part.strip():
        parts.append(current_part.strip())
    
    return parts


def get_deepgram_audio(text_part, part_num, model=SELECTED_MODEL, max_retries=5):
    """Get audio from Deepgram API with robust retry logic"""
    url = f"https://api.deepgram.com/v1/speak?model={model}"
    payload = {"text": text_part}
    
    for attempt in range(max_retries):
        try:
            # Progressive timeout increase
            timeout = 120 + (attempt * 30)
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=(15, timeout)
            )
            
            if response.status_code == 200:
                return (part_num, response.content, None)
            elif response.status_code == 429:
                wait = 15 + (attempt * 5)
                print(f"   Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                error_msg = f"Status {response.status_code}"
                if attempt == max_retries - 1:
                    return (part_num, None, error_msg)
                time.sleep(5)
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait = min((attempt + 1) * 3, 15)
                print(f"   Timeout, retry in {wait}s...")
                time.sleep(wait)
            else:
                return (part_num, None, "Timeout")
                
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                wait = min((attempt + 1) * 5, 20)
                print(f"   Connection error, retry in {wait}s...")
                time.sleep(wait)
            else:
                return (part_num, None, "Connection failed")
                
        except Exception as e:
            if attempt == max_retries - 1:
                return (part_num, None, str(e)[:100])
            time.sleep(3)
    
    return (part_num, None, "Max retries exceeded")


def save_progress(audio_results, filename="output_partial.mp3"):
    """Save partial results in case of interruption"""
    if audio_results:
        chunks = [audio_results[i] for i in sorted(audio_results.keys())]
        with open(filename, "wb") as f:
            f.write(b"".join(chunks))
        return True
    return False


if __name__ == "__main__":
    try:
        # Split text
        text_parts = split_text(message, max_length=1500)
        total_parts = len(text_parts)
        
        print(f"\n{'='*60}")
        print(f"🎵 DEEPGRAM TEXT-TO-SPEECH GENERATOR")
        print(f"{'='*60}")
        print(f"📝 Total parts: {total_parts}")
        print(f"📊 Total characters: {len(message):,}")
        print(f"🎙️  Model: {SELECTED_MODEL}")
        print(f"⏱️  Estimated time: ~{total_parts * 2} minutes")
        print(f"{'='*60}\n")
        
        file_path = "output.mp3"
        audio_results = {}
        failed_parts = []
        
        start_time = time.time()
        
        # Process each part
        for i, part in enumerate(text_parts, 1):
            elapsed = time.time() - start_time
            avg_time = elapsed / i if i > 0 else 0
            remaining = (total_parts - i) * avg_time
            
            print(f"[{i}/{total_parts}] {len(part):4d} chars | ETA: {int(remaining/60)}m {int(remaining%60)}s", end=" ")
            
            result = get_deepgram_audio(part, i)
            part_num, audio_data, error = result
            
            if audio_data:
                audio_results[part_num] = audio_data
                print(f"✓ {len(audio_data)/1024:.0f}KB")
            else:
                failed_parts.append((part_num, error))
                print(f"✗ {error}")
            
            # Save progress every 3 parts
            if i % 3 == 0:
                save_progress(audio_results)
            
            # Rate limiting
            if i < total_parts:
                time.sleep(2)
        
        total_time = time.time() - start_time
        
        # Results summary
        print(f"\n{'='*60}")
        print(f"📊 PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Successful: {len(audio_results)}/{total_parts}")
        print(f"✗ Failed: {len(failed_parts)}/{total_parts}")
        print(f"⏱️  Total time: {int(total_time/60)}m {int(total_time%60)}s")
        print(f"{'='*60}\n")
        
        if failed_parts:
            print("❌ Failed parts:")
            for pnum, err in failed_parts[:5]:
                print(f"   Part {pnum}: {err}")
            if len(failed_parts) > 5:
                print(f"   ... and {len(failed_parts)-5} more")
            print()
        
        if not audio_results:
            print("❌ No audio generated!")
            print("\n💡 Troubleshooting:")
            print("   1. Check internet connection")
            print("   2. Verify API key at https://console.deepgram.com/")
            print("   3. Check Deepgram service status")
            print("   4. Try a different network/VPN\n")
            exit(1)
        
        # Combine and save
        print("🔄 Combining audio chunks...")
        audio_chunks = [audio_results[i] for i in sorted(audio_results.keys())]
        audio_bytes = b"".join(audio_chunks)
        
        print(f"💾 Saving to {file_path}...")
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        
        file_size_mb = len(audio_bytes) / 1024 / 1024
        
        print(f"\n{'='*60}")
        print(f"🎉 SUCCESS!")
        print(f"{'='*60}")
        print(f"📁 File: {file_path}")
        print(f"📦 Size: {file_size_mb:.2f} MB")
        print(f"🎵 Duration: ~{len(message)/150:.1f} minutes (estimated)")
        print(f"✓ Quality: {len(audio_chunks)}/{total_parts} parts included")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! Saving progress...")
        if save_progress(audio_results):
            print(f"✓ Partial audio saved as output_partial.mp3")
        exit(1)
        
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        save_progress(audio_results)
        exit(1)
