import React, { useState, useRef, useEffect } from 'react';
import useWebSocket from 'react-use-websocket';
import {
    Box,
    VStack,
    HStack,
    Input,
    Button,
    Select,
    Text,
    Avatar,
    Badge,
    useToast,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalCloseButton,
    Image,
    Spinner,
    Divider,
    IconButton,
    Tooltip
} from '@chakra-ui/react';
import { 
    FaRobot, 
    FaUser, 
    FaImage, 
    FaSearch, 
    FaTwitter, 
    FaNewspaper,
    FaCoins,
    FaPaperPlane,
    FaTimes,
    FaRedo
} from 'react-icons/fa';

const InteractiveChat = () => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            type: 'ai',
            content: 'Welcome! I am your Crypto Research AI powered by ROMA Framework.\n\nI can help you with:\n• Real-time price checks\n• Investment analysis\n• Latest crypto news\n• AI-generated images\n\nWhat would you like to know?',
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [selectedTool, setSelectedTool] = useState('research');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const toast = useToast();

    // WebSocket connection
    const { sendJsonMessage, lastJsonMessage, readyState, getWebSocket } = useWebSocket(
        process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:5001',
        {
            shouldReconnect: () => true,
            reconnectAttempts: 10,
            reconnectInterval: 3000,
            share: false, // Prevent sharing connections
            filter: () => true, // Accept all messages
        }
    );

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Handle WebSocket messages
    useEffect(() => {
        if (lastJsonMessage) {
            console.log('[FRONTEND] Received WebSocket message:', lastJsonMessage);
            
            // Prevent duplicate messages by checking if we already have this message
            setMessages(prev => {
                // Check if this message already exists (by content and timestamp)
                const isDuplicate = prev.some(msg => 
                    msg.content === lastJsonMessage.content && 
                    msg.type === (lastJsonMessage.sender === 'ai' ? 'ai' : 'user') &&
                    Math.abs(new Date() - new Date(msg.timestamp)) < 1000 // Within 1 second
                );
                
                if (isDuplicate) {
                    console.log('[FRONTEND] Duplicate message detected, skipping');
                    return prev;
                }
                
                // Convert backend message to frontend format
                const frontendMessage = {
                    id: Date.now() + Math.random(), // More unique ID
                    type: lastJsonMessage.sender === 'ai' ? 'ai' : 'user',
                    content: lastJsonMessage.content,
                    timestamp: new Date(),
                    tool: lastJsonMessage.tool || 'research',
                    api_source: lastJsonMessage.api_source,
                    has_error: lastJsonMessage.has_error || false,
                    retry_available: lastJsonMessage.retry_available || false,
                    image_url: lastJsonMessage.image_url
                };
                
                return [...prev, frontendMessage];
            });
            
            setIsLoading(false);
        }
    }, [lastJsonMessage]);

    // WebSocket connection status
    useEffect(() => {
        console.log('[FRONTEND] WebSocket readyState:', readyState);
        if (readyState === 1) {
            console.log('[FRONTEND] WebSocket connected successfully');
        } else if (readyState === 3) {
            console.log('[FRONTEND] WebSocket disconnected');
        }
    }, [readyState]);

    // Cleanup WebSocket connection on unmount
    useEffect(() => {
        return () => {
            const ws = getWebSocket();
            if (ws && ws.readyState === WebSocket.OPEN) {
                console.log('[FRONTEND] Cleaning up WebSocket connection');
                ws.close();
            }
        };
    }, [getWebSocket]);


    const analyzeContext = (query) => {
        const queryLower = query.toLowerCase();
        
        // CoinGecko patterns - price, market data, specific coins
        const coingeckoPatterns = [
            'price', 'market cap', 'volume', 'trading', '24h', 'hourly', 'daily',
            'bitcoin', 'ethereum', 'btc', 'eth', 'usdt', 'usdc', 'token price',
            'current price', 'market data', 'trading volume', 'price chart',
            'coin price', 'crypto price', 'how much', 'worth', 'value'
        ];
        
        // Perplexity patterns - deep analysis, trends, opinions
        const perplexityPatterns = [
            'analysis', 'analyze', 'trend', 'trends', 'future', 'prediction',
            'deep research', 'expert opinion', 'market outlook', 'forecast',
            'why', 'how', 'what if', 'explain', 'understand', 'insight',
            'regulatory', 'adoption', 'institutional', 'ecosystem', 'development',
            'compare', 'difference', 'pros and cons', 'risk', 'opportunity'
        ];
        
        // OpenAI patterns - chat context, summarization
        const openaiPatterns = [
            'summarize', 'summary', 'chat', 'discussion', 'conversation',
            'what did we talk', 'context', 'based on our chat', 'from our discussion',
            'recap', 'overview', 'key points', 'main points', 'conclusion',
            'personal', 'my', 'for me', 'recommendation', 'advice', 'suggestion'
        ];
        
        // Count matches for each source
        const coingeckoScore = coingeckoPatterns.filter(pattern => 
            queryLower.includes(pattern)
        ).length;
        
        const perplexityScore = perplexityPatterns.filter(pattern => 
            queryLower.includes(pattern)
        ).length;
        
        const openaiScore = openaiPatterns.filter(pattern => 
            queryLower.includes(pattern)
        ).length;
        
        // Determine best source
        if (coingeckoScore > perplexityScore && coingeckoScore > openaiScore) {
            return 'coingecko';
        } else if (perplexityScore > openaiScore) {
            return 'perplexity';
        } else if (openaiScore > 0) {
            return 'openai';
        } else {
            // Default to Perplexity for general queries
            return 'perplexity';
        }
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;

        const userMessage = {
            id: Date.now(),
            type: 'user',
            content: inputValue,
            timestamp: new Date(),
            tool: selectedTool
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        // Send real request to backend via WebSocket
        const message = {
            type: 'user_message',
            tool: selectedTool,
            content: inputValue,
            user: 'user123'
        };
        
        try {
            sendJsonMessage(message);
            console.log('[FRONTEND] Sent WebSocket message:', message);
        } catch (error) {
            console.error('[FRONTEND] WebSocket send error:', error);
            const errorMessage = {
                id: Date.now() + 1,
                type: 'ai',
                content: `❌ **Connection Error:** Cannot connect to backend server.\n\nPlease check if backend is running on port 5001.`,
                timestamp: new Date(),
                tool: selectedTool,
                has_error: true,
                retry_available: true
            };
            setMessages(prev => [...prev, errorMessage]);
            setIsLoading(false);
        }
    };

    const generateMockResponse = (tool, query) => {
        const detectedSource = analyzeContext(query);
        
        const responses = {
            'research': `🔍 **Research Results for "${query}"**

${detectedSource === 'coingecko' ? 
`📊 **CoinGecko Data:**
• Current Price: $0.000123 (+15.67% 24h)
• Market Cap: $2.3M
• Volume: $456K
• RSI: 65.4 (Neutral-Bullish)
• 24h High: $0.000135
• 24h Low: $0.000110

📈 **Technical Analysis:**
• Support: $0.000100
• Resistance: $0.000150
• Trading pairs: ETH, BTC, USDT

💡 **Context Analysis:** Detected price/market query → Using CoinGecko API` : 
detectedSource === 'perplexity' ?
`🔍 **Deep Research (Perplexity AI):**
• Comprehensive market analysis and trends
• Expert opinions and predictions
• Regulatory developments
• Technical indicators and patterns
• Risk assessment and opportunities

📊 **Market Sentiment:**
• Fear & Greed Index: 45 (Neutral)
• BTC Dominance: 52.3%
• AI tokens showing strong momentum
• Institutional adoption increasing

💡 **Context Analysis:** Detected analysis/trend query → Using Perplexity AI` :
`🤖 **AI Analysis (OpenAI):**
• Synthesized insights from chat history
• Contextual understanding of your research
• Personalized recommendations
• Risk-adjusted strategies
• Market timing suggestions

💡 **Context Analysis:** Detected chat context query → Using OpenAI GPT-4`}

🎯 **Smart Detection:** Query analyzed and routed to optimal source
📊 **Confidence:** High accuracy based on keyword analysis`,

            'create-x-post': `🐦 **X Post Created from "${query}":**

"🚀 ${query} showing incredible momentum! 

📊 Key highlights:
• Price up 15.67% in 24h
• Strong fundamentals
• Growing community buzz

Perfect time for DYOR! 🧠

#Crypto #${query.replace(/\s+/g, '')} #DeFi #Web3"

📏 **Character Count:** 158/280
✅ **Optimized for engagement**
🎯 **Based on research data**`,

            'generate-image': `🎨 **Image Generated for X Post:**

🖼️ **Description:** "${query}"
📐 **Style:** Modern crypto-themed illustration
🎨 **Resolution:** 1080x1080 (Twitter optimized)

✨ **Features:**
• Clean, professional design
• Crypto/blockchain visual elements
• High contrast for social media
• Brandable color scheme

💡 **Perfect for:**
• Twitter/X post headers
• Social media campaigns
• Presentation slides
• Marketing materials

🔗 **Ready to download and use!**`
        };

        return responses[tool] || `I've processed your request: "${query}"`;
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const handleRetry = (message) => {
        // Find the original user message that led to this AI response
        const messageIndex = messages.findIndex(msg => msg.id === message.id);
        let originalQuery = 'Please try again';
        
        // Look for the user message before this AI response
        if (messageIndex > 0) {
            for (let i = messageIndex - 1; i >= 0; i--) {
                if (messages[i].type === 'user') {
                    originalQuery = messages[i].content;
                    break;
                }
            }
        }
        
        // Send retry request via WebSocket
        const retryMessage = {
            type: 'user_message',
            tool: 'research',
            content: originalQuery,
            user: 'user123'
        };
        
        try {
            sendJsonMessage(retryMessage);
            console.log('[FRONTEND] Sent retry WebSocket message:', retryMessage);
            setIsLoading(true);
        } catch (error) {
            console.error('[FRONTEND] Retry WebSocket send error:', error);
            toast({
                title: 'Retry failed',
                description: 'Cannot connect to backend server',
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const clearChat = () => {
        setMessages([
            {
                id: 1,
                type: 'ai',
                content: '👋 Chào bạn! Tôi là AI Research Assistant mới. Tôi có thể:\n\n🔍 **Research:** Giá coin, phân tích thị trường, tin tức crypto\n📰 **News:** Tin tức mới nhất từ các nguồn uy tín\n🤖 **AI Analysis:** Tổng hợp và giải thích dễ hiểu\n\nBạn muốn tôi giúp gì?',
                timestamp: new Date()
            }
        ]);
        toast({
            title: 'Chat cleared!',
            status: 'info',
            duration: 2000,
            isClosable: true,
        });
    };

    return (
        <Box maxW="800px" mx="auto" p={6}>
            <VStack spacing={6} align="stretch">
                {/* Header */}
                <Box textAlign="center">
                    <Text fontSize="2xl" fontWeight="bold" color="blue.600" mb={2}>
                        AI Research Chat
                    </Text>
                    <HStack justify="center" spacing={4} mb={2}>
                        <Badge 
                            colorScheme={readyState === 1 ? "green" : readyState === 3 ? "red" : "yellow"}
                            variant="outline"
                        >
                            {readyState === 1 ? "Connected" : readyState === 3 ? "Disconnected" : "Connecting"}
                        </Badge>
                    </HStack>
                    <Text color="gray.600" fontSize="sm">
                        Powered by ROMA Framework + Multi-AI Architecture
                    </Text>
                </Box>

                {/* Chat Messages */}
                <Box 
                    height="400px" 
                    overflowY="auto" 
                    border="1px solid" 
                    borderColor="gray.200" 
                    borderRadius="md" 
                    p={4}
                    bg="white"
                >
                    <VStack spacing={4} align="stretch">
                        {messages.map((message) => (
                            <Box key={message.id}>
                                <HStack spacing={3} align="flex-start">
                                    <Avatar
                                        size="sm"
                                        icon={message.type === 'ai' ? <FaRobot /> : <FaUser />}
                                        bg={message.type === 'ai' ? 'blue.500' : 'green.500'}
                                    />
                                    <Box flex={1}>
                                        <HStack spacing={2} mb={1}>
                                            <Text fontSize="sm" fontWeight="bold">
                                                {message.type === 'ai' ? 'AI Assistant' : 'You'}
                                            </Text>
                                            {message.tool && (
                                                <Badge 
                                                    colorScheme="blue"
                                                    size="sm"
                                                >
                                                    {message.api_source || 'AI'}
                                                </Badge>
                                            )}
                                            <Text fontSize="xs" color="gray.500">
                                                {message.timestamp.toLocaleTimeString()}
                                            </Text>
                                        </HStack>
                                        <Box
                                            p={3}
                                            bg={message.type === 'ai' ? 'blue.50' : 'gray.50'}
                                            borderRadius="md"
                                            borderLeft="3px solid"
                                            borderLeftColor={message.type === 'ai' ? 'blue.500' : 'green.500'}
                                        >
                                            <Text
                                                whiteSpace="pre-wrap" 
                                                fontSize="sm"
                                                dangerouslySetInnerHTML={{
                                                    __html: message.content
                                                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                                        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, title, url) => {
                                                            // Clean title from problematic quotes and characters
                                                            const cleanTitle = title
                                                                .replace(/"/g, '&quot;')
                                                                .replace(/'/g, '&#39;')
                                                                .replace(/"/g, '&quot;')
                                                                .replace(/'/g, '&#39;')
                                                                .replace(/&/g, '&amp;')
                                                                .replace(/</g, '&lt;')
                                                                .replace(/>/g, '&gt;');
                                                            return `<a href="${url}" target="_blank" rel="noopener noreferrer" style="color: #3182ce; text-decoration: underline;">${cleanTitle}</a>`;
                                                        })
                                                }}
                                            />
                                                    {message.image_url && (
                                                        <Box mt={2}>
                                                            <img 
                                                                src={message.image_url} 
                                                                alt="Generated" 
                                                                style={{ 
                                                                    maxWidth: '100%', 
                                                                    borderRadius: '8px',
                                                                    border: '1px solid #e2e8f0'
                                                                }} 
                                                            />
                                                        </Box>
                                                    )}
                                            {message.retry_available && (
                                                <Box mt={2}>
                                                    <Button 
                                                        size="sm" 
                                                        colorScheme="orange" 
                                                        variant="outline"
                                                        onClick={() => handleRetry(message)}
                                                        leftIcon={<FaRedo />}
                                                    >
                                                        Retry
                                                    </Button>
                                                </Box>
                                            )}
                                        </Box>
                                    </Box>
                                </HStack>
                            </Box>
                        ))}
                        
                        {isLoading && (
                            <HStack spacing={3} align="flex-start">
                                <Avatar size="sm" icon={<FaRobot />} bg="blue.500" />
                                <Box flex={1}>
                                    <Text fontSize="sm" fontWeight="bold" mb={1}>
                                        AI Assistant
                                    </Text>
                                    <HStack spacing={2}>
                                        <Spinner size="sm" />
                                        <Text fontSize="sm" color="gray.500">
                                            Processing...
                                        </Text>
                                    </HStack>
                                </Box>
                            </HStack>
                        )}
                        <div ref={messagesEndRef} />
                    </VStack>
                </Box>

                {/* Input Area */}
                <Box p={4} bg="white" borderRadius="md" border="1px solid" borderColor="gray.200">
                    <VStack spacing={3}>
                        <HStack spacing={2} w="100%">
                            <Input
                                placeholder="Ask me anything about crypto..."
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={handleKeyPress}
                                size="lg"
                            />
                            <Button
                                colorScheme="blue"
                                size="lg"
                                onClick={handleSendMessage}
                                isDisabled={!inputValue.trim() || isLoading}
                                leftIcon={<FaPaperPlane />}
                            >
                                Send
                            </Button>
                        </HStack>
                        
                        <HStack spacing={2} justify="flex-end" w="100%">
                            <Tooltip label="Clear chat">
                                <IconButton
                                    size="sm"
                                    icon={<FaTimes />}
                                    onClick={clearChat}
                                    variant="ghost"
                                />
                            </Tooltip>
                        </HStack>
                    </VStack>
                </Box>

            </VStack>

        </Box>
    );
};

export default InteractiveChat;
