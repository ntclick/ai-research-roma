import asyncio
import aiohttp
import os
from typing import Dict, Any, List

class CryptoResearchAgent:
    def __init__(self):
        self.coingecko_api_key = os.getenv('COINGECKO_API_KEY')
        self.fal_api_key = os.getenv('FAL_AI_API_KEY')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
    async def research_coin(self, coin_symbol: str) -> Dict[str, Any]:
        """Research a specific cryptocurrency"""
        
        # Get basic coin data from CoinGecko
        coin_data = await self._get_coingecko_data(coin_symbol)
        
        if 'error' in coin_data:
            return {
                'coin': coin_symbol,
                'report': f"Không tìm thấy thông tin cho {coin_symbol}. Vui lòng kiểm tra lại tên hoặc ký hiệu coin.",
                'data': {},
                'analysis': {}
            }
        
        # Get price analysis
        price_analysis = await self._analyze_price_trends(coin_data)
        
        # Generate comprehensive report
        report = await self._generate_report(coin_symbol, coin_data, price_analysis)
        
        return {
            'coin': coin_symbol,
            'report': report,
            'data': coin_data,
            'analysis': price_analysis
        }
    
    async def _get_coingecko_data(self, coin_symbol: str) -> Dict:
        """Fetch data from CoinGecko API"""
        base_url = "https://api.coingecko.com/api/v3"
        
        headers = {}
        if self.coingecko_api_key:
            headers['x-cg-demo-api-key'] = self.coingecko_api_key
            
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                # Get coin ID first
                async with session.get(f"{base_url}/search?query={coin_symbol}") as resp:
                    search_data = await resp.json()
                    
                    if not search_data.get('coins'):
                        return {'error': 'Coin not found'}
                        
                    coin_id = search_data['coins'][0]['id']
                
                # Get detailed coin data
                async with session.get(
                    f"{base_url}/coins/{coin_id}?localization=false&tickers=false&market_data=true"
                ) as resp:
                    return await resp.json()
        except Exception as e:
            return {'error': str(e)}
    
    async def _analyze_price_trends(self, coin_data: Dict) -> Dict:
        """Analyze price trends from coin data"""
        if 'error' in coin_data:
            return {'error': 'No price data available'}
            
        market_data = coin_data.get('market_data', {})
        
        return {
            'current_price_usd': market_data.get('current_price', {}).get('usd'),
            'market_cap': market_data.get('market_cap', {}).get('usd'),
            'market_cap_rank': coin_data.get('market_cap_rank'),
            'volume_24h': market_data.get('total_volume', {}).get('usd'),
            'price_change_24h': market_data.get('price_change_percentage_24h'),
            'price_change_7d': market_data.get('price_change_percentage_7d'),
            'price_change_30d': market_data.get('price_change_percentage_30d'),
            'ath': market_data.get('ath', {}).get('usd'),
            'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd'),
            'atl': market_data.get('atl', {}).get('usd'),
            'atl_change_percentage': market_data.get('atl_change_percentage', {}).get('usd'),
        }
    
    async def _generate_report(self, coin_symbol: str, coin_data: Dict, price_analysis: Dict) -> str:
        """Generate a comprehensive research report"""
        
        name = coin_data.get('name', coin_symbol)
        symbol = coin_data.get('symbol', '').upper()
        
        report = f"""
📊 BÁO CÁO NGHIÊN CỨU: {name} ({symbol})

🔍 THÔNG TIN CƠ BẢN:
- Tên: {name}
- Ký hiệu: {symbol}
- Rank: #{price_analysis.get('market_cap_rank', 'N/A')}

💰 GIÁ & THỊ TRƯỜNG:
- Giá hiện tại: ${price_analysis.get('current_price_usd', 0):,.2f}
- Market Cap: ${price_analysis.get('market_cap', 0):,.0f}
- Khối lượng 24h: ${price_analysis.get('volume_24h', 0):,.0f}

📈 BIẾN ĐỘNG GIÁ:
- 24 giờ: {price_analysis.get('price_change_24h', 0):.2f}%
- 7 ngày: {price_analysis.get('price_change_7d', 0):.2f}%
- 30 ngày: {price_analysis.get('price_change_30d', 0):.2f}%

🎯 ĐỈNH/ĐÁY LỊCH SỬ:
- ATH: ${price_analysis.get('ath', 0):,.2f} ({price_analysis.get('ath_change_percentage', 0):.2f}% từ ATH)
- ATL: ${price_analysis.get('atl', 0):,.8f} ({price_analysis.get('atl_change_percentage', 0):.2f}% từ ATL)

📝 MÔ TẢ:
{coin_data.get('description', {}).get('en', 'Không có mô tả')[:500]}...

🔗 LIÊN KẾT:
- Website: {', '.join(coin_data.get('links', {}).get('homepage', [])[:2])}
- Explorer: {', '.join(coin_data.get('links', {}).get('blockchain_site', [])[:2])}
"""
        
        return report.strip()

    async def analyze_x_post(self, post_url: str) -> Dict[str, Any]:
        """Analyze a Twitter/X post"""
        
        analysis = f"""
🐦 PHÂN TÍCH BÀI POST X/TWITTER

URL: {post_url}

📝 TỔNG QUAN:
Đây là một bài post trên X/Twitter liên quan đến crypto.

⚠️ LƯU Ý:
- Luôn verify thông tin từ nhiều nguồn
- Cẩn thận với các bài post có tính chất FOMO
- Kiểm tra độ tin cậy của tài khoản đăng bài
- Đừng đưa ra quyết định đầu tư chỉ dựa trên một bài post

💡 KHUYẾN NGHỊ:
- Research thêm về project từ các nguồn chính thống
- Kiểm tra whitepaper và roadmap
- Đánh giá team và community
- Phân tích tokenomics
"""
        
        return {
            'url': post_url,
            'analysis': analysis
        }
    
    async def create_x_post(self, data: str, perspective: str = "neutral") -> Dict[str, Any]:
        """Create X post from provided data"""
        
        # Simple post generation based on perspective
        perspectives = {
            "bullish": "🚀",
            "bearish": "⚠️",
            "neutral": "📊"
        }
        
        emoji = perspectives.get(perspective, "📊")
        
        # Create a concise post (max 280 chars)
        post = f"{emoji} {data[:250]} #Crypto #Blockchain"
        
        if len(post) > 280:
            post = post[:277] + "..."
        
        return {
            'post_content': post,
            'character_count': len(post),
            'perspective': perspective
        }
    
    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        """Generate image using fal.ai Flux"""
        
        try:
            # Note: Requires fal_client to be installed and configured
            # pip install fal-client
            import fal_client
            
            handler = await fal_client.submit_async(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "image_size": "square_hd",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                },
            )
            
            result = await handler.get()
            
            return {
                'success': True,
                'image_url': result['images'][0]['url'],
                'prompt': prompt
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'fal_client chưa được cài đặt. Chạy: pip install fal-client'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

