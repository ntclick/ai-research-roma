import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Input,
    VStack,
    HStack,
    Text,
    Alert,
    AlertIcon,
    useToast,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
    Divider
} from '@chakra-ui/react';
import { useWeb3 } from '../../hooks/useWeb3';
import { GMTokenService } from '../../services/gmTokenService';

const TokenEconomy = () => {
    const [ethAmount, setEthAmount] = useState('0.01');
    const [credits, setCredits] = useState(0);
    const [tokenBalance, setTokenBalance] = useState(0);
    const [canCheckIn, setCanCheckIn] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [lastCheckIn, setLastCheckIn] = useState(null);
    const [timeUntilCheckIn, setTimeUntilCheckIn] = useState('');
    
    const { account, signer } = useWeb3();
    const toast = useToast();

    useEffect(() => {
        if (account && signer) {
            loadData();
        }
    }, [account, signer]);

    useEffect(() => {
        if (!canCheckIn && lastCheckIn) {
            const interval = setInterval(() => {
                updateTimeUntilCheckIn();
            }, 1000);
            
            return () => clearInterval(interval);
        }
    }, [canCheckIn, lastCheckIn]);

    const loadData = async () => {
        try {
            const gmService = new GMTokenService(
                process.env.REACT_APP_GM_TOKEN_CONTRACT, 
                signer
            );
            
            const [userCredits, balance, canCheck, lastCheck] = await Promise.all([
                gmService.getResearchCredits(account),
                gmService.getTokenBalance(account),
                gmService.canCheckIn(account),
                gmService.getLastCheckIn(account)
            ]);
            
            setCredits(parseFloat(userCredits));
            setTokenBalance(parseFloat(balance));
            setCanCheckIn(canCheck);
            
            if (lastCheck > 0) {
                setLastCheckIn(lastCheck * 1000);
            }
        } catch (error) {
            console.error('Failed to load data:', error);
            toast({
                title: 'Lỗi',
                description: 'Không thể tải dữ liệu từ blockchain',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        }
    };

    const updateTimeUntilCheckIn = () => {
        if (!lastCheckIn) return;
        
        const nextCheckIn = lastCheckIn + (24 * 60 * 60 * 1000);
        const now = Date.now();
        const diff = nextCheckIn - now;
        
        if (diff <= 0) {
            setCanCheckIn(true);
            setTimeUntilCheckIn('');
            return;
        }
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        setTimeUntilCheckIn(`${hours}h ${minutes}m ${seconds}s`);
    };

    const handlePurchaseTokens = async () => {
        if (!ethAmount || parseFloat(ethAmount) <= 0) {
            toast({
                title: 'Lỗi',
                description: 'Vui lòng nhập số lượng ETH hợp lệ',
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
            return;
        }
        
        setIsLoading(true);
        try {
            const gmService = new GMTokenService(
                process.env.REACT_APP_GM_TOKEN_CONTRACT, 
                signer
            );
            
            await gmService.purchaseTokens(ethAmount);
            
            toast({
                title: 'Thành công!',
                description: `Đã mua ${calculateTokens(ethAmount)} GM Tokens`,
                status: 'success',
                duration: 5000,
                isClosable: true,
            });
            
            await loadData();
        } catch (error) {
            console.error('Purchase failed:', error);
            toast({
                title: 'Giao dịch thất bại',
                description: error.message || 'Vui lòng thử lại',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleDailyCheckIn = async () => {
        setIsLoading(true);
        try {
            const gmService = new GMTokenService(
                process.env.REACT_APP_GM_TOKEN_CONTRACT, 
                signer
            );
            
            await gmService.dailyCheckIn();
            
            toast({
                title: 'Check-in thành công!',
                description: 'Bạn nhận được 50 GM Credits',
                status: 'success',
                duration: 5000,
                isClosable: true,
            });
            
            await loadData();
        } catch (error) {
            console.error('Check-in failed:', error);
            toast({
                title: 'Check-in thất bại',
                description: error.message || 'Vui lòng thử lại',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    const calculateTokens = (eth) => {
        return Math.floor(parseFloat(eth) / 0.001);
    };

    return (
        <Box p={6} maxW="md" mx="auto">
            <VStack spacing={6}>
                {/* Balance Display */}
                <Box w="100%" p={6} borderWidth={2} borderRadius="lg" bg="blue.50">
                    <VStack spacing={3}>
                        <Stat textAlign="center">
                            <StatLabel fontSize="md" color="gray.600">
                                Research Credits
                            </StatLabel>
                            <StatNumber fontSize="4xl" color="blue.600">
                                {credits.toFixed(0)} GM
                            </StatNumber>
                            <StatHelpText>
                                Token Balance: {tokenBalance.toFixed(2)} GM
                            </StatHelpText>
                        </Stat>
                    </VStack>
                </Box>

                {/* Daily Check-in */}
                <Box w="100%" p={5} borderWidth={1} borderRadius="lg" bg="white">
                    <VStack spacing={4}>
                        <Text fontSize="xl" fontWeight="bold">
                            Check-in hàng ngày
                        </Text>
                        <Text color="gray.600" textAlign="center">
                            Nhận 50 GM Credits miễn phí mỗi ngày
                        </Text>
                        
                        {canCheckIn ? (
                            <Button 
                                colorScheme="green" 
                                size="lg" 
                                onClick={handleDailyCheckIn}
                                isLoading={isLoading}
                                w="100%"
                            >
                                Check-in (+50 GM)
                            </Button>
                        ) : (
                            <VStack w="100%">
                                <Button 
                                    colorScheme="gray" 
                                    size="lg" 
                                    isDisabled
                                    w="100%"
                                >
                                    Đã check-in hôm nay
                                </Button>
                                {timeUntilCheckIn && (
                                    <Text fontSize="sm" color="orange.500">
                                        Check-in tiếp theo: {timeUntilCheckIn}
                                    </Text>
                                )}
                            </VStack>
                        )}
                    </VStack>
                </Box>

                <Divider />

                {/* Purchase Tokens */}
                <Box w="100%" p={5} borderWidth={1} borderRadius="lg" bg="white">
                    <VStack spacing={4}>
                        <Text fontSize="xl" fontWeight="bold">
                            Mua GM Tokens
                        </Text>
                        
                        <HStack w="100%">
                            <Input
                                type="number"
                                value={ethAmount}
                                onChange={(e) => setEthAmount(e.target.value)}
                                placeholder="0.01"
                                step="0.001"
                                min="0.001"
                                size="lg"
                            />
                            <Text fontSize="lg" fontWeight="semibold" minW="60px">
                                ETH
                            </Text>
                        </HStack>
                        
                        <Text fontSize="lg" color="blue.600" fontWeight="semibold">
                            = {calculateTokens(ethAmount)} GM Tokens
                        </Text>
                        
                        <Button 
                            colorScheme="blue" 
                            size="lg" 
                            onClick={handlePurchaseTokens}
                            isLoading={isLoading}
                            w="100%"
                        >
                            Mua Tokens
                        </Button>
                        
                        <Alert status="info" borderRadius="md">
                            <AlertIcon />
                            <Text fontSize="sm">
                                1 GM Token = 0.001 ETH = 1 lượt research
                            </Text>
                        </Alert>
                    </VStack>
                </Box>
            </VStack>
        </Box>
    );
};

export default TokenEconomy;

