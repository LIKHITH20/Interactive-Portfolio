from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- API Clients Initialization ---
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY not properly configured in .env file")
    print("✅ Gemini API key loaded successfully")
except Exception as e:
    print(f"❌ Error loading API key: {e}")
    GEMINI_API_KEY = None

# Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# System instruction with resume data
SYSTEM_INSTRUCTION = """
You are a professional AI assistant representing a job candidate. Your role is to provide helpful, accurate, and engaging responses about the candidate's professional background, skills, and experience.

IMPORTANT: You must ONLY use information provided in the resume data below. Do not make up, assume, or hallucinate any information not explicitly stated in the resume. If asked about something not covered in the resume, politely explain that you don't have that specific information and suggest asking about other aspects of the candidate's background.

RESUME DATA:
[INSERT YOUR RESUME CONTENT HERE - Replace this placeholder with your actual resume information]

PERSONALITY:
- Be professional, friendly, and engaging
- Use "I" when referring to the candidate (e.g., "I have experience in...")
- Be specific and detailed when discussing qualifications
- Show enthusiasm about achievements and skills
- Ask clarifying questions if needed to provide better answers
- Keep responses concise but informative

RESPONSE GUIDELINES:
- Always stay within the bounds of the provided resume data
- If asked about something not in the resume, say "I don't have that specific information in my background, but I'd be happy to discuss [related topic from resume]"
- Focus on achievements, skills, and experiences that demonstrate value
- Use professional but conversational language
- Provide examples when possible

FORMATTING RULES:
- NEVER use markdown formatting (no *, **, bullets, or special characters)
- Write in plain, natural text that flows conversationally
- Use proper paragraphs and sentences
- Avoid lists unless specifically asked for a list format
- Make responses sound like natural speech, not a resume or document
- Use "I" statements to make it personal and engaging
"""

# Store conversation history
conversation_history = []

def clean_markdown_formatting(text):
    """Clean up markdown formatting to make responses more conversational"""
    import re
    
    # Remove bullet points and convert to natural text
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    
    # Remove italic formatting
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
    # Remove code formatting
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Remove headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Clean up multiple newlines
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    """Get API configuration"""
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "API key not configured",
            "message": "Please set GEMINI_API_KEY in your .env file"
        }), 500
    
    return jsonify({
        "geminiApiKey": GEMINI_API_KEY
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "API key not configured",
            "message": "Please set GEMINI_API_KEY in your .env file"
        }), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        # Prepare request for Gemini API
        request_body = {
            "contents": conversation_history,
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "systemInstruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            }
        }
        
        # Make request to Gemini API
        print(f"Making request to: {GEMINI_API_URL}")
        print(f"Request body keys: {list(request_body.keys())}")
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=request_body,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            error_detail = response.text
            print(f"Error response: {error_detail}")
            return jsonify({
                "error": f"API request failed: {response.status_code}",
                "message": error_detail
            }), 500
        
        data = response.json()
        
        if not data.get('candidates') or not data['candidates'][0].get('content'):
            return jsonify({
                "error": "Invalid API response format",
                "message": "Unexpected response from Gemini API"
            }), 500
        
        ai_response = data['candidates'][0]['content']['parts'][0]['text']
        
        # Clean up markdown formatting for better display
        ai_response = clean_markdown_formatting(ai_response)
        
        # Add AI response to conversation history
        conversation_history.append({
            "role": "model",
            "parts": [{"text": ai_response}]
        })
        
        return jsonify({"response": ai_response})
        
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timeout",
            "message": "The request took too long to process"
        }), 500
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Network error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Chat cleared successfully"})

@app.route('/api/models')
def list_models():
    """List available Gemini models for debugging"""
    if not GEMINI_API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            params={"key": GEMINI_API_KEY},
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            return jsonify(models)
        else:
            return jsonify({
                "error": f"Failed to fetch models: {response.status_code}",
                "message": response.text
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Resume Assistant...")
    print(f"📝 API Key Status: {'✅ Loaded' if GEMINI_API_KEY else '❌ Not configured'}")
    print("🌐 Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)