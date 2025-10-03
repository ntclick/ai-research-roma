# Crypto Research App với ROMA Framework

**👨‍💻 Author:** [@trungkts29](https://x.com/trungkts29)

Ứng dụng web React tích hợp ROMA framework cho nghiên cứu cryptocurrency với AI.

## Tính năng chính

- 💰 **Token Economy**: Mua GM Token bằng Sepolia ETH (1 GM = 0.001 ETH = 1 lượt research)
- 🎁 **Check-in hàng ngày**: Nhận 50 GM Credits miễn phí
- 🤖 **AI Research Chat**: Nghiên cứu coin, phân tích giá, tạo nội dung
- 🔗 **Blockchain Integration**: Smart contract trên Sepolia testnet
- 🎨 **Image Generation**: Tạo hình ảnh với fal.ai Flux

## Công nghệ sử dụng

### Frontend
- React 18
- Chakra UI
- ethers.js v6
- WebSocket (react-use-websocket)
- MetaMask integration

### Backend
- Python 3.8+
- **[ROMA Framework](https://github.com/sentient-agi/ROMA)** ⭐ - Recursive multi-agent system
  - SentientAgent for AI research
  - Tavily/Serper for web search
  - OpenAI/Anthropic LLMs
- WebSocket server (asyncio)
- CoinGecko API
- fal.ai API for image generation

### Blockchain
- Solidity 0.8.20
- Hardhat development environment
- OpenZeppelin Contracts v5
- Sepolia Testnet

### AI & Search
- **Google Gemini 1.5** (via ROMA) - **MIỄN PHÍ** 1500 req/day 🎉
- OpenAI GPT-4 (via ROMA) - Alternative có phí
- Anthropic Claude (via ROMA) - Alternative có phí
- Tavily Search API (1000 free searches/month)

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd crypto-research-app
```

### 2. Setup Smart Contract

```bash
cd backend/contracts
npm install

# Copy và cấu hình .env
cp .env.example .env
# Điền các thông tin: SEPOLIA_RPC_URL, PRIVATE_KEY, ETHERSCAN_API_KEY

# Deploy contract lên Sepolia
npm run deploy:sepolia
```

### 3. Setup Backend

```bash
cd ../../backend
pip install -r requirements.txt

# Copy và cấu hình .env
cp .env.example .env
# Điền các API keys: COINGECKO_API_KEY, FAL_AI_API_KEY, etc.

# Start WebSocket server
python websocket_server.py
```

### 4. Setup Frontend

```bash
cd ../frontend
npm install

# Copy và cấu hình .env
cp .env.example .env
# Điền contract address từ bước deploy và các thông tin khác

# Start development server
npm start
```

Ứng dụng sẽ chạy tại `http://localhost:3000`

## Cấu trúc dự án

```
crypto-research-app/
├── frontend/                  # React App
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/         # Research chat components
│   │   │   ├── Wallet/       # Wallet connection
│   │   │   └── TokenEconomy/ # Token purchase & check-in
│   │   ├── hooks/
│   │   │   └── useWeb3.js    # Web3 connection hook
│   │   ├── services/
│   │   │   └── gmTokenService.js  # Smart contract interface
│   │   ├── config/
│   │   └── App.js
│   └── package.json
│
├── backend/                   # Python Backend
│   ├── roma_agents/
│   │   └── crypto_research_agent.py
│   ├── contracts/            # Smart contracts
│   │   ├── GMToken.sol
│   │   └── hardhat.config.js
│   ├── scripts/
│   │   └── deploy.js
│   ├── websocket_server.py
│   └── requirements.txt
│
└── docs/
```

## Sử dụng

### 1. Kết nối ví MetaMask

- Click "Kết nối MetaMask"
- Chuyển sang Sepolia Testnet
- Approve connection

### 2. Lấy GM Credits

**Cách 1: Check-in hàng ngày**
- Vào tab "Token Economy"
- Click "Check-in (+50 GM)"
- Nhận 50 GM Credits miễn phí

**Cách 2: Mua GM Tokens**
- Nhập số lượng ETH muốn mua
- Click "Mua Tokens"
- Confirm transaction trong MetaMask

### 3. Sử dụng Research Chat

- Chọn công cụ (Nghiên cứu Coin, Phân tích Giá, etc.)
- Nhập yêu cầu research
- Click "Gửi (1 GM)" để gửi
- Mỗi yêu cầu tiêu tốn 1 GM Credit

## Các công cụ Research

1. **🔍 Nghiên cứu Coin**: Phân tích toàn diện về một cryptocurrency
2. **📊 Phân tích Giá**: Phân tích chi tiết về giá và market data
3. **🐦 Phân tích bài X**: Phân tích nội dung từ Twitter/X
4. **✍️ Viết bài X**: Tạo nội dung post cho Twitter/X
5. **🎨 Tạo hình ảnh**: Generate hình ảnh với AI

## Smart Contract

### GMToken Contract

**Address**: `[Sẽ được cập nhật sau khi deploy]`

**Các function chính:**
- `purchaseTokens()`: Mua GM tokens với ETH
- `dailyCheckIn()`: Check-in hàng ngày nhận 50 GM
- `getResearchCredits(address)`: Xem số credits còn lại
- `useResearchCredit(address, amount)`: Sử dụng credits (owner only)

**Token Economics:**
- 1 GM Token = 0.001 ETH
- 1 GM Token = 1 lượt research
- Check-in hàng ngày: 50 GM (1 lần/24h)

## API Keys cần thiết

### CoinGecko API
- Đăng ký tại: https://www.coingecko.com/en/api
- Free tier: 10-50 calls/minute

### fal.ai API
- Đăng ký tại: https://fal.ai
- Dùng cho image generation

### Twitter Bearer Token (Optional)
- Đăng ký Twitter Developer Account
- Dùng cho phân tích posts

### Infura/Alchemy
- RPC endpoint cho Sepolia
- Đăng ký tại: https://infura.io hoặc https://alchemy.com

## Testing

### Frontend
```bash
cd frontend
npm test
```

### Smart Contract
```bash
cd backend/contracts
npx hardhat test
```

## Deployment

### Production Frontend
```bash
cd frontend
npm run build
# Deploy build folder lên hosting (Vercel, Netlify, etc.)
```

### Production Backend
```bash
# Sử dụng Docker hoặc deploy lên cloud service
# Đảm bảo WebSocket server accessible
```

## Troubleshooting

### MetaMask không kết nối được
- Kiểm tra đã cài MetaMask extension
- Refresh trang và thử lại
- Kiểm tra network đã chọn đúng Sepolia

### Transaction failed
- Kiểm tra đủ ETH trong ví (cho gas fees)
- Kiểm tra đã chọn đúng network (Sepolia)
- Xem chi tiết lỗi trong console

### WebSocket không kết nối
- Kiểm tra backend server đã chạy
- Kiểm tra URL trong .env đúng
- Kiểm tra firewall không block port 5001

## Lưu ý bảo mật

⚠️ **QUAN TRỌNG:**
- Không commit file `.env` lên git
- Không chia sẻ private key
- Chỉ dùng testnet ETH, không dùng mainnet
- Backup private key an toàn

## Roadmap

- [ ] Tích hợp ROMA agents nâng cao
- [ ] Thêm nhiều công cụ research
- [ ] Portfolio tracking
- [ ] Social features
- [ ] Mobile app
- [ ] Deploy lên mainnet

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## License

MIT License

## Hỗ trợ

Nếu gặp vấn đề, vui lòng:
- Mở issue trên GitHub
- Liên hệ qua email: [your-email]
- Join Discord community: [link]

---

Made with ❤️ using ROMA Framework

