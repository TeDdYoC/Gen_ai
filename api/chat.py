import os
import json
import google.generativeai as genai
from flask import request, jsonify
import traceback

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
 
def handler(request):
    """Vercel serverless function entry point for chat"""
    print("💬 /api/chat endpoint called.")
    
    if request.method == 'GET':
        return jsonify({"message": "Chat endpoint is working. Send a POST request with history."})
    
    if not GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY environment variable is not set.")
        return jsonify({"error": "GEMINI_API_KEY not configured."}), 500
    
    try:
        data = request.get_json()
        if not data:
            print("❌ ERROR: No JSON data received.")
            return jsonify({"error": "No JSON data received."}), 400
            
        history = data.get('history', [])
        language = data.get('language', 'English')
        
        if not history:
            print("❌ ERROR: No chat history provided.")
            return jsonify({"error": "No chat history provided."}), 400
        
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        chat = gemini_model.start_chat(history=history[:-1])
        user_question = history[-1]['parts'][0]['text']
        
        prompt = f"Based on the document context I provided earlier, answer this question in {language}: {user_question}"
        print("Waiting for Gemini API response...")
        response = chat.send_message(prompt)
        print("✅ AI chat response generated successfully.")
        
        return jsonify({"response": response.text})
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ FATAL ERROR in /api/chat: {str(e)}")
        print(error_traceback)
        return jsonify({"error": str(e), "traceback": error_traceback}), 500
