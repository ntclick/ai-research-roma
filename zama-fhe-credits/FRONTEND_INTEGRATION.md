# 🌐 Frontend Integration Guide

Integration của AIResearchCredits contract với React/Next.js frontend

---

## 📦 Installation

```bash
npm install fhevmjs ethers
```

---

## 🔧 Setup FHE Instance

### 1. Create FHE Context

```javascript
// contexts/FHEContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { createInstance } from 'fhevmjs';
import { BrowserProvider } from 'ethers';

const FHEContext = createContext();

export function FHEProvider({ children }) {
  const [fheInstance, setFheInstance] = useState(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    initFHE();
  }, []);

  async function initFHE() {
    try {
      const provider = new BrowserProvider(window.ethereum);
      const network = await provider.getNetwork();
      
      // Get public key from Gateway
      const publicKey = await provider.call({
        to: "0xc8c9303Cd7F337fab769686B593B87DC3403E0ce", // Gateway address
        data: "0xd83554f4" // getPublicKey() selector
      });
      
      const instance = await createInstance({
        chainId: Number(network.chainId),
        publicKey: publicKey
      });
      
      setFheInstance(instance);
      setIsReady(true);
      console.log("✅ FHE Instance initialized");
    } catch (error) {
      console.error("❌ FHE init error:", error);
    }
  }

  return (
    <FHEContext.Provider value={{ fheInstance, isReady }}>
      {children}
    </FHEContext.Provider>
  );
}

export function useFHE() {
  return useContext(FHEContext);
}
```

---

## 💰 Credit Management Hook

### 2. Create useCredits Hook

```javascript
// hooks/useCredits.js
import { useState, useEffect } from 'react';
import { BrowserProvider, Contract, formatEther, parseEther } from 'ethers';
import { useFHE } from '../contexts/FHEContext';

const CONTRACT_ADDRESS = "0x..."; // Your deployed contract
const ABI = [...]; // Contract ABI

export function useCredits() {
  const { fheInstance, isReady } = useFHE();
  const [contract, setContract] = useState(null);
  const [balance, setBalance] = useState(null);
  const [canCheckIn, setCanCheckIn] = useState(false);
  const [timeUntilCheckIn, setTimeUntilCheckIn] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isReady) {
      initContract();
      loadData();
    }
  }, [isReady]);

  async function initContract() {
    const provider = new BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    const c = new Contract(CONTRACT_ADDRESS, ABI, signer);
    setContract(c);
  }

  async function loadData() {
    if (!contract) return;
    
    try {
      const [canCheck, timeLeft] = await Promise.all([
        contract.canCheckInToday(),
        contract.timeUntilNextCheckIn()
      ]);
      
      setCanCheckIn(canCheck);
      setTimeUntilCheckIn(Number(timeLeft));
      
      // Request balance decryption
      await requestBalance();
    } catch (error) {
      console.error("Load data error:", error);
    }
  }

  // Daily Check-in
  async function dailyCheckIn() {
    if (!contract) return;
    
    setIsLoading(true);
    try {
      const tx = await contract.dailyCheckIn();
      await tx.wait();
      
      console.log("✅ Checked in! +10 credits");
      await loadData();
      return true;
    } catch (error) {
      console.error("❌ Check-in error:", error);
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  // Buy Credits
  async function buyCredits(amount) {
    if (!contract) return;
    
    setIsLoading(true);
    try {
      const cost = parseEther((amount * 0.01).toString());
      const tx = await contract.buyCredits(amount, { value: cost });
      await tx.wait();
      
      console.log(`✅ Bought ${amount} credits for ${formatEther(cost)} ETH`);
      await loadData();
      return true;
    } catch (error) {
      console.error("❌ Buy credits error:", error);
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  // Use Credits (Encrypted)
  async function useCredits(amount) {
    if (!contract || !fheInstance) return;
    
    setIsLoading(true);
    try {
      // Encrypt amount
      const encrypted = fheInstance.encrypt32(amount);
      
      const tx = await contract.useCredits(
        encrypted.handles[0],
        encrypted.inputProof
      );
      await tx.wait();
      
      console.log(`✅ Used ${amount} credits (encrypted)`);
      await loadData();
      return true;
    } catch (error) {
      console.error("❌ Use credits error:", error);
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  // Request Balance Decryption
  async function requestBalance() {
    if (!contract) return;
    
    try {
      const tx = await contract.requestBalanceDecryption();
      await tx.wait();
      
      // Listen for decryption result
      contract.once("CreditsDecrypted", (user, decryptedBalance) => {
        setBalance(Number(decryptedBalance));
        console.log("💰 Balance decrypted:", decryptedBalance);
      });
    } catch (error) {
      console.error("❌ Request balance error:", error);
    }
  }

  return {
    balance,
    canCheckIn,
    timeUntilCheckIn,
    isLoading,
    dailyCheckIn,
    buyCredits,
    useCredits,
    requestBalance,
    refresh: loadData
  };
}
```

