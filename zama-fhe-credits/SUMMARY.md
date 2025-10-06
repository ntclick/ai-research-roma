# 📊 AIResearchCredits - Project Summary

**Encrypted Credit System for AI Research using Zama FHE**

Author: [@trungkts29](https://x.com/trungkts29)

---

## 🎯 Tổng Quan

Smart contract quản lý credits cho AI Research với mã hóa end-to-end sử dụng **Zama's Fully Homomorphic Encryption (FHE)**.

### Tính Năng Chính

| Feature | Description | Encryption |
|---------|-------------|------------|
| 🎁 Daily Check-in | +10 credits mỗi 24h | Balance encrypted (euint32) |
| 💰 Buy Credits | 0.01 ETH per credit | Balance encrypted (euint32) |
| 🔐 Use Credits | Deduct encrypted amount | Fully encrypted operation |
| 👁️ View Balance | Request decryption via Gateway | Secure MPC decryption |

---

## 📁 Project Structure

```
zama-fhe-credits/
├── contracts/
│   └── AIResearchCredits.sol       # Main FHE contract (235 lines)
├── scripts/
│   ├── deploy.js                   # Deploy to Zama Devnet
│   ├── export-abi.js               # Export ABI for frontend
│   └── check-balance.js            # Check wallet balance
├── test/
│   └── AIResearchCredits.test.js   # 18 test cases
├── hardhat.config.js               # Hardhat + fhevm config
├── package.json                    # Dependencies
├── README.md                       # Main documentation
├── DEPLOYMENT_GUIDE.md             # Step-by-step deployment
├── FRONTEND_INTEGRATION.md         # React integration guide
└── SUMMARY.md                      # This file
```

---

## 🔐 Smart Contract Details

### Contract: `AIResearchCredits.sol`

**Solidity Version:** 0.8.24  
**License:** MIT  
**Network:** Zama Devnet (Chain ID: 8009)

### State Variables

```solidity
// Encrypted (confidential)
mapping(address => euint32) private encryptedCredits;

// Public (for verification)
mapping(address => uint256) public lastCheckIn;

// Constants
uint256 public constant DAILY_CHECKIN_REWARD = 10;
uint256 public constant CREDIT_PRICE = 0.01 ether;
uint256 public constant CHECKIN_COOLDOWN = 1 days;
```

### Key Functions

#### 1. `dailyCheckIn()`
- **Purpose**: Nhận 10 credits miễn phí
- **Cooldown**: 24 giờ
- **Gas**: ~150k
- **Event**: `CheckedIn(address, uint256)`

#### 2. `buyCredits(uint32 amount)`
- **Purpose**: Mua credits bằng ETH
- **Price**: 0.01 ETH per credit
- **Gas**: ~180k
- **Event**: `CreditsPurchased(address, uint256, uint256)`
- **Refund**: Tự động hoàn lại ETH dư

#### 3. `useCredits(einput, bytes)`
- **Purpose**: Sử dụng credits (encrypted)
- **Input**: Encrypted amount + proof
- **Gas**: ~220k
- **Event**: `CreditsUsed(address, uint256)`
- **Logic**: Conditional subtraction (only if balance sufficient)

#### 4. `getEncryptedBalance()`
- **Purpose**: Lấy encrypted balance handle
- **Returns**: `euint32` (encrypted)
- **View**: Read-only

#### 5. `requestBalanceDecryption()`
- **Purpose**: Yêu cầu decrypt balance
- **Process**: Async via Gateway
- **Callback**: `balanceDecryptionCallback()`
- **Event**: `CreditsDecrypted(address, uint32)`

### Security Features

- ✅ **Encrypted State**: Balances stored as `euint32`
- ✅ **Access Control**: Only user can decrypt own balance
- ✅ **Safe Math**: FHE operations (TFHE.add, TFHE.sub, TFHE.gte)
- ✅ **Cooldown Protection**: 24h between check-ins
- ✅ **Owner Withdrawal**: Only owner can withdraw ETH
- ✅ **Refund Mechanism**: Excess ETH returned automatically

---

## 🧪 Testing

### Test Suite: 18 Tests

```bash
npm test
```

**Coverage:**
- ✅ Deployment checks
- ✅ Daily check-in logic
- ✅ Buy credits (with refunds)
- ✅ Use credits (encrypted)
- ✅ Balance queries
- ✅ Owner functions
- ✅ Time helpers

**All tests passing:** ✅

---

## 🚀 Deployment

### Quick Start

```bash
# 1. Install
npm install

# 2. Configure
cp env.template .env
# Edit .env with your PRIVATE_KEY

# 3. Get testnet tokens
# Visit: https://faucet.devnet.zama.ai

# 4. Check balance
npm run balance

# 5. Compile
npm run compile

# 6. Deploy
npm run deploy

# 7. Export ABI
npm run export-abi
```

### Deployment Output

```
✅ AIResearchCredits deployed to: 0xabcd...ef12
🎁 Daily Reward: 10 credits
💵 Credit Price: 0.01 ETH
⏰ Check-in Cooldown: 24 hours
```

---

## 🌐 Network Configuration

### Zama Devnet (Testnet)

| Parameter | Value |
|-----------|-------|
| **Chain ID** | 8009 |
| **RPC URL** | https://devnet.zama.ai |
| **Gateway** | https://gateway.devnet.zama.ai |
| **Explorer** | https://explorer.devnet.zama.ai |
| **Faucet** | https://faucet.devnet.zama.ai |
| **Currency** | ZAMA (testnet) |

### Add to MetaMask

```javascript
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [{
    chainId: '0x1F49',
    chainName: 'Zama Devnet',
    rpcUrls: ['https://devnet.zama.ai'],
    nativeCurrency: { name: 'ZAMA', symbol: 'ZAMA', decimals: 18 },
    blockExplorerUrls: ['https://explorer.devnet.zama.ai']
  }]
});
```

---

## 💻 Frontend Integration

### Dependencies

```bash
npm install fhevmjs ethers
```

### Initialize FHE

```javascript
import { createInstance } from "fhevmjs";

const fheInstance = await createInstance({
  chainId: 8009,
  publicKey: await getPublicKey()
});
```

### Encrypt Input

```javascript
const amount = 5;
const encrypted = fheInstance.encrypt32(amount);

await contract.useCredits(
  encrypted.handles[0],
  encrypted.inputProof
);
```

### Decrypt Balance

```javascript
// Request decryption
await contract.requestBalanceDecryption();

// Listen for result
contract.on("CreditsDecrypted", (user, balance) => {
  console.log(`Balance: ${balance} credits`);
});
```

---

## 📊 Cost Analysis

### Gas Costs (Zama Devnet)

| Operation | Gas | Est. Cost | FHE Fee | Total |
|-----------|-----|-----------|---------|-------|
| Deploy | 2.5M | $0.05 | - | $0.05 |
| Daily Check-in | 150k | $0.003 | $0.01-0.1 | $0.05 |
| Buy Credits | 180k | $0.004 | $0.01-0.1 | $0.10 |
| Use Credits | 220k | $0.005 | $0.03-0.3 | $0.15 |
| Decrypt Balance | 120k | $0.002 | $0.01-0.1 | $0.08 |

*Testnet estimates. Mainnet may vary.*

### FHE Coprocessor Fees (Mainnet, 2025)

- **ZKPoK verification**: $0.016 to $0.0002 per bit
- **Bridging**: $0.016 to $0.0002 per bit
- **Decryption**: $0.0016 to $0.00002 per bit

**Example (64-bit balance):**
- ZKPoK: 64 × $0.016 = $1.02 (max)
- Decryption: 64 × 3 × $0.0016 = $0.31 (max)
- **Total**: ~$1.30 per transaction (max)

For large users with volume discounts: **~$0.01 per transaction**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  User Wallet (MetaMask)             │
│  - Encrypt inputs with fhevmjs      │
│  - Sign transactions                │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  AIResearchCredits.sol (On-chain)   │
│  ┌────────────────────────────────┐ │
│  │  Encrypted State (euint32)     │ │
│  │  - User balances               │ │
│  │  - Operations (add/sub/gte)    │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Public State                  │ │
│  │  - Last check-in timestamps    │ │
│  │  - Constants                   │ │
│  └────────────────────────────────┘ │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Zama FHE Coprocessor               │
│  - Compute on encrypted data        │
│  - Gateway for decryption (MPC)     │
│  - ZK proofs verification           │
└─────────────────────────────────────┘
```

---

## 🔬 Technology Stack

### Blockchain
- **Solidity**: 0.8.24
- **Hardhat**: 2.22.0
- **Network**: Zama Devnet (EVM compatible)

### Cryptography
- **TFHE**: Fully Homomorphic Encryption
- **MPC**: Multi-Party Computation (key management)
- **ZK Proofs**: Input verification

### Frontend
- **fhevmjs**: FHE encryption library
- **ethers.js**: Web3 interactions
- **React**: UI framework

### Testing
- **Hardhat Test**: Unit tests
- **Chai**: Assertions
- **Network Helpers**: Time manipulation

---

## 📈 Use Cases

### 1. AI Research App

```javascript
// User workflow
1. Connect wallet → MetaMask
2. Daily check-in → +10 credits
3. Run AI query → -1 credit (encrypted)
4. Need more? → Buy with ETH
5. View balance → Decrypt via Gateway
```

### 2. Pay-per-Query Model

- **Free tier**: 10 credits/day (check-in)
- **Paid tier**: Buy credits as needed
- **Privacy**: Balance hidden from others
- **Compliance**: On-chain audit trail

### 3. Token Economy

- **Credit = Usage Right**: 1 credit = 1 AI query
- **Monetization**: 0.01 ETH per credit
- **Daily Engagement**: Check-in rewards
- **Scalability**: FHE operations on L1/L2

---

## 🛣️ Roadmap

### Phase 1: Testnet (Current) ✅
- ✅ Smart contract development
- ✅ FHE integration
- ✅ Testing & deployment
- ✅ Documentation

### Phase 2: Mainnet Prep (Q4 2025)
- [ ] Security audit
- [ ] Frontend integration
- [ ] User testing
- [ ] Performance optimization

### Phase 3: Mainnet Launch (End 2025)
- [ ] Ethereum deployment
- [ ] $ZAMA token integration
- [ ] Multi-chain support
- [ ] Production monitoring

### Phase 4: Expansion (2026)
- [ ] Solana support
- [ ] Credit transfer feature
- [ ] Subscription model
- [ ] DAO governance

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Main documentation |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment |
| `FRONTEND_INTEGRATION.md` | React integration guide |
| `SUMMARY.md` | Project overview (this file) |

### External Resources

- **Zama Protocol**: https://docs.zama.ai/protocol
- **FHEVM Whitepaper**: https://github.com/zama-ai/fhevm
- **Solidity Guides**: https://docs.zama.ai/protocol/solidity-guides
- **Examples**: https://docs.zama.ai/protocol/examples

---

## 🎓 Learning Resources

### Understanding FHE

1. **What is FHE?**
   - Encrypt data → Compute → Decrypt result
   - No intermediate decryption needed
   - Post-quantum secure

2. **Why Zama?**
   - 100x faster than 5 years ago
   - Developer-friendly (Solidity)
   - Production-ready

3. **Use Cases:**
   - Confidential DeFi
   - Private voting
   - Encrypted AI
   - Compliance + Privacy

### Code Examples

**Encrypted Addition:**
```solidity
euint32 a = TFHE.asEuint32(10);
euint32 b = TFHE.asEuint32(20);
euint32 result = TFHE.add(a, b); // = 30 (encrypted)
```

**Encrypted Comparison:**
```solidity
euint32 balance = encryptedCredits[user];
euint32 cost = TFHE.asEuint32(5);
ebool canAfford = TFHE.gte(balance, cost); // true/false (encrypted)
```

**Conditional Logic:**
```solidity
euint32 newBalance = TFHE.select(
  canAfford,
  TFHE.sub(balance, cost), // If true
  balance                  // If false
);
```

---

## 🔐 Security Considerations

### ✅ Strengths

- **End-to-End Encryption**: Balances never exposed
- **No Trusted Third Party**: MPC for key management
- **Post-Quantum**: FHE resistant to quantum attacks
- **Publicly Verifiable**: All operations on-chain
- **Access Control**: Only user can decrypt own data

### ⚠️ Limitations

- **Gas Costs**: FHE operations more expensive than plaintext
- **Latency**: Decryption via Gateway (async)
- **Complexity**: Requires fhevmjs for encryption
- **Testnet Only**: Not audited for production

### 🛡️ Best Practices

1. ✅ Always encrypt sensitive inputs
2. ✅ Validate decryption requests
3. ✅ Use access control (TFHE.allow)
4. ✅ Test thoroughly on testnet
5. ❌ Never expose private keys
6. ❌ Don't trust client-side validation only

---

## 📞 Support & Community

### Get Help

- **GitHub Issues**: https://github.com/ntclick/ai-research-roma/issues
- **Twitter**: https://x.com/trungkts29
- **Zama Discord**: https://discord.gg/zama

### Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

---

## 📄 License

**MIT License**

```
Copyright (c) 2025 @trungkts29

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **Zama Team**: Revolutionary FHE technology
- **FHEVM**: Confidential smart contract framework
- **Community**: Testers and contributors
- **Supporters**: Everyone using AI Research app

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Lines of Code | ~800 (Solidity + JS) |
| Test Cases | 18 (all passing) |
| Documentation | 4 comprehensive guides |
| Dependencies | 6 npm packages |
| Security | FHE + MPC + ZK |
| License | MIT (open source) |
| Author | @trungkts29 |

---

## 🎯 Next Steps

### For Developers

1. ✅ Clone repository
2. ✅ Read DEPLOYMENT_GUIDE.md
3. ✅ Deploy to Zama Devnet
4. ✅ Integrate with frontend (FRONTEND_INTEGRATION.md)
5. ✅ Test thoroughly
6. ⏳ Wait for mainnet (Q4 2025)

### For Users

1. ✅ Connect to Zama Devnet
2. ✅ Get testnet tokens
3. ✅ Check in daily (+10 credits)
4. ✅ Try AI research queries
5. ✅ Buy credits if needed
6. ✅ Provide feedback

---

**🚀 Built with ❤️ using Zama FHE**

**🔗 Live Demo**: https://airesearch-tools.vercel.app  
**📦 GitHub**: https://github.com/ntclick/ai-research-roma  
**🐦 Twitter**: https://x.com/trungkts29

---

**Last Updated**: October 6, 2025  
**Version**: 1.0.0  
**Status**: ✅ **Testnet Ready**

