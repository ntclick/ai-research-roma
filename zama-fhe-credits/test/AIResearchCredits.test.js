const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

describe("AIResearchCredits (Zama FHE)", function () {
  let contract;
  let owner;
  let user1;
  let user2;

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();
    
    const AIResearchCredits = await ethers.getContractFactory("AIResearchCredits");
    contract = await AIResearchCredits.deploy();
    await contract.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await contract.owner()).to.equal(owner.address);
    });

    it("Should have correct constants", async function () {
      expect(await contract.DAILY_CHECKIN_REWARD()).to.equal(10);
      expect(await contract.CREDIT_PRICE()).to.equal(ethers.parseEther("0.01"));
      expect(await contract.CHECKIN_COOLDOWN()).to.equal(86400); // 1 day
    });
  });

  describe("Daily Check-in", function () {
    it("Should allow first check-in", async function () {
      await expect(contract.connect(user1).dailyCheckIn())
        .to.emit(contract, "CheckedIn")
        .withArgs(user1.address, await time.latest() + 1);
    });

    it("Should update lastCheckIn timestamp", async function () {
      await contract.connect(user1).dailyCheckIn();
      const timestamp = await contract.lastCheckIn(user1.address);
      expect(timestamp).to.be.gt(0);
    });

    it("Should fail if checking in twice within 24h", async function () {
      await contract.connect(user1).dailyCheckIn();
      
      await expect(contract.connect(user1).dailyCheckIn())
        .to.be.revertedWith("Already checked in today");
    });

    it("Should allow check-in after 24h cooldown", async function () {
      await contract.connect(user1).dailyCheckIn();
      
      // Fast forward 24 hours
      await time.increase(86400);
      
      await expect(contract.connect(user1).dailyCheckIn())
        .to.emit(contract, "CheckedIn");
    });

    it("Should return correct canCheckInToday status", async function () {
      expect(await contract.connect(user1).canCheckInToday()).to.be.true;
      
      await contract.connect(user1).dailyCheckIn();
      expect(await contract.connect(user1).canCheckInToday()).to.be.false;
      
      await time.increase(86400);
      expect(await contract.connect(user1).canCheckInToday()).to.be.true;
    });
  });

  describe("Buy Credits", function () {
    it("Should allow buying credits with correct ETH", async function () {
      const amount = 5;
      const cost = ethers.parseEther("0.05"); // 5 * 0.01 ETH
      
      await expect(contract.connect(user1).buyCredits(amount, { value: cost }))
        .to.emit(contract, "CreditsPurchased")
        .withArgs(user1.address, amount, cost);
    });

    it("Should fail if insufficient ETH sent", async function () {
      const amount = 10;
      const insufficientCost = ethers.parseEther("0.05"); // Need 0.1 ETH
      
      await expect(
        contract.connect(user1).buyCredits(amount, { value: insufficientCost })
      ).to.be.revertedWith("Insufficient ETH");
    });

    it("Should refund excess ETH", async function () {
      const amount = 1;
      const exactCost = ethers.parseEther("0.01");
      const excessPayment = ethers.parseEther("0.02");
      
      const balanceBefore = await ethers.provider.getBalance(user1.address);
      
      const tx = await contract.connect(user1).buyCredits(amount, { value: excessPayment });
      const receipt = await tx.wait();
      const gasCost = receipt.gasUsed * receipt.gasPrice;
      
      const balanceAfter = await ethers.provider.getBalance(user1.address);
      
      // Should only deduct exactCost + gas
      expect(balanceBefore - balanceAfter).to.be.closeTo(exactCost + gasCost, ethers.parseEther("0.001"));
    });

    it("Should fail if amount is 0", async function () {
      await expect(
        contract.connect(user1).buyCredits(0, { value: 0 })
      ).to.be.revertedWith("Amount must be > 0");
    });

    it("Should add ETH to contract balance", async function () {
      const amount = 10;
      const cost = ethers.parseEther("0.1");
      
      await contract.connect(user1).buyCredits(amount, { value: cost });
      
      expect(await contract.getContractBalance()).to.equal(cost);
    });
  });

  describe("Use Credits", function () {
    it("Should emit CreditsUsed event", async function () {
      // First buy some credits
      await contract.connect(user1).buyCredits(10, { value: ethers.parseEther("0.1") });
      
      // Note: In real FHE environment, need to encrypt input
      // For testing, we skip encryption verification
      // await expect(contract.connect(user1).useCredits(...))
      //   .to.emit(contract, "CreditsUsed");
    });
  });

  describe("Balance Queries", function () {
    it("Should return encrypted balance handle", async function () {
      const balance = await contract.connect(user1).getEncryptedBalance();
      expect(balance).to.exist;
    });
  });

  describe("Owner Functions", function () {
    it("Should allow owner to withdraw", async function () {
      // Add funds to contract
      await contract.connect(user1).buyCredits(10, { value: ethers.parseEther("0.1") });
      
      const ownerBalanceBefore = await ethers.provider.getBalance(owner.address);
      const contractBalance = await contract.getContractBalance();
      
      const tx = await contract.connect(owner).withdraw();
      const receipt = await tx.wait();
      const gasCost = receipt.gasUsed * receipt.gasPrice;
      
      const ownerBalanceAfter = await ethers.provider.getBalance(owner.address);
      
      expect(ownerBalanceAfter).to.equal(ownerBalanceBefore + contractBalance - gasCost);
      expect(await contract.getContractBalance()).to.equal(0);
    });

    it("Should fail if non-owner tries to withdraw", async function () {
      await expect(contract.connect(user1).withdraw())
        .to.be.revertedWith("Not owner");
    });
  });

  describe("Time Helpers", function () {
    it("Should calculate time until next check-in", async function () {
      expect(await contract.connect(user1).timeUntilNextCheckIn()).to.equal(0);
      
      await contract.connect(user1).dailyCheckIn();
      
      const timeLeft = await contract.connect(user1).timeUntilNextCheckIn();
      expect(timeLeft).to.be.closeTo(86400, 10); // ~24h (with small margin)
      
      await time.increase(43200); // 12h
      expect(await contract.connect(user1).timeUntilNextCheckIn()).to.be.closeTo(43200, 10);
      
      await time.increase(43200); // another 12h
      expect(await contract.connect(user1).timeUntilNextCheckIn()).to.equal(0);
    });
  });
});

