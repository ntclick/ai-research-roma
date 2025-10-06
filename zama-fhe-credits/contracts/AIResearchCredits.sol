// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "fhevm/lib/TFHE.sol";
import "fhevm/config/ZamaFHEVMConfig.sol";
import "fhevm/gateway/GatewayCaller.sol";

/**
 * @title AIResearchCredits
 * @notice Encrypted AI Research Credits System with Daily Check-in
 * @dev Uses Zama FHE for confidential balance tracking
 * @author @trungkts29 (https://x.com/trungkts29)
 */
contract AIResearchCredits is GatewayCaller {
    // Encrypted balances (confidential)
    mapping(address => euint32) private encryptedCredits;
    
    // Last check-in timestamp (public for verification)
    mapping(address => uint256) public lastCheckIn;
    
    // Constants
    uint256 public constant DAILY_CHECKIN_REWARD = 10;
    uint256 public constant CREDIT_PRICE = 0.01 ether; // 0.01 ETH per credit
    uint256 public constant CHECKIN_COOLDOWN = 1 days;
    
    // Owner
    address public owner;
    
    // Events
    event CheckedIn(address indexed user, uint256 timestamp);
    event CreditsPurchased(address indexed user, uint256 amount, uint256 cost);
    event CreditsUsed(address indexed user, uint256 amount);
    event CreditsDecrypted(address indexed user, uint32 balance);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @notice Daily check-in to receive 10 free credits
     * @dev Encrypted addition, cooldown check done in plaintext
     */
    function dailyCheckIn() external {
        require(
            block.timestamp >= lastCheckIn[msg.sender] + CHECKIN_COOLDOWN,
            "Already checked in today"
        );
        
        // Get current balance (encrypted)
        euint32 currentBalance = encryptedCredits[msg.sender];
        
        // Add 10 credits (encrypted operation)
        euint32 reward = TFHE.asEuint32(DAILY_CHECKIN_REWARD);
        encryptedCredits[msg.sender] = TFHE.add(currentBalance, reward);
        
        // Allow user to decrypt their own balance
        TFHE.allowThis(encryptedCredits[msg.sender]);
        TFHE.allow(encryptedCredits[msg.sender], msg.sender);
        
        // Update timestamp
        lastCheckIn[msg.sender] = block.timestamp;
        
        emit CheckedIn(msg.sender, block.timestamp);
    }
    
    /**
     * @notice Buy AI research credits with ETH
     * @param amount Number of credits to purchase
     */
    function buyCredits(uint32 amount) external payable {
        require(amount > 0, "Amount must be > 0");
        
        uint256 cost = amount * CREDIT_PRICE;
        require(msg.value >= cost, "Insufficient ETH");
        
        // Get current balance (encrypted)
        euint32 currentBalance = encryptedCredits[msg.sender];
        
        // Add purchased credits (encrypted)
        euint32 purchaseAmount = TFHE.asEuint32(amount);
        encryptedCredits[msg.sender] = TFHE.add(currentBalance, purchaseAmount);
        
        // Allow user to decrypt their own balance
        TFHE.allowThis(encryptedCredits[msg.sender]);
        TFHE.allow(encryptedCredits[msg.sender], msg.sender);
        
        emit CreditsPurchased(msg.sender, amount, cost);
        
        // Refund excess ETH
        if (msg.value > cost) {
            payable(msg.sender).transfer(msg.value - cost);
        }
    }
    
    /**
     * @notice Use credits for AI research (encrypted deduction)
     * @param encryptedAmount Encrypted amount to use (from frontend)
     */
    function useCredits(einput encryptedAmount, bytes calldata inputProof) external {
        // Decrypt user input
        euint32 amount = TFHE.asEuint32(encryptedAmount, inputProof);
        
        // Get current balance
        euint32 currentBalance = encryptedCredits[msg.sender];
        
        // Check if balance >= amount (encrypted comparison)
        ebool hasEnough = TFHE.gte(currentBalance, amount);
        
        // Conditional subtraction (only if hasEnough == true)
        euint32 newBalance = TFHE.select(
            hasEnough,
            TFHE.sub(currentBalance, amount), // If enough: subtract
            currentBalance                     // If not enough: keep same
        );
        
        encryptedCredits[msg.sender] = newBalance;
        
        // Allow user to decrypt
        TFHE.allowThis(encryptedCredits[msg.sender]);
        TFHE.allow(encryptedCredits[msg.sender], msg.sender);
        
        emit CreditsUsed(msg.sender, 0); // Amount hidden for privacy
    }
    
    /**
     * @notice Get encrypted balance (only user can decrypt)
     * @return Encrypted balance as euint32
     */
    function getEncryptedBalance() external view returns (euint32) {
        return encryptedCredits[msg.sender];
    }
    
    /**
     * @notice Request decryption of balance (via Zama Gateway)
     * @dev This triggers async decryption, result comes via callback
     */
    function requestBalanceDecryption() external {
        uint256[] memory cts = new uint256[](1);
        cts[0] = Gateway.toUint256(encryptedCredits[msg.sender]);
        
        Gateway.requestDecryption(
            cts,
            this.balanceDecryptionCallback.selector,
            0,
            block.timestamp + 100,
            false
        );
    }
    
    /**
     * @notice Callback after decryption (called by Gateway)
     */
    function balanceDecryptionCallback(
        uint256 /*requestId*/,
        uint256[] memory decryptedValues
    ) public onlyGateway {
        uint32 balance = uint32(decryptedValues[0]);
        emit CreditsDecrypted(msg.sender, balance);
    }
    
    /**
     * @notice Check if user can check-in today
     */
    function canCheckInToday() external view returns (bool) {
        return block.timestamp >= lastCheckIn[msg.sender] + CHECKIN_COOLDOWN;
    }
    
    /**
     * @notice Time until next check-in
     */
    function timeUntilNextCheckIn() external view returns (uint256) {
        uint256 nextCheckIn = lastCheckIn[msg.sender] + CHECKIN_COOLDOWN;
        if (block.timestamp >= nextCheckIn) {
            return 0;
        }
        return nextCheckIn - block.timestamp;
    }
    
    /**
     * @notice Owner withdraw ETH
     */
    function withdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
    
    /**
     * @notice Contract balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

