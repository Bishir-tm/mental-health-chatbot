# AI Mental Health Chatbot with TinyLLaMA

An offline, local AI mental health support chatbot that uses TinyLLaMA 1.1B model to provide Cognitive Behavioral Therapy (CBT) based support. Perfect for student projects and environments where privacy and offline functionality are important.

## Features

- 🤖 **Offline AI**: Runs TinyLLaMA 1.1B completely offline on your device
- 🧠 **CBT-Focused**: Provides cognitive behavioral therapy techniques
- ⚠️ **Crisis Detection**: Identifies high-risk situations and provides emergency resources
- 🔒 **Privacy First**: All conversations stay on your device
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **No API Keys**: No need for external API services
- 📦 **Portable**: Can be zipped and transferred between computers without re-downloading

## System Requirements

- **RAM**: At least 4GB (8GB recommended)
- **Storage**: At least 5GB free space for model files
- **Python**: 3.8 or higher
- **Internet**: Required only for initial model download

## Setup Options

### Option 1: Regular Setup (Downloads model each time)

#### Quick Setup

1. **Clone or Download the Project**
2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   python app.py
   ```

### Option 2: Portable Setup (Transfer-friendly)

#### Create Portable Version

1. **Run the portable setup script**

   ```bash
   python portable_setup.py
   ```

   This will:

   - Download the TinyLLaMA model (~2.2GB) to `models/` folder
   - Create `app_portable.py` that uses local cache
   - Generate run scripts for easy startup

2. **Run the portable version**

   ```bash
   # Windows
   run_portable.bat

   # Linux/Mac
   ./run_portable.sh

   # Or manually
   python app_portable.py
   ```

#### Transfer to Another Computer

1. **Zip the entire project folder** (including `models/` directory)
2. **Extract on target computer**
3. **Install Python dependencies only**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run immediately** (no model download needed)
   ```bash
   python app_portable.py
   ```

## How It Works

### Architecture Overview

```
Frontend (Bootstrap UI) ↔ Flask Backend ↔ TinyLLaMA Model (Local Cache)
```

### Core Components

#### 1. Frontend Interface

- **HTML/CSS/JS**: Responsive chat interface using Bootstrap
- **Status Indicator**: Shows model loading state (🟡 Loading → 🟢 Ready)
- **Emergency Modal**: Quick access to crisis resources
- **Message History**: User/assistant conversation display

#### 2. Backend Processing

- **Flask Server**: Handles API endpoints (`/api/chat`, `/api/health`)
- **Model Management**: Loads and manages TinyLLaMA model
- **Response Generation**: Creates CBT-focused therapeutic responses

#### 3. AI Model Integration

- **TinyLLaMA 1.1B**: Lightweight language model optimized for chat
- **Local Inference**: All processing happens on your device
- **Custom Prompting**: Specialized prompts for mental health support

### CBT Techniques Implemented

1. **Thought Pattern Recognition**: Identifies cognitive distortions
2. **Gentle Questioning**: Promotes self-reflection through questions
3. **Reframing Suggestions**: Offers alternative perspectives
4. **Behavioral Activation**: Suggests small, manageable actions
5. **Psychoeducation**: Explains CBT concepts in accessible terms

### Crisis Detection System

#### Pattern Matching

- Keywords: "suicide", "kill myself", "end my life", etc.
- Phrases indicating self-harm intent
- Expressions of hopelessness with specific plans

#### AI-Enhanced Assessment

- Contextual analysis of user messages
- Risk level classification (HIGH_RISK/LOW_RISK)
- Automatic crisis response with emergency resources

## File Structure

```
flask_mental_health_chatbot/
├── app.py                    # Original app (downloads model to HF cache)
├── app_portable.py           # Portable app (uses local model cache)
├── portable_setup.py         # Script to create portable version
├── installationScript.py     # Original installation script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── README.md                # Documentation
├── models/                  # Local model cache (created by portable_setup.py)
│   └── transformers_cache/  # TinyLLaMA model files (~2.2GB)
├── templates/
│   └── index.html           # Main HTML template
├── static/
│   ├── style.css           # Custom styles
│   └── script.js           # Frontend JavaScript
├── run_chatbot.bat         # Windows run script (original)
├── run_portable.bat        # Windows run script (portable)
└── run_portable.sh         # Unix run script (portable)
```

## Usage Guide

### Starting a Conversation

1. Wait for "🟢 AI Model Ready" indicator
2. Type your message in the input field
3. The AI responds with CBT-focused support

### Emergency Features

- **Crisis Detection**: Automatic monitoring for high-risk language
- **Emergency Button**: Immediate access to crisis resources
- **Local Resources**: Nigerian emergency contacts (112, SURPIN)

### Example Interactions

**User**: "I feel like everything I do is wrong"  
**AI**: "That sounds like a really difficult feeling. When you say 'everything,' could we look at some specific examples? Sometimes our minds can paint situations with a very broad brush when we're struggling."

## Technical Details

### Model Information

- **Model**: TinyLLaMA-1.1B-Chat-v1.0
- **Size**: ~2.2GB
- **Type**: Causal Language Model optimized for chat
- **Performance**: Runs efficiently on modest hardware

### Performance Optimization

- **Automatic GPU Detection**: Uses CUDA if available
- **Memory Management**: Efficient model loading and caching
- **Response Caching**: Local model cache prevents re-downloads

### Privacy & Security

- **Local Processing**: All conversations stay on your device
- **No External Calls**: After initial setup, no internet required
- **No Logging**: User conversations are not stored
- **Model Caching**: Models cached locally for offline use

## Troubleshooting

### Common Issues

#### "Model is still loading"

- **First run**: Wait for ~2.2GB download to complete
- **Subsequent runs**: Model loads from cache (faster)
- **Check**: Ensure sufficient disk space and RAM

#### "Model cache not found" (Portable version)

- **Solution**: Run `python portable_setup.py` first
- **Or**: Copy `models/` folder from another setup

#### Import/Dependency Errors

- **Solution**: Ensure you're in virtual environment
- **Command**: `pip install -r requirements.txt`
- **Check**: Python version 3.8+

#### Performance Issues

- **RAM**: Close other applications to free memory
- **CPU**: Model runs on CPU if no GPU available
- **Storage**: Ensure 5GB+ free space

### Development Notes

#### Customizing Responses

- **Temperature**: Adjust creativity in `generate_response()`
- **System Prompts**: Modify therapeutic approach in code
- **Crisis Keywords**: Update `assess_risk()` function

#### Adding Features

- **New CBT Techniques**: Extend `generate_therapeutic_response()`
- **UI Improvements**: Modify `templates/index.html` and CSS
- **Additional Languages**: Update crisis resources and prompts

## Educational Value

Perfect for demonstrating:

- **AI Integration**: Local LLM deployment and management
- **Web Development**: Full-stack Flask application
- **Mental Health Tech**: CBT techniques in software
- **Privacy-First Design**: Offline AI processing
- **Deployment Strategies**: Portable vs. cloud-based solutions

## License & Ethics

- **Educational Purpose**: Built for learning and support
- **Not Medical Device**: Supplements, doesn't replace professional care
- **Crisis Safety**: Includes emergency resource integration
- **Ethical AI**: Focused on harm prevention and user wellbeing

## Support & Contribution

### Getting Help

1. Check troubleshooting section
2. Verify system requirements
3. Review console output for errors
4. Try fresh virtual environment

### Contributing

- **Bug Reports**: Document steps to reproduce
- **Feature Requests**: Suggest CBT technique improvements
- **Code Contributions**: Follow existing code patterns
- **Documentation**: Help improve setup instructions

---

**⚠️ Important Disclaimer**: This chatbot is for educational and support purposes only. It is not a substitute for professional mental health care. If you or someone you know is in crisis, please contact emergency services or mental health professionals immediately.

**Emergency Contacts (Nigeria):**

- Emergency Hotline: 112
- SURPIN: 08092106463
- Mentally Aware Nigeria Initiative: 08182260572
