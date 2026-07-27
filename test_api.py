import requests

DEEPGRAM_API_KEY = "8f4971764dabf4387c9d61a9fee92bc5e6377c2f"
SELECTED_MODEL = "aura-2-helena-en"
DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={SELECTED_MODEL}"

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}

# Test with short text
payload = {
    "text": "Hello, this is a test."
}

print(f"Testing Deepgram API...")
print(f"URL: {DEEPGRAM_URL}")
print(f"API Key: {DEEPGRAM_API_KEY[:10]}...")

try:
    response = requests.post(DEEPGRAM_URL, headers=headers, json=payload, timeout=15)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"✓ Success! Audio size: {len(response.content)} bytes")
        with open("test_output.mp3", "wb") as f:
            f.write(response.content)
        print("✓ Test audio saved to test_output.mp3")
    else:
        print(f"✗ Error Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("✗ Request timed out")
except Exception as e:
    print(f"✗ Error: {e}")
