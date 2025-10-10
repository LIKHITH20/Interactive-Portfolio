from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import requests
import json
import time
from datetime import datetime

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
Likhith Shivashankar
Melbourne VIC 3006 | Mobile: 0466 226 324 | Email: likhithshivashankar@gmail.com
LinkedIn: https://www.linkedin.com/in/likhith-shivashankar/ | GitHub:  https://github.com/LIKHITH20
Profile
Results-driven Data Science graduate with over 3 years of diverse experience in AI/ML Engineering, Software Development, and Data Analytics. Proven expertise in Python, NLP, Machine Learning, and Data Processing, with hands-on experience in real-time AI solutions, Cloud Technologies, and Automation. Adept at leveraging analytical skills and technical acumen to drive data-driven insights and optimise system performance. 

Key Skills
•	Programming Languages: Python, R Programming Language, Java, Structured Query Language (SQL), C, C#.
•	Development Tools: HTML, CSS, Microsoft Azure, MySQL, Lang Chain, GenAI.
•	Visualisation Tools: Tableau, Power BI.
•	Development Methodologies: Agile, NLP, Git.
•	Soft skills: Communication, Leadership, Critical Thinking, Teamwork, Time Management, Stakeholder Engagement.

Education
RMIT University, Master of Data Science	July 2023 - June 2025
Visvesvaraya Technological University, Bachelor of Engineering	August 2016 - September 2020

Work experience
StarPlan AI, AI/ML Engineer (Contract)	Jul 2025 – Aug 2025
•	Designed and implemented conversational AI agents for automated interviews, enabling structured, context-aware dialogue with dynamic flow control.
•	Integrated advanced speech recognition, synthesis, and speaker diarization models to deliver accurate, human-like interactions and high-quality transcriptions.
•	Collaborated directly with the CEO to align technical design with business goals, co-developing a scalable solution that streamlined candidate screening and reduced interviewer workload.
•	Enhanced system reliability through iterative testing, minimizing hallucinations and ensuring consistent, professional candidate experiences.
Focus Bear, Machine Learning Intern	March 2025 – June 2025
•	Led the development of LLM-powered classification systems to monitor user activity and attention levels, supporting digital interventions for individuals with ADHD in a healthcare-focused application.
•	Developed attention scoring models using behavioural mapping and regression analysis to identify key focus patterns from app usage data, aiding early insights into cognitive engagement.
•	Communicated weekly research findings and strategic recommendations to industry partners and academic supervisors, demonstrating leadership, adaptability, and AI/ML application in the digital health domain.
Kois AI, AI/ML Engineer Intern	November 2024 – March 2025
•	Built a real-time conversational loop combining speech-to-text, contextual response generation, and speech synthesis, enabling continuous, natural user interaction.
•	Developed a dynamic audio recording system with silence detection, improving usability and ensuring accurate capture of user input.
•	Integrated OpenAI’s API to generate contextually relevant responses, enhancing the quality and engagement of conversations.
•	Collaborated with the CEO to align technical development with product vision, delivering a functional prototype that demonstrated the potential of conversational AI for scalable user engagement.
Accenture India, Software Engineer	November 2020–June 2023
•	Engineered and implemented scalable software solutions in collaboration with development and testing teams, ensuring optimal functionality and performance to meet client specifications.
•	Modernised legacy codebases by updating them to current development standards, resulting in enhanced system functionality and maintainability.
•	Led the migration of approximately 42TB of data utilising third-party tools such as ShareGate, Metalogix Content Matrix, and Apps4Pro Data Migration, achieving near-zero client escalations.
•	Developed custom applications using Power Apps, automated workflows with Power Automate, and created interactive dashboards in Power BI to enhance data accessibility and support decision-making processes.
•	Earned multiple accolades for consistently meeting project deadlines and delivering high-quality software solutions to end-users.

Projects
Bayesian CHD Risk Prediction – Framingham Dataset | Master’s Degree Coursework Research Project
•	Developed a Bayesian logistic regression model using R to predict 10-year coronary heart disease risk, leveraging hierarchical priors and MCMC sampling (Gibbs & Metropolis-Hastings) for posterior inference.
•	Achieved 84.8% accuracy with high recall; identified key risk factors through feature selection and posterior analysis.
•	Tuned convergence diagnostics (ESS, MCSE, shrink factor) for model stability.
•	Led a 3-member team through structured research planning and iterative model refinement.
•	Tools: R, Bayesian Inference, MCMC, Feature Selection, Model Calibration.
Sachin Tendulkar’s Cricket Journey – Power BI Dashboard | Data Visualization Project
•	Cleaned and transformed raw cricket statistics using Power BI and DAX to build interactive dashboards narrating career milestones.
•	Applied data storytelling techniques to convert complex metrics into intuitive visual narratives for performance reporting.
•	Tools: Power BI, DAX, Excel, Data Cleaning, Business Intelligence.
Certifications
•	Microsoft 365 Fundamentals (MS-900)
•	Microsoft Power Platform Fundamentals (PL-900)
•	Microsoft Azure Fundamental (AZ-900)
•	Microsoft Security, Compliance, and Identity Fundamentals (SC-900)
VISA Details
•	Visa Status: Temporary Graduate visa (subclass 485)
•	Work Rights: Unrestricted
•	Visa Expiry: 19/08/2028
References
Avishek Sengupta, Associate Manager, Accenture India, email: avishek.sengupta@accenture.com, tel: (+91) 8585 019 188
Rui Liu, Co-Founder, Kois AI, email: ruiliu@kois.ai , tel: +61 413678116
Jeremy Nagel, Founder, Focus Bear, email: jeremy@focusbear.io , tel: +61 414885787
Khushboo Patel, Customer Service Manager, Coles Group, email: khushboop1911@gmail.com , tel: +61 406087976

