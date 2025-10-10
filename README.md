# AI Resume Assistant

A professional conversational AI interface that allows recruiters to interact with your resume using Google's Gemini API. Built with Python Flask and modern web technologies.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# Replace 'your_gemini_api_key_here' with your actual API key
```

### 3. Add Your Resume Data
Edit `app.py` and replace the placeholder in the `SYSTEM_INSTRUCTION` variable (around line 20) with your actual resume content.

### 4. Start the Application
```bash
python3 app.py
```

### 5. Open in Browser
Navigate to `http://localhost:5000`

## 🔧 Setup Instructions

### Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

### Add Your Resume Data
Edit the `SYSTEM_INSTRUCTION` variable in `app.py`:
```python
SYSTEM_INSTRUCTION = """
You are a professional AI assistant representing a job candidate...

RESUME DATA:
[Your actual resume content goes here]

PERSONALITY:
- Be professional, friendly, and engaging
- Use "I" when referring to the candidate
...
"""
```

## 🎯 Features

- **Professional UI**: Modern, responsive design with Tailwind CSS
- **Secure API Management**: Environment variables with `.env` file
- **Conversation Memory**: Maintains context throughout the chat
- **Mobile Responsive**: Works perfectly on all devices
- **Error Handling**: Comprehensive error messages and debugging
- **Clear Chat**: Reset conversation history anytime

## 🔐 Security

- ✅ API keys stored in `.env` file (not in code)
- ✅ `.env` file excluded from git (`.gitignore`)
- ✅ Only `.env.example` committed (safe template)
- ✅ Server-side API key handling

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # HTML template
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .env                   # Your actual environment (not committed)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Check `.env` file has your actual API key
   - Restart server after updating `.env`
   - Verify API key has proper permissions

2. **404 Errors**
   - Verify API key is correct
   - Check Gemini API endpoint is accessible
   - Ensure server is running on correct port

3. **Server Won't Start**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python installation
   - Verify port 5000 is available

### Debug Mode

The application includes detailed logging:
- API key status on startup
- Request/response details
- Error messages with context

## 🎨 Customization

### UI Customization
- Edit `templates/index.html`
- Modify Tailwind CSS classes
- Update colors in the configuration

### AI Behavior
- Edit `SYSTEM_INSTRUCTION` in `app.py`
- Adjust temperature, topK, topP in API calls
- Modify conversation flow and responses

## 📝 Usage

1. **Start the application**: `python3 app.py`
2. **Open your browser**: Go to `http://localhost:5000`
3. **Ask questions**: About your professional background
4. **Get responses**: Intelligent answers based on your resume

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this for your own resume projects!

---

**Note**: Remember to never commit your actual API key to version control. Always use the `.env.example` template and keep your `.env` file local and secure.