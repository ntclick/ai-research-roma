# 🧪 Testing & Monitoring Guide

**Project:** Crypto Research AI with ROMA Framework  
**Author:** [@trungkts29](https://x.com/trungkts29)

---

## ✅ Deployment Status Check

### **Backend (Railway)**
**Latest Logs:**
```
[CONFIG] Server will bind to 0.0.0.0:8080 ✅
[DEBUG] API Keys Status:
  GOOGLE_API_KEY: Loaded ✅
  OPENAI_API_KEY: Loaded ✅
[ROMA Framework - AI Architecture]
  🧠 Brain: OpenAI GPT-4o-mini ✓
  🤖 Worker: Google Gemini ✓  ← WORKING!
[Data Sources]
  📊 CoinGecko API: ✓
  📰 RSS News: ✓
  🎨 fal.ai Image: ✓
WebSocket server started on ws://0.0.0.0:8080 ✅
Client connected. Total clients: 2 ✅
```

**Status:** ✅ **ALL SYSTEMS GREEN**

---

## 🧪 Test Cases

### **1. Price Queries (CoinGecko)**

| Query | Expected Result | API Route |
|-------|----------------|-----------|
| `check btc` | Bitcoin price + 24h change | CoinGecko |
| `btc` | Bitcoin price (quick) | CoinGecko |
| `eth` | Ethereum price | CoinGecko |
| `bitcoin price` | Bitcoin full details | CoinGecko |
| `sol market cap` | Solana market cap | CoinGecko |

**Expected Response Format:**
```
💰 Bitcoin (BTC)
Price: $XX,XXX.XX
24h Change: +X.XX%
Market Cap: $XXX.XXB
Volume: $XX.XXB

📊 Data from CoinGecko API
```

### **2. News Queries (RSS Feeds)**

| Query | Expected Result | Sources |
|-------|----------------|---------|
| `btc news` | Bitcoin news (7 days) | 4 RSS feeds |
| `ethereum updates` | Ethereum news | Filtered by "ethereum" |
| `crypto news` | General crypto news | Top 5 articles |

**Expected Response Format:**
```
📰 Latest News - BITCOIN

1. [Article Title](link)
   📅 Oct 3, 2025

2. [Article Title](link)
   📅 Oct 2, 2025

...

📊 Source: RSS News (Last 7 Days)
```

### **3. Definition Queries (Gemini/OpenAI)**

| Query | Expected Result | AI Model |
|-------|----------------|----------|
| `what is bitcoin` | 2-3 sentence explanation | Gemini → OpenAI backup |
| `explain ethereum` | Concise definition | Gemini → OpenAI backup |
| `what is defi` | DeFi explanation | Gemini → OpenAI backup |

**Expected Response Format:**
```
Bitcoin is the first and largest cryptocurrency, created in 2009. 
It operates on a decentralized blockchain network without central 
authority.

📊 Source: Gemini Worker
```

### **4. Image Generation (fal.ai)**

| Query | Expected Result | Model |
|-------|----------------|-------|
| `create image bitcoin logo` | AI-generated image URL | FLUX.1 [dev] |
| `generate eth coin` | Ethereum themed image | FLUX.1 [dev] |

**Expected Response Format:**
```
🎨 Image Generated!

Model: FLUX.1 [dev]
Resolution: 1024x768
Prompt: Enhanced by AI

Source: fal.ai
```

---

## 📊 Monitoring & Logs

### **Railway Logs (Real-time)**

**View logs:**
```bash
Railway Dashboard → Deployments → Click latest → Deploy Logs
```

**What to look for:**

1. **Successful Startup:**
```
[CONFIG] Server will bind to 0.0.0.0:8080
[DEBUG] GOOGLE_API_KEY: Loaded  ← Must see this
🤖 Worker: Google Gemini ✓        ← Must be ✓
WebSocket server started          ← Server running
```

2. **Client Connections:**
```
Client connected. Total clients: 1
```

3. **Query Processing:**
```
[ROMA] Processing query: check btc
[BRAIN] OpenAI routing result: coingecko
[API CALL] CoinGecko: Fetching data for bitcoin
[API CALL] CoinGecko: Success - bitcoin = $XX,XXX
```

### **Vercel Logs**

**View logs:**
```bash
Vercel Dashboard → Deployments → Click latest → Logs
```

**What to look for:**

1. **Build Success:**
```
✓ Collecting page data
✓ Generating static pages
✓ Build completed
```

2. **Runtime:**
```
[FRONTEND] WebSocket readyState: 1  ← Connected
[FRONTEND] WebSocket connected successfully
```

---

## 🐛 Common Issues & Solutions

### **Issue 1: Gemini shows ✗**

**Symptoms:**
```
🤖 Worker: Google Gemini ✗
```

**Solution:**
1. Railway Dashboard → Variables
2. Verify `GOOGLE_API_KEY` exists
3. Settings → Restart Deployment

### **Issue 2: "Bạn có thể cho biết rõ hơn"**

**Symptoms:** AI responds in Vietnamese

**Solution:**
- ✅ Already fixed in latest deployment
- Verify commit: "Fix: Force all AI responses to English"

### **Issue 3: "check btc" asks for clarification**

**Symptoms:**
```
"Could you be more specific about 'check btc'?"
```

**Solution:**
- ✅ Already fixed with improved routing
- Verify commit: "Improve routing: Better recognition"

### **Issue 4: WebSocket connection fails**

**Symptoms:**
```
[FRONTEND] WebSocket readyState: 3  ← Disconnected
```

**Solution:**
1. Check Railway backend is running
2. Verify URL in Vercel env: `wss://web-production-6b11c.up.railway.app`
3. Check browser console for errors

---

## 🧪 Manual Testing

### **Test via Browser Console**

1. Open: https://airesearch-tools.vercel.app
2. Open DevTools (F12)
3. Console tab

**Test WebSocket connection:**
```javascript
// Should see in console:
[FRONTEND] WebSocket connected successfully
```

**Send test message:**
```javascript
// Type a query in the UI, watch console:
[FRONTEND] Sent WebSocket message: {type: 'user_message', content: 'check btc'}
[FRONTEND] Received WebSocket message: {type: 'research_response', ...}
```

### **Test via wscat (Terminal)**

```bash
# Install wscat
npm install -g wscat

# Connect to backend
wscat -c wss://web-production-6b11c.up.railway.app

# Send query
> {"type": "user_message", "tool": "research", "content": "check btc", "user": "test"}

# Expected response:
< {"type": "research_response", "content": "💰 Bitcoin...", ...}
```

---

## 📈 Performance Metrics

### **Expected Response Times**

| Query Type | Expected Time | Bottleneck |
|------------|---------------|------------|
| Price query | 0.5-1s | CoinGecko API |
| News query | 1-2s | RSS parsing |
| Definition | 1-3s | Gemini/OpenAI |
| Image gen | 5-10s | fal.ai FLUX |

### **API Rate Limits**

| API | Free Tier Limit | Current Usage |
|-----|----------------|---------------|
| Gemini | 60 req/min | Low |
| OpenAI | Varies by plan | Low |
| CoinGecko | 30 calls/min | Low |
| fal.ai | Credits-based | Per generation |

---

## ✅ Health Check Checklist

Run this checklist every day:

- [ ] Railway backend is running (check Dashboard)
- [ ] Vercel frontend is accessible
- [ ] WebSocket connection works (test in browser)
- [ ] All API keys are valid (check Railway Variables)
- [ ] No errors in Railway logs
- [ ] No errors in Vercel logs
- [ ] Test each query type:
  - [ ] `check btc` → Shows price
  - [ ] `btc news` → Shows news
  - [ ] `what is bitcoin` → Shows definition
  - [ ] `create image bitcoin` → Generates image

---

## 📞 Support & Debugging

### **Get Detailed Logs**

**Railway:**
```bash
Railway Dashboard → Deployments → Deploy Logs → Copy all
```

**Vercel:**
```bash
vercel logs https://airesearch-tools.vercel.app
```

### **Debug Mode**

Already enabled in code:
```python
[DEBUG] API Keys Status: ...  ← Shows key loading
[ROMA-SOLVE] ...              ← Shows task execution
[API CALL] ...                ← Shows API calls
[BRAIN] OpenAI routing ...    ← Shows routing decisions
```

---

## 🎯 Success Criteria

Your deployment is successful if:

✅ Railway logs show all systems ✓  
✅ Gemini API key loaded  
✅ WebSocket server running on 0.0.0.0:8080  
✅ Clients can connect  
✅ `check btc` returns price immediately  
✅ All responses in English  
✅ No Vietnamese text in responses  

---

**🎉 Current Status: ALL TESTS PASSING!**

**Live URLs:**
- Frontend: https://airesearch-tools.vercel.app
- Backend: wss://web-production-6b11c.up.railway.app

Made with ❤️ by [@trungkts29](https://x.com/trungkts29)

