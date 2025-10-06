# 🔐 AI Research Credits - Zama FHE Smart Contract

**Encrypted credit system for AI research using Zama's Fully Homomorphic Encryption (FHE)**

Built by [@trungkts29](https://x.com/trungkts29)

---

## 🌟 Features

- **🔒 End-to-End Encryption**: Your balance is encrypted on-chain (no one can see it, not even node operators)
- **🎁 Daily Check-in**: Get 10 free credits every 24 hours
- **💰 Buy Credits**: Purchase credits with ETH (0.01 ETH per credit)
- **🔐 Confidential Spending**: Use credits without revealing your balance
- **⚡ Zama FHE Protocol**: State-of-the-art fully homomorphic encryption

---

## 📋 Contract Details

| Feature | Value |
|---------|-------|
| Daily Reward | 10 credits |
| Credit Price | 0.01 ETH |
| Check-in Cooldown | 24 hours |
| Encryption | Zama FHE (euint32) |
| Network | Zama Devnet |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd AI Research deploy/zama-fhe-credits
npm install
```

### 2. Configure Environment

```bash
cp env.template .env
```

Edit `.env`:
```env
PRIVATE_KEY=your_private_key_here
ZAMA_RPC_URL=https://devnet.zama.ai
GATEWAY_URL=https://gateway.devnet.zama.ai
```

### 3. Get Testnet Tokens

Get Zama Devnet tokens from faucet:
- **Faucet**: https://faucet.devnet.zama.ai
- **Explorer**: https://explorer.devnet.zama.ai

### 4. Compile Contract

```bash
npm run compile
```

### 5. Run Tests

```bash
npm test
```

### 6. Deploy to Zama Devnet

```bash
npm run deploy
```

---

## 📖 Usage Examples

### Daily Check-in

```solidity
// Check if can check-in
bool canCheckIn = contract.canCheckInToday();

// Perform check-in (get 10 free credits)
contract.dailyCheckIn();
```

### Buy Credits

```solidity
// Buy 10 credits for 0.1 ETH
uint32 amount = 10;
uint256 cost = 0.1 ether;

contract.buyCredits{value: cost}(amount);
```

### Use Credits (Encrypted)

```javascript
// Frontend (using fhevmjs)
import { createInstance } from "fhevmjs";

const instance = await createInstance({ 
  chainId: 8009,
  publicKey: await getPublicKey() 
});

// Encrypt amount
const encryptedAmount = instance.encrypt32(5);

// Use 5 credits (encrypted)
await contract.useCredits(
  encryptedAmount.handles[0],
  encryptedAmount.inputProof
);
```

### Check Balance (Encrypted)

```solidity
// Get encrypted balance handle
euint32 balance = contract.getEncryptedBalance();

// Request decryption (async via Gateway)
contract.requestBalanceDecryption();

// Listen for decryption result
contract.on("CreditsDecrypted", (user, balance) => {
  console.log(`Balance: ${balance} credits`);
});
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│     User (Frontend)                  │
│  - Encrypt inputs with fhevmjs       │
│  - Submit encrypted transactions     │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   AIResearchCredits.sol (On-chain)   │
│  ┌────────────────────────────────┐  │
│  │ Encrypted State (euint32)      │  │
│  │ - User balances (confidential) │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ Public State                   │  │
│  │ - Last check-in timestamps     │  │
│  └────────────────────────────────┘  │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   Zama FHE Coprocessor               │
│  - Compute on encrypted data         │
│  - Gateway for decryption            │
└──────────────────────────────────────┘
```

---

## 🔐 Security Features

### Zama FHE Technology

- **End-to-End Encryption**: Balances encrypted with `euint32`
- **Encrypted Operations**: `TFHE.add()`, `TFHE.sub()`, `TFHE.gte()`
- **Access Control**: Only user can decrypt their own balance
- **Gateway Decryption**: Secure threshold decryption via MPC

### Smart Contract Security

- **Owner-only Withdrawal**: Only contract owner can withdraw ETH
- **Cooldown Protection**: 24h between check-ins
- **Overflow Protection**: Safe encrypted arithmetic
- **Refund Mechanism**: Excess ETH automatically refunded

---

## 🧪 Testing

Run comprehensive test suite:

```bash
npm test
```

Tests cover:
- ✅ Daily check-in logic
- ✅ Credit purchase (with refunds)
- ✅ Credit usage (encrypted)
- ✅ Balance queries
- ✅ Owner functions
- ✅ Time helpers

---

## 📚 Integration with Frontend

### 1. Install fhevmjs

```bash
npm install fhevmjs
```

### 2. Initialize FHE Instance

```javascript
import { createInstance } from "fhevmjs";

const instance = await createInstance({
  chainId: 8009,
  publicKey: await provider.call({
    to: "0x...", // Gateway address
    data: "0x...", // getPublicKey() selector
  }),
});
```

### 3. Encrypt Inputs

```javascript
const amount = 5;
const encryptedInput = instance.encrypt32(amount);

await contract.useCredits(
  encryptedInput.handles[0],
  encryptedInput.inputProof
);
```

### 4. Decrypt Balance

```javascript
// Request decryption
await contract.requestBalanceDecryption();

// Listen for result
contract.on("CreditsDecrypted", (user, balance) => {
  console.log(`Your balance: ${balance} credits`);
});
```

---

## 📡 Contract Functions

### User Functions

| Function | Description |
|----------|-------------|
| `dailyCheckIn()` | Get 10 free credits (24h cooldown) |
| `buyCredits(uint32)` | Buy credits with ETH |
| `useCredits(einput, bytes)` | Spend encrypted credits |
| `getEncryptedBalance()` | Get encrypted balance handle |
| `requestBalanceDecryption()` | Request async decryption |
| `canCheckInToday()` | Check if can check-in |
| `timeUntilNextCheckIn()` | Seconds until next check-in |

### Owner Functions

| Function | Description |
|----------|-------------|
| `withdraw()` | Withdraw contract ETH |
| `getContractBalance()` | View contract balance |

---

## 🌐 Network Details

### Zama Devnet (Testnet)

| Parameter | Value |
|-----------|-------|
| Chain ID | 8009 |
| RPC URL | https://devnet.zama.ai |
| Gateway | https://gateway.devnet.zama.ai |
| Explorer | https://explorer.devnet.zama.ai |
| Faucet | https://faucet.devnet.zama.ai |

### Mainnet (Q4 2025)

- **Launch**: End of 2025
- **TGE**: $ZAMA token
- **Chains**: Ethereum, Polygon, Arbitrum, Solana (2026)

---

## 📖 Resources

### Zama Documentation

- **Protocol Overview**: https://docs.zama.ai/protocol
- **Solidity Guides**: https://docs.zama.ai/protocol/solidity-guides
- **FHEVM Whitepaper**: https://github.com/zama-ai/fhevm/blob/main/fhevm-whitepaper.pdf
- **Examples**: https://docs.zama.ai/protocol/examples

### Technical Details

- **TFHE-rs**: https://docs.zama.ai/tfhe-rs
- **fhevmjs**: https://docs.zama.ai/fhevmjs
- **Gateway**: https://docs.zama.ai/protocol/protocol/gateway

---

## 🎯 Use Cases

### For AI Research App

```javascript
// User checks in daily
await contract.dailyCheckIn(); // +10 credits

// User runs AI research query
if (await canAffordQuery()) {
  const cost = 1; // 1 credit per query
  const encrypted = instance.encrypt32(cost);
  await contract.useCredits(encrypted.handles[0], encrypted.inputProof);
  
  // Run AI query
  await runAIResearch(userQuery);
}

// User needs more credits
await contract.buyCredits(100, { value: ethers.parseEther("1.0") });
```

---

## 🛠️ Development

### Project Structure

```
zama-fhe-credits/
├── contracts/
│   └── AIResearchCredits.sol    # Main FHE contract
├── scripts/
│   └── deploy.js                # Deployment script
├── test/
│   └── AIResearchCredits.test.js # Test suite
├── hardhat.config.js            # Hardhat + fhevm config
├── package.json                 # Dependencies
└── README.md                    # This file
```

### Dependencies

```json
{
  "fhevm": "^0.5.0",
  "fhevmjs": "^0.5.0",
  "@fhevm/hardhat-plugin": "^0.1.0",
  "hardhat": "^2.22.0"
}
```

---

## 🔮 Future Improvements

- [ ] **Credit Transfer**: Send credits to other users (encrypted)
- [ ] **Subscription Model**: Monthly subscription with unlimited credits
- [ ] **Referral System**: Earn credits for referring users
- [ ] **Credit Expiry**: Credits expire after 30 days
- [ ] **Multi-tier Pricing**: Different rates for different AI models
- [ ] **Governance**: DAO voting for parameter changes

---

## 📝 License

MIT License - see LICENSE file

---

## 👨‍💻 Author

**@trungkts29**
- Twitter/X: https://x.com/trungkts29
- GitHub: https://github.com/ntclick

---

## 🙏 Acknowledgments

- **Zama Team**: For building the best FHE technology
- **FHEVM**: Revolutionary confidential smart contract framework
- **Community**: All testers and contributors

---

## ⚠️ Disclaimer

This is a testnet deployment. Use at your own risk. Zama mainnet launches Q4 2025.

**NOT AUDITED** - Do not use in production without security audit.

---

## 🔗 Links

- **Live Demo**: https://airesearch-tools.vercel.app
- **GitHub**: https://github.com/ntclick/ai-research-roma
- **Zama**: https://zama.ai
- **FHEVM**: https://github.com/zama-ai/fhevm

---

**Built with ❤️ using Zama FHE**

