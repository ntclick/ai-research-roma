import React from 'react';
import {
    Box,
    Button,
    VStack,
    Text,
    Heading,
    Container,
    Icon
} from '@chakra-ui/react';
import { FaWallet } from 'react-icons/fa';
import { useWeb3 } from '../../hooks/useWeb3';

const WalletConnection = () => {
    const { connectWallet, isConnecting } = useWeb3();

    return (
        <Container maxW="md" centerContent>
            <Box
                p={8}
                borderWidth={1}
                borderRadius="lg"
                boxShadow="lg"
                textAlign="center"
                bg="white"
            >
                <VStack spacing={6}>
                    <Icon as={FaWallet} boxSize={16} color="blue.500" />
                    
                    <Heading size="lg">
                        Crypto Research App
                    </Heading>
                    
                    <Text color="gray.600">
                        Kết nối ví MetaMask để bắt đầu nghiên cứu crypto với AI
                    </Text>
                    
                    <VStack spacing={2} align="stretch" w="100%">
                        <Text fontSize="sm" color="gray.500">
                            ✓ Mua GM Token bằng Sepolia ETH
                        </Text>
                        <Text fontSize="sm" color="gray.500">
                            ✓ Check-in hàng ngày nhận 50 GM miễn phí
                        </Text>
                        <Text fontSize="sm" color="gray.500">
                            ✓ Chat AI nghiên cứu coin & tạo nội dung
                        </Text>
                    </VStack>
                    
                    <Button
                        colorScheme="blue"
                        size="lg"
                        onClick={connectWallet}
                        isLoading={isConnecting}
                        loadingText="Đang kết nối..."
                        w="100%"
                    >
                        Kết nối MetaMask
                    </Button>
                    
                    <Text fontSize="xs" color="gray.400">
                        Hỗ trợ Sepolia Test Network
                    </Text>
                </VStack>
            </Box>
        </Container>
    );
};

export default WalletConnection;

