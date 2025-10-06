require("@nomicfoundation/hardhat-toolbox");
require("@fhevm/hardhat-plugin");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  
  networks: {
    // Zama Devnet (Testnet)
    zama: {
      url: "https://devnet.zama.ai",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 8009,
    },
    
    // Local Hardhat node for testing
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 31337,
    },
    
    // Hardhat network (in-memory)
    hardhat: {
      chainId: 31337,
    },
  },
  
  // FHEVM Config
  fhevm: {
    enabled: true,
    networkName: "zama",
    coprocessorEndpoint: "https://gateway.devnet.zama.ai",
  },
  
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
  
  mocha: {
    timeout: 100000,
  },
};

