import React, { useState, useEffect, useRef } from 'react';
import { 
    Box, 
    Input, 
    Button, 
    VStack, 
    HStack, 
    Text,
    Select,
    Spinner,
    Avatar,
    useToast
} from '@chakra-ui/react';
import useWebSocket from 'react-use-websocket';
import { useWeb3 } from '../../hooks/useWeb3';
import { GMTokenService } from '../../services/gmTokenService';

const ResearchChat = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [selectedTool, setSelectedTool] = useState('coin-research');
    const [isTyping, setIsTyping] = useState(false);
    const [credits, setCredits] = useState(0);
    
    const { account, signer } = useWeb3();
    const messagesEndRef = useRef(null);
    const toast = useToast();
    
    const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
        process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:5001',
        {
            shouldReconnect: () => true,
            reconnectAttempts: 10,
            reconnectInterval: 3000,
        }
    );

    useEffect(() => {
        if (lastJsonMessage) {
            setMessages(prev => [...prev, lastJsonMessage]);
            setIsTyping(false);
        }
    }, [lastJsonMessage]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        if (account && signer) {
            loadCredits();
        }
    }, [account, signer]);

    const loadCredits = async () => {
        try {
            const gmService = new GMTokenService(
                process.env.REACT_APP_GM_TOKEN_CONTRACT, 
                signer
            );
            const userCredits = await gmService.getResearchCredits(account);
            setCredits(parseFloat(userCredits));
        } catch (error) {
            console.error('Failed to load credits:', error);
        }
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim()) {
            toast({
                title: 'Lỗi',
                description: 'Vui lòng nhập nội dung',
                status: 'warning',
                duration: 3000,
                isClosable: true,
            });
            return;
        }
        
        if (credits < 1) {
            toast({
                title: 'Không đủ credits',
                description: 'Vui lòng mua thêm GM tokens hoặc check-in hàng ngày',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
            return;
        }

        // Deduct 1 credit (optimistic update)
        setCredits(prev => prev - 1);
        
        const message = {
            type: 'research_request',
            tool: selectedTool,
            content: inputValue,
            user: account,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, {
            ...message,
            sender: 'user'
        }]);

        setIsTyping(true);
        sendJsonMessage(message);
        setInputValue('');
    };

    const toolOptions = [
        { value: 'coin-research', label: '🔍 Nghiên cứu Coin' },
        { value: 'price-analysis', label: '📊 Phân tích Giá' },
        { value: 'x-post-analysis', label: '🐦 Phân tích bài X' },
        { value: 'create-x-post', label: '✍️ Viết bài X' },
        { value: 'generate-image', label: '🎨 Tạo hình ảnh' }
    ];

    const getConnectionStatus = () => {
        const status = ['Đang kết nối...', 'Đã kết nối', 'Đang ngắt kết nối...', 'Ngắt kết nối'][readyState];
        const color = ['orange', 'green', 'orange', 'red'][readyState];
        return { status, color };
    };

    const { status: connectionStatus, color: statusColor } = getConnectionStatus();

    return (
        <Box h="calc(100vh - 200px)" display="flex" flexDirection="column">
            {/* Header */}
            <Box p={4} bg="blue.50" borderRadius="md" mb={4}>
                <HStack justify="space-between">
                    <VStack align="start" spacing={1}>
                        <Text fontSize="lg" fontWeight="bold">
                            Research Credits: {credits.toFixed(0)} GM
                        </Text>
                        <Text fontSize="xs" color="gray.600">
                            {connectionStatus}
                        </Text>
                    </VStack>
                    <Box w="10px" h="10px" borderRadius="full" bg={`${statusColor}.500`} />
                </HStack>
            </Box>

            {/* Tool Selection */}
            <Box mb={4}>
                <Select 
                    value={selectedTool} 
                    onChange={(e) => setSelectedTool(e.target.value)}
                    size="lg"
                >
                    {toolOptions.map(option => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </Select>
            </Box>

            {/* Messages */}
            <Box 
                flex={1} 
                overflowY="auto" 
                p={4} 
                border="1px solid" 
                borderColor="gray.200"
                borderRadius="md"
                bg="gray.50"
            >
                <VStack spacing={4} align="stretch">
                    {messages.length === 0 && (
                        <Box textAlign="center" py={10}>
                            <Text color="gray.500">
                                Bắt đầu cuộc trò chuyện nghiên cứu crypto...
                            </Text>
                        </Box>
                    )}
                    
                    {messages.map((message, index) => (
                        <HStack
                            key={index}
                            alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'}
                            maxW="75%"
                            spacing={3}
                        >
                            {message.sender === 'ai' && (
                                <Avatar size="sm" name="AI" bg="purple.500" />
                            )}
                            
                            <Box
                                bg={message.sender === 'user' ? 'blue.500' : 'white'}
                                color={message.sender === 'user' ? 'white' : 'black'}
                                p={4}
                                borderRadius="lg"
                                boxShadow="md"
                            >
                                <Text whiteSpace="pre-wrap">{message.content}</Text>
                                {message.image && (
                                    <Box mt={3}>
                                        <img 
                                            src={message.image} 
                                            alt="Generated" 
                                            style={{
                                                maxWidth: '100%', 
                                                borderRadius: '8px'
                                            }} 
                                        />
                                    </Box>
                                )}
                            </Box>
                            
                            {message.sender === 'user' && (
                                <Avatar size="sm" name={account} bg="blue.500" />
                            )}
                        </HStack>
                    ))}
                    
                    {isTyping && (
                        <HStack alignSelf="flex-start" maxW="75%" spacing={3}>
                            <Avatar size="sm" name="AI" bg="purple.500" />
                            <Box bg="white" p={4} borderRadius="lg" boxShadow="md">
                                <HStack>
                                    <Spinner size="sm" color="purple.500" />
                                    <Text color="gray.600">AI đang soạn phản hồi...</Text>
                                </HStack>
                            </Box>
                        </HStack>
                    )}
                </VStack>
                <div ref={messagesEndRef} />
            </Box>

            {/* Input */}
            <HStack mt={4}>
                <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Nhập yêu cầu research..."
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    size="lg"
                    bg="white"
                />
                <Button 
                    onClick={handleSendMessage}
                    colorScheme="blue"
                    disabled={!inputValue.trim() || credits < 1 || isTyping}
                    size="lg"
                    minW="120px"
                >
                    Gửi (1 GM)
                </Button>
            </HStack>
        </Box>
    );
};

export default ResearchChat;

