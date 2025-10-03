import asyncio
import json
import websockets
import os
import sys
from pathlib import Path
import locale
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Load API keys from .env

# Fix Windows console encoding for Vietnamese characters
import builtins
_builtin_print = builtins.print
def safe_print(*args, **kwargs):
    """Print with automatic fallback for Unicode errors on Windows"""
    safe_args = []
    for arg in args:
        if isinstance(arg, str):
            # Replace problematic Vietnamese characters with ASCII
            safe_str = arg.replace('ạ', 'a').replace('ả', 'a').replace('ã', 'a')
            safe_str = safe_str.replace('ê', 'e').replace('ế', 'e').replace('ề', 'e')
            safe_str = safe_str.replace('ô', 'o').replace('ố', 'o').replace('ồ', 'o')
            safe_str = safe_str.replace('ư', 'u').replace('ứ', 'u').replace('ừ', 'u')
            safe_str = safe_str.replace('đ', 'd').replace('Đ', 'D')
            safe_args.append(safe_str)
        else:
            safe_args.append(arg)
    try:
        _builtin_print(*safe_args, **kwargs)
    except:
        pass  # Silently ignore print errors
builtins.print = safe_print

# Add parent directory to path to import roma_agents
sys.path.append(str(Path(__file__).parent))

# Import ROMA Framework (REQUIRED)
from roma_agents.crypto_roma_agent import CryptoROMAAgent
from roma_agents.api_integrations import APIIntegrations

print("="*60)
print("[INIT] 🚀 ROMA Framework ACTIVE")
print("[INIT] 🧠 AI: Gemini (Primary) + OpenAI (Backup)")
print("[INIT] 📊 Data: CoinGecko + RSS News + fal.ai")
print("[INIT] 🔄 Recursive Open Meta-Agent v0.2")
print("[INIT] 👨‍💻 Author: @trungkts29 (https://x.com/trungkts29)")
print("="*60)
USE_ROMA = True

