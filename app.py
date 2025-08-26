import os
import json
import re
from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Global variables to store the model and tokenizer
model = None
tokenizer = None
text_generator = None

def initialize_model():
    """Initialize TinyLLaMA model and tokenizer"""
    global model, tokenizer, text_generator
    
    try:
        print("Loading TinyLLaMA model... This may take a few minutes on first run.")
        
        # Model name for TinyLLaMA 1.1B
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
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
        
        print("TinyLLaMA model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def generate_response(prompt, max_length=50):  # Even shorter
    """Generate response using TinyLLaMA with aggressive cleaning"""
    global text_generator
    
    try:
        # Simpler prompt format
        formatted_prompt = f"You are a supportive mental health assistant. User says: {prompt}\nYour response:"
        
        outputs = text_generator(
            formatted_prompt,
            max_new_tokens=max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            truncation=True,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        generated_text = outputs[0]['generated_text']
        
        # Extract response after "Your response:"
        if "Your response:" in generated_text:
            response = generated_text.split("Your response:")[-1].strip()
        else:
            response = generated_text[len(formatted_prompt):].strip()
        
        # Aggressive cleaning - stop at ANY indication of dialogue
        dialogue_indicators = [
            "User", "user", "Human", "human", "Assistant", "assistant",
            "Q:", "A:", "Question:", "Answer:", "Me:", "You:", "\n"
        ]
        
        for indicator in dialogue_indicators:
            if indicator in response:
                response = response.split(indicator)[0].strip()
        
        # Take only the first sentence
        first_sentence = response.split('.')[0] + '.' if '.' in response else response
        
        # Remove any remaining problematic patterns
        first_sentence = first_sentence.replace('"', '').replace("'", '').strip()
        
        return first_sentence if first_sentence and len(first_sentence) > 5 else "I understand. Can you tell me more about how you're feeling?"
        
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
        r'\b(kill myself|end my life|suicide|want to die)\b',
        r'\b(going to hurt myself|plan to hurt|self harm)\b',
        r'\b(can\'t go on|nothing to live for|better off dead)\b',
        r'\b(going to end it|ready to die|want to disappear forever)\b'
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
            history_context += f"{role}: {msg['content']}\n"
    
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
    print("Starting AI Mental Health Chatbot...")
    print("Initializing TinyLLaMA model...")
    
    if initialize_model():
        print("✅ Model loaded successfully!")
        print("🚀 Starting Flask server...")
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("❌ Failed to load model. Please check your internet connection and try again.")
        print("Make sure you have enough disk space and RAM (at least 4GB recommended).")