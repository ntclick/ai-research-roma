import React, { useState } from 'react';
import {
    Box,
    Button,
    VStack,
    Text,
    Alert,
    AlertIcon,
    AlertTitle,
    AlertDescription,
    Code,
    Divider,
    OrderedList,
    ListItem,
    Link,
    Tabs,
    TabList,
    TabPanels,
    Tab,
    TabPanel,
    Input,
    useToast
} from '@chakra-ui/react';
import { FaExternalLinkAlt, FaCopy } from 'react-icons/fa';

const ContractDeploy = () => {
    const [deployedAddress, setDeployedAddress] = useState('');
    const toast = useToast();

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        toast({
            title: 'Đã copy!',
            status: 'success',
            duration: 2000,
            isClosable: true,
        });
    };

    const handleSaveAddress = () => {
        if (deployedAddress) {
            localStorage.setItem('api_gmContract', deployedAddress);
            process.env.REACT_APP_GM_TOKEN_CONTRACT = deployedAddress;
            toast({
                title: 'Đã lưu contract address!',
                description: 'Bạn có thể bắt đầu sử dụng app',
                status: 'success',
                duration: 5000,
                isClosable: true,
            });
        }
    };

    return (
        <Box p={6} maxW="4xl" mx="auto">
            <VStack spacing={6} align="stretch">
                <Box>
                    <Text fontSize="2xl" fontWeight="bold" mb={2}>
                        🚀 Deploy Smart Contract
                    </Text>
                    <Text color="gray.600">
                        Hướng dẫn deploy GM Token contract lên Sepolia testnet
                    </Text>
                </Box>

                <Alert status="info" borderRadius="md">
                    <AlertIcon />
                    <Box>
                        <AlertTitle>Yêu cầu trước khi deploy:</AlertTitle>
                        <AlertDescription fontSize="sm">
                            • Đã cài Node.js và npm<br/>
                            • Có MetaMask với Sepolia ETH (ít nhất 0.1 ETH)<br/>
                            • Đã có Infura/Alchemy project ID
                        </AlertDescription>
                    </Box>
                </Alert>

                <Tabs colorScheme="blue">
                    <TabList>
                        <Tab>📋 Hướng dẫn Deploy</Tab>
                        <Tab>💾 Lưu Contract Address</Tab>
                    </TabList>

                    <TabPanels>
                        <TabPanel>
                            <VStack spacing={6} align="stretch">
                                {/* Step 1 */}
                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontSize="lg" fontWeight="bold" mb={3}>
                                        Bước 1: Lấy Sepolia ETH
                                    </Text>
                                    <Text mb={3}>
                                        Truy cập các faucets để lấy testnet ETH miễn phí:
                                    </Text>
                                    <VStack align="stretch" spacing={2}>
                                        <Link href="https://sepoliafaucet.com" isExternal color="blue.600">
                                            • Sepolia Faucet <FaExternalLinkAlt style={{display: 'inline'}} />
                                        </Link>
                                        <Link href="https://www.alchemy.com/faucets/ethereum-sepolia" isExternal color="blue.600">
                                            • Alchemy Faucet <FaExternalLinkAlt style={{display: 'inline'}} />
                                        </Link>
                                        <Link href="https://faucet.quicknode.com/ethereum/sepolia" isExternal color="blue.600">
                                            • QuickNode Faucet <FaExternalLinkAlt style={{display: 'inline'}} />
                                        </Link>
                                    </VStack>
                                </Box>

                                {/* Step 2 */}
                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontSize="lg" fontWeight="bold" mb={3}>
                                        Bước 2: Lấy Private Key từ MetaMask
                                    </Text>
                                    <OrderedList spacing={2} pl={4}>
                                        <ListItem>Mở MetaMask extension</ListItem>
                                        <ListItem>Click vào 3 chấm → Account details</ListItem>
                                        <ListItem>Click "Export Private Key"</ListItem>
                                        <ListItem>Nhập password MetaMask</ListItem>
                                        <ListItem>Copy private key (bắt đầu với 0x)</ListItem>
                                    </OrderedList>
                                    <Alert status="warning" mt={3} size="sm">
                                        <AlertIcon />
                                        <Text fontSize="sm">
                                            ⚠️ KHÔNG BAO GIỜ chia sẻ private key với ai!
                                        </Text>
                                    </Alert>
                                </Box>

                                {/* Step 3 */}
                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontSize="lg" fontWeight="bold" mb={3}>
                                        Bước 3: Cấu hình .env
                                    </Text>
                                    <Text mb={2}>
                                        Tạo file <Code>.env</Code> trong thư mục <Code>backend/contracts/</Code>:
                                    </Text>
                                    <Box position="relative">
                                        <Button
                                            size="xs"
                                            position="absolute"
                                            right={2}
                                            top={2}
                                            onClick={() => copyToClipboard('SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID\nPRIVATE_KEY=your_metamask_private_key\nETHERSCAN_API_KEY=your_etherscan_key')}
                                            leftIcon={<FaCopy />}
                                        >
                                            Copy
                                        </Button>
                                        <Code display="block" p={4} bg="gray.800" color="green.300" borderRadius="md" fontSize="sm">
                                            SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID<br/>
                                            PRIVATE_KEY=your_metamask_private_key<br/>
                                            ETHERSCAN_API_KEY=your_etherscan_key
                                        </Code>
                                    </Box>
                                </Box>

                                {/* Step 4 */}
                                <Box p={4} borderWidth={1} borderRadius="md" bg="blue.50">
                                    <Text fontSize="lg" fontWeight="bold" mb={3}>
                                        Bước 4: Deploy Contract
                                    </Text>
                                    <Text mb={3}>
                                        Mở terminal và chạy các lệnh sau:
                                    </Text>
                                    
                                    <VStack align="stretch" spacing={3}>
                                        <Box>
                                            <Text fontSize="sm" fontWeight="bold" mb={1}>
                                                1. Di chuyển vào thư mục contracts:
                                            </Text>
                                            <Box position="relative">
                                                <Button
                                                    size="xs"
                                                    position="absolute"
                                                    right={2}
                                                    top={2}
                                                    onClick={() => copyToClipboard('cd backend/contracts')}
                                                    leftIcon={<FaCopy />}
                                                >
                                                    Copy
                                                </Button>
                                                <Code display="block" p={3} bg="gray.800" color="white" borderRadius="md">
                                                    cd backend/contracts
                                                </Code>
                                            </Box>
                                        </Box>

                                        <Box>
                                            <Text fontSize="sm" fontWeight="bold" mb={1}>
                                                2. Cài đặt dependencies:
                                            </Text>
                                            <Box position="relative">
                                                <Button
                                                    size="xs"
                                                    position="absolute"
                                                    right={2}
                                                    top={2}
                                                    onClick={() => copyToClipboard('npm install')}
                                                    leftIcon={<FaCopy />}
                                                >
                                                    Copy
                                                </Button>
                                                <Code display="block" p={3} bg="gray.800" color="white" borderRadius="md">
                                                    npm install
                                                </Code>
                                            </Box>
                                        </Box>

                                        <Box>
                                            <Text fontSize="sm" fontWeight="bold" mb={1}>
                                                3. Compile contract:
                                            </Text>
                                            <Box position="relative">
                                                <Button
                                                    size="xs"
                                                    position="absolute"
                                                    right={2}
                                                    top={2}
                                                    onClick={() => copyToClipboard('npx hardhat compile')}
                                                    leftIcon={<FaCopy />}
                                                >
                                                    Copy
                                                </Button>
                                                <Code display="block" p={3} bg="gray.800" color="white" borderRadius="md">
                                                    npx hardhat compile
                                                </Code>
                                            </Box>
                                        </Box>

                                        <Box>
                                            <Text fontSize="sm" fontWeight="bold" mb={1}>
                                                4. Deploy lên Sepolia:
                                            </Text>
                                            <Box position="relative">
                                                <Button
                                                    size="xs"
                                                    position="absolute"
                                                    right={2}
                                                    top={2}
                                                    onClick={() => copyToClipboard('npm run deploy:sepolia')}
                                                    leftIcon={<FaCopy />}
                                                >
                                                    Copy
                                                </Button>
                                                <Code display="block" p={3} bg="gray.800" color="white" borderRadius="md">
                                                    npm run deploy:sepolia
                                                </Code>
                                            </Box>
                                        </Box>
                                    </VStack>

                                    <Alert status="success" mt={4}>
                                        <AlertIcon />
                                        <Box>
                                            <AlertTitle fontSize="sm">Output sẽ hiển thị:</AlertTitle>
                                            <Code fontSize="sm" mt={1}>
                                                GMToken deployed to: 0x1234...abcd
                                            </Code>
                                        </Box>
                                    </Alert>
                                </Box>

                                {/* Step 5 */}
                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontSize="lg" fontWeight="bold" mb={3}>
                                        Bước 5: Verify Contract (Optional)
                                    </Text>
                                    <Text mb={3}>
                                        Verify contract trên Etherscan để public source code:
                                    </Text>
                                    <Box position="relative">
                                        <Button
                                            size="xs"
                                            position="absolute"
                                            right={2}
                                            top={2}
                                            onClick={() => copyToClipboard('npx hardhat verify --network sepolia YOUR_CONTRACT_ADDRESS')}
                                            leftIcon={<FaCopy />}
                                        >
                                            Copy
                                        </Button>
                                        <Code display="block" p={3} bg="gray.800" color="white" borderRadius="md">
                                            npx hardhat verify --network sepolia YOUR_CONTRACT_ADDRESS
                                        </Code>
                                    </Box>
                                </Box>
                            </VStack>
                        </TabPanel>

                        <TabPanel>
                            <VStack spacing={6} align="stretch">
                                <Alert status="info">
                                    <AlertIcon />
                                    <AlertDescription>
                                        Sau khi deploy thành công, nhập contract address vào đây để lưu vào app
                                    </AlertDescription>
                                </Alert>

                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontWeight="bold" mb={3}>
                                        Contract Address:
                                    </Text>
                                    <Input
                                        placeholder="0x..."
                                        value={deployedAddress}
                                        onChange={(e) => setDeployedAddress(e.target.value)}
                                        fontFamily="monospace"
                                        size="lg"
                                    />
                                    <Button
                                        colorScheme="blue"
                                        size="lg"
                                        onClick={handleSaveAddress}
                                        mt={4}
                                        w="100%"
                                        isDisabled={!deployedAddress}
                                    >
                                        💾 Lưu Contract Address
                                    </Button>
                                </Box>

                                <Box p={4} bg="green.50" borderRadius="md">
                                    <Text fontWeight="bold" mb={2}>
                                        ✅ Sau khi lưu contract address:
                                    </Text>
                                    <OrderedList spacing={1} pl={4} fontSize="sm">
                                        <ListItem>Contract address được lưu vào localStorage</ListItem>
                                        <ListItem>Cập nhật trong tab Settings → API Settings</ListItem>
                                        <ListItem>Bắt đầu sử dụng app với contract của bạn</ListItem>
                                        <ListItem>Check-in nhận 50 GM hoặc mua tokens</ListItem>
                                    </OrderedList>
                                </Box>

                                <Divider />

                                <Box p={4} borderWidth={1} borderRadius="md">
                                    <Text fontWeight="bold" mb={3}>
                                        📝 View Contract trên Etherscan:
                                    </Text>
                                    {deployedAddress ? (
                                        <Link 
                                            href={`https://sepolia.etherscan.io/address/${deployedAddress}`}
                                            isExternal 
                                            color="blue.600"
                                        >
                                            {deployedAddress} <FaExternalLinkAlt style={{display: 'inline'}} />
                                        </Link>
                                    ) : (
                                        <Text fontSize="sm" color="gray.500">
                                            Nhập contract address để xem trên Etherscan
                                        </Text>
                                    )}
                                </Box>
                            </VStack>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </VStack>
        </Box>
    );
};

export default ContractDeploy;

