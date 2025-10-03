import { ethers } from 'ethers';

const GM_TOKEN_ABI = [
    "function purchaseTokens() external payable",
    "function dailyCheckIn() external",
    "function getResearchCredits(address user) external view returns (uint256)",
    "function balanceOf(address account) external view returns (uint256)",
    "function lastCheckIn(address user) external view returns (uint256)",
    "event TokensPurchased(address buyer, uint256 amount, uint256 ethPaid)",
    "event DailyCheckIn(address user, uint256 amount)"
];

export class GMTokenService {
    constructor(contractAddress, signer) {
        this.contract = new ethers.Contract(contractAddress, GM_TOKEN_ABI, signer);
        this.signer = signer;
        this.contractAddress = contractAddress;
    }

    async purchaseTokens(ethAmount) {
        try {
            const tx = await this.contract.purchaseTokens({
                value: ethers.parseEther(ethAmount.toString())
            });
            
            const receipt = await tx.wait();
            return receipt;
        } catch (error) {
            console.error('Purchase tokens failed:', error);
            throw error;
        }
    }

    async dailyCheckIn() {
        try {
            const tx = await this.contract.dailyCheckIn();
            const receipt = await tx.wait();
            return receipt;
        } catch (error) {
            console.error('Daily check-in failed:', error);
            throw error;
        }
    }

    async getResearchCredits(userAddress) {
        try {
            const credits = await this.contract.getResearchCredits(userAddress);
            return ethers.formatEther(credits);
        } catch (error) {
            console.error('Failed to get research credits:', error);
            return '0';
        }
    }

    async getTokenBalance(userAddress) {
        try {
            const balance = await this.contract.balanceOf(userAddress);
            return ethers.formatEther(balance);
        } catch (error) {
            console.error('Failed to get token balance:', error);
            return '0';
        }
    }

    async getLastCheckIn(userAddress) {
        try {
            const timestamp = await this.contract.lastCheckIn(userAddress);
            return Number(timestamp);
        } catch (error) {
            console.error('Failed to get last check-in:', error);
            return 0;
        }
    }

    async canCheckIn(userAddress) {
        try {
            const lastCheckInTime = await this.getLastCheckIn(userAddress);
            if (lastCheckInTime === 0) return true;
            
            const currentTime = Math.floor(Date.now() / 1000);
            const oneDayInSeconds = 24 * 60 * 60;
            
            return currentTime >= (lastCheckInTime + oneDayInSeconds);
        } catch (error) {
            console.error('Failed to check if can check in:', error);
            return false;
        }
    }
}

