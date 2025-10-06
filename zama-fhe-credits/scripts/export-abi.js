const fs = require('fs');
const path = require('path');

console.log("📦 Exporting ABI for frontend...\n");

const artifactPath = path.join(
  __dirname, 
  '../artifacts/contracts/AIResearchCredits.sol/AIResearchCredits.json'
);

if (!fs.existsSync(artifactPath)) {
  console.error("❌ Artifact not found. Run 'npm run compile' first.");
  process.exit(1);
}

const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));

const exportData = {
  contractName: "AIResearchCredits",
  abi: artifact.abi,
  bytecode: artifact.bytecode,
  compiler: {
    version: artifact.compiler.version,
    runs: artifact.compiler.runs
  },
  networks: {
    "zama-devnet": {
      chainId: 8009,
      rpcUrl: "https://devnet.zama.ai",
      explorer: "https://explorer.devnet.zama.ai",
      address: "PASTE_DEPLOYED_ADDRESS_HERE"
    }
  },
  constants: {
    DAILY_CHECKIN_REWARD: 10,
    CREDIT_PRICE: "0.01",
    CHECKIN_COOLDOWN: 86400
  }
};

const outputPath = path.join(__dirname, '../abi.json');
fs.writeFileSync(outputPath, JSON.stringify(exportData, null, 2));

console.log("✅ ABI exported successfully!");
console.log("📍 Output:", outputPath);
console.log("\n📋 Contents:");
console.log(`   - ABI: ${artifact.abi.length} functions`);
console.log(`   - Bytecode: ${artifact.bytecode.length} bytes`);
console.log("\n📝 Next steps:");
console.log("   1. Copy abi.json to frontend/src/contracts/");
console.log("   2. Update 'address' field after deployment");
console.log("   3. Import in frontend:\n");
console.log("      import CONTRACT from './contracts/abi.json';");
console.log("      const contract = new Contract(CONTRACT.networks['zama-devnet'].address, CONTRACT.abi, signer);");
console.log("\n✨ Done!\n");

