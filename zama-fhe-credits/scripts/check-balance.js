const hre = require("hardhat");

async function main() {
  console.log("💰 Checking Wallet Balance\n");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

  const [signer] = await hre.ethers.getSigners();
  const address = await signer.getAddress();
  const balance = await hre.ethers.provider.getBalance(address);
  
  const network = await hre.ethers.provider.getNetwork();
  
  console.log("📍 Address:", address);
  console.log("🌐 Network:", network.name, `(Chain ID: ${network.chainId})`);
  console.log("💵 Balance:", hre.ethers.formatEther(balance), "ETH");
  console.log();
  
  if (balance === 0n) {
    console.log("⚠️  WARNING: Balance is 0!");
    console.log("🚰 Get testnet tokens from faucet:");
    console.log("   https://faucet.devnet.zama.ai");
    console.log();
  } else if (balance < hre.ethers.parseEther("0.1")) {
    console.log("⚠️  WARNING: Balance is low (< 0.1 ETH)");
    console.log("💡 Consider getting more from faucet for deployment");
    console.log();
  } else {
    console.log("✅ Balance sufficient for deployment");
    console.log();
  }
  
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

