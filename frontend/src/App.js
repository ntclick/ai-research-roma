import React from 'react';
import { 
    ChakraProvider, 
    Container, 
    Box,
    Text,
    VStack,
    Alert,
    AlertIcon,
    Link,
    Icon
} from '@chakra-ui/react';
import { FaYoutube } from 'react-icons/fa';
import InteractiveChat from './components/InteractiveChat';

function App() {
    return (
        <ChakraProvider>
            <Box minH="100vh" bg="gray.50">
                <Container maxW="container.xl" py={10}>
                    <VStack spacing={8}>
                        <Box textAlign="center">
                            <Text fontSize="4xl" fontWeight="bold" color="blue.600" mb={2}>
                                Crypto Research AI
                            </Text>
                            <Text fontSize="md" color="gray.500">
                                ROMA Framework + Multi-AI Architecture
                            </Text>
                            <Text fontSize="sm" color="gray.400" mt={1}>
                                👨‍💻 by <a href="https://x.com/trungkts29" target="_blank" rel="noopener noreferrer" style={{color: '#1DA1F2', textDecoration: 'none'}}>@trungkts29</a>
                            </Text>
                        </Box>

                        <Box w="100%" maxW="1200px">
                            <InteractiveChat />
                        </Box>

                        <Box p={4} bg="blue.50" borderRadius="md" w="100%" maxW="1200px">
                            <Text fontWeight="bold" mb={2}>Quick Start</Text>
                            <VStack align="stretch" spacing={1} fontSize="sm" color="gray.700">
                                <Text>• "check btc" - Get real-time price data</Text>
                                <Text>• "should i buy ethereum" - Investment analysis</Text>
                                <Text>• "bitcoin news" - Latest crypto news</Text>
                                <Text>• "create image bitcoin logo" - AI image generation</Text>
                            </VStack>
                        </Box>

                        <Box p={4} bg="red.50" borderRadius="md" w="100%" maxW="1200px" textAlign="center">
                            <Text fontWeight="bold" mb={2} fontSize="lg">
                                🎥 Demo Video
                            </Text>
                            <Link 
                                href="https://youtu.be/3Oihz5XFWpw" 
                                isExternal 
                                color="red.600"
                                fontWeight="semibold"
                                _hover={{ color: 'red.700', textDecoration: 'underline' }}
                            >
                                <Icon as={FaYoutube} mr={2} boxSize={5} />
                                Watch Full Demo & Tutorial on YouTube
                            </Link>
                        </Box>
                    </VStack>
                </Container>
            </Box>
        </ChakraProvider>
    );
}

export default App;
