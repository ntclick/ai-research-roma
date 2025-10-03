export const PRODUCTION_CONFIG = {
    ROMA_API_URL: 'https://your-roma-backend.com',
    WEBSOCKET_URL: 'wss://your-roma-backend.com',
    GM_TOKEN_CONTRACT: '0x...', // Production contract address
    SEPOLIA_RPC_URL: 'https://sepolia.infura.io/v3/your-key',
};

export const DEVELOPMENT_CONFIG = {
    ROMA_API_URL: 'http://localhost:5001',
    WEBSOCKET_URL: 'ws://localhost:5001',
    GM_TOKEN_CONTRACT: process.env.REACT_APP_GM_TOKEN_CONTRACT,
    SEPOLIA_RPC_URL: process.env.REACT_APP_SEPOLIA_RPC_URL,
};

export const getConfig = () => {
    return process.env.NODE_ENV === 'production' 
        ? PRODUCTION_CONFIG 
        : DEVELOPMENT_CONFIG;
};

