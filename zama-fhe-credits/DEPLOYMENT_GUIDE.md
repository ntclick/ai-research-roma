# 🚀 Deployment Guide - AIResearchCredits

Hướng dẫn chi tiết deploy smart contract lên Zama Devnet

---

## 📋 Prerequisites

### 1. Cài đặt Dependencies

```bash
cd AI Research deploy/zama-fhe-credits
npm install
```

### 2. Cấu hình Environment

```bash
cp env.template .env
```

Chỉnh sửa `.env`:
```env
PRIVATE_KEY=your_wallet_private_key_without_0x
ZAMA_RPC_URL=https://devnet.zama.ai
GATEWAY_URL=https://gateway.devnet.zama.ai
```

**⚠️ Lấy Private Key từ MetaMask:**
1. MetaMask → Settings → Security & Privacy
2. "Reveal Private Key"
3. Copy (không bao gồm "0x")
4. Paste vào `.env`

### 3. Lấy Testnet Tokens

**Zama Devnet Faucet:**
- URL: https://faucet.devnet.zama.ai
- Nhập địa chỉ wallet
- Nhận 1 ZAMA (testnet ETH)

**Kiểm tra balance:**
```bash
npx hardhat run scripts/check-balance.js --network zama
```

---

## 🔨 Compile Contract

```bash
npm run compile
```

**Output:**
```
Compiled 1 Solidity file successfully
✓ AIResearchCredits.sol
```

**Kiểm tra artifacts:**
```bash
ls artifacts/contracts/AIResearchCredits.sol/
```

Sẽ thấy:
- `AIResearchCredits.json` (ABI + bytecode)

---

## 🧪 Run Tests (Optional)

```bash
npm test
```

**Test cases:**
- ✅ Daily check-in logic
- ✅ Buy credits with ETH
- ✅ Credit usage (encrypted)
- ✅ Balance queries
- ✅ Owner functions
- ✅ Time helpers

**Expected output:**
```
  AIResearchCredits (Zama FHE)
    Deployment
      ✔ Should set the right owner
      ✔ Should have correct constants
    Daily Check-in
      ✔ Should allow first check-in
      ✔ Should fail if checking in twice within 24h
    ...
  
  18 passing (2.3s)
```

---

## 🌐 Deploy to Zama Devnet

### Step 1: Deploy Contract

```bash
npm run deploy
```

**Expected output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Deploying AIResearchCredits (Zama FHE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Deployer: 0x1234...5678
💰 Balance: 1.0 ETH

⏳ Deploying contract...
✅ AIResearchCredits deployed to: 0xabcd...ef12

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Contract Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️  Name: AIResearchCredits
📍 Address: 0xabcd...ef12
👤 Owner: 0x1234...5678
🎁 Daily Reward: 10 credits
💵 Credit Price: 0.01 ETH
⏰ Check-in Cooldown: 24 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Verify contract on Zama explorer
2. Update frontend with contract address
3. Test daily check-in functionality
4. Test buy credits (0.01 ETH per credit)

🔗 Zama Devnet Explorer:
   https://explorer.devnet.zama.ai/address/0xabcd...ef12

✨ Author: @trungkts29 (https://x.com/trungkts29)
```

### Step 2: Save Contract Address

**Tạo file `deployed-address.json`:**
```json
{
  "network": "zama-devnet",
  "chainId": 8009,
  "contract": "AIResearchCredits",
  "address": "0xYOUR_CONTRACT_ADDRESS",
  "deployer": "0xYOUR_WALLET_ADDRESS",
  "timestamp": "2025-10-06T...",
  "constants": {
    "dailyReward": 10,
    "creditPrice": "0.01",
    "cooldown": 86400
  }
}
```

### Step 3: Verify on Explorer

**Zama Devnet Explorer:**
https://explorer.devnet.zama.ai

**Tìm contract:**
1. Paste địa chỉ contract vào search
2. Kiểm tra:
   - ✅ Contract code
   - ✅ Transaction history
   - ✅ Balance

---

## 🧪 Test Deployed Contract

### Test 1: Daily Check-in

```bash
npx hardhat run scripts/test-checkin.js --network zama
```

**Tạo `scripts/test-checkin.js`:**
```javascript
async function main() {
  const [signer] = await ethers.getSigners();
  const contract = await ethers.getContractAt(
    "AIResearchCredits", 
    "0xYOUR_CONTRACT_ADDRESS"
  );
  
  console.log("Testing daily check-in...");
  const tx = await contract.dailyCheckIn();
  await tx.wait();
  
  console.log("✅ Check-in successful! +10 credits");
}

main().catch(console.error);
```

### Test 2: Buy Credits

```javascript
// Buy 10 credits for 0.1 ETH
const tx = await contract.buyCredits(10, { 
  value: ethers.parseEther("0.1") 
});
await tx.wait();
```

### Test 3: Check Balance

```javascript
// Request decryption
const tx = await contract.requestBalanceDecryption();
await tx.wait();

// Listen for result
contract.once("CreditsDecrypted", (user, balance) => {
  console.log(`Balance: ${balance} credits`);
});
```

---

## 📦 Export ABI for Frontend

### Tạo file `abi.json`:

```bash
node scripts/export-abi.js
```

**`scripts/export-abi.js`:**
```javascript
const fs = require('fs');
const path = require('path');

const artifactPath = path.join(
  __dirname, 
  '../artifacts/contracts/AIResearchCredits.sol/AIResearchCredits.json'
);

const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));

const exportData = {
  contractName: "AIResearchCredits",
  abi: artifact.abi,
  bytecode: artifact.bytecode,
  networks: {
    "zama-devnet": {
      chainId: 8009,
      address: "0xYOUR_CONTRACT_ADDRESS"
    }
  }
};

