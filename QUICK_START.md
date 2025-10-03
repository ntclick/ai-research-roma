# 🚀 Quick Start - Crypto Research App

## ✅ Ứng dụng đã được setup hoàn chỉnh!

### 📱 Truy cập ứng dụng:
- **Frontend:** http://localhost:5000
- **Backend WebSocket:** ws://localhost:5001
- **Contract:** `0x586C0bcaBFf5e3E2700f947408856BBBBcF0E2D6` (Sepolia)

---

## 🔧 Lệnh chạy trong PowerShell

### **Terminal 1 - Backend:**
```powershell
cd "F:\Work\Cryoto\ai research\crypto-research-app\backend"
py websocket_server.py
```

### **Terminal 2 - Frontend:**
```powershell
cd "F:\Work\Cryoto\ai research\crypto-research-app\frontend"
npm start
# Tự động chạy trên port 5000 (từ .env.local)
```

---

## 📋 Checklist trước khi chạy

### ✅ Đã cài đặt:
- [x] Node.js & npm
- [x] Python 3.13
- [x] Git
- [x] MetaMask extension

### ✅ Đã setup:
- [x] Frontend dependencies (`npm install`)
- [x] Backend dependencies (`py -m pip install -r requirements.txt`)
- [x] Contract deployed to Sepolia
- [x] `.env` files configured

---

## 🎯 Tính năng chính

### 1. **💰 Token Economy**
- Mua GM tokens bằng Sepolia ETH (1 GM = 0.001 ETH)
- Daily check-in nhận 50 GM miễn phí
- 1 GM = 1 research turn

### 2. **💬 AI Research Chat**
Tools có sẵn:
- 🔍 **Nghiên cứu Coin** - Phân tích chi tiết cryptocurrency
- 📊 **Phân tích Giá** - Biểu đồ và xu hướng
- 🐦 **Phân tích X/Twitter** - Phân tích posts
- ✍️ **Viết bài X** - Tạo content
- 🎨 **Tạo hình ảnh** - AI image generation

### 3. **⚙️ Settings**
- Cấu hình API keys (CoinGecko, fal.ai, Twitter)
- Blockchain configuration
- Contract address

### 4. **🚀 Deploy Contract**
- Hướng dẫn chi tiết deploy smart contract
- Contract verification
- Save contract address

---

## 🔑 Configuration Files

### **frontend/.env.local**
```env
PORT=5000
REACT_APP_WEBSOCKET_URL=ws://localhost:5001
REACT_APP_SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/76b44e6470c34a5289c6ce728464de8e
REACT_APP_GM_TOKEN_CONTRACT=0x586C0bcaBFf5e3E2700f947408856BBBBcF0E2D6
```

### **backend/.env**
```env
GOOGLE_API_KEY=AIzaSy-replace-with-your-key
GOOGLE_MODEL=gemini-1.5-flash
TAVILY_API_KEY=tvly-replace-if-you-have
COINGECKO_API_KEY=
HOST=localhost
PORT=5001
```

### **backend/contracts/.env**
```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/76b44e6470c34a5289c6ce728464de8e
PRIVATE_KEY=0x859b25f164df967d1b6b04b81693a9f53785a6f2b03bf3c6b20796f60ca8d814
ETHERSCAN_API_KEY=SMYU9ZMV9DB55ZAFPW5JKN56S52RVBIWX6
```

---

## 🔍 Kiểm tra status

### Check ports đang chạy:
```powershell
# Frontend (Port 5000)
netstat -ano | findstr ":5000"

# Backend (Port 5001)
netstat -ano | findstr ":5001"
```

### Check Node processes:
```powershell
Get-Process | Where-Object {$_.ProcessName -eq "node"}
```

### Stop processes:
```powershell
# Stop specific port
Get-Process | Where-Object {$_.Id -eq PROCESS_ID} | Stop-Process -Force

# Stop all Node processes
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Stop-Process -Force
```

---

## 🐛 Troubleshooting

### **Frontend không chạy trên port 5000:**
```powershell
# Đảm bảo file .env.local tồn tại
Test-Path "frontend\.env.local"

# Nếu không có, tạo mới:
@"
PORT=5000
REACT_APP_WEBSOCKET_URL=ws://localhost:5001
REACT_APP_SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/76b44e6470c34a5289c6ce728464de8e
REACT_APP_GM_TOKEN_CONTRACT=0x586C0bcaBFf5e3E2700f947408856BBBBcF0E2D6
"@ | Out-File -FilePath "frontend\.env.local" -Encoding utf8
```

### **WebSocket connection failed:**
1. Kiểm tra backend đang chạy: `netstat -ano | findstr ":5001"`
2. Restart backend: 
   ```powershell
   cd backend
   py websocket_server.py
   ```

### **Contract call failed:**
1. Đảm bảo đã connect MetaMask
2. Switch sang Sepolia network
3. Check contract address đúng trong Settings

### **JavaScript errors:**
```powershell
# Clear cache và rebuild
cd frontend
Remove-Item -Recurse -Force node_modules\.cache
npm start
```

---

## 📚 Tech Stack

### **Frontend:**
- React.js 18
- Chakra UI
- ethers.js v6
- react-use-websocket

### **Backend:**
- Python 3.13
- WebSocket (websockets)
- Google Gemini AI
- ROMA Framework (optional)

### **Blockchain:**
- Solidity 0.8.20
- Hardhat
- OpenZeppelin
- Sepolia Testnet

---

## 🔗 Useful Links

- **Contract on Etherscan:** https://sepolia.etherscan.io/address/0x586C0bcaBFf5e3E2700f947408856BBBBcF0E2D6
- **Sepolia Faucet:** https://sepoliafaucet.com
- **Google Gemini API:** https://ai.google.dev
- **CoinGecko API:** https://www.coingecko.com/en/api
- **ROMA Framework:** https://github.com/sentient-agi/ROMA

---

## 🎉 Quick Test

1. **Start backend:**
   ```powershell
   cd backend
   py websocket_server.py
   ```

2. **Start frontend (terminal mới):**
   ```powershell
   cd frontend
   npm start
   ```

3. **Open browser:**
   - Go to http://localhost:5000
   - Connect MetaMask
   - Try daily check-in
   - Chat với AI research

---

**✅ Ứng dụng sẵn sàng sử dụng! Happy researching! 🚀**

