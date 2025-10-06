const hre = require("hardhat");

async function main() {
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("🚀 Deploying AIResearchCredits (Zama FHE)");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

  const [deployer] = await hre.ethers.getSigners();
  
  console.log("📍 Deployer:", deployer.address);
  console.log("💰 Balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)), "ETH\n");

  // Deploy contract
  console.log("⏳ Deploying contract...");
  const AIResearchCredits = await hre.ethers.getContractFactory("AIResearchCredits");
  const contract = await AIResearchCredits.deploy();
  
  await contract.waitForDeployment();
  const address = await contract.getAddress();
  
  console.log("✅ AIResearchCredits deployed to:", address);
  console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("📋 Contract Details:");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("🏷️  Name: AIResearchCredits");
  console.log("📍 Address:", address);
  console.log("👤 Owner:", deployer.address);
  console.log("🎁 Daily Reward: 10 credits");
  console.log("💵 Credit Price: 0.01 ETH");
  console.log("⏰ Check-in Cooldown: 24 hours");
  console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("📝 Next Steps:");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("1. Verify contract on Zama explorer");
  console.log("2. Update frontend with contract address");
  console.log("3. Test daily check-in functionality");
  console.log("4. Test buy credits (0.01 ETH per credit)");
  console.log("\n🔗 Zama Devnet Explorer:");
  console.log(`   https://explorer.devnet.zama.ai/address/${address}`);
  console.log("\n✨ Author: @trungkts29 (https://x.com/trungkts29)\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

