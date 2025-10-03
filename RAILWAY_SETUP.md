# 🚂 Railway Deployment Guide

## ✅ GitHub Repository Connected

Your repo is linked: https://github.com/ntclick/ai-research-roma

---

## 🔧 Railway Configuration Steps

### **Step 1: Set Environment Variables**

Go to your Railway project → **Variables** tab and add:

```bash
# Google Gemini (Primary AI)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-1.5-flash

# OpenAI (Routing Brain + Backup)
OPENAI_API_KEY=your_openai_api_key_here

# CoinGecko (Crypto Prices)
COINGECKO_API_KEY=your_coingecko_api_key_here

# fal.ai (Image Generation)
FAL_API_KEY=your_fal_api_key_here

# Optional
TAVILY_API_KEY=your_tavily_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Server Config (Railway sets PORT automatically)
HOST=0.0.0.0
```

**📝 Note:** Add your REAL API keys directly in Railway Dashboard → Variables (they will be encrypted)

### **Step 2: Configure Build Settings**

Railway should auto-detect Python. If not:

1. Go to **Settings** → **Build**
2. **Build Command:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start Command:**
   ```bash
   cd backend && python websocket_server.py
   ```

### **Step 3: Update WebSocket Server for Railway**

Railway provides `PORT` environment variable. Update `websocket_server.py`:

```python
# Use Railway's PORT or default to 5001
PORT = int(os.getenv('PORT', 5001))
```

This is already configured in your code! ✅

### **Step 4: Deploy**

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Add Railway configuration"
   git push
   ```

2. Railway will auto-deploy! 🚀

---

## 🌐 After Deployment

Railway will give you a URL like:
```
https://your-app.railway.app
```

### **WebSocket URL:**
```
wss://your-app.railway.app
```

Update frontend `.env`:
```bash
REACT_APP_WEBSOCKET_URL=wss://your-app.railway.app
```

---

## 🧪 Testing

Once deployed, test WebSocket connection:

```bash
# Test backend health
curl https://your-app.railway.app

# Test WebSocket (use wscat)
npm install -g wscat
wscat -c wss://your-app.railway.app
```

---

## 📊 Monitoring

Railway Dashboard shows:
- ✅ Deployment logs
- ✅ Memory usage
- ✅ CPU usage
- ✅ Network traffic

---

## 🔒 Security Note

**IMPORTANT:** Your API keys are now in Railway's environment variables (encrypted).

**DO NOT** commit real `.env` file to GitHub! ✅ Already protected by `.gitignore`

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check logs in Railway dashboard
# Ensure requirements.txt is in /backend/
```

### WebSocket Connection Fails
```bash
# Check server logs
# Ensure PORT is set correctly
# Try wss:// instead of ws:// (Railway uses HTTPS)
```

### Module Not Found
```bash
# Add missing package to backend/requirements.txt
# Push to GitHub, Railway will rebuild
```

---

## 💰 Railway Pricing

**Free Tier:**
- $5 free credits/month
- Enough for development/testing
- Sleeps after inactivity (wakes on request)

**Hobby Plan:** $5/month
- No sleep
- More resources

---

## 🚀 Production Checklist

Before going live:

- [ ] All API keys added to Railway Variables
- [ ] Frontend deployed (Vercel/Netlify) with correct WebSocket URL
- [ ] WebSocket connection tested
- [ ] Error handling tested
- [ ] Monitoring enabled
- [ ] Backup API keys stored securely

---

**🎉 Your AI Research ROMA app is now deployed on Railway!**

**Live URL:** Check Railway dashboard for your deployment URL

