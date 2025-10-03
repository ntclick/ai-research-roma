# Hướng dẫn Setup Chi tiết

## Yêu cầu hệ thống

- Node.js v16+ và npm
- Python 3.8+
- MetaMask browser extension
- Git

## Bước 1: Chuẩn bị môi trường

### 1.1 Cài đặt Node.js và Python

**Windows:**
- Download Node.js từ: https://nodejs.org/
- Download Python từ: https://www.python.org/downloads/

**macOS:**
```bash
brew install node
brew install python@3.9
```

**Linux:**
```bash
sudo apt update
sudo apt install nodejs npm
sudo apt install python3 python3-pip
```

### 1.2 Cài đặt MetaMask

- Cài extension từ: https://metamask.io/
- Tạo hoặc import ví
- Lưu seed phrase an toàn

### 1.3 Lấy Sepolia ETH (testnet)

**Faucets:**
- https://sepoliafaucet.com/
- https://www.alchemy.com/faucets/ethereum-sepolia
- https://faucet.quicknode.com/ethereum/sepolia

Cần ít nhất 0.1 ETH để test.

## Bước 2: Đăng ký API Keys

### 2.1 Infura (hoặc Alchemy)

**Infura:**
1. Đăng ký tại: https://infura.io/
2. Tạo project mới
3. Copy Project ID
4. RPC URL: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

**Alchemy (alternative):**
1. Đăng ký tại: https://alchemy.com/
2. Tạo app với Sepolia network
3. Copy HTTPS URL

### 2.2 CoinGecko API

1. Đăng ký tại: https://www.coingecko.com/en/api
2. Chọn Free tier (đủ cho development)
3. Copy API key từ dashboard
4. Rate limit: 10-50 calls/minute

### 2.3 fal.ai API

1. Đăng ký tại: https://fal.ai/
2. Vào API Keys section
3. Tạo new API key
4. Copy và lưu key

### 2.4 Etherscan API (cho verification)

1. Đăng ký tại: https://etherscan.io/
2. Vào API Keys section
3. Tạo free API key
4. Copy key

### 2.5 Twitter API (Optional)

1. Đăng ký Twitter Developer Account: https://developer.twitter.com/
2. Tạo app mới
3. Generate Bearer Token
4. Copy token

## Bước 3: Deploy Smart Contract

### 3.1 Setup contract project

```bash
cd backend/contracts
npm install

# Tạo file .env
cp .env.example .env
```

### 3.2 Cấu hình .env cho contracts

Mở `backend/contracts/.env` và điền:

```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=your_metamask_private_key_here
ETHERSCAN_API_KEY=your_etherscan_api_key
```

**⚠️ Lấy Private Key từ MetaMask:**
1. Mở MetaMask
2. Click 3 dots → Account details
3. Click "Export Private Key"
4. Nhập password
5. Copy key (BẮT ĐẦU với 0x)

### 3.3 Compile contract

```bash
npx hardhat compile
```

### 3.4 Deploy contract

```bash
npm run deploy:sepolia
```

Output sẽ hiển thị contract address:
```
GMToken deployed to: 0x1234567890abcdef...
```

**LƯU LẠI địa chỉ này!** Cần dùng cho frontend.

### 3.5 Verify contract (Optional)

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS>
```

## Bước 4: Setup Backend

### 4.1 Install Python dependencies

```bash
cd ../../backend
pip install -r requirements.txt

# Hoặc dùng virtual environment (khuyến nghị)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4.2 Cấu hình .env cho backend

```bash
cp .env.example .env
```

Mở `backend/.env` và điền:

```env
# API Keys
COINGECKO_API_KEY=your_coingecko_key
FAL_AI_API_KEY=your_fal_ai_key
TWITTER_BEARER_TOKEN=your_twitter_token

# Server
HOST=localhost
PORT=5001
```

### 4.3 Test backend

```bash
python websocket_server.py
```

Nếu thành công, sẽ hiển thị:
```
🚀 WebSocket server started on ws://localhost:5001
Waiting for connections...
```

Giữ terminal này chạy.

## Bước 5: Setup Frontend

### 5.1 Install dependencies

Mở terminal mới:

```bash
cd frontend
npm install
```

### 5.2 Cấu hình .env cho frontend

```bash
cp .env.example .env
```

Mở `frontend/.env` và điền:

```env
# API Keys
REACT_APP_COINGECKO_API_KEY=your_coingecko_key
REACT_APP_FAL_AI_API_KEY=your_fal_ai_key
REACT_APP_TWITTER_BEARER_TOKEN=your_twitter_token

# ROMA Backend
REACT_APP_ROMA_API_URL=http://localhost:5000
REACT_APP_WEBSOCKET_URL=ws://localhost:5001

# Blockchain
REACT_APP_SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
REACT_APP_GM_TOKEN_CONTRACT=0x... # Địa chỉ contract từ bước 3.4
```

### 5.3 Start frontend

```bash
npm start
```

App sẽ mở tại: `http://localhost:3000`

## Bước 6: Testing Application

### 6.1 Kết nối ví

1. Mở `http://localhost:3000`
2. Click "Kết nối MetaMask"
3. Approve connection
4. Đảm bảo đã chọn Sepolia network

### 6.2 Test check-in

1. Vào tab "Token Economy"
2. Click "Check-in (+50 GM)"
3. Confirm transaction
4. Đợi transaction complete
5. Verify credits tăng lên 50

### 6.3 Test mua tokens

1. Nhập 0.01 ETH
2. Click "Mua Tokens"
3. Confirm transaction
4. Verify nhận 10 GM tokens

### 6.4 Test research chat

1. Vào tab "Research Chat"
2. Chọn "Nghiên cứu Coin"
3. Nhập: "BTC"
4. Click "Gửi (1 GM)"
5. Đợi AI response

## Troubleshooting Common Issues

### Issue: Contract deploy failed

**Solution:**
- Kiểm tra đủ Sepolia ETH
- Verify PRIVATE_KEY đúng format
- Check RPC URL hoạt động

```bash
# Test RPC connection
curl https://sepolia.infura.io/v3/YOUR_PROJECT_ID \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Issue: npm install failed

**Solution:**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules và reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Python dependencies error

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install specific versions
pip install websockets==12.0
pip install aiohttp==3.9.0
```

### Issue: MetaMask không kết nối

**Solution:**
- Clear browser cache
- Disable other wallet extensions
- Try incognito mode
- Check MetaMask settings → Connected sites

### Issue: WebSocket connection failed

**Solution:**
- Verify backend đang chạy
- Check port 5001 không bị block
- Windows: Check Windows Firewall
- Verify .env URL đúng

### Issue: Transaction always fails

**Solution:**
```bash
# Test contract trên Remix IDE
# 1. Copy GMToken.sol sang remix.ethereum.org
# 2. Compile với Solidity 0.8.20
# 3. Deploy với MetaMask
# 4. Test các functions
```

## Next Steps

Sau khi setup thành công:

1. **Customize UI**: Modify Chakra UI components theo ý muốn
2. **Add more tools**: Thêm các research tools mới
3. **Integrate ROMA**: Setup ROMA framework đầy đủ
4. **Add analytics**: Track usage và performance
5. **Deploy production**: Lên Vercel/Netlify (frontend) và cloud (backend)

## Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [ethers.js Documentation](https://docs.ethers.org/)
- [Chakra UI Components](https://chakra-ui.com/docs)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation)

## Hỗ trợ

Nếu gặp vấn đề không giải quyết được:
1. Check logs trong console (F12)
2. Review .env configuration
3. Verify all services running
4. Open GitHub issue với error details