fs.writeFileSync(
  path.join(__dirname, '../abi.json'),
  JSON.stringify(exportData, null, 2)
);

console.log("✅ ABI exported to abi.json");
```

### Copy ABI to Frontend

```bash
cp abi.json ../frontend/src/contracts/AIResearchCredits.json
```

---

## 🔗 Update Frontend

### 1. Install Dependencies

```bash
cd ../frontend
npm install fhevmjs ethers
```

### 2. Update Contract Address

**`frontend/src/config/contracts.js`:**
```javascript
export const CONTRACTS = {
  AIResearchCredits: {
    address: "0xYOUR_CONTRACT_ADDRESS",
    chainId: 8009,
    network: "zama-devnet"
  }
};
```

### 3. Import ABI

```javascript
import AIResearchCreditsABI from './contracts/AIResearchCredits.json';

const contract = new Contract(
  CONTRACTS.AIResearchCredits.address,
  AIResearchCreditsABI.abi,
  signer
);
```

---

## 🌐 Configure MetaMask

### Add Zama Devnet to MetaMask

**Manual:**
1. MetaMask → Settings → Networks → Add Network
2. Nhập:
   - **Network Name**: Zama Devnet
   - **RPC URL**: https://devnet.zama.ai
   - **Chain ID**: 8009
   - **Currency Symbol**: ZAMA
   - **Explorer**: https://explorer.devnet.zama.ai

**Hoặc dùng script:**
```javascript
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [{
    chainId: '0x1F49', // 8009 in hex
    chainName: 'Zama Devnet',
    rpcUrls: ['https://devnet.zama.ai'],
    nativeCurrency: {
      name: 'ZAMA',
      symbol: 'ZAMA',
      decimals: 18
    },
    blockExplorerUrls: ['https://explorer.devnet.zama.ai']
  }]
});
```

---

## 📊 Monitoring

### Check Contract Balance

```javascript
const balance = await contract.getContractBalance();
console.log(`Contract ETH: ${ethers.formatEther(balance)}`);
```

### Withdraw Funds (Owner Only)

```javascript
// Only deployer can call
const tx = await contract.withdraw();
await tx.wait();
console.log("✅ Funds withdrawn");
```

### Listen to Events

```javascript
// Check-in events
contract.on("CheckedIn", (user, timestamp) => {
  console.log(`${user} checked in at ${timestamp}`);
});

// Purchase events
contract.on("CreditsPurchased", (user, amount, cost) => {
  console.log(`${user} bought ${amount} credits for ${cost} ETH`);
});

// Decryption events
contract.on("CreditsDecrypted", (user, balance) => {
  console.log(`${user}'s balance: ${balance} credits`);
});
```

---

## 🔒 Security Checklist

- [x] Private key trong `.env` (không commit lên Git)
- [x] `.gitignore` bao gồm `.env`
- [x] Contract deployed bởi trusted wallet
- [x] Owner address đúng
- [x] Constants đúng (daily reward, price, cooldown)
- [x] Testnet trước khi lên mainnet
- [ ] Security audit (trước mainnet)

---

## 🐛 Troubleshooting

### Lỗi: "Insufficient funds"

**Giải pháp:**
```bash
# Kiểm tra balance
npx hardhat run scripts/check-balance.js --network zama

# Lấy thêm từ faucet
# https://faucet.devnet.zama.ai
```

### Lỗi: "Already checked in today"

**Giải pháp:**
```javascript
// Kiểm tra thời gian còn lại
const timeLeft = await contract.timeUntilNextCheckIn();
console.log(`Wait ${timeLeft} seconds`);
```

### Lỗi: "Transaction failed"

**Giải pháp:**
1. Kiểm tra gas limit
2. Kiểm tra nonce
3. Xem logs trên explorer
4. Thử lại với gas cao hơn

---

## 📈 Cost Breakdown

### Gas Costs (Zama Devnet)

| Function | Gas Used | Est. Cost |
|----------|----------|-----------|
| Deploy | ~2,500,000 | $0.05 |
| dailyCheckIn() | ~150,000 | $0.003 |
| buyCredits() | ~180,000 | $0.004 |
| useCredits() | ~220,000 | $0.005 |
| requestBalanceDecryption() | ~120,000 | $0.002 |

*Testnet costs, mainnet sẽ khác*

### FHE Coprocessor Fees

- **Encryption**: Free (client-side)
- **Operations**: $0.01-0.10 per transaction
- **Decryption**: $0.0016-0.00002 per bit

---

## 🎯 Post-Deployment Tasks

1. **Update README:**
   - [ ] Thêm deployed address
   - [ ] Thêm explorer link
   - [ ] Update status badge

2. **Update Frontend:**
   - [ ] Contract address
   - [ ] ABI import
   - [ ] Network config

3. **Testing:**
   - [ ] Daily check-in
   - [ ] Buy credits
   - [ ] Use credits
   - [ ] Balance decryption

4. **Documentation:**
   - [ ] User guide
   - [ ] API reference
   - [ ] Video tutorial

---

## 🚀 Mainnet Deployment (Q4 2025)

**Coming soon:**
- Ethereum mainnet
- Polygon
- Arbitrum
- Solana (2026)

**Preparation:**
1. Security audit
2. Testnet testing hoàn thiện
3. Legal compliance
4. User documentation
5. Support system

---

## 📞 Support

**Issues?**
- GitHub: https://github.com/ntclick/ai-research-roma/issues
- Twitter: https://x.com/trungkts29
- Zama Discord: https://discord.gg/zama

---

**✨ Deployment guide by @trungkts29**

**🔗 Resources:**
- Zama Docs: https://docs.zama.ai
- Explorer: https://explorer.devnet.zama.ai
- Faucet: https://faucet.devnet.zama.ai

