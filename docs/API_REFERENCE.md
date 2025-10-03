# API Reference

## Smart Contract API

### GMToken.sol

#### Functions

**purchaseTokens()**
```solidity
function purchaseTokens() external payable
```
Mua GM tokens với ETH.
- Rate: 1 GM = 0.001 ETH
- Tự động mint tokens và cộng research credits

**dailyCheckIn()**
```solidity
function dailyCheckIn() external
```
Check-in hàng ngày nhận 50 GM.
- Chỉ 1 lần/24 giờ
- Tự động mint 50 GM tokens

**getResearchCredits(address user)**
```solidity
function getResearchCredits(address user) external view returns (uint256)
```
Lấy số research credits của user.

## WebSocket API

### Connection
```
ws://localhost:5001
```

### Message Format

**Request:**
```json
{
  "type": "research_request",
  "tool": "coin-research",
  "content": "BTC",
  "user": "0x...",
  "timestamp": "2025-10-01T..."
}
```

**Response:**
```json
{
  "type": "research_response",
  "tool": "coin-research",
  "content": "Report content...",
  "data": {},
  "sender": "ai"
}
```

### Tools

1. `coin-research`: Nghiên cứu cryptocurrency
2. `price-analysis`: Phân tích giá
3. `x-post-analysis`: Phân tích Twitter post
4. `create-x-post`: Tạo nội dung Twitter
5. `generate-image`: Tạo hình ảnh AI

## CoinGecko API Integration

### Endpoints Used

- `/search?query={symbol}` - Tìm kiếm coin
- `/coins/{id}` - Chi tiết coin

## React Hooks

### useWeb3

```javascript
const {
  account,      // Connected wallet address
  provider,     // ethers.js provider
  signer,       // ethers.js signer
  chainId,      // Current chain ID
  isConnecting, // Connection status
  connectWallet,
  disconnectWallet,
  switchToSepolia
} = useWeb3();
```

## Services

### GMTokenService

```javascript
const service = new GMTokenService(contractAddress, signer);

// Methods
await service.purchaseTokens(ethAmount);
await service.dailyCheckIn();
await service.getResearchCredits(address);
await service.getTokenBalance(address);
await service.canCheckIn(address);
```