---

## 🎨 UI Components

### 3. Credits Display Component

```jsx
// components/CreditsDisplay.jsx
import { useCredits } from '../hooks/useCredits';

export default function CreditsDisplay() {
  const { balance, isLoading, requestBalance } = useCredits();

  return (
    <div className="credits-display">
      <h3>Your Credits</h3>
      
      {balance !== null ? (
        <div className="balance">
          <span className="amount">{balance}</span>
          <span className="label">credits</span>
        </div>
      ) : (
        <button onClick={requestBalance} disabled={isLoading}>
          {isLoading ? "Decrypting..." : "Show Balance"}
        </button>
      )}
      
      <p className="info">
        🔒 Your balance is encrypted on-chain
      </p>
    </div>
  );
}
```

### 4. Daily Check-in Component

```jsx
// components/DailyCheckIn.jsx
import { useCredits } from '../hooks/useCredits';
import { useState, useEffect } from 'react';

export default function DailyCheckIn() {
  const { canCheckIn, timeUntilCheckIn, dailyCheckIn, isLoading } = useCredits();
  const [countdown, setCountdown] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      const hours = Math.floor(timeUntilCheckIn / 3600);
      const minutes = Math.floor((timeUntilCheckIn % 3600) / 60);
      const seconds = timeUntilCheckIn % 60;
      
      setCountdown(`${hours}h ${minutes}m ${seconds}s`);
    }, 1000);
    
    return () => clearInterval(interval);
  }, [timeUntilCheckIn]);

  return (
    <div className="check-in">
      <h3>📅 Daily Check-in</h3>
      
      {canCheckIn ? (
        <button 
          onClick={dailyCheckIn}
          disabled={isLoading}
          className="btn-primary"
        >
          {isLoading ? "Processing..." : "Check In (+10 Credits)"}
        </button>
      ) : (
        <div className="cooldown">
          <p>Next check-in in:</p>
          <div className="countdown">{countdown}</div>
        </div>
      )}
    </div>
  );
}
```

### 5. Buy Credits Component

```jsx
// components/BuyCredits.jsx
import { useState } from 'react';
import { useCredits } from '../hooks/useCredits';

export default function BuyCredits() {
  const { buyCredits, isLoading } = useCredits();
  const [amount, setAmount] = useState(10);

  const packages = [
    { credits: 10, price: 0.1, popular: false },
    { credits: 50, price: 0.5, popular: true },
    { credits: 100, price: 1.0, popular: false },
  ];

  async function handleBuy(credits) {
    const success = await buyCredits(credits);
    if (success) {
      alert(`✅ Successfully bought ${credits} credits!`);
    }
  }

  return (
    <div className="buy-credits">
      <h3>💳 Buy Credits</h3>
      
      <div className="packages">
        {packages.map(pkg => (
          <div 
            key={pkg.credits} 
            className={`package ${pkg.popular ? 'popular' : ''}`}
          >
            {pkg.popular && <span className="badge">BEST VALUE</span>}
            
            <div className="amount">{pkg.credits}</div>
            <div className="label">credits</div>
            <div className="price">{pkg.price} ETH</div>
            
            <button 
              onClick={() => handleBuy(pkg.credits)}
              disabled={isLoading}
            >
              {isLoading ? "Processing..." : "Buy Now"}
            </button>
          </div>
        ))}
      </div>
      
      <p className="rate">💡 Rate: 0.01 ETH per credit</p>
    </div>
  );
}
```

