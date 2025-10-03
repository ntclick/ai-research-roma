import asyncio
import aiohttp
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Load API keys from .env

class APIIntegrations:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.coingecko_api_key = os.getenv('COINGECKO_API_KEY')
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        self.fal_api_key = os.getenv('FAL_API_KEY')
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')  # Railway uses GOOGLE_API_KEY
        
        # Debug: Check if keys are loaded
        print("[DEBUG] API Keys Status:")
        print(f"  GOOGLE_API_KEY: {'Loaded (' + self.gemini_api_key[:20] + '...)' if self.gemini_api_key else 'NOT FOUND'}")
        print(f"  OPENAI_API_KEY: {'Loaded' if self.openai_api_key else 'NOT FOUND'}")
        
        print("============================================================")
        print("[ROMA Framework - AI Architecture]")
        print(f"  🧠 Brain (Routing & Interaction): OpenAI GPT-4o-mini {'✓' if self.openai_api_key else '✗'}")
        print(f"  🤖 Worker (Simple Answers): Google Gemini {'✓' if self.gemini_api_key else '✗'}")
        print("[Data Sources]")
        print(f"  📊 CoinGecko API: {'✓' if self.coingecko_api_key else '✗'}")
        print(f"  📰 RSS News: ✓")
        print(f"  🎨 fal.ai Image: {'✓' if self.fal_api_key else '✗'}")
        print("============================================================")

    async def analyze_context_with_openai(self, query: str) -> Dict[str, Any]:
        """BRAIN: OpenAI routes queries and decides what info to send to other functions"""
        if not self.openai_api_key:
            return {'success': False, 'error': 'OpenAI API key required for routing', 'api_source': 'None'}
        
        print(f"[API CALL] OpenAI: Analyzing context for query: {query[:50]}...")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are an AI routing expert. Route queries to the most appropriate API.

Available APIs:
1. CoinGecko - ONLY for specific price/market cap/volume queries: "price", "giá", "market cap"
2. Perplexity AI - For explanations, definitions, deep analysis, research, "what is", "explain", "why", "how", "should I"
3. OpenAI - For summarizing, combining info from multiple sources
4. fal.ai - For image generation
5. rss_news - For latest news: "news", "tin tức"

ROUTING RULES (in priority order):
1. X/Twitter URLs ("x.com", "twitter.com", "analyze tweet"): → twitter_analysis
2. Questions/definitions ("what is", "explain"): → perplexity
3. Specific price queries ("btc price", "check price"): → coingecko
4. News requests ("news", "updates"): → rss_news
5. Image generation ("create image", "generate image"): → falai
6. Vague queries: → ask_user

RESPONSE LANGUAGE:
- ALWAYS respond in English (never Vietnamese)

Return ONLY JSON:
{
    "selected_api": "coingecko|perplexity|falai|rss_news|twitter_analysis|ask_user",
    "reason": "Why this API",
    "confidence": 0.0-1.0,
    "clarification": "For ask_user only, IN ENGLISH"
}

