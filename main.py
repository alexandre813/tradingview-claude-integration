import os
import json
import requests
from flask import Flask, request
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Anthropic client
client = Anthropic()

# Configuration
TRADINGVIEW_WEBHOOK_TOKEN = os.getenv("TRADINGVIEW_WEBHOOK_TOKEN", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")

# Conversation history for Claude
conversation_history = []

def analyze_with_claude(market_data: dict) -> str:
    """Send market data to Claude for analysis"""
    
    # Format the market data for Claude
    user_message = f"""
    Analyse cette donnée TradingView et fournis tes recommandations de trading:
    
    Symbole: {market_data.get('symbol', 'N/A')}
    Prix actuel: {market_data.get('price', 'N/A')}
    Changement (%): {market_data.get('change_percent', 'N/A')}
    Volume: {market_data.get('volume', 'N/A')}
    Signal: {market_data.get('signal', 'N/A')}
    Résistance: {market_data.get('resistance', 'N/A')}
    Support: {market_data.get('support', 'N/A')}
    
    Fournis:
    1. Une analyse technique brève
    2. Le sentiment du marché (haussier/baissier)
    3. Les niveaux d'entrée/sortie recommandés
    4. Le risque/récompense potentiel
    """
    
    # Add to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Call Claude API
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=conversation_history
    )
    
    # Extract response
    assistant_message = response.content[0].text
    
    # Add to history for context
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

@app.route('/webhook/tradingview', methods=['POST'])
def tradingview_webhook():
    """Receive alerts from TradingView"""
    
    # Verify token
    token = request.args.get('token')
    if token != TRADINGVIEW_WEBHOOK_TOKEN:
        return {'error': 'Unauthorized'}, 401
    
    try:
        data = request.json
        
        # Extract market data
        market_data = {
            'symbol': data.get('ticker', 'UNKNOWN'),
            'price': data.get('close', 0),
            'change_percent': data.get('change_percent', 0),
            'volume': data.get('volume', 0),
            'signal': data.get('alert_message', ''),
            'resistance': data.get('resistance', 'N/A'),
            'support': data.get('support', 'N/A'),
            'timestamp': data.get('timestamp', '')
        }
        
        # Get Claude analysis
        analysis = analyze_with_claude(market_data)
        
        # Return results
        return {
            'status': 'success',
            'market_data': market_data,
            'analysis': analysis
        }, 200
    
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/analyze', methods=['POST'])
def analyze_manual():
    """Manual analysis endpoint"""
    
    try:
        data = request.json
        analysis = analyze_with_claude(data)
        
        return {
            'status': 'success',
            'analysis': analysis
        }, 200
    
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {'status': 'ok'}, 200

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return {'status': 'Conversation history cleared'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