---

## 🔗 Integration with AI Research App

### 6. Protect AI Queries with Credits

```javascript
// In your ResearchChat component
import { useCredits } from '../hooks/useCredits';

function ResearchChat() {
  const { balance, useCredits, isLoading } = useCredits();
  const [query, setQuery] = useState('');

  async function handleResearch() {
    // Check balance
    if (balance === null) {
      alert("Please decrypt your balance first");
      return;
    }
    
    if (balance < 1) {
      alert("Insufficient credits! Please buy more or check in daily.");
      return;
    }
    
    // Deduct 1 credit (encrypted)
    const success = await useCredits(1);
    if (!success) {
      alert("Failed to use credit");
      return;
    }
    
    // Run AI research
    await runAIResearch(query);
  }

  return (
    <div>
      <input 
        value={query} 
        onChange={e => setQuery(e.target.value)}
        placeholder="Ask anything..."
      />
      
      <button onClick={handleResearch} disabled={isLoading}>
        {isLoading ? "Processing..." : "Research (1 credit)"}
      </button>
      
      <p>Balance: {balance !== null ? `${balance} credits` : "Hidden"}</p>
    </div>
  );
}
```

---

## 📱 Complete App Structure

```jsx
// App.jsx
import { FHEProvider } from './contexts/FHEContext';
import CreditsDisplay from './components/CreditsDisplay';
import DailyCheckIn from './components/DailyCheckIn';
import BuyCredits from './components/BuyCredits';
import ResearchChat from './components/ResearchChat';

export default function App() {
  return (
    <FHEProvider>
      <div className="app">
        <header>
          <h1>🔐 AI Research with Zama FHE</h1>
        </header>
        
        <main>
          <aside className="sidebar">
            <CreditsDisplay />
            <DailyCheckIn />
            <BuyCredits />
          </aside>
          
          <section className="content">
            <ResearchChat />
          </section>
        </main>
      </div>
    </FHEProvider>
  );
}
```

---

## 🎯 Usage Flow

```
1. User connects wallet (MetaMask)
   ↓
2. FHE instance initializes
   ↓
3. User checks in daily (+10 credits)
   ↓
4. Balance encrypted on-chain
   ↓
5. User requests decryption to view balance
   ↓
6. User runs AI query → Deduct 1 credit (encrypted)
   ↓
7. Balance updated (still encrypted)
   ↓
8. User can buy more credits with ETH
```

---

## 🔒 Security Notes

- Balances are **encrypted end-to-end** (euint32)
- Only user can decrypt their own balance
- All operations happen on encrypted data
- No plaintext balances stored on-chain
- Gateway provides secure decryption via MPC

---

## 📊 Cost Estimation

| Action | Gas Cost | FHE Fee | Total |
|--------|----------|---------|-------|
| Daily Check-in | ~50k gas | $0.01-0.1 | ~$0.05 |
| Buy Credits | ~80k gas | $0.01-0.1 | ~$0.10 |
| Use Credits | ~120k gas | $0.03-0.3 | ~$0.15 |
| Decrypt Balance | ~100k gas | $0.01-0.1 | ~$0.08 |

*Estimates for Zama Devnet. Mainnet costs may vary.*

---

## ✅ Testing Checklist

- [ ] FHE instance initializes correctly
- [ ] Daily check-in works (24h cooldown)
- [ ] Buy credits with ETH
- [ ] Use credits (encrypted deduction)
- [ ] Balance decryption via Gateway
- [ ] Countdown timer displays correctly
- [ ] Error handling (insufficient balance, etc.)
- [ ] MetaMask connection

---

**🎉 Integration complete! Your AI Research app now has encrypted credit management with Zama FHE!**

