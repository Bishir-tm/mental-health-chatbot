
import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get('messages', [])

    if not messages:
        return jsonify({'error': 'No messages found.'}), 400

    # The rest of the AI logic will go here
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
    prompt = f"""You are a risk assessment expert for a mental health chatbot. Your primary responsibility is to identify any indication of a user being in an imminent crisis situation. It is crucial to avoid over-reacting to general feelings of depression or hopelessness. Only escalate if there is a clear and immediate danger.

    Based on the user's input, determine if the user is in a high-risk situation requiring immediate professional help. A high-risk situation is defined by explicit statements of self-harm, a plan to self-harm, or an intent to act on suicidal thoughts immediately.

    Respond with a JSON object with two keys: 'is_high_risk' (boolean) and 'response' (string).

    If the user is in a high-risk situation (imminent danger):
    1. Set is_high_risk to true.
    2. Generate a response that is first calming and empathetic, then clearly and directly provides resources. The response should be something like: "It sounds like you are going through a very difficult time, and I want you to know that your safety is the most important thing. Please connect with someone who can support you right now. You can call the Nigerian emergency hotline at 112, or reach out to the Suicide Research and Prevention Initiative (SURPIN) at 08092106463."

    If the user is NOT in a high-risk situation (no imminent danger, even if they express sadness or hopelessness):
    1. Set is_high_risk to false.
    2. Leave the response field empty.

    User Input: {user_input}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    # Debugging: Print the raw response from the API
    print("Gemini API Response (Risk Assessment):", response.text)

    try:
        # Attempt to parse the JSON response
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Handle cases where the response is not valid JSON
        return {"is_high_risk": False, "response": ""}

def generate_therapeutic_response(user_input, chat_history):
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    prompt = f"""You are a chatbot designed to provide Cognitive Behavioral Therapy (CBT)-based support. Your goal is to help users identify and challenge their negative thought patterns.

    User History:
    {history_str}

    Based on the user's input, generate a response that is:
    1.  **Empathetic and Validating**: Start by acknowledging the user's feelings.
    2.  **CBT-Focused**: Gently guide the user to examine their thoughts. Help them identify potential cognitive distortions (e.g., all-or-nothing thinking, catastrophizing).
    3.  **Action-Oriented**: Encourage a small, manageable step, like reframing a thought or a simple behavioral experiment.
    4.  **Concise**: Keep the response to a few clear, supportive sentences.

    Avoid giving generic advice. Instead, ask questions that prompt reflection.

    User Input: {user_input}
    Response:"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text


if __name__ == '__main__':
    app.run(debug=True)
