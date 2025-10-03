import React, { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Input,
    VStack,
    Text,
    FormControl,
    FormLabel,
    FormHelperText,
    Alert,
    AlertIcon,
    AlertTitle,
    AlertDescription,
    useToast,
    InputGroup,
    InputRightElement,
    IconButton,
    Divider,
    Link
} from '@chakra-ui/react';
import { FaEye, FaEyeSlash, FaExternalLinkAlt } from 'react-icons/fa';

const ApiSettings = () => {
    const [apis, setApis] = useState({
        coingecko: '',
        falai: '',
        twitter: '',
        sepoliaRpc: '',
        gmContract: ''
    });
    
    const [showKeys, setShowKeys] = useState({
        coingecko: false,
        falai: false,
        twitter: false
    });
    
    const toast = useToast();

    // Load từ localStorage khi component mount
    useEffect(() => {
        const savedApis = {
            coingecko: localStorage.getItem('api_coingecko') || '',
            falai: localStorage.getItem('api_falai') || '',
            twitter: localStorage.getItem('api_twitter') || '',
            sepoliaRpc: localStorage.getItem('api_sepoliaRpc') || process.env.REACT_APP_SEPOLIA_RPC_URL || '',
            gmContract: localStorage.getItem('api_gmContract') || process.env.REACT_APP_GM_TOKEN_CONTRACT || ''
        };
        setApis(savedApis);
    }, []);

    const handleSave = () => {
        // Lưu vào localStorage
        localStorage.setItem('api_coingecko', apis.coingecko);
        localStorage.setItem('api_falai', apis.falai);
        localStorage.setItem('api_twitter', apis.twitter);
        localStorage.setItem('api_sepoliaRpc', apis.sepoliaRpc);
        localStorage.setItem('api_gmContract', apis.gmContract);
        
        // Cập nhật env variables (chỉ trong runtime)
        if (apis.sepoliaRpc) {
            process.env.REACT_APP_SEPOLIA_RPC_URL = apis.sepoliaRpc;
        }
        if (apis.gmContract) {
            process.env.REACT_APP_GM_TOKEN_CONTRACT = apis.gmContract;
        }
        
        toast({
            title: 'Đã lưu cài đặt!',
            description: 'API keys đã được lưu vào trình duyệt',
            status: 'success',
            duration: 3000,
            isClosable: true,
        });
    };

    const handleClear = () => {
        setApis({
            coingecko: '',
            falai: '',
            twitter: '',
            sepoliaRpc: '',
            gmContract: ''
        });
        
        localStorage.removeItem('api_coingecko');
        localStorage.removeItem('api_falai');
        localStorage.removeItem('api_twitter');
        localStorage.removeItem('api_sepoliaRpc');
        localStorage.removeItem('api_gmContract');
        
        toast({
            title: 'Đã xóa cài đặt',
            description: 'Tất cả API keys đã được xóa',
            status: 'info',
            duration: 3000,
            isClosable: true,
        });
    };

    const toggleShowKey = (key) => {
        setShowKeys(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    return (
        <Box p={6} maxW="2xl" mx="auto">
            <VStack spacing={6} align="stretch">
                <Box>
                    <Text fontSize="2xl" fontWeight="bold" mb={2}>
                        ⚙️ Cài đặt API Keys
                    </Text>
                    <Text color="gray.600">
                        Cấu hình các API keys để sử dụng đầy đủ tính năng
                    </Text>
                </Box>

                <Alert status="warning" borderRadius="md">
                    <AlertIcon />
                    <Box>
                        <AlertTitle>Lưu ý bảo mật!</AlertTitle>
                        <AlertDescription fontSize="sm">
                            API keys được lưu trong localStorage của trình duyệt. 
                            Không chia sẻ keys với người khác.
                        </AlertDescription>
                    </Box>
                </Alert>

                <Divider />

                {/* Blockchain Configuration */}
                <Box p={4} borderWidth={1} borderRadius="md" bg="blue.50">
                    <Text fontSize="lg" fontWeight="bold" mb={4}>
                        🔗 Blockchain Configuration
                    </Text>
                    
                    <VStack spacing={4}>
                        <FormControl isRequired>
                            <FormLabel>Sepolia RPC URL</FormLabel>
                            <Input
                                placeholder="https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
                                value={apis.sepoliaRpc}
                                onChange={(e) => setApis({...apis, sepoliaRpc: e.target.value})}
                                bg="white"
                            />
                            <FormHelperText>
                                Lấy từ{' '}
                                <Link href="https://infura.io" isExternal color="blue.600">
                                    Infura <FaExternalLinkAlt style={{display: 'inline'}} />
                                </Link>
                                {' '}hoặc{' '}
                                <Link href="https://alchemy.com" isExternal color="blue.600">
                                    Alchemy <FaExternalLinkAlt style={{display: 'inline'}} />
                                </Link>
                            </FormHelperText>
                        </FormControl>

                        <FormControl isRequired>
                            <FormLabel>GM Token Contract Address</FormLabel>
                            <Input
                                placeholder="0x..."
                                value={apis.gmContract}
                                onChange={(e) => setApis({...apis, gmContract: e.target.value})}
                                bg="white"
                                fontFamily="monospace"
                            />
                            <FormHelperText>
                                Contract address sau khi deploy (xem phần Deploy bên dưới)
                            </FormHelperText>
                        </FormControl>
                    </VStack>
                </Box>

                {/* Research APIs */}
                <Box p={4} borderWidth={1} borderRadius="md">
                    <Text fontSize="lg" fontWeight="bold" mb={4}>
                        🔍 Research APIs
                    </Text>
                    
                    <VStack spacing={4}>
                        <FormControl>
                            <FormLabel>CoinGecko API Key</FormLabel>
                            <InputGroup>
                                <Input
                                    type={showKeys.coingecko ? "text" : "password"}
                                    placeholder="CG-xxxxxxxxxxxx"
                                    value={apis.coingecko}
                                    onChange={(e) => setApis({...apis, coingecko: e.target.value})}
                                />
                                <InputRightElement>
                                    <IconButton
                                        size="sm"
                                        icon={showKeys.coingecko ? <FaEyeSlash /> : <FaEye />}
                                        onClick={() => toggleShowKey('coingecko')}
                                        variant="ghost"
                                    />
                                </InputRightElement>
                            </InputGroup>
                            <FormHelperText>
                                <Link href="https://www.coingecko.com/en/api" isExternal color="blue.600">
                                    Đăng ký miễn phí <FaExternalLinkAlt style={{display: 'inline'}} />
                                </Link>
                                {' '}- Free tier: 10-50 calls/minute
                            </FormHelperText>
                        </FormControl>

                        <FormControl>
                            <FormLabel>fal.ai API Key (Optional)</FormLabel>
                            <InputGroup>
                                <Input
                                    type={showKeys.falai ? "text" : "password"}
                                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                                    value={apis.falai}
                                    onChange={(e) => setApis({...apis, falai: e.target.value})}
                                />
                                <InputRightElement>
                                    <IconButton
                                        size="sm"
                                        icon={showKeys.falai ? <FaEyeSlash /> : <FaEye />}
                                        onClick={() => toggleShowKey('falai')}
                                        variant="ghost"
                                    />
                                </InputRightElement>
                            </InputGroup>
                            <FormHelperText>
                                <Link href="https://fal.ai" isExternal color="blue.600">
                                    Đăng ký tại fal.ai <FaExternalLinkAlt style={{display: 'inline'}} />
                                </Link>
                                {' '}- Dùng cho tạo hình ảnh AI
                            </FormHelperText>
                        </FormControl>

                        <FormControl>
                            <FormLabel>Twitter Bearer Token (Optional)</FormLabel>
                            <InputGroup>
                                <Input
                                    type={showKeys.twitter ? "text" : "password"}
                                    placeholder="AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxx"
                                    value={apis.twitter}
                                    onChange={(e) => setApis({...apis, twitter: e.target.value})}
                                />
                                <InputRightElement>
                                    <IconButton
                                        size="sm"
                                        icon={showKeys.twitter ? <FaEyeSlash /> : <FaEye />}
                                        onClick={() => toggleShowKey('twitter')}
                                        variant="ghost"
                                    />
                                </InputRightElement>
                            </InputGroup>
                            <FormHelperText>
                                <Link href="https://developer.twitter.com" isExternal color="blue.600">
                                    Twitter Developer Portal <FaExternalLinkAlt style={{display: 'inline'}} />
                                </Link>
                                {' '}- Dùng cho phân tích X posts
                            </FormHelperText>
                        </FormControl>
                    </VStack>
                </Box>

                {/* Action Buttons */}
                <Box pt={4}>
                    <VStack spacing={3}>
                        <Button
                            colorScheme="blue"
                            size="lg"
                            onClick={handleSave}
                            w="100%"
                        >
                            💾 Lưu cài đặt
                        </Button>
                        
                        <Button
                            variant="outline"
                            colorScheme="red"
                            size="sm"
                            onClick={handleClear}
                            w="100%"
                        >
                            🗑️ Xóa tất cả
                        </Button>
                    </VStack>
                </Box>

                {/* Status */}
                <Box p={4} bg="gray.50" borderRadius="md">
                    <Text fontSize="sm" fontWeight="bold" mb={2}>
                        📊 Trạng thái:
                    </Text>
                    <VStack align="stretch" spacing={1} fontSize="sm">
                        <Text>
                            ✅ Sepolia RPC: {apis.sepoliaRpc ? '✓ Đã cấu hình' : '✗ Chưa cấu hình'}
                        </Text>
                        <Text>
                            ✅ GM Contract: {apis.gmContract ? '✓ Đã cấu hình' : '✗ Chưa cấu hình'}
                        </Text>
                        <Text>
                            {apis.coingecko ? '✅' : '⚠️'} CoinGecko: {apis.coingecko ? 'Đã cấu hình' : 'Chưa cấu hình (khuyến nghị)'}
                        </Text>
                        <Text>
                            {apis.falai ? '✅' : 'ℹ️'} fal.ai: {apis.falai ? 'Đã cấu hình' : 'Chưa cấu hình (optional)'}
                        </Text>
                        <Text>
                            {apis.twitter ? '✅' : 'ℹ️'} Twitter: {apis.twitter ? 'Đã cấu hình' : 'Chưa cấu hình (optional)'}
                        </Text>
                    </VStack>
                </Box>
            </VStack>
        </Box>
    );
};

export default ApiSettings;