CRITICAL INSTRUCTIONS:
- ONLY use information explicitly provided in the RESUME DATA above
- Do NOT make assumptions about dates, current status, or experiences not mentioned
- If the resume says "pursuing" or "current", use that exact language
- If the resume mentions specific dates, use those exact dates
- Include ALL types of experience mentioned (Software Engineering, AI/ML, etc.)
- Do NOT add information not present in the resume data

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
- Include ALL relevant experience types (Not everything is AI/ML in experience)

FORMATTING RULES:
- NEVER use markdown formatting (no *, **, bullets, or special characters)
- Write in plain, natural text that flows conversationally
- Use proper paragraphs and sentences
- Avoid lists unless specifically asked for a list format
- Make responses sound like natural speech, not a resume or document
- Use "I" statements to make it personal and engaging
"""

# Store conversation history and analytics
conversation_history = []
conversation_analytics = {
    "total_messages": 0,
    "session_start": datetime.now().isoformat(),
    "topics_discussed": [],
    "response_times": []
}

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

@app.route('/experience')
def experience():
    return render_template('experience.html')

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
    """Handle chat messages with enhanced features"""
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "API key not configured",
            "message": "Please set GEMINI_API_KEY in your .env file"
        }), 500
    
    start_time = time.time()
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        message_type = data.get('type', 'text')  # text, voice, etc.
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Track analytics
        conversation_analytics["total_messages"] += 1
        
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_message}],
            "timestamp": datetime.now().isoformat(),
            "type": message_type
        })
        
        # Clean conversation history for API (remove extra fields)
        clean_conversation = []
        for msg in conversation_history:
            clean_msg = {
                "role": msg["role"],
                "parts": msg["parts"]
            }
            clean_conversation.append(clean_msg)
        
        # Prepare request for Gemini API
        request_body = {
            "contents": clean_conversation,
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
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=request_body,
            timeout=30
        )
        
        response_time = time.time() - start_time
        conversation_analytics["response_times"].append(response_time)
        
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
            "parts": [{"text": ai_response}],
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time
        })
        
        # Extract topics for analytics (simple keyword extraction)
        topics = extract_topics(user_message)
        conversation_analytics["topics_discussed"].extend(topics)
        
        return jsonify({
            "response": ai_response,
            "response_time": round(response_time, 2),
            "message_id": len(conversation_history)
        })
        
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

def extract_topics(message):
    """Extract topics from user message for analytics"""
    topics = []
    message_lower = message.lower()
    
    topic_keywords = {
        "education": ["education", "degree", "university", "college", "master", "bachelor"],
        "experience": ["experience", "work", "job", "career", "role", "position"],
        "skills": ["skills", "technology", "programming", "coding", "technical"],
        "projects": ["project", "portfolio", "work", "build", "develop"],
        "ai_ml": ["ai", "machine learning", "ml", "artificial intelligence", "data science"],
        "software": ["software", "engineering", "development", "programming"]
    }
    
    for topic, keywords in topic_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            topics.append(topic)
    
    return topics

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    conversation_analytics["total_messages"] = 0
    conversation_analytics["topics_discussed"] = []
    conversation_analytics["response_times"] = []
    conversation_analytics["session_start"] = datetime.now().isoformat()
    return jsonify({"message": "Chat cleared successfully"})

@app.route('/api/analytics')
def get_analytics():
    """Get conversation analytics"""
    avg_response_time = sum(conversation_analytics["response_times"]) / len(conversation_analytics["response_times"]) if conversation_analytics["response_times"] else 0
    
    return jsonify({
        "total_messages": conversation_analytics["total_messages"],
        "session_duration": (datetime.now() - datetime.fromisoformat(conversation_analytics["session_start"])).total_seconds(),
        "average_response_time": round(avg_response_time, 2),
        "topics_discussed": list(set(conversation_analytics["topics_discussed"])),
        "conversation_length": len(conversation_history)
    })

@app.route('/api/voice', methods=['POST'])
def handle_voice():
    """Handle voice input (placeholder for future voice features)"""
    return jsonify({
        "message": "Voice features coming soon!",
        "status": "development"
    })

if __name__ == '__main__':
    print("🚀 Starting Advanced AI Resume Assistant...")
    print(f"📝 API Key Status: {'✅ Loaded' if GEMINI_API_KEY else '❌ Not configured'}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🎯 Features: Interactive UI, Analytics, Voice Ready")
    app.run(debug=True, host='0.0.0.0', port=5000)