import os
import json
import google.generativeai as genai
from flask import request, jsonify

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Handler for Vercel
def handler(request):
    """Vercel serverless function entry point for chat"""
    print("💬 /api/chat endpoint called")
    
    if request.method == 'GET':
        return jsonify({"message": "Chat endpoint is working. Send POST request with history."})
    
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured"}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        history = data.get('history', [])
        language = data.get('language', 'English')
        
        if not history:
            return jsonify({"error": "No chat history provided"}), 400
        
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Start chat with previous history
        chat = gemini_model.start_chat(history=history[:-1])
        user_question = history[-1]['parts'][0]['text']
        
        prompt = f"Based on the document context I provided earlier, answer this question in {language}: {user_question}"
        response = chat.send_message(prompt)
        
        return jsonify({"response": response.text})
        
    except Exception as e:
        print(f"❌ Error in /api/chat: {str(e)}")
        return jsonify({"error": str(e)}), 500