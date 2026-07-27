# 🔑 API Key Management Guide

## ✨ Dynamic API Key Feature Added!

Aap ab **frontend se directly** API key change kar sakte hain without redeploying!

---

## 📱 How to Use (Frontend)

### Step 1: Open App Sidebar
```
http://localhost:8501
```
- Sidebar mein scroll karein top pe
- **"🔑 API Configuration"** section dikhega

### Step 2: Enter New API Key
```
1. "Deepgram API Key" field mein click karein
2. Current key select karke delete karein
3. Naya API key paste karein
4. Enter press karein
```

### Step 3: Test API Key
```
1. "🔍 Test Key" button click karein
2. Wait for validation
3. ✅ "Valid!" ya ❌ "Invalid" dekhein
```

### Step 4: Start Using
```
- Agar key valid hai
- Immediately use kar sakte hain
- Generate button kaam karega
```

---

## 🔄 When to Change API Key

### Scenario 1: Limit Exceeded
```
❌ Error: "quota_exceeded" or "insufficient_credits"

Solution:
1. Deepgram console pe jao
2. New API key generate karo
3. App sidebar mein paste karo
4. Test karo
5. Continue using!
```

### Scenario 2: Key Expired
```
❌ Error: "invalid_credentials" or "unauthorized"

Solution:
1. Login to console.deepgram.com
2. Revoke old key
3. Create new key
4. Update in app
```

### Scenario 3: Rate Limited
```
⚠️ Error: "rate_limit_exceeded"

Solution:
- Wait a few minutes
- Or switch to different key
- Or upgrade Deepgram plan
```

---

## 🎯 Getting New API Key

### Method 1: Deepgram Console (Recommended)

```
1. Visit: https://console.deepgram.com
2. Login to your account
3. Click "API Keys" in sidebar
4. Click "Create New Key"
5. Name it (e.g., "TTS App Key 2")
6. Copy the key
7. Paste in app
```

### Method 2: Free Trial

```
If you don't have an account:

1. Go to: https://console.deepgram.com/signup
2. Sign up (free)
3. Get $200 free credits
4. Generate API key
5. Use in app
```

---

## 💡 App Features

### 1. Live API Key Update
```python
✅ No restart needed
✅ No redeployment needed
✅ Instant switch
✅ Test before using
```

### 2. API Key Validation
```python
✅ "Test Key" button
✅ Real-time validation
✅ Status indicator
✅ Error messages
```

### 3. Reset Option
```python
✅ "Reset" button
✅ Restores default key
✅ One-click reset
```

### 4. Secure Storage
```python
✅ Stored in session
✅ Not visible in logs
✅ Password field (hidden)
✅ Not committed to git
```

---

## 🔒 Security Best Practices

### DO:
```
✅ Use different keys for dev/prod
✅ Rotate keys regularly
✅ Monitor usage dashboard
✅ Set billing alerts
✅ Revoke unused keys
```

### DON'T:
```
❌ Share API keys publicly
❌ Commit keys to git
❌ Use same key everywhere
❌ Leave expired keys active
❌ Ignore rate limits
```

---

## 📊 Monitoring Usage

### Check Credits:
```
1. Login to console.deepgram.com
2. Go to "Billing" or "Usage"
3. See remaining credits
4. Check usage graphs
```

### Set Alerts:
```
1. Billing section
2. Set credit threshold
3. Get email when low
4. Generate new key in advance
```

---

## 🚀 Advanced: Multiple Keys

### For High Volume:
```python
# Method 1: Round Robin
keys = [
    "key1...",
    "key2...",
    "key3..."
]

# Switch when limit hit
current_key = keys[counter % len(keys)]
```

### For Team Usage:
```python
# Different keys per user
user_keys = {
    "user1": "key1...",
    "user2": "key2...",
    "admin": "key3..."
}
```

---

## 🐛 Troubleshooting

### Error: "Invalid API Key"
```
Solution:
1. Check key is complete (40 chars)
2. No extra spaces
3. Not expired
4. Has permissions
```

### Error: "Cannot connect"
```
Solution:
1. Check internet connection
2. Try ping console.deepgram.com
3. Check firewall settings
4. Try different network
```

### Error: "Quota exceeded"
```
Solution:
1. Generate new key
2. Or wait for quota reset
3. Or upgrade plan
4. Or buy more credits
```

---

## 📝 Example Usage Flow

```
Day 1:
- Generate key1
- Use in app
- Works fine

Day 30:
- Key1 limit reached
- Generate key2
- Open app sidebar
- Paste key2
- Click "Test Key"
- ✅ Valid!
- Continue using

Day 60:
- Key2 limit reached
- Generate key3
- Repeat process
- No downtime!
```

---

## 🎉 Benefits

### No Redeployment:
```
✅ Change key instantly
✅ No app restart
✅ No code changes
✅ No GitHub push
✅ No waiting
```

### User-Friendly:
```
✅ Simple UI
✅ Clear instructions
✅ Instant feedback
✅ Error handling
✅ Reset option
```

### Flexible:
```
✅ Multiple keys support
✅ Easy switching
✅ Test before use
✅ Secure storage
```

---

## 🔗 Quick Links

- **Get API Key**: https://console.deepgram.com
- **Documentation**: https://developers.deepgram.com
- **Pricing**: https://deepgram.com/pricing
- **Support**: https://deepgram.com/support

---

## 📞 Need Help?

### If key not working:
1. Check guide above
2. Verify in Deepgram console
3. Test with curl command
4. Contact Deepgram support

### If app not accepting key:
1. Check key length (40 chars)
2. No spaces/newlines
3. Use "Test Key" button
4. Check browser console

---

Made with ❤️ | API Key Management Made Easy! 🔑✨
