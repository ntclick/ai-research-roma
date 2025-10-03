# Production Deployment Guide

## Frontend Deployment (Vercel)

### 1. Build Production

```bash
cd frontend
npm run build
```

### 2. Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel --prod
```

### 3. Environment Variables

Thêm trong Vercel dashboard:
- `REACT_APP_GM_TOKEN_CONTRACT`
- `REACT_APP_WEBSOCKET_URL`
- `REACT_APP_SEPOLIA_RPC_URL`

## Backend Deployment

### Option 1: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "websocket_server.py"]
```

Build và run:
```bash
docker build -t crypto-research-backend .
docker run -p 5001:5001 crypto-research-backend
```

### Option 2: Cloud Services

**Heroku:**
```bash
heroku create crypto-research-backend
git push heroku main
```

**AWS/GCP/Azure:**
Deploy như Python WebSocket service thông thường.

## Smart Contract Production

### Deploy to Mainnet

1. Get mainnet ETH
2. Update hardhat.config.js với mainnet RPC
3. Deploy:

```bash
npm run deploy:mainnet
```

### Security Checklist

- [ ] Audit smart contract code
- [ ] Test trên testnet 
- [ ] Verify contract trên Etherscan
- [ ] Setup monitoring
- [ ] Backup private keys

