"""
Crypto Research ROMA Agent
Uses ROMA Framework for intelligent crypto research
"""
import sys
import os
from pathlib import Path

# Add ROMA to path
sys.path.append(str(Path(__file__).parent.parent / 'ROMA' / 'src'))

from typing import Dict, Any, List
import asyncio
from roma_agents.api_integrations import APIIntegrations

class CryptoROMAAgent:
    """
    ROMA-powered Crypto Research Agent
    Implements recursive task decomposition for crypto research
    """
    
    def __init__(self):
        self.api_integrations = APIIntegrations()
        self.max_recursion_depth = 2  # Prevent infinite loops
        print("[ROMA] Crypto Research Agent initialized")
    
    async def solve(self, task: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """
        Main ROMA solve loop: Atomizer -> Planner/Executor -> Aggregator
        """
        try:
            query = task.get('query', '')
            task_type = task.get('type', 'research')
            
            print("="*60)
            print(f"[ROMA-SOLVE] Starting solve for: {query}")
            print(f"[ROMA-SOLVE] Task type: {task_type}, Depth: {depth}/{self.max_recursion_depth}")
            print("="*60)
            
            # Check recursion depth limit
            if depth >= self.max_recursion_depth:
                print(f"[ROMA-SOLVE] MAX DEPTH REACHED - Forcing atomic execution")
                return await self._execute(task)
            
            # Step 1: Atomizer - Is this task atomic?
            if await self._is_atomic(task):
                # Step 2: Executor - Execute atomic task
                return await self._execute(task)
            else:
                # Step 2: Planner - Break down into subtasks
                subtasks = await self._plan(task)
                
                # Recursive solve for each subtask
                results = []
                for i, subtask in enumerate(subtasks, 1):
                    print(f"[ROMA-SOLVE] Processing subtask {i}/{len(subtasks)}: {subtask.get('query', '')[:50]}")
                    result = await self.solve(subtask, depth + 1)  # Pass depth + 1
                    results.append(result)
                
                # Step 3: Aggregator - Combine results
                return await self._aggregate(task, results)
        
        except Exception as e:
            error_msg = str(e)
            print(f"[ROMA-SOLVE] EXCEPTION: {error_msg}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'ROMA Exception: {error_msg}',
                'query': task.get('query', ''),
                'api': 'ROMA'
            }
    
    async def _is_atomic(self, task: Dict[str, Any]) -> bool:
        """
        Atomizer: Determine if task can be executed directly or needs decomposition
        """
        query = task.get('query', '').lower()
        
        # COMPLEX research questions need ROMA's multi-source analysis
        complex_keywords = [
            'should i', 'worth', 'buy',  # Investment/purchase questions
            'why', 'how', 'analyze', 'compare',  # Analysis requests
            'where', 'which',  # Location/selection questions
            'trend', 'future', 'predict', 'forecast',  # Predictions
            'best coin', 'top', 'which coin'  # Comparisons
        ]
        
        for keyword in complex_keywords:
            if keyword in query:
                print(f"[ROMA-Atomizer] COMPLEX task detected - needs planning: {query[:50]}")
                return False
        
        # SIMPLE queries are atomic (price, news, single fact)
        simple_keywords = ['price', 'gia', 'check', 'cost', 'value', 'news', 'tin tuc']
        for keyword in simple_keywords:
            if keyword in query:
                print(f"[ROMA-Atomizer] ATOMIC task - direct execution: {query[:50]}")
                return True
        
        # Default: atomic for safety
        print(f"[ROMA-Atomizer] Default to ATOMIC: {query[:50]}")
        return True
    
    async def _plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Planner: Use OpenAI to break down complex queries into optimal subtasks
        """
        query = task.get('query', '')
        print(f"[ROMA-Planner] Planning multi-source research for: {query[:50]}...")
        
        # Use OpenAI to intelligently plan subtasks
        planning_prompt = f"""You are a crypto research task planner. Break down this query into 2-3 specific subtasks.

Query: "{query}"

Available APIs:
- CoinGecko: Get price, market cap, volume for specific coins
- Perplexity: Deep research, analysis, recommendations, explanations
- RSS News: Latest crypto news

Rules:
1. For investment questions ("co nen mua", "should I buy"): price + news + analysis
2. For location questions ("mua o dau", "where to buy"): price + exchange recommendations
3. For comparison ("btc vs eth"): data for both coins + comparison analysis
4. For analysis ("why", "how"): supporting data + deep research

Output JSON array of subtasks:
[
  {{"query": "bitcoin price", "type": "price"}},
  {{"query": "best bitcoin exchanges 2025", "type": "analysis"}},
  {{"query": "bitcoin buying guide", "type": "analysis"}}
]

Return ONLY the JSON array, no explanation."""

        try:
            # Call OpenAI for intelligent planning
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_integrations.openai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4.1-mini",
                "messages": [{"role": "user", "content": planning_prompt}],
                "max_tokens": 300,
                "temperature": 0.3
            }
            
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        plan_text = data['choices'][0]['message']['content'].strip()
                        
                        # Parse JSON response
                        import json
                        # Remove markdown code blocks if present
                        if '```json' in plan_text:
                            plan_text = plan_text.split('```json')[1].split('```')[0].strip()
                        elif '```' in plan_text:
                            plan_text = plan_text.split('```')[1].split('```')[0].strip()
                        
                        subtasks = json.loads(plan_text)
                        print(f"[ROMA-Planner] OpenAI created {len(subtasks)} subtasks:")
                        for i, st in enumerate(subtasks, 1):
                            print(f"  [{i}] Query: '{st.get('query', '')}' | Type: {st.get('type', 'unknown')}")
                        return subtasks
                    else:
                        print(f"[ROMA-Planner] OpenAI planning failed: {response.status}")
        except Exception as e:
            print(f"[ROMA-Planner] OpenAI planning exception: {str(e)}")
        
        # Fallback: Use original query as single task
        print(f"[ROMA-Planner] Fallback to single task")
        return [task]
    
    async def _execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executor: Execute atomic task using appropriate API
        """
        query = task.get('query', '')
        task_type = task.get('type', 'research')
        
        print(f"[ROMA-Executor] ===== EXECUTING TASK =====")
        print(f"[ROMA-Executor] Query: {query}")
        print(f"[ROMA-Executor] Type: {task_type}")
        
        # Use OpenAI to route to correct API
        try:
            context_analysis = await self.api_integrations.analyze_context_with_openai(query)
            
            if not context_analysis['success']:
                error_detail = context_analysis.get('error', 'Unknown error')
                print(f"[ROMA-Executor] Context analysis FAILED: {error_detail}")
                return {
                    'success': False,
                    'error': f'Failed to analyze context: {error_detail}',
                    'query': query,
                    'api': 'OpenAI Routing'
                }
        except Exception as e:
            print(f"[ROMA-Executor] Context analysis EXCEPTION: {str(e)}")
            return {
                'success': False,
                'error': f'Context analysis exception: {str(e)}',
                'query': query,
                'api': 'OpenAI Routing'
            }
        
        selected_api = context_analysis['selected_api']
        print(f"[ROMA-Executor] Routing to: {selected_api}")
        
        # Route to appropriate API
        if selected_api == 'coingecko':
            print(f"[ROMA-Executor] Routing to CoinGecko")
            # Extract coin (name/symbol/ticker) with OpenAI GPT-4o-mini
            coin_extraction = await self.api_integrations.extract_coin_name_with_openai(query)
            print(f"[ROMA-Executor] OpenAI GPT-4o-mini extraction: {coin_extraction}")
            
            if coin_extraction['success']:
                coin_id = coin_extraction['coin_id']
                print(f"[ROMA-Executor] Fetching CoinGecko data for: {coin_id}")
                result = await self.api_integrations.get_coingecko_data(coin_id)
                print(f"[ROMA-Executor] CoinGecko result success: {result.get('success')}")
                if result.get('success'):
                    print(f"[ROMA-Executor] Coin: {result.get('name')} ({result.get('symbol')}) = ${result.get('price')}")
                
                return {
                    'success': result.get('success', False),
                    'data': result,
                    'query': query,
                    'api': 'CoinGecko'
                }
            else:
                print(f"[ROMA-Executor] OpenAI extraction FAILED: {coin_extraction.get('error')}")
                return {
                    'success': False,
                    'error': f"Could not extract coin name: {coin_extraction.get('error')}",
                    'query': query,
                    'api': 'CoinGecko'
                }
        
        elif selected_api == 'perplexity':
            # Worker: Gemini trả lời câu đơn giản (with OpenAI backup)
            try:
                print(f"[WORKER] Trying Gemini for simple answer...")
                
                # Use Gemini for concise answers
                research_prompt = f"""Trả lời câu hỏi sau BẰNG NGÔN NGỮ của câu hỏi: {query}

YÊU CẦU:
- Tiếng Việt → trả lời tiếng Việt
- English → answer in English  
- CHỈ 2-3 câu ngắn gọn
- Tập trung vào điểm chính

Ví dụ:
"coin là gì" → "Coin (tiền điện tử) là đơn vị tiền tệ số chạy trên blockchain riêng. Ví dụ: Bitcoin, Ethereum, Solana."

"what is ethereum" → "Ethereum is a blockchain platform that enables smart contracts and dApps. It uses ETH as its native cryptocurrency."

Trả lời:"""
                
                import google.generativeai as genai
                genai.configure(api_key=self.api_integrations.gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                generation_config = {
                    'temperature': 0.2,
                    'max_output_tokens': 150
                }
                
                response = model.generate_content(research_prompt, generation_config=generation_config)
                content = response.text.strip()
                print(f"[WORKER] Gemini success")
                
                return {
                    'success': True,
                    'data': {'content': content, 'api_source': 'Gemini Worker'},
                    'query': query,
                    'api': 'Gemini'
                }
                
            except Exception as e:
                print(f"[WORKER] Gemini FAILED: {str(e)}")
                print(f"[WORKER] Falling back to OpenAI...")
                
                # Backup: OpenAI takes over
                try:
                    import aiohttp
                    url = "https://api.openai.com/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {self.api_integrations.openai_api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": research_prompt}],
                        "max_tokens": 150,
                        "temperature": 0.2
                    }
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post(url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                content = data['choices'][0]['message']['content']
                                print(f"[WORKER] OpenAI backup success")
                                return {
                                    'success': True,
                                    'data': {'content': content, 'api_source': 'OpenAI Backup'},
                                    'query': query,
                                    'api': 'OpenAI'
                                }
                            else:
                                return {
                                    'success': False,
                                    'error': f'Both Gemini and OpenAI failed',
                                    'query': query,
                                    'api': 'None'
                                }
                except Exception as openai_error:
                    print(f"[WORKER] OpenAI backup also FAILED: {str(openai_error)}")
                    return {
                        'success': False,
                        'error': f'All LLMs failed: Gemini ({str(e)}), OpenAI ({str(openai_error)})',
                        'query': query,
                        'api': 'None'
                    }
        
        elif selected_api == 'rss_news':
            try:
                print(f"[ROMA-Executor] Calling RSS News...")
                result = await self.api_integrations.get_rss_news(query)
                print(f"[ROMA-Executor] RSS result: success={result.get('success')}")
                
                if result.get('success'):
                    return {
                        'success': True,
                        'data': result,
                        'query': query,
                        'api': 'RSS News'
                    }
                else:
                    # No news found - return helpful message
                    return {
                        'success': True,
                        'data': {
                            'content': f"No recent news found for this query. Try: 'bitcoin news' or 'crypto news today'",
                            'api_source': 'RSS News'
                        },
                        'query': query,
                        'api': 'RSS News'
                    }
            except Exception as e:
                print(f"[ROMA-Executor] RSS EXCEPTION: {str(e)}")
                return {
                    'success': False,
                    'error': f'RSS error: {str(e)}',
                    'query': query,
                    'api': 'RSS News'
                }
        
        elif selected_api == 'falai' or 'create image' in query.lower() or 'tao hinh' in query.lower():
            print(f"[ROMA-Executor] Image generation request")
            
            # Extract user's image description
            user_description = query
            if 'create image' in query.lower():
                user_description = query.split('create image', 1)[1].strip()
            elif 'tao hinh' in query.lower():
                user_description = query.split('tao hinh', 1)[1].strip()
            
            print(f"[ROMA-Executor] User description: {user_description}")
            
            if len(user_description.split()) < 3:
                return {
                    'success': True,
                    'data': {
                        'content': 'Please describe the image. Example:\n- "ETH coin with text \'to the moon\'"\n- "Bitcoin rocket in space"',
                        'api_source': 'Clarification'
                    },
                    'query': query,
                    'api': 'Clarification',
                    'needs_clarification': True
                }
            
            # STEP 1: Enhance prompt with Gemini (primary) or OpenAI (backup)
            print(f"[BRAIN] Enhancing image prompt...")
            
            try:
                # Try Gemini first
                if self.api_integrations.gemini_api_key:
                    import google.generativeai as genai
                    genai.configure(api_key=self.api_integrations.gemini_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    enhance_prompt = f"""Convert this image description into a detailed FLUX prompt:

User request: {user_description}

Create a professional image generation prompt that:
- Keeps ALL user's text requests (e.g., "ETH to the moon")
- Adds artistic details (style, lighting, composition)
- Optimizes for FLUX.1 model

Return ONLY the enhanced prompt, no explanations."""
                    
                    response = model.generate_content(enhance_prompt, generation_config={'temperature': 0.7, 'max_output_tokens': 200})
                    enhanced_prompt = response.text.strip()
                    print(f"[BRAIN] Gemini enhanced: {enhanced_prompt[:80]}...")
                else:
                    raise Exception("No Gemini key, using OpenAI")
                    
            except Exception as e:
                print(f"[BRAIN] Gemini failed, using OpenAI backup...")
                
                # Backup: OpenAI
                import aiohttp
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_integrations.openai_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": f"Enhance this for FLUX image generation, keep all text requests: {user_description}"}],
                    "max_tokens": 200,
                    "temperature": 0.7
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            enhanced_prompt = data['choices'][0]['message']['content'].strip()
                            print(f"[BRAIN] OpenAI enhanced: {enhanced_prompt[:80]}...")
                        else:
                            # Fallback to user description
                            enhanced_prompt = user_description
                            print(f"[BRAIN] Using original prompt")
            
            # STEP 2: Send enhanced prompt to fal.ai
            result = await self.api_integrations.generate_image_with_fal(enhanced_prompt)
            return {
                'success': result.get('success', False),
                'data': result,
                'query': query,
                'api': 'fal.ai'
            }
        
        elif selected_api == 'twitter_analysis':
            try:
                print(f"[ROMA-Executor] Twitter/X analysis request")
                result = await self.api_integrations.analyze_twitter_post(query)
                print(f"[ROMA-Executor] Twitter result: success={result.get('success')}")
                
                if result.get('success'):
                    return {
                        'success': True,
                        'data': {'content': result['content'], 'api_source': result['api_source']},
                        'query': query,
                        'api': 'Twitter Analysis'
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('error', 'Twitter analysis failed'),
                        'query': query,
                        'api': 'Twitter Analysis'
                    }
            except Exception as e:
                print(f"[ROMA-Executor] Twitter EXCEPTION: {str(e)}")
                return {
                    'success': False,
                    'error': f'Twitter analysis error: {str(e)}',
                    'query': query,
                    'api': 'Twitter Analysis'
                }
        
        elif selected_api == 'ask_user':
            return {
                'success': True,
                'data': {
                    'content': context_analysis.get('clarification', 'Please clarify your request'),
                    'api_source': 'Clarification'
                },
                'query': query,
                'api': 'Clarification',
                'needs_clarification': True
            }
        
        # Default fallback
        print(f"[ROMA-Executor] WARNING: Unknown API route selected: {selected_api}")
        return {
            'success': False,
            'error': f'Unknown API route: {selected_api}',
            'query': query,
            'api': 'Unknown'
        }
    
    async def _aggregate(self, task: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregator: Combine results from subtasks into final answer
        """
        query = task.get('query', '')
        print(f"[ROMA-Aggregator] Aggregating {len(results)} results for: {query[:50]}...")
        
        # Combine all results into a comprehensive response
        try:
            combined_content = f"[COMPREHENSIVE ANALYSIS] {query}\n\n"
            
            for i, result in enumerate(results, 1):
                if result.get('success'):
                    data = result.get('data', {})
                    api_name = result.get('api', 'Unknown')
                    
                    combined_content += f"**{i}. {api_name} Analysis:**\n"
                    
                    if 'content' in data:
                        combined_content += f"{data['content']}\n\n"
                    elif 'price' in data:
                        price_str = f"${data['price']:,.2f}" if data['price'] > 0 else "N/A"
                        combined_content += f"Current Price: {price_str}\n"
                        combined_content += f"24h Change: {data.get('change_24h', 'N/A')}%\n\n"
                else:
                    print(f"[ROMA-Aggregator] Subtask {i} failed: {result.get('error')}")
        except Exception as e:
            print(f"[ROMA-Aggregator] Content combination EXCEPTION: {str(e)}")
            combined_content = f"Error combining results: {str(e)}"
        
        # Use OpenAI to synthesize final answer
        try:
            print(f"[ROMA-Aggregator] Calling OpenAI synthesis...")
            synthesis = await self.api_integrations.analyze_with_openai(
                combined_content,
                f"Original question: {query}"
            )
            
            if synthesis.get('success'):
                final_content = f"{combined_content}\n\n**[AI SYNTHESIS]**\n{synthesis['analysis']}"
                print(f"[ROMA-Aggregator] Synthesis successful")
            else:
                final_content = combined_content
                print(f"[ROMA-Aggregator] Synthesis failed: {synthesis.get('error')}")
        except Exception as e:
            print(f"[ROMA-Aggregator] Synthesis EXCEPTION: {str(e)}")
            final_content = combined_content
        
        print(f"[ROMA-Aggregator] Aggregation complete")
        
        return {
            'success': True,
            'data': {
                'content': final_content,
                'api_source': 'ROMA Aggregated'
            },
            'query': query,
            'api': 'ROMA',
            'subtask_count': len(results)
        }

