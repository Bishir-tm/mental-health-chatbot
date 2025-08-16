import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Gemini API
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual Google Gemini API key
# or set it as an environment variable (recommended).
# For example: os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Define the prompts
ASSESS_RISK_PROMPT = """You are a risk assessment expert for a mental health chatbot.

Based on the user's input, determine if the user is in a high-risk situation requiring professional help.
If the user is in a high-risk situation, set isHighRisk to true and generate a message suggesting a professional referral.
If the user is not in a high-risk situation, set isHighRisk to false and leave the response empty.

User Input: {user_input}
"""

THERAPEUTIC_RESPONSE_PROMPT = """You are a chatbot designed to provide Cognitive Behavioral Therapy (CBT)-based support. Your goal is to help users identify and challenge their negative thought patterns.

User History: {user_history}

Based on the user's input, generate a response that is:
1.  **Empathetic and Validating**: Start by acknowledging the user's feelings.
2.  **CBT-Focused**: Gently guide the user to examine their thoughts. Help them identify potential cognitive distortions (e.g., all-or-nothing thinking, catastrophizing).
3.  **Action-Oriented**: Encourage a small, manageable step, like reframing a thought or a simple behavioral experiment.
4.  **Concise**: Keep the response to a few clear, supportive sentences.

Avoid giving generic advice. Instead, ask questions that prompt reflection.

User Input: {user_input}
Response:"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    chat_history = data.get('chatHistory', [])

    user_messages = [msg for msg in chat_history if msg['role'] == 'user']
    latest_user_message = user_messages[-1] if user_messages else None

    if not latest_user_message:
        return jsonify({'error': 'No user message found.'}), 400

    user_input = latest_user_message['content']
    user_history = "\n".join([f"User: {msg['content']}" for msg in user_messages[:-1]])

    try:
        # Risk Assessment
        risk_assessment_full_prompt = ASSESS_RISK_PROMPT.format(user_input=user_input)
        risk_response = model.generate_content(risk_assessment_full_prompt)
        
        # Assuming the model's response for risk assessment can be parsed to determine high risk
        # This part needs careful handling as Gemini's output might not be directly parsable as JSON
        # For simplicity, let's assume a keyword check or a structured output from Gemini
        # In a real scenario, you'd use a more robust parsing mechanism or a function calling approach
        
        # Placeholder for risk assessment logic:
        # If the model's response contains certain keywords indicating high risk,
        # or if you can structure the prompt to return a boolean/JSON.
        # For now, let's assume if the response contains "professional help" or "high risk"
        # it's considered high risk. This is a very basic and potentially unreliable check.
        
        is_high_risk = "professional help" in risk_response.text.lower() or "high risk" in risk_response.text.lower()
        
        if is_high_risk:
            # Extract the suggested referral message from the risk_response
            # This also needs robust parsing based on how your prompt is designed
            response_content = risk_response.text # Assuming the full response is the referral message
            return jsonify({'response': response_content})
        else:
            # Therapeutic Response
            therapeutic_full_prompt = THERAPEUTIC_RESPONSE_PROMPT.format(
                user_input=user_input,
                user_history=user_history
            )
            therapeutic_response = model.generate_content(therapeutic_full_prompt)
            return jsonify({'response': therapeutic_response.text})

    except Exception as e:
        print(f"Error getting AI response: {e}")
        return jsonify({'error': 'An error occurred while processing your request. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)