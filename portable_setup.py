
import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def print_step(step, description):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {description}")
    print('='*60)

def create_portable_structure():
    """Create portable directory structure"""
    print("Creating portable structure...")
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create cache directory
    cache_dir = models_dir / "transformers_cache"
    cache_dir.mkdir(exist_ok=True)
    
    return models_dir, cache_dir

def download_and_cache_model(cache_dir):
    """Download model to local cache directory"""
    print("Downloading TinyLLaMA model to local cache...")

    # Use raw strings for Windows paths
    cache_path = str(cache_dir.absolute())
    
    download_script = f'''
import os
os.environ["TRANSFORMERS_CACHE"] = r"{cache_path}"
os.environ["HF_HOME"] = r"{cache_path}"

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Downloading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    cache_dir=r"{cache_path}"
)

print("Model downloaded successfully!")
'''
    
    # Write and run download script
    with open("download_model.py", "w") as f:
        f.write(download_script)
    
    try:
        subprocess.run([sys.executable, "download_model.py"], check=True)
        os.remove("download_model.py")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading model: {e}")
        return False

def create_portable_app():
    """Create modified app.py that uses local cache"""
    print("Creating portable app.py...")
    
    portable_app_content = '''import os
import json
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dotenv import load_dotenv

load_dotenv()

# Set local cache directory
MODELS_DIR = Path(__file__).parent / "models" / "transformers_cache"
os.environ["TRANSFORMERS_CACHE"] = str(MODELS_DIR.absolute())
os.environ["HF_HOME"] = str(MODELS_DIR.absolute())

app = Flask(__name__)

# Global variables to store the model and tokenizer
model = None
tokenizer = None
text_generator = None

def initialize_model():
    """Initialize TinyLLaMA model and tokenizer from local cache"""
    global model, tokenizer, text_generator
    
    try:
        print("Loading TinyLLaMA model from local cache...")
        
        # Model name for TinyLLaMA 1.1B
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        # Load tokenizer and model from cache
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=MODELS_DIR,
            local_files_only=True  # Only use cached files
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            cache_dir=MODELS_DIR,
            local_files_only=True  # Only use cached files
        )
        
        # Create text generation pipeline
        text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device=0 if torch.cuda.is_available() else -1,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        print("Model loaded successfully from local cache!")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure the model files are in the models/transformers_cache directory")
        return False

def generate_response(prompt, max_length=200):
    """Generate response using TinyLLaMA"""
    global text_generator
    
    try:
        # Format prompt for chat model
        formatted_prompt = f"<|system|>\nYou are a helpful mental health support assistant trained in Cognitive Behavioral Therapy (CBT). Provide empathetic, supportive responses.\n<|user|>\n{prompt}\n<|assistant|>\n"
        
        # Generate response with max_new_tokens instead of max_length
        outputs = text_generator(
            formatted_prompt,
            max_new_tokens=max_length,  # This is the key fix!
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            truncation=True,  # Add explicit truncation
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # Extract the generated text
        generated_text = outputs[0]['generated_text']
        
        # Extract only the assistant's response
        if "<|assistant|>" in generated_text:
            response = generated_text.split("<|assistant|>")[-1].strip()
        else:
            response = generated_text[len(formatted_prompt):].strip()
        
        # Clean up the response
        response = response.replace("<|end|>", "").replace("<|endoftext|>", "").strip()
        
        # Limit response length
        sentences = response.split('. ')
        if len(sentences) > 3:
            response = '. '.join(sentences[:3]) + '.'
        
        return response if response else "I understand you're going through something difficult. Can you tell me more about how you're feeling?"
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm here to listen and support you. Can you share what's on your mind today?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global text_generator
    
    if text_generator is None:
        return jsonify({'error': 'Model is still loading. Please wait a moment and try again.'}), 503
    
    data = request.get_json()
    messages = data.get('messages', [])

    if not messages:
        return jsonify({'error': 'No messages found.'}), 400

    try:
        user_input = messages[-1]['content']
        chat_history = messages[:-1]

        # Assess risk
        risk_assessment = assess_risk(user_input)

        if risk_assessment.get('is_high_risk'):
            return jsonify({'response': risk_assessment.get('response'), 'crisis': True})

        # Generate therapeutic response
        therapeutic_response = generate_therapeutic_response(user_input, chat_history)
        return jsonify({'response': therapeutic_response, 'crisis': False})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

def assess_risk(user_input):
    """Assess if user input indicates high-risk situation"""
    
    # High-risk keywords and phrases
    high_risk_patterns = [
        r'\\b(kill myself|end my life|suicide|want to die)\\b',
        r'\\b(going to hurt myself|plan to hurt|self harm)\\b',
        r'\\b(can\\'t go on|nothing to live for|better off dead)\\b',
        r'\\b(going to end it|ready to die|want to disappear forever)\\b'
    ]
    
    # Check for high-risk patterns
    user_lower = user_input.lower()
    for pattern in high_risk_patterns:
        if re.search(pattern, user_lower):
            return {
                "is_high_risk": True,
                "response": "It sounds like you are going through a very difficult time, and I want you to know that your safety is the most important thing. Please connect with someone who can support you right now. You can call the Nigerian emergency hotline at 112, or reach out to the Suicide Research and Prevention Initiative (SURPIN) at 08092106463. You don't have to go through this alone."
            }
    
    # Use AI for more nuanced assessment
    assessment_prompt = f"""Analyze this message for signs of immediate self-harm risk. Respond with only 'HIGH_RISK' or 'LOW_RISK'.

Look for explicit statements about:
- Plans to hurt oneself
- Immediate intent to self-harm
- Active suicidal ideation with method or timeline

Message: "{user_input}"

Assessment:"""

    try:
        assessment_response = generate_response(assessment_prompt, max_length=10)
        
        if "HIGH_RISK" in assessment_response.upper():
            return {
                "is_high_risk": True,
                "response": "It sounds like you are going through a very difficult time, and I want you to know that your safety is the most important thing. Please connect with someone who can support you right now. You can call the Nigerian emergency hotline at 112, or reach out to the Suicide Research and Prevention Initiative (SURPIN) at 08092106463. You don't have to go through this alone."
            }
    except:
        pass
    
    return {"is_high_risk": False, "response": ""}

def generate_therapeutic_response(user_input, chat_history):
    """Generate CBT-focused therapeutic response"""
    
    # Build conversation context
    history_context = ""
    if chat_history:
        recent_messages = chat_history[-4:]  # Last 4 messages for context
        for msg in recent_messages:
            role = "User" if msg['role'] == 'user' else "Assistant"
            history_context += f"{role}: {msg['content']}\\n"
    
    # Create CBT-focused prompt
    prompt = f"""You are a mental health support chatbot specializing in Cognitive Behavioral Therapy (CBT). Your goal is to help users identify and challenge negative thought patterns.

Conversation history:
{history_context}

User's current message: "{user_input}"

Provide a response that is:
1. Empathetic and validating - acknowledge their feelings
2. CBT-focused - help identify thinking patterns or cognitive distortions
3. Ask gentle questions to promote self-reflection
4. Suggest a small, manageable step or reframing technique
5. Keep it concise and supportive (2-3 sentences max)

Response:"""

    return generate_response(prompt, max_length=100)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the model is loaded and ready"""
    global text_generator
    
    if text_generator is None:
        return jsonify({'status': 'loading', 'message': 'Model is still loading...'}), 503
    else:
        return jsonify({'status': 'ready', 'message': 'Model is ready to chat!'})

if __name__ == '__main__':
    print("Starting AI Mental Health Chatbot (Portable Version)...")
    
    # Check if model cache exists
    if not MODELS_DIR.exists() or not any(MODELS_DIR.iterdir()):
        print("Model cache not found!")
        print("Please run the portable setup script first to download the model.")
        print("Or copy the 'models' folder from a computer that has already downloaded it.")
        sys.exit(1)
    
    print("Model cache found, initializing...")
    
    if initialize_model():
        print("Model loaded successfully!")
        print("Starting Flask server...")
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("Failed to load model from cache.")
        print("You may need to re-download the model or check the cache integrity.")
'''
    
    with open("app_portable.py", "w") as f:
        f.write(portable_app_content)
    
    return True

def create_run_scripts():
    """Create platform-specific run scripts"""
    
    # Windows batch file
    windows_script = '''@echo off
echo AI Mental Health Chatbot - Portable Version
echo ===============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run portable_setup.py first
    pause
    exit /b 1
)

REM Check if models directory exists
if not exist "models" (
    echo Models directory not found!
    echo Please run portable_setup.py first to download the model
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\\Scripts\\activate

echo Starting portable chatbot server...
echo.
echo The chatbot will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app_portable.py

echo.
echo Chatbot stopped. Press any key to exit.
pause'''
    
    # Linux/Mac shell script
    unix_script = '''#!/bin/bash
echo "AI Mental Health Chatbot - Portable Version"
echo "==============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run portable_setup.py first"
    exit 1
fi

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "Models directory not found!"
    echo "Please run portable_setup.py first to download the model"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting portable chatbot server..."
echo ""
echo "The chatbot will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app_portable.py'''
    
    with open("run_portable.bat", "w") as f:
        f.write(windows_script)
    
    with open("run_portable.sh", "w") as f:
        f.write(unix_script)
    
    # Make shell script executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run_portable.sh", 0o755)

def main():
    """Main setup function for portable version"""
    print("AI Mental Health Chatbot - Portable Setup")
    print("This will create a portable version that can be zipped and transferred")
    
    print_step(1, "Creating Portable Structure")
    models_dir, cache_dir = create_portable_structure()
    
    print_step(2, "Downloading Model to Local Cache")
    if not download_and_cache_model(cache_dir):
        print("Failed to download model")
        return False
    
    print_step(3, "Creating Portable App")
    create_portable_app()
    
    print_step(4, "Creating Run Scripts")
    create_run_scripts()
    
    print_step(5, "Setup Complete!")
    print("Portable setup complete!")
    print("\nYour project is now portable! Here's what was created:")
    print("- models/ - Contains the TinyLLaMA model files")
    print("- app_portable.py - Modified app that uses local cache")
    print("- run_portable.bat/.sh - Easy run scripts")
    
    print("\nTo transfer to another computer:")
    print("1. Zip the entire project folder")
    print("2. Extract on the target computer")
    print("3. Install Python dependencies: pip install -r requirements.txt")
    print("4. Run: python app_portable.py (or use the run scripts)")
    
    print("\nNo re-downloading needed on the target computer!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\nPortable setup failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
