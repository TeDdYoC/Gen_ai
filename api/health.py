import os
from flask import jsonify, request

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS_JSON")

def handler(request):
    """Vercel serverless function entry point for health check"""
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running",
        "gemini_configured": bool(GEMINI_API_KEY),
        "gcp_configured": bool(GCP_CREDENTIALS_JSON)
    })
    
