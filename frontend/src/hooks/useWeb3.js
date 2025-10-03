import { useState, useEffect } from 'react';
// import { ethers } from 'ethers';
// import detectEthereumProvider from '@metamask/detect-provider';

// DISABLED: MetaMask integration not needed for current version
export const useWeb3 = () => {
    const [account, setAccount] = useState(null);
    const [provider, setProvider] = useState(null);
    const [signer, setSigner] = useState(null);
    const [chainId, setChainId] = useState(null);
    const [isConnecting, setIsConnecting] = useState(false);

    useEffect(() => {
        // Disabled MetaMask auto-connect to prevent errors
        const init = async () => {
            /* DISABLED
            const ethereumProvider = await detectEthereumProvider();
            
            if (ethereumProvider && ethereumProvider.isMetaMask) {
                const ethersProvider = new ethers.BrowserProvider(ethereumProvider);
                setProvider(ethersProvider);
                
                // Check if already connected
                const accounts = await ethereumProvider.request({ 
                    method: 'eth_accounts' 
                });
                
                if (accounts.length > 0) {
                    setAccount(accounts[0]);
                    setSigner(await ethersProvider.getSigner());
                }
                
                const network = await ethersProvider.getNetwork();
                setChainId(network.chainId);
                
                // Listen for account changes
                ethereumProvider.on('accountsChanged', async (accounts) => {
                    if (accounts.length > 0) {
                        setAccount(accounts[0]);
                        setSigner(await ethersProvider.getSigner());
                    } else {
                        setAccount(null);
                        setSigner(null);
                    }
                });
                
                ethereumProvider.on('chainChanged', (chainId) => {
                    setChainId(parseInt(chainId, 16));
                    window.location.reload();
                });
            }
            */
        };
        
        // init(); // Disabled MetaMask initialization
    }, []);

    const connectWallet = async () => {
        // DISABLED: MetaMask not needed for current version
        alert('MetaMask integration coming soon! Currently, you can use AI Research Chat without wallet connection.');
        return;
        
        /* DISABLED
        if (!provider) {
            alert('Please install MetaMask!');
            return;
        }
        
        setIsConnecting(true);
        try {
            const accounts = await window.ethereum.request({
                method: 'eth_requestAccounts',
            });
            
            setAccount(accounts[0]);
            setSigner(await provider.getSigner());
            
            // Switch to Sepolia if not already
            await switchToSepolia();
        } catch (error) {
            console.error('Failed to connect wallet:', error);
        } finally {
            setIsConnecting(false);
        }
        */
    };

    const switchToSepolia = async () => {
        try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0xaa36a7' }], // Sepolia chain ID
            });
        } catch (error) {
            // This error code indicates that the chain has not been added to MetaMask
            if (error.code === 4902) {
                try {
                    await window.ethereum.request({
                        method: 'wallet_addEthereumChain',
                        params: [{
                            chainId: '0xaa36a7',
                            chainName: 'Sepolia Test Network',
                            nativeCurrency: {
                                name: 'ETH',
                                symbol: 'ETH',
                                decimals: 18
                            },
                            rpcUrls: ['https://sepolia.infura.io/v3/'],
                            blockExplorerUrls: ['https://sepolia.etherscan.io']
                        }]
                    });
                } catch (addError) {
                    console.error('Failed to add Sepolia network:', addError);
                }
            } else {
                console.error('Failed to switch to Sepolia:', error);
            }
        }
    };

    const disconnectWallet = () => {
        setAccount(null);
        setSigner(null);
    };

    return {
        account,
        provider,
        signer,
        chainId,
        isConnecting,
        connectWallet,
        disconnectWallet,
        switchToSepolia
    };
};