class ResearchWebSocketServer:
    def __init__(self, host=None, port=None):
        # Railway provides PORT env variable, defaults to 5001 for local dev
        self.host = host or os.getenv('HOST', '0.0.0.0')
        self.port = port or int(os.getenv('PORT', 5001))
        print(f"[CONFIG] Server will bind to {self.host}:{self.port}")
        self.conversation_history = {}  # Track conversation per client
        
        # Initialize ROMA Agent or fallback to API Integrations
        if USE_ROMA:
            self.roma_agent = CryptoROMAAgent()
            self.api_integrations = self.roma_agent.api_integrations
            print("[INIT] Using ROMA Agent for research")
        else:
            self.api_integrations = APIIntegrations()
            self.roma_agent = None
            print("[INIT] Using direct API integrations")
        
        self.connected_clients = set()
    
    async def register_client(self, websocket):
        """Register a new client"""
        self.connected_clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.connected_clients)}")
        
    async def unregister_client(self, websocket):
        """Unregister a client"""
        self.connected_clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(self.connected_clients)}")
    
    async def handle_message(self, websocket, message_data):
        """Handle incoming messages from clients"""
        try:
            message_type = message_data.get('type')
            tool = message_data.get('tool')
            content = message_data.get('content')
            user = message_data.get('user')
            
            print(f"Processing request - Tool: {tool}, User: {user[:8]}...")
            
            # Process based on tool selection (only research tool now)
            if tool == 'research':
                # Smart research with API integration + context
                user_id = message_data.get('user', 'default')
                response = await self._handle_research_request(content, user_id)
            else:
                response = {
                    'type': 'error',
                    'content': f'Tool không được hỗ trợ: {tool}. Chỉ hỗ trợ Research tool.',
                    'sender': 'ai'
                }
            
            # Send response back to client
            await websocket.send(json.dumps(response))
            print(f"Response sent for tool: {tool}")
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            error_response = {
                'type': 'error',
                'content': f'Lỗi xử lý: {str(e)}',
                'sender': 'ai'
            }
            await websocket.send(json.dumps(error_response))
    
    async def handle_client(self, websocket):
        """Handle individual client connections"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                try:
                    message_data = json.loads(message)
                    await self.handle_message(websocket, message_data)
                except json.JSONDecodeError:
                    error_response = {
                        'type': 'error',
                        'content': 'Invalid JSON format',
                        'sender': 'ai'
                    }
                    await websocket.send(json.dumps(error_response))
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by client")
        except Exception as e:
            print(f"Error in client handler: {str(e)}")
        finally:
            await self.unregister_client(websocket)

    async def _handle_research_request(self, query: str, user_id: str = 'default'):
        """Handle research requests using ROMA Framework or direct API routing"""
        try:
            # Get conversation history for context
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            history = self.conversation_history[user_id]
            
            # Add context to query if pronouns detected
            enhanced_query = query
            if any(word in query.lower() for word in ['it', 'that', 'this', 'them', 'those', 'no', 'nó', 'đó', 'này']):
                # Use OpenAI to resolve pronoun with context
                if history:
                    last_coins = [msg.get('coin') for msg in history[-3:] if msg.get('coin')]
                    if last_coins:
                        enhanced_query = f"{query} (context: referring to {last_coins[-1]})"
                        print(f"[CONTEXT] Enhanced query: {enhanced_query}")
            
            # Use ROMA Agent if available
            if USE_ROMA and self.roma_agent:
                print(f"[ROMA] Processing query: {enhanced_query[:50]}...")
                
                # Create ROMA task
                task = {
                    'query': enhanced_query,
                    'type': 'research',
                    'history': history[-5:] if history else []  # Last 5 messages
                }
                
                # Use ROMA's solve() method
                result = await self.roma_agent.solve(task)
                
                if result['success']:
                    data = result.get('data', {})
                    api_source = result.get('api', 'ROMA')
                    image_url = None  # Initialize
                    
                    # Format content based on API type
                    if 'content' in data:
                        # Perplexity, RSS, OpenAI - already has formatted content
                        content = data['content']
                    elif 'image_url' in data:
                        # fal.ai - Image generation
                        image_url = data['image_url']  # Extract image URL
                        content = f"🎨 **Image Generated!**\n\n"
                        content += f"**Model:** {data.get('model', 'FLUX.1')}\n"
                        content += f"**Resolution:** {data.get('width', 'N/A')}x{data.get('height', 'N/A')}\n"
                        content += f"**Prompt:** {data.get('prompt', 'N/A')}\n\n"
                        content += f"Source: {data.get('api_source', 'fal.ai')}"
                    elif 'price' in data:
                        # CoinGecko - format price data
                        price_str = f"${data['price']:,.2f}" if data.get('price', 0) > 0 else "N/A"
                        change_str = f"{data.get('change_24h', 0):+.2f}%" if data.get('change_24h') else "N/A"
                        market_cap_str = f"${data.get('market_cap', 0):,.0f}" if data.get('market_cap', 0) > 0 else "N/A"
                        volume_str = f"${data.get('volume', 0):,.0f}" if data.get('volume', 0) > 0 else "N/A"
                        
                        content = f"**{data.get('name', 'Unknown')} ({data.get('symbol', 'N/A')})**\n\n"
                        content += f"Price: {price_str}\n"
                        content += f"24h Change: {change_str}\n"
                        content += f"Market Cap: {market_cap_str}\n"
                        content += f"Volume: {volume_str}\n"
                        if data.get('website'):
                            content += f"Website: {data['website']}\n"
                        content += f"\nSource: {data.get('api_source', api_source)}"
                    else:
                        content = f"❌ No valid data format from {api_source}"
                    
                    # Extract only AI synthesis part
                    if 'subtask_count' in result:
                        if "[AI SYNTHESIS]" in content:
                            synthesis_part = content.split("[AI SYNTHESIS]")[-1].strip()
                            content = synthesis_part
                        # Already clean content, no extra formatting needed
                    
                    # Save to conversation history
                    coin_mentioned = None
                    if 'coin_id' in data:
                        coin_mentioned = data.get('coin_id')
                    elif 'name' in data:
                        coin_mentioned = data.get('symbol', data.get('name'))
                    
                    self.conversation_history[user_id].append({
                        'query': query,
                        'coin': coin_mentioned,
                        'api': api_source,
                        'timestamp': asyncio.get_event_loop().time()
                    })
                    
                    # Keep only last 10 messages
                    if len(self.conversation_history[user_id]) > 10:
                        self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
                    
                    # Build response
                    response = {
                        'type': 'research_response',
                        'tool': 'research',
                        'content': content,
                        'sender': 'ai',
                        'api_source': api_source,
                        'has_error': False,
                        'retry_available': False,
                        'roma_powered': True
                    }
                    
                    # Add image_url if generated
                    if image_url:
                        response['image_url'] = image_url
                        print(f"[RESPONSE] Including image_url: {image_url[:50]}...")
                    
                    return response
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"[ROMA] ROMA execution failed: {error_msg}")
                    return {
                        'type': 'error',
                        'content': f"❌ **ROMA Error:** {error_msg}",
                        'sender': 'ai',
                        'api_source': 'ROMA',
                        'has_error': True,
                        'retry_available': True
                    }
            
            # Fallback to direct API routing
            # HYBRID APPROACH: OpenAI for routing (better intent) + Gemini for heavy context (cheaper)
            print(f"[ROUTING] Analyzing query with OpenAI GPT-4.1 Mini (routing logic): {query[:50]}...")
            
            # Step 1: Use OpenAI GPT-4.1 Mini for intent understanding & routing
            context_analysis = await self.api_integrations.analyze_context_with_openai(query)
            
            if not context_analysis['success']:
                print(f"[ROUTING] OpenAI analysis failed, using fallback: {context_analysis.get('error')}")
                # Fallback to simple keyword matching
                return await self._handle_research_request_fallback(query)
            
            selected_api = context_analysis['selected_api']
            reason = context_analysis['reason']
            confidence = context_analysis['confidence']
            
            print(f"[ROUTING] OpenAI selected: {selected_api} (confidence: {confidence}) - {reason}")
            
            # Route to appropriate API based on OpenAI analysis
            if selected_api == 'ask_user':
                # Ask user for clarification
                clarification = context_analysis.get('clarification', 'Bạn có thể làm rõ yêu cầu của mình không?')
                return {
                    'type': 'research_response',
                    'tool': 'research',
                    'content': f"🤔 **Cần làm rõ yêu cầu:**\n\n{clarification}\n\n💡 **Gợi ý:**\n• \"giá [coin]\" - Xem giá coin\n• \"[coin] news\" - Tin tức về coin\n• \"có nên mua [coin] không?\" - Phân tích đầu tư\n• \"[coin] price\" - Giá coin bằng tiếng Anh",
                    'sender': 'ai',
                    'api_source': 'Clarification',
                    'has_error': False,
                    'retry_available': False
                }
            elif selected_api == 'coingecko':
                # Step 2: Use OpenAI GPT-4o-mini to extract coin (name/symbol/ticker)
                print(f"[ROUTING] Executing: CoinGecko API with OpenAI GPT-4o-mini extraction")
                coin_extraction = await self.api_integrations.extract_coin_name_with_openai(query)
                
                if coin_extraction['success']:
                    coin_name = coin_extraction['coin_id']
                    print(f"[ROUTING] OpenAI extracted coin ID: {coin_name}")
                else:
                    # Fallback to simple extraction with coin mapping
                    query_lower = query.lower()
                    
                    # Simple coin mapping for fallback
                    fallback_coin_mapping = {
                        'btc': 'bitcoin',
                        'eth': 'ethereum',
                        'sol': 'solana',
                        'ada': 'cardano',
                        'dot': 'polkadot',
                        'link': 'chainlink',
                        'matic': 'matic-network',
                        'polygon': 'matic-network',
                        'avax': 'avalanche-2',
                        'arb': 'arbitrum',
                        'op': 'optimism',
                        'atom': 'cosmos',
                        'near': 'near',
                        'algo': 'algorand',
                        'ftm': 'fantom',
                        'inj': 'injective-protocol',
                        'sei': 'sei-network',
                        'sui': 'sui',
                        'apt': 'aptos',
                        'aptos': 'aptos',
                        'mina': 'mina-protocol',
                        'celo': 'celo',
                        'succinct': 'succinct',
                        'sp1': 'succinct',
                        'prove': 'provenance-blockchain',
                        'hash': 'provenance-blockchain',
                        'provenance': 'provenance-blockchain',
                        'newton protocol': 'newton-protocol',
                        'newt': 'newton-protocol',
                        'newton project': 'newton-project',
                        'newton on base': 'newton-on-base',
                        'ntn': 'newton',
                        'pepe': 'pepe',
                        'doge': 'dogecoin',
                        'dogecoin': 'dogecoin',
                        'shib': 'shiba-inu',
                        'shiba': 'shiba-inu',
                        'bonk': 'bonk',
                        'floki': 'floki',
                        'wojak': 'wojak',
                        'uni': 'uniswap',
                        'uniswap': 'uniswap',
                        'cake': 'pancakeswap-token',
                        'pancakeswap': 'pancakeswap-token',
                        'aave': 'aave',
                        'comp': 'compound-governance-token',
                        'compound': 'compound-governance-token',
                        'crv': 'curve-dao-token',
                        'curve': 'curve-dao-token',
                        'mkr': 'maker',
                        'maker': 'maker',
                        'rndr': 'render-token',
                        'render': 'render-token',
                        'fet': 'fetch-ai',
                        'fetch': 'fetch-ai',
                        'sand': 'the-sandbox',
                        'sandbox': 'the-sandbox',
                        'axs': 'axie-infinity',
                        'axie': 'axie-infinity',
                        'usdt': 'tether',
                        'tether': 'tether',
                        'usdc': 'usd-coin',
                        'dai': 'dai'
                    }
                    
                    # Extract potential coin name
                    words = query_lower.replace('giá', '').replace('price', '').replace('of', '').replace('the', '').replace('check', '').strip().split()
                    potential_coin = words[0] if words else None
                    
                    # Map to CoinGecko ID
                    coin_name = fallback_coin_mapping.get(potential_coin, potential_coin)
                    print(f"[ROUTING] Fallback extraction: '{potential_coin}' -> '{coin_name}'")
                
                if coin_name:
                    print(f"[ROUTING] Trying to fetch data for coin: {coin_name}")
                    result = await self.api_integrations.get_coingecko_data(coin_name)
                    if result['success']:
                        # Format price data nicely
                        price_str = f"${result['price']:,.2f}" if result['price'] > 0 else "N/A"
                        change_str = f"{result['change_24h']:+.2f}%" if result['change_24h'] else "N/A"
                        market_cap_str = f"${result['market_cap']:,.0f}" if result['market_cap'] > 0 else "N/A"
                        volume_str = f"${result['volume']:,.0f}" if result['volume'] > 0 else "N/A"
                        
                        content = f"📊 **{result['name']} ({result['symbol']})**\n\n"
                        content += f"💰 **Giá hiện tại:** {price_str}\n"
                        content += f"📈 **Thay đổi 24h:** {change_str}\n"
                        content += f"🏪 **Vốn hóa thị trường:** {market_cap_str}\n"
                        content += f"📊 **Khối lượng giao dịch:** {volume_str}\n"
                        if result.get('website'):
                            content += f"🌐 **Website:** {result['website']}\n"
                        content += f"\n💡 **Nguồn:** {result['api_source']}\n"
                        content += f"🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                        api_source = result['api_source']
                    else:
                        # Handle different error types
                        error_msg = result.get('error', '')
                        if "API key invalid" in str(error_msg) or "401" in str(error_msg):
                            content = f"❌ **CoinGecko API Key Issue:**\n\nAPI key không hợp lệ hoặc đã hết hạn. Vui lòng:\n\n• Kiểm tra CoinGecko API key trong backend/.env\n• Đảm bảo key còn hiệu lực\n• Liên hệ admin để cập nhật key\n\n💡 **Nguồn:** CoinGecko API\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                        elif "rate limit" in str(error_msg).lower() or "429" in str(error_msg):
                            content = f"❌ **Rate Limit Exceeded:**\n\nCoinGecko API đã vượt quá giới hạn request. Vui lòng thử lại sau 1 phút.\n\n💡 **Nguồn:** CoinGecko API\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                        elif "404" in str(error_msg) or "not found" in str(error_msg).lower():
                            content = f"❌ **Không tìm thấy coin:** '{coin_name}'\n\nCoin này không có trong CoinGecko database. Vui lòng kiểm tra:\n\n• Tên coin chính xác (ví dụ: bitcoin, ethereum, pepe)\n• Coin có thể chưa được list trên CoinGecko\n• Thử với tên khác của coin\n\n💡 **Nguồn:** CoinGecko API\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                        else:
                            content = f"❌ **API Error:** {error_msg}\n\n🔄 **Retry available** - Click retry button to try again"
                        api_source = result.get('api_source', 'CoinGecko')
                else:
                    content = f"📊 **CoinGecko Analysis:**\n\nTôi đã phát hiện yêu cầu về giá coin nhưng không tìm thấy coin cụ thể. Vui lòng chỉ rõ tên coin:\n\n**Major Coins:** Bitcoin (BTC), Ethereum (ETH), Solana (SOL), Cardano (ADA)\n**Layer 1/2:** Sui (SUI), Aptos (APT), Near (NEAR), Sei (SEI)\n**Meme Coins:** Pepe (PEPE), Dogecoin (DOGE), Shiba Inu (SHIB), Bonk (BONK)\n**DeFi:** Uniswap (UNI), Aave (AAVE), Compound (COMP)\n**AI/Gaming:** Render (RNDR), Fetch.ai (FET), Sandbox (SAND)\n**Stablecoins:** Tether (USDT), USD Coin (USDC), DAI\n\n💡 **Nguồn:** CoinGecko API\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                    api_source = 'CoinGecko'
                    
            elif selected_api == 'perplexity':
                # Use Perplexity
                print(f"[ROUTING] Executing: Perplexity AI")
                result = await self.api_integrations.get_perplexity_research(query)
                if result['success']:
                    content = f"🔍 **Deep Research (Perplexity AI):**\n\n{result['content']}\n\n💡 **Source:** {result['api_source']}\n🎯 **AI Analysis:** {reason} (confidence: {confidence:.1%})"
                    api_source = result['api_source']
                else:
                    content = f"❌ **API Error:** {result.get('error')}\n\n🔄 **Retry available** - Click retry button to try again"
                    api_source = result.get('api_source', 'Perplexity AI')
                    
            elif selected_api == 'openai':
                # Use OpenAI for synthesis
                print(f"[ROUTING] Executing: OpenAI Synthesis")
                result = await self.api_integrations.analyze_with_openai(query, "Tổng hợp thông tin từ chat và các nguồn khác")
                if result['success']:
                    content = f"🤖 **AI Tổng hợp (OpenAI GPT-4):**\n\n{result['analysis']}\n\n💡 **Nguồn:** {result['api_source']}\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                    api_source = result['api_source']
                else:
                    content = f"❌ **API Error:** {result.get('error')}\n\n🔄 **Retry available** - Click retry button to try again"
                    api_source = result.get('api_source', 'OpenAI GPT-4')
                    
            elif selected_api == 'falai':
                # Use fal.ai for image generation
                print(f"[ROUTING] Executing: fal.ai Image Generation")
                result = await self.api_integrations.generate_image_with_fal(query)
                if result['success']:
                    content = f"🎨 **Hình ảnh đã tạo:**\n\n**Prompt:** {query}\n**Model:** {result['model']}\n\n💡 **Nguồn:** {result['api_source']}\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                    api_source = result['api_source']
                    image_url = result['image_url']
                else:
                    content = f"❌ **API Error:** {result.get('error')}\n\n🔄 **Retry available** - Click retry button to try again"
                    api_source = result.get('api_source', 'fal.ai')
                    image_url = None
                    
            elif selected_api == 'rss_news':
                # Use RSS News
                print(f"[ROUTING] Executing: RSS News")
                result = await self.api_integrations.get_rss_news(query)
                if result['success']:
                    content = f"{result['content']}\n\n💡 **Nguồn:** {result['api_source']}\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                    api_source = result['api_source']
                else:
                    content = f"❌ **API Error:** {result.get('error')}\n\n🔄 **Retry available** - Click retry button to try again"
                    api_source = result.get('api_source', 'RSS News')
            else:
                # Default to Perplexity
                print(f"[ROUTING] Default: Perplexity AI")
                result = await self.api_integrations.get_perplexity_research(query)
                if result['success']:
                    content = f"🔍 **Research (Perplexity AI):**\n\n{result['content']}\n\n💡 **Nguồn:** {result['api_source']}\n🎯 **AI phân tích:** {reason} (độ tin cậy: {confidence:.0%})"
                    api_source = result['api_source']
                else:
                    content = f"❌ **API Error:** {result.get('error')}\n\n🔄 **Retry available** - Click retry button to try again"
                    api_source = result.get('api_source', 'Perplexity AI')
            
            response = {
                'type': 'research_response',
                'tool': 'research',
                'content': content,
                'sender': 'ai',
                'api_source': api_source,
                'has_error': 'API Error' in content,
                'retry_available': 'API Error' in content
            }
            
            # Add image URL if available (for fal.ai responses)
            if 'image_url' in locals() and image_url:
                response['image_url'] = image_url
                
            return response
            
        except Exception as e:
            print(f"[ERROR] Research request failed: {str(e)}")
            return {
                'type': 'error',
                'content': f'❌ **System Error:** {str(e)}\n\n🔄 **Retry available** - Click retry button to try again',
                'sender': 'ai',
                'api_source': 'System',
                'has_error': True,
                'retry_available': True
            }

    async def _handle_research_request_fallback(self, query: str):
        """Fallback method using simple keyword matching when OpenAI fails"""
        print(f"[ROUTING] Using fallback keyword matching for: {query[:50]}...")
        
        query_lower = query.lower()
        
        # Simple keyword matching
        if any(word in query_lower for word in ['price', 'market', 'giá', 'giá']):
            # CoinGecko fallback with expanded coin list
            coin_mapping = {
                # Major coins
                'bitcoin': 'bitcoin', 'btc': 'bitcoin',
                'ethereum': 'ethereum', 'eth': 'ethereum',
                'solana': 'solana', 'sol': 'solana',
                'cardano': 'cardano', 'ada': 'cardano',
                'polkadot': 'polkadot', 'dot': 'polkadot',
                'chainlink': 'chainlink', 'link': 'chainlink',
                'avalanche': 'avalanche-2', 'avax': 'avalanche-2',
                'polygon': 'matic-network', 'matic': 'matic-network',
                
                # Layer 1 & 2
                'sui': 'sui', 'aptos': 'aptos', 'apt': 'aptos',
                'near': 'near-protocol', 'near': 'near-protocol',
                'algorand': 'algorand', 'algo': 'algorand',
                'fantom': 'fantom', 'ftm': 'fantom',
                'cosmos': 'cosmos', 'atom': 'cosmos',
                'injective': 'injective-protocol', 'inj': 'injective-protocol',
                'sei': 'sei-network',
                
                # Meme coins
                'pepe': 'pepe', 'doge': 'dogecoin', 'shiba': 'shiba-inu',
                'bonk': 'bonk', 'floki': 'floki', 'wojak': 'wojak',
                
                # DeFi tokens
                'uniswap': 'uniswap', 'uni': 'uniswap',
                'pancakeswap': 'pancakeswap-token', 'cake': 'pancakeswap-token',
                'aave': 'aave', 'compound': 'compound-governance-token', 'comp': 'compound-governance-token',
                'curve': 'curve-dao-token', 'crv': 'curve-dao-token',
                'maker': 'maker', 'mkr': 'maker',
                
                # AI & Gaming
                'render': 'render-token', 'rndr': 'render-token',
                'fetch': 'fetch-ai', 'fet': 'fetch-ai',
                'the-sandbox': 'sandbox', 'sand': 'sandbox',
                'axie': 'axie-infinity', 'axs': 'axie-infinity',
                
                # Stablecoins
                'tether': 'tether', 'usdt': 'tether',
                'usd-coin': 'usd-coin', 'usdc': 'usd-coin',
                'dai': 'dai'
            }
            
            # Extract coin name from query
            coin_name = None
            for coin_name_key, coin_id_map in coin_mapping.items():
                if coin_name_key in query_lower:
                    coin_name = coin_id_map
                    break
            
            # If no specific coin found, try to extract from query directly
            if not coin_name:
                words = query_lower.replace('giá', '').replace('price', '').replace('of', '').replace('the', '').strip().split()
                if words:
                    potential_coin = words[0]
                    coin_name = potential_coin
            
            if coin_name:
                print(f"[FALLBACK] Trying to fetch data for coin: {coin_name}")
                result = await self.api_integrations.get_coingecko_data(coin_name)
                if result['success']:
                    content = f"📊 **{result['name']} ({result['symbol']})**\n\n💰 **Giá hiện tại:** ${result['price']:,.2f}\n📈 **Thay đổi 24h:** {result['change_24h']:+.2f}%\n\n💡 **Nguồn:** {result['api_source']}\n🎯 **Method:** Keyword fallback"
                    return {
                        'type': 'research_response',
                        'tool': 'research',
                        'content': content,
                        'sender': 'ai',
                        'api_source': result['api_source'],
                        'has_error': False,
                        'retry_available': False
                    }
                else:
                    # Handle coin not found in fallback
                    if "404" in str(result.get('error', '')) or "not found" in str(result.get('error', '')).lower():
                        content = f"❌ **Không tìm thấy coin:** '{coin_name}'\n\nCoin này không có trong CoinGecko database.\n\n💡 **Nguồn:** CoinGecko API (Fallback)\n🎯 **Method:** Keyword fallback"
                        return {
                            'type': 'research_response',
                            'tool': 'research',
                            'content': content,
                            'sender': 'ai',
                            'api_source': 'CoinGecko (Fallback)',
                            'has_error': True,
                            'retry_available': False
                        }
        
        # Default to Perplexity
        result = await self.api_integrations.get_perplexity_research(query)
        if result['success']:
            content = f"🔍 **Research (Fallback):**\n\n{result['content']}\n\n💡 **Source:** {result['api_source']}\n🎯 **Method:** Keyword fallback"
            return {
                'type': 'research_response',
                'tool': 'research',
                'content': content,
                'sender': 'ai',
                'api_source': result['api_source'],
                'has_error': False,
                'retry_available': False
            }
        else:
            return {
                'type': 'error',
                'content': f'❌ **Fallback Error:** {result.get("error")}\n\n🔄 **Retry available** - Click retry button to try again',
                'sender': 'ai',
                'api_source': 'Fallback',
                'has_error': True,
                'retry_available': True
            }

    async def _handle_image_generation(self, prompt: str):
        """Handle image generation with fal.ai"""
        try:
            result = await self.api_integrations.generate_image_with_fal(prompt)
            if result['success']:
                return {
                    'type': 'research_response',
                    'tool': 'generate-image',
                    'content': f"🎨 **Image Generated Successfully!**\n\n**Prompt:** {prompt}\n**Model:** {result['model']}\n**Resolution:** 1080x1080 (Twitter optimized)\n\n✨ Ready for X/Twitter post!",
                    'image_url': result['image_url'],
                    'sender': 'ai'
                }
            else:
                return {
                    'type': 'error',
                    'content': f"❌ Image generation failed: {result.get('error')}",
                    'sender': 'ai'
                }
        except Exception as e:
            return {
                'type': 'error',
                'content': f'Image generation error: {str(e)}',
                'sender': 'ai'
            }

    async def start(self):
        """Start the WebSocket server"""
        async with websockets.serve(
            self.handle_client, 
            self.host, 
            self.port,
            # Allow connections from any origin (for development)
            origins=None  # Accept all origins in development
        ):
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            print("Waiting for connections...")
            await asyncio.Future()  # run forever

# Start WebSocket server
if __name__ == "__main__":
    server = ResearchWebSocketServer()
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")

