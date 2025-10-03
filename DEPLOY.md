# 🚀 Deployment Guide

**Author:** [@trungkts29](https://x.com/trungkts29)

## 📋 Prerequisites

### API Keys Required:
1. **Google Gemini** (Primary AI) - [Get key](https://makersuite.google.com/app/apikey)
2. **OpenAI** (Brain + Backup) - [Get key](https://platform.openai.com/api-keys)
3. **CoinGecko** (Crypto prices) - [Get key](https://www.coingecko.com/en/api)
4. **fal.ai** (Image generation) - [Get key](https://fal.ai/dashboard)

Optional:
- **Tavily API** - Web search
- **Perplexity API** - Research

---

## 🌐 Deploy to Vercel

### 1. Setup Vercel Project

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd "AI Research deploy"
vercel
```

### 2. Configure Environment Variables

Go to **Vercel Dashboard > Project Settings > Environment Variables** and add:

```
GOOGLE_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
COINGECKO_API_KEY=CG-...
FAL_API_KEY=16a9a508-...
GOOGLE_MODEL=gemini-1.5-flash
HOST=0.0.0.0
PORT=5001
```

### 3. Deploy

```bash
vercel --prod
```

---

## 📦 Deploy to GitHub

### 1. Initialize Git

```bash
cd "AI Research deploy"
git init
git add .
git commit -m "Initial commit - Crypto Research AI by @trungkts29"
```

### 2. Create GitHub Repo

1. Go to [GitHub](https://github.com/new)
2. Create repository: `crypto-research-ai`
3. Don't initialize with README

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/crypto-research-ai.git
git branch -M main
git push -u origin main
```

---

## 🔧 Local Development

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your API keys
cp .env.example .env

# Run server
python websocket_server.py
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start
```

Frontend: http://localhost:3000  
Backend: ws://localhost:5001

---

## 🎯 Features

✅ **RSS News** - 7-day filter, coin-specific, no duplicates  
✅ **Image Generation** - AI-enhanced prompts, fal.ai FLUX.1 [dev]  
✅ **Twitter/X Analysis** - Auto-detect URLs, credibility warnings  
✅ **Price Tracking** - Real-time CoinGecko data  
✅ **Multi-AI Architecture** - OpenAI (Brain), Gemini (Worker)  
✅ **ROMA Framework** - Recursive task decomposition  

---

## 📝 Architecture

```
User Query
    ↓
OpenAI GPT-4o-mini (Brain) - Routing
    ↓
├─ CoinGecko → Price data
├─ RSS News → Latest news (7 days)
├─ Gemini → Definitions, prompt enhancement
├─ fal.ai → Image generation
└─ Twitter Analysis → X/Twitter posts
    ↓
ROMA Framework - Task decomposition & aggregation
    ↓
User Response
```

---

## 🔐 Security

- Never commit `.env` with real API keys
- Use environment variables on Vercel
- Add `.env` to `.gitignore`
- Use `.env.example` as template

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend connection issues
```bash
# Check REACT_APP_WEBSOCKET_URL in .env
REACT_APP_WEBSOCKET_URL=ws://localhost:5001

# Clear cache and restart
rm -rf node_modules
npm install
npm start
```

### API Rate Limits
- **Gemini fails** → OpenAI backup activates
- **CoinGecko limit** → Use free tier or upgrade
- **fal.ai credits** → Check dashboard

---

## 📞 Support

**Author:** [@trungkts29](https://x.com/trungkts29)  
**GitHub Issues:** Create an issue on GitHub repo  
**Twitter/X:** DM @trungkts29

---

## 📄 License

MIT License - Free to use and modify

---

**⭐ Star on GitHub if you find this useful!**

