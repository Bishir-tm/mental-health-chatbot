# AI Mental Health Chatbot (Flask Version)

This is a Flask-based replication of the AI Mental Health Chatbot application.

## Setup and Run Instructions

1.  **Navigate to the application directory:**
    ```bash
    cd C:\Users\Personal Computer\Documents\Bishir TM\flask_mental_health_chatbot
    ```

2.  **Install Python dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```

3.  **Set your Google Gemini API Key:**
    You need a Google Gemini API key to run this application. You can obtain one from [Google AI Studio](https://aistudio.google.com/fundamentals/api_key).

    Set the API key as an environment variable:
    
    **On Windows (Command Prompt):**
    ```bash
    set GOOGLE_API_KEY=YOUR_API_KEY
    ```
    **On Windows (PowerShell):**
    ```powershell
    $env:GOOGLE_API_KEY="YOUR_API_KEY"
    ```
    **On macOS/Linux:**
    ```bash
    export GOOGLE_API_KEY=YOUR_API_KEY
    ```
    Replace `YOUR_API_KEY` with your actual API key.

4.  **Run the Flask application:**
    ```bash
    flask run
    ```

    The application will typically run on `http://127.0.0.1:5000/`.

## Important Notes

*   The risk assessment logic in `app.py` is a basic keyword check. For a production-grade application, you would need a more robust method to parse the AI model's output for risk assessment (e.g., structured JSON output from the model, or a more sophisticated NLP approach).
*   The styling is a basic recreation of the original application's look and feel using plain CSS. It does not use Tailwind CSS.