Examples:
- "https://x.com/user/status/123" → {"selected_api": "twitter_analysis", "reason": "X/Twitter URL", "confidence": 0.95}
- "analyze tweet x.com/..." → {"selected_api": "twitter_analysis", "reason": "Tweet analysis", "confidence": 0.9}
- "bitcoin price" → {"selected_api": "coingecko", "reason": "Price query", "confidence": 0.95}
- "coin là gì" → {"selected_api": "perplexity", "reason": "Definition needed", "confidence": 0.9}
- "btc news" → {"selected_api": "rss_news", "reason": "Latest news", "confidence": 0.9}
- "create image btc" → {"selected_api": "falai", "reason": "Image generation", "confidence": 0.9}"""
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            "max_tokens": 150,
            "temperature": 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content'].strip()
                        
                        # Parse JSON response
                        try:
                            result = json.loads(content)
                            print(f"[BRAIN] OpenAI routing result: {result}")
                            return {
                                'success': True,
                                'selected_api': result.get('selected_api', 'perplexity'),
                                'reason': result.get('reason', 'Default routing'),
                                'confidence': result.get('confidence', 0.7),
                                'clarification': result.get('clarification', ''),
                                'api_source': 'OpenAI Brain'
                            }
                        except json.JSONDecodeError:
                            print(f"[API CALL] OpenAI: Failed to parse JSON response: {content}")
                            return {
                                'success': False,
                                'error': 'Invalid JSON response from OpenAI',
                                'api_source': 'OpenAI GPT-4.1 Mini'
                            }
                    else:
                        error_text = await response.text()
                        print(f"[API CALL] OpenAI: HTTP {response.status}: {error_text}")
                        return {
                            'success': False,
                            'error': f'OpenAI API error: {response.status} - {error_text}',
                            'api_source': 'OpenAI GPT-4.1 Mini'
                        }
        except Exception as e:
            error_msg = str(e)
            print(f"[API CALL] OpenAI: Exception: {error_msg}")
            return {'success': False, 'error': error_msg, 'api_source': 'OpenAI GPT-4.1 Mini'}

    async def get_rss_news(self, query: str) -> Dict[str, Any]:
        """OPTIMIZED: Fast, accurate, cost-free RSS news"""
        print(f"[RSS] Fetching news for: {query[:50]}...")
        
        import feedparser
        import re
        
        # STEP 1: Simple coin extraction (NO OpenAI - Save cost!)
        coin_name = None
        query_lower = query.lower()
        
        # Coin mapping with regex patterns
        coin_patterns = {
            'bitcoin': r'\b(btc|bitcoin)\b',
            'ethereum': r'\b(eth|ethereum)\b',
            'solana': r'\b(sol|solana)\b',
            'sui': r'\b(sui)\b',
            'cardano': r'\b(ada|cardano)\b',
            'polkadot': r'\b(dot|polkadot)\b',
            'chainlink': r'\b(link|chainlink)\b',
            'avalanche': r'\b(avax|avalanche)\b',
            'polygon': r'\b(matic|polygon)\b',
            'ripple': r'\b(xrp|ripple)\b',
            'arbitrum': r'\b(arb|arbitrum)\b',
            'optimism': r'\b(op|optimism)\b',
            'cosmos': r'\b(atom|cosmos)\b',
            'near': r'\b(near)\b',
            'aptos': r'\b(apt|aptos)\b'
        }
        
        # Match coin from query
        for coin, pattern in coin_patterns.items():
            if re.search(pattern, query_lower):
                coin_name = coin
                print(f"[RSS] Detected coin: {coin_name}")
                break
        
        # STEP 2: Top 4 RSS feeds only (Fast & Reliable)
        rss_feeds = [
            'https://coindesk.com/arc/outboundfeeds/rss/',
            'https://cointelegraph.com/rss',
            'https://decrypt.co/feed',
            'https://www.theblock.co/rss.xml'
        ]
        
        # STEP 3: Build regex pattern for coin-specific filtering
        coin_regex = None
        if coin_name:
            coin_regex = coin_patterns.get(coin_name)
        
        all_news = []
        coin_specific_news = []
        
        try:
            # STEP 4: Fetch from feeds (30 entries each = 120 total for better 7-day coverage)
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    if not feed.entries:
                        continue
                    print(f"[RSS] Parsing {feed_url}: {len(feed.entries)} entries")
                    
                    # Process 30 newest entries per feed (for 7-day coverage)
                    for entry in feed.entries[:30]:
                        title = entry.get('title', '').encode('utf-8', errors='ignore').decode('utf-8')
                        link = entry.get('link', '')
                        published = entry.get('published', '')
                        
                        # STEP 5: Strict coin-specific filter using regex
                        if coin_name and coin_regex:
                            if re.search(coin_regex, title, re.IGNORECASE):
                                coin_specific_news.append({
                                    'title': title,
                                    'link': link,
                                    'published': published
                                })
                                print(f"[RSS] ✓ MATCH: {title[:50]}...")
                        else:
                            # General crypto news (no specific coin)
                            if any(kw in title.lower() for kw in ['crypto', 'bitcoin', 'blockchain']):
                                all_news.append({
                                    'title': title,
                                    'link': link,
                                    'published': published
                                })
                        
                except Exception as feed_error:
                    print(f"[RSS] Error: {feed_error}")
                    continue
            
            # STEP 6: Filter by date (last 7 days only)
            from datetime import datetime, timedelta
            from dateutil import parser as date_parser
            
            one_week_ago = datetime.now() - timedelta(days=7)
            recent_news = []
            
            for news in coin_specific_news:
                try:
                    pub_date = date_parser.parse(news['published'])
                    if pub_date.replace(tzinfo=None) >= one_week_ago:
                        recent_news.append(news)
                except:
                    # If can't parse date, include it anyway
                    recent_news.append(news)
            
            coin_specific_news = recent_news
            
            # STEP 7: Deduplication
            seen_titles = set()
            unique_coin_news = []
            for news in coin_specific_news:
                title_lower = news['title'].lower().strip()
                if title_lower not in seen_titles:
                    seen_titles.add(title_lower)
                    unique_coin_news.append(news)
            
            coin_specific_news = unique_coin_news
            print(f"[RSS] Found {len(coin_specific_news)} unique {coin_name.upper() if coin_name else 'crypto'} news (last 7 days)")
            
            # STEP 8: Sort by newest
            coin_specific_news.sort(key=lambda x: x['published'], reverse=True)
            
            # STEP 9: Smart selection
            if coin_name:
                if len(coin_specific_news) >= 5:
                    all_news = coin_specific_news[:5]
                    print(f"[RSS] ✅ Returning {len(all_news)} {coin_name.upper()} news")
                elif len(coin_specific_news) >= 1:
                    all_news = coin_specific_news
                    print(f"[RSS] ⚠️ Only {len(all_news)} {coin_name.upper()} news in last 7 days")
                else:
                    print(f"[RSS] ❌ No {coin_name.upper()} news in last 7 days")
                    return {
                        'success': True,
                        'content': f"**No {coin_name.upper()} News Found**\n\nNo news about {coin_name.upper()} in the last 7 days from major sources.\n\n💡 Try:\n- `{coin_name} price` - Check price\n- `crypto news` - General crypto news",
                        'api_source': 'RSS News'
                    }
            else:
                # General crypto news
                all_news = all_news[:5]
        
            # STEP 10: Format output (English)
            content = f"**📰 Latest News"
            if coin_name:
                content += f" - {coin_name.upper()}"
                if len(all_news) < 5:
                    content += f" ({len(all_news)} found in last 7 days)"
            content += "**\n\n"
            
            for i, news in enumerate(all_news, 1):
                clean_title = (news['title']
                             .replace('\u2019', "'")
                             .replace('\u2013', '-')
                             .replace('\n', ' ')
                             .strip())
                content += f"{i}. **[{clean_title}]({news['link']})**\n"
                if news.get('published'):
                    content += f"   📅 {news['published']}\n\n"
            
            # Add helpful message if not enough news
            if coin_name and len(all_news) < 5:
                content += f"\n💡 _Only {len(all_news)} news about {coin_name.upper()} in the last 7 days. Try `crypto news` for general updates._"
            
            print(f"[RSS] ✅ Success - {len(all_news)} news (last 7 days)")
            return {
                'success': True,
                'content': content,
                'api_source': 'RSS News (Last 7 Days)'
            }
        
        except Exception as e:
            error_msg = str(e)
            print(f"[API CALL] RSS News: EXCEPTION - {error_msg}")
            return {'success': False, 'error': error_msg, 'api_source': 'RSS News'}
    
    async def get_coingecko_data(self, coin_symbol: str) -> Dict[str, Any]:
        """Fetch coin data from CoinGecko API"""
        print(f"[API CALL] CoinGecko: Fetching data for {coin_symbol}")
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_symbol,
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }
        
        headers = {}
        if self.coingecko_api_key:
            headers['x-cg-demo-api-key'] = self.coingecko_api_key
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if coin_symbol in data:
                            coin_data = data[coin_symbol]
                            print(f"[API CALL] CoinGecko: Success - {coin_symbol} = ${coin_data.get('usd', 0)}")
                            return {
                                'success': True,
                                'name': coin_symbol.replace('-', ' ').title(),
                                'symbol': coin_symbol.upper(),
                                'price': coin_data.get('usd', 0),
                                'market_cap': coin_data.get('usd_market_cap', 0),
                                'volume': coin_data.get('usd_24h_vol', 0),
                                'change_24h': coin_data.get('usd_24h_change', 0),
                                'api_source': 'CoinGecko API'
                            }
                        else:
                            return {'success': False, 'error': f'Coin "{coin_symbol}" not found', 'api_source': 'CoinGecko API'}
                    else:
                        error_text = await response.text()
                        return {'success': False, 'error': f'CoinGecko error: {response.status}', 'api_source': 'CoinGecko API'}
        except Exception as e:
            print(f"[API CALL] CoinGecko: EXCEPTION - {str(e)}")
            return {'success': False, 'error': str(e), 'api_source': 'CoinGecko API'}
    
    async def generate_image_with_fal(self, prompt: str) -> Dict[str, Any]:
        """Generate image using fal-client library (per official docs)"""
        if not self.fal_api_key:
            return {'success': False, 'error': 'fal.ai API key not available', 'api_source': 'fal.ai'}
        
        print(f"[IMAGE] FLUX.1 [dev]: {prompt[:50]}...")
        
        try:
            import fal_client
            
            # Set API key as per docs
            os.environ['FAL_KEY'] = self.fal_api_key
            
            # Callback for progress updates (per docs)
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"[IMAGE] 📝 {log.get('message', '')}")
            
            # Subscribe with logging (per docs example)
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: fal_client.subscribe(
                    "fal-ai/flux/dev",
                    arguments={
                        "prompt": prompt,
                        "image_size": "landscape_4_3",
                        "num_inference_steps": 28,
                        "guidance_scale": 3.5,
                        "num_images": 1,
                        "enable_safety_checker": True,
                        "output_format": "jpeg"
                    },
                    with_logs=True,
                    on_queue_update=on_queue_update
                )
            )
            
            # Parse result per docs output schema
            if result and 'images' in result:
                images = result['images']
                if images and len(images) > 0:
                    image_url = images[0]['url']
                    width = images[0].get('width', 'unknown')
                    height = images[0].get('height', 'unknown')
                    print(f"[IMAGE] ✅ Generated: {width}x{height}")
                    return {
                        'success': True,
                        'image_url': image_url,
                        'width': width,
                        'height': height,
                        'model': 'FLUX.1 [dev]',
                        'prompt': result.get('prompt', prompt),
                        'api_source': 'fal.ai'
                    }
            
            print(f"[IMAGE] ❌ No images in result: {result}")
            return {'success': False, 'error': 'No images generated', 'api_source': 'fal.ai'}
            
        except Exception as e:
            print(f"[IMAGE] 💥 ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e), 'api_source': 'fal.ai'}
    
    async def analyze_with_openai(self, content: str, context: str = "") -> Dict[str, Any]:
        """Analyze content with OpenAI"""
        if not self.openai_api_key:
            return {'success': False, 'error': 'OpenAI API key not available', 'api_source': 'OpenAI'}
        
        print(f"[API CALL] OpenAI: Analyzing content...")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a neutral crypto analyst. Provide concise, factual analysis in 2-3 sentences. Match the language of the content."},
                {"role": "user", "content": f"Analyze: {content}\n\nContext: {context}"}
            ],
            "max_tokens": 300,
            "temperature": 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        analysis = data['choices'][0]['message']['content']
                        print(f"[API CALL] OpenAI: Success")
                        return {'success': True, 'analysis': analysis, 'api_source': 'OpenAI GPT-4o-mini'}
                    else:
                        return {'success': False, 'error': f'OpenAI error: {response.status}', 'api_source': 'OpenAI'}
        except Exception as e:
            print(f"[API CALL] OpenAI: EXCEPTION - {str(e)}")
            return {'success': False, 'error': str(e), 'api_source': 'OpenAI'}
    
    async def extract_coin_name_with_openai(self, query: str) -> Dict[str, Any]:
        """Use OpenAI GPT-4o-mini to extract coin name and map to CoinGecko coin ID"""
        if not self.openai_api_key:
            return {'success': False, 'error': 'OpenAI API key not available', 'api_source': 'OpenAI'}
        
        print(f"[API CALL] OpenAI: Extracting coin name from: {query[:50]}...")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are a cryptocurrency expert. Extract the coin name from user queries and map it to the correct CoinGecko coin ID.

Return ONLY a JSON response with this exact format:
{
    "coin_id": "coingecko-coin-id",
    "coin_name": "Full coin name",
    "confidence": 0.0-1.0
}

Common mappings:
- "btc" = "bitcoin"
- "eth" = "ethereum" 
- "sol" = "solana"
- "sui" = "sui"
- "ada" = "cardano"
- "dot" = "polkadot"
- "link" = "chainlink"
- "arb" = "arbitrum"
- "op" = "optimism"
- "matic" = "matic-network"
- "avax" = "avalanche-2"

Use standard CoinGecko coin IDs. If unsure, return confidence < 0.7."""
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content'].strip()
                        
                        # Parse JSON response
                        try:
                            result = json.loads(content)
                            print(f"[API CALL] OpenAI: Coin extraction result: {result}")
                            return {
                                'success': True,
                                'coin_id': result.get('coin_id', ''),
                                'coin_name': result.get('coin_name', ''),
                                'confidence': result.get('confidence', 0.7),
                                'api_source': 'OpenAI GPT-4o-mini'
                            }
                        except json.JSONDecodeError:
                            print(f"[API CALL] OpenAI: Failed to parse JSON: {content}")
                            return {
                                'success': False,
                                'error': 'Invalid JSON response from OpenAI',
                                'api_source': 'OpenAI GPT-4o-mini'
                            }
                    else:
                        error_text = await response.text()
                        print(f"[API CALL] OpenAI: HTTP {response.status}: {error_text}")
                        return {
                            'success': False,
                            'error': f'OpenAI API error: {response.status}',
                            'api_source': 'OpenAI GPT-4o-mini'
                        }
        except Exception as e:
            error_msg = str(e)
            print(f"[API CALL] OpenAI: Exception: {error_msg}")
            return {'success': False, 'error': error_msg, 'api_source': 'OpenAI GPT-4o-mini'}
    
    async def analyze_twitter_post(self, url: str) -> Dict[str, Any]:
        """Analyze X/Twitter post using Gemini (primary) or OpenAI (backup)"""
        print(f"[TWITTER] Analyzing: {url[:60]}...")
        
        # Extract tweet ID from URL
        import re
        tweet_match = re.search(r'status/(\d+)', url)
        if not tweet_match:
            return {'success': False, 'error': 'Invalid X/Twitter URL format', 'api_source': 'Twitter Analysis'}
        
        tweet_id = tweet_match.group(1)
        
        # Try Gemini first
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""Analyze this X/Twitter post URL: {url}

Provide concise analysis in 3-4 sentences covering:
- Content summary
- Crypto market implications (if any)
- Credibility assessment
- Key takeaways

ALWAYS respond in English.

Note: Since I cannot directly access X/Twitter, provide general analysis guidance for posts about crypto."""
                
                response = model.generate_content(prompt, generation_config={'temperature': 0.3, 'max_output_tokens': 200})
                content = response.text.strip()
                print(f"[TWITTER] Gemini analysis success")
                
                return {
                    'success': True,
                    'content': f"🐦 **X/Twitter Post Analysis**\n\n**URL:** {url}\n\n{content}\n\n💡 _Always verify crypto information from multiple sources._",
                    'api_source': 'Gemini Analysis'
                }
                
            except Exception as e:
                print(f"[TWITTER] Gemini failed: {e}")
        
        # Fallback to OpenAI
        if self.openai_api_key:
            try:
                import aiohttp
                url_api = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": f"Analyze this X/Twitter post for crypto insights: {url}. Provide 3-4 sentence analysis covering content, market implications, and credibility."}],
                    "max_tokens": 200,
                    "temperature": 0.3
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url_api, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            analysis = data['choices'][0]['message']['content']
                            print(f"[TWITTER] OpenAI backup success")
                            
                            return {
                                'success': True,
                                'content': f"🐦 **X/Twitter Post Analysis**\n\n**URL:** {url}\n\n{analysis}\n\n💡 _Always verify crypto information from multiple sources._",
                                'api_source': 'OpenAI Analysis'
                            }
            except Exception as e:
                print(f"[TWITTER] OpenAI backup failed: {e}")
        
        # Final fallback
        return {
            'success': True,
            'content': f"""🐦 **X/Twitter Post**\n\n**URL:** {url}\n\n**Analysis Guidelines:**\n- Verify information from multiple sources\n- Check account credibility\n- Be cautious of FOMO content\n- Don't base investment decisions on single posts\n\n💡 _Configure API keys for AI-powered analysis._""",
            'api_source': 'Basic Analysis'
        }
