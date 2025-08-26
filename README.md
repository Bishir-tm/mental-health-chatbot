# AI Mental Health Chatbot with TinyLLaMA

An offline, local AI mental health support chatbot that uses TinyLLaMA 1.1B model to provide Cognitive Behavioral Therapy (CBT) based support. Perfect for student projects and environments where privacy and offline functionality are important.

## Features

- 🤖 **Offline AI**: Runs TinyLLaMA 1.1B completely offline on your device
- 🧠 **CBT-Focused**: Provides cognitive behavioral therapy techniques
- ⚠️ **Crisis Detection**: Identifies high-risk situations and provides emergency resources
- 🔒 **Privacy First**: All conversations stay on your device
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **No API Keys**: No need for external API services

## System Requirements

- **RAM**: At least 4GB (8GB recommended)
- **Storage**: At least 5GB free space for model files
- **Python**: 3.8 or higher
- **Internet**: Required only for initial model download

## Quick Setup Guide

### 1. Clone or Download the Project

```bash
cd your-project-directory
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you install, PyTorch and other ML libraries will download (~2-3GB). This may take some time depending on your internet connection.

### 4. Run the Application

```bash
python app.py
```

### 5. First Run Experience

- The application will automatically download TinyLLaMA model (~2.2GB) on first run
- You'll see "AI Model Loading..." status indicator
- Once loaded, the status will change to "🟢 AI Model Ready"
- The download happens only once - subsequent runs will be faster

### 6. Open in Browser

Navigate to `http://127.0.0.1:5000` in your web browser.

## Usage Guide

### Starting a Conversation

- Wait for the "🟢 AI Model Ready" status indicator
- Type your message in the input field
- The AI will respond with CBT-focused support

### Emergency Features

- **Crisis Detection**: The system monitors for high-risk language
- **Emergency Button**: Click for immediate access to crisis resources
- **Nigerian Resources**: Includes local emergency contacts (112, SURPIN)

### CBT Approach

The chatbot uses Cognitive Behavioral Therapy techniques including:

- Thought pattern identification
- Cognitive distortion recognition
- Gentle questioning for self-reflection
- Small, manageable action suggestions

## Technical Details

### Model Information

- **Model**: TinyLLaMA-1.1B-Chat-v1.0
- **Size**: ~2.2GB
- **Type**: Causal Language Model optimized for chat
- **Performance**: Runs well on modest hardware

### Architecture

```
Frontend (HTML/CSS/JS) ↔ Flask Backend ↔ TinyLLaMA Model
```

### File Structure

```
flask_mental_health_chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (optional)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Styles
    └── script.js         # Frontend JavaScript
```

## Troubleshooting

### Model Loading Issues

- **Slow Loading**: First run downloads ~2.2GB. Be patient!
- **Memory Error**: Ensure you have at least 4GB RAM available
- **Disk Space**: Model needs ~5GB total storage space

### Performance Optimization

- **GPU**: If you have CUDA-compatible GPU, the model will automatically use it
- **CPU Only**: Model runs fine on CPU but may be slower
- **Memory**: Close other applications to free up RAM

### Common Error Solutions

#### "Model is still loading"

- Wait for the download to complete (first run only)
- Check your internet connection
- Ensure sufficient disk space

#### "Connection Error"

- Restart the Flask application
- Check if port 5000 is available
- Try `python app.py` again

#### "Import Error"

- Ensure you're in the virtual environment
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## Development Notes

### Model Customization

You can modify the model behavior by adjusting:

- Temperature (creativity): `temperature=0.7`
- Response length: `max_length` parameter
- System prompts in the code

### Adding Features

- Crisis keywords can be modified in `assess_risk()` function
- CBT prompts can be customized in `generate_therapeutic_response()`
- UI can be enhanced by modifying templates and CSS

### Performance Monitoring

The app includes:

- Model status checking endpoint (`/api/health`)
- Error handling and fallbacks
- Loading indicators for user feedback

## Security & Privacy

- All conversations stay on your local device
- No data is sent to external servers after initial model download
- Model files are cached locally for offline use
- No logging of user conversations

## Student Project Notes

This implementation is perfect for:

- **Academic Projects**: Demonstrates AI, NLP, and web development
- **Privacy Research**: Shows local AI deployment
- **Mental Health Tech**: Combines psychology with technology
- **Full-Stack Development**: Covers frontend, backend, and ML integration

## License & Ethics

- Built for educational and supportive purposes
- Not a replacement for professional mental health care
- Includes crisis detection and emergency resources
- Encourages professional help when needed

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all requirements are met
3. Try running in a fresh virtual environment
4. Check the console output for specific error messages

---

**Important**: This chatbot is for educational and support purposes only. It is not a substitute for professional mental health care. If you or someone you know is in crisis, please contact emergency services or mental health professionals immediately.
