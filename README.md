# 🚀 Crypto Research AI with ROMA Framework

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Active-brightgreen?style=for-the-badge)](https://airesearch-tools.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-Railway-blue?style=for-the-badge)](https://railway.app)
[![Framework](https://img.shields.io/badge/Framework-ROMA-purple?style=for-the-badge)](https://github.com/ntclick/ai-research-roma)

**👨‍💻 Author:** [@trungkts29](https://x.com/trungkts29)

An advanced cryptocurrency research assistant powered by the ROMA (Recursive Open Meta-Agent) Framework. Combines multiple AI models and data sources to provide comprehensive crypto market analysis, real-time price tracking, news aggregation, and AI-powered image generation.

## 🌐 Live Demo

**Try it now:** https://airesearch-tools.vercel.app

**Backend API:** wss://web-production-6b11c.up.railway.app

**Status:** ✅ **LIVE & OPERATIONAL**

## 🎥 Demo Video

Watch the full demo and tutorial:

[![Demo Video](https://img.youtube.com/vi/3Oihz5XFWpw/maxresdefault.jpg)](https://youtu.be/3Oihz5XFWpw)

**[▶️ Watch on YouTube](https://youtu.be/3Oihz5XFWpw)**

---

## ✨ Key Features

### 🤖 **Multi-AI Architecture**
- **OpenAI GPT-4o-mini** - Intelligent routing brain that analyzes queries and determines optimal data sources
- **Google Gemini 1.5 Flash** - Primary AI worker for quick answers, definitions, and prompt enhancement
- **Automatic Fallback** - If Gemini hits rate limits, OpenAI seamlessly takes over

### 📊 **Real-Time Crypto Data**
- Live cryptocurrency prices from CoinGecko API
- Support for 15+ major cryptocurrencies (Bitcoin, Ethereum, Solana, etc.)
- Market cap, volume, and 24h price change tracking
- Automatic coin name recognition from natural language queries

### 📰 **Smart News Aggregation**
- Aggregates from 4 major crypto news sources (CoinDesk, CoinTelegraph, Decrypt, The Block)
- **7-day time filter** - Only shows recent, relevant news
- **Coin-specific filtering** - Regex-based matching for targeted news
- **Duplicate removal** - Clean, unique headlines
- **English language** - All user-facing messages in English

### 🎨 **AI Image Generation**
- Powered by fal.ai FLUX.1 [dev] model
- **AI-enhanced prompts** - Gemini/OpenAI automatically improves your image descriptions
- High-quality cryptocurrency-themed image generation
- Direct integration with Python fal-client library

### 🧠 **ROMA Framework**
- **Recursive Task Decomposition** - Breaks complex queries into manageable subtasks
- **Multi-Source Aggregation** - Combines data from multiple APIs intelligently
- **Atomic Task Execution** - Efficient parallel processing
- **Smart Planning** - OpenAI creates optimal research strategies

---

## 🏗️ Architecture

```
User Query
    ↓
┌─────────────────────────────────────┐
│  OpenAI GPT-4o-mini (Routing Brain) │
│  Analyzes intent & routes to APIs   │
└─────────────────────────────────────┘
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│   CoinGecko     │    RSS News      │  Gemini Worker  │
│  Price Data     │  Last 7 Days     │  Definitions    │
│  Market Stats   │  Coin-Specific   │  Enhancement    │
└─────────────────┴──────────────────┴─────────────────┘
    ↓
┌─────────────────────────────────────┐
│        ROMA Framework               │
│  Task Planning → Execution →        │
│  Aggregation → Response Generation  │
└─────────────────────────────────────┘
    ↓
Formatted Response to User
```

---

## 📋 Supported Queries

### **Price Queries**
- `"BTC price"` - Get current Bitcoin price
- `"Ethereum market cap"` - Market capitalization data
- `"SOL volume"` - Trading volume information
- `"check LINK"` - Quick price check

### **News Queries**
- `"Bitcoin news"` - Latest BTC news (7 days)
- `"Ethereum updates"` - ETH-specific news
- `"crypto news"` - General cryptocurrency news
- Automatically filters for coin mentions using regex

### **Analysis Queries**
- `"What is Bitcoin?"` - Get detailed explanations
- `"Should I buy ETH?"` - Investment analysis (combines price + news + AI insights)
- `"Explain Solana"` - Comprehensive overviews
- Complex queries are automatically decomposed into subtasks

### **Image Generation**
- `"create image Bitcoin logo modern"` - AI generates crypto-themed images
- `"generate ETH coin with text 'to the moon'"` - Custom designs
- AI automatically enhances your prompt for better results

---

## 🚀 Quick Start

### **Backend Setup**

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your API keys to .env:
# GOOGLE_API_KEY=your_gemini_key
# OPENAI_API_KEY=your_openai_key
# COINGECKO_API_KEY=your_coingecko_key
# FAL_API_KEY=your_fal_key

# Run server
python websocket_server.py
```

Backend runs on `ws://localhost:5001`

### **Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start
```

Frontend runs on `http://localhost:3000`

---

## 🔑 Required API Keys

1. **Google Gemini** (Primary AI)
   - Get at: https://makersuite.google.com/app/apikey
   - Free tier: 60 requests/minute

2. **OpenAI** (Routing + Backup)
   - Get at: https://platform.openai.com/api-keys
   - Model: GPT-4o-mini (cost-effective)

3. **CoinGecko** (Crypto Prices)
   - Get at: https://www.coingecko.com/en/api
   - Free tier: 30 calls/minute

4. **fal.ai** (Image Generation)
   - Get at: https://fal.ai/dashboard
   - Credits required for image generation

---

## 🎯 How It Works

### **1. Intelligent Query Routing**

When you send a query like `"Bitcoin price"`:

1. **OpenAI Brain** analyzes the query
2. Determines intent: Price query
3. Routes to: CoinGecko API
4. Extracts coin: "Bitcoin" → `bitcoin` ID
5. Fetches live price data
6. Returns formatted response

### **2. Multi-Source Complex Queries**

For `"Should I buy Ethereum?"`:

1. **OpenAI Brain** detects complexity
2. **ROMA Planner** creates subtasks:
   - Task 1: Get ETH price (CoinGecko)
   - Task 2: Get ETH news (RSS)
   - Task 3: Generate analysis (Gemini)
3. **Parallel execution** of all tasks
4. **Aggregator** combines results
5. Returns comprehensive investment analysis

### **3. News Filtering Pipeline**

For `"Solana news"`:

1. Fetches from 4 RSS feeds (120 entries total)
2. Regex filter: `\b(sol|solana)\b` (case-insensitive)
3. Date filter: Last 7 days only
4. Deduplication: Remove identical headlines
5. Returns top 5 most recent matches

### **4. AI-Enhanced Image Generation**

For `"create image Bitcoin rocket"`:

1. **User prompt:** "Bitcoin rocket"
2. **Gemini enhances:** "A sleek Bitcoin coin designed as a rocket ship launching into space, golden metallic texture, dramatic lighting, cryptocurrency theme, high quality digital art"
3. **fal.ai generates:** Using FLUX.1 [dev] model
4. **Returns:** Image URL + metadata

---

## 📊 Technical Stack

### **Backend**
- Python 3.8+
- WebSocket server (`websockets` library)
- Async/await for concurrent API calls
- ROMA Framework for task orchestration

### **Frontend**
- React 18
- Chakra UI for components
- WebSocket client (`react-use-websocket`)
- Markdown rendering for responses

### **AI Models**
- OpenAI GPT-4o-mini (routing, extraction, backup)
- Google Gemini 1.5 Flash (definitions, enhancement)
- fal.ai FLUX.1 [dev] (image generation)

### **Data Sources**
- CoinGecko API (cryptocurrency data)
- RSS Feeds: CoinDesk, CoinTelegraph, Decrypt, The Block
- feedparser for RSS parsing
- Regex for coin-specific filtering

---

## 🔧 Configuration

### **Backend Environment Variables**

```bash
# AI Models
GOOGLE_API_KEY=your_key_here
GOOGLE_MODEL=gemini-1.5-flash
OPENAI_API_KEY=your_key_here

# Data Sources
COINGECKO_API_KEY=your_key_here
FAL_API_KEY=your_key_here

# Server
HOST=localhost
PORT=5001
```

### **Frontend Environment Variables**

```bash
REACT_APP_WEBSOCKET_URL=ws://localhost:5001
```

---

## 📈 Performance Optimizations

### **News Fetching**
- ✅ Reduced from 18 to 4 RSS feeds (faster)
- ✅ Regex-based filtering (no AI cost)
- ✅ 7-day limit (relevant results)
- ✅ Duplicate removal (cleaner output)

### **AI Usage**
- ✅ OpenAI only for routing & extraction (low cost)
- ✅ Gemini for simple tasks (free tier)
- ✅ Automatic fallback prevents failures

### **Caching**
- ✅ WebSocket maintains connection
- ✅ Conversation history (last 10 messages)

---

## 🛠️ Development

### **Project Structure**

```
crypto-research-ai/
├── backend/
│   ├── websocket_server.py       # Main WebSocket server
│   ├── roma_agents/
│   │   ├── crypto_roma_agent.py  # ROMA task orchestration
│   │   └── api_integrations.py   # API clients (OpenAI, Gemini, etc.)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── InteractiveChat.jsx  # Main chat interface
│   │   └── App.js
│   └── package.json
└── docs/
```

### **Adding New Data Sources**

1. Add API client to `api_integrations.py`
2. Update routing rules in `analyze_context_with_openai()`
3. Add executor case in `crypto_roma_agent.py`

---

## 📄 License

MIT License - Free to use and modify

---

## 🙏 Acknowledgments

- **ROMA Framework** - For recursive task orchestration
- **OpenAI** - GPT-4o-mini model
- **Google** - Gemini 1.5 Flash model
- **fal.ai** - FLUX.1 image generation
- **CoinGecko** - Cryptocurrency data API

---

## 📞 Support

**Author:** [@trungkts29](https://x.com/trungkts29)

For questions, issues, or feature requests:
- GitHub Issues (after repo creation)
- Direct message on X/Twitter: @trungkts29

---

## 🌟 Features Roadmap

- [ ] Support for more cryptocurrencies
- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Historical data analysis
- [ ] Multi-language support
- [ ] Mobile app

---

**⭐ Star this repo if you find it useful!**

Made with ❤️ by [@trungkts29](https://x.com/trungkts29)
