
import io

import os
import json

gcp_creds_json = os.environ.get("GCP_CREDENTIALS_JSON")
print(f"DEBUG: GCP_CREDENTIALS_JSON is set: {bool(gcp_creds_json)}")
if gcp_creds_json:
    try:
        parsed_json = json.loads(gcp_creds_json)
        print(f"DEBUG: JSON parsed successfully. Keys: {parsed_json.keys()}")
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON parsing failed: {e}")
        print(f"DEBUG: Raw JSON (first 50 chars): {gcp_creds_json[:50]}")
        

import google.generativeai as genai
import PyPDF2
import docx
import datetime
import uuid
import traceback
from flask import Flask, request, jsonify
from google.cloud import vision, storage, bigquery
from google.oauth2 import service_account


app = Flask(__name__)

# --- Your existing code from analyze.py, chat.py, and health.py ---
# --- Environment Variables (Set these in Vercel Dashboard) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET")
GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS_JSON")

# --- Initialize GCP credentials from environment ---
credentials = None
if GCP_CREDENTIALS_JSON:
    try:
        credentials_info = json.loads(GCP_CREDENTIALS_JSON)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        print("✅ GCP Credentials loaded successfully.")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Failed to parse GCP_CREDENTIALS_JSON. Details: {e}")
    except Exception as e:
        print(f"❌ ERROR: GCP Credentials loading failed. Details: {e}")
else:
    print("⚠️ WARNING: GCP_CREDENTIALS_JSON environment variable is not set.")

# --- Embedded Knowledge Base ---
LEGAL_KNOWLEDGE_BASE = """
--- BHARATIYA NYAYA SANHITA (BNS) SUMMARY ---
... (rest of the knowledge base) ...
"""

def extract_text_from_file_in_memory(file_storage, filename):
    ... (rest of the extract_text_from_file_in_memory function) ...

def upload_to_gcs_from_memory(file_bytes, filename, document_id):
    ... (rest of the upload_to_gcs_from_memory function) ...

def log_to_bigquery(metadata):
    ... (rest of the log_to_bigquery function) ...

# --- Define API routes using Flask decorators ---
@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze_handler():
    # Your existing handler logic from analyze.py
    if request.method == 'GET':
        return jsonify({"message": "Analyze endpoint is working. Send a POST request with a file."})
    
    # ... rest of the POST logic ...

@app.route('/api/chat', methods=['GET', 'POST'])
def chat_handler():
    # Your existing handler logic from chat.py
    if request.method == 'GET':
        return jsonify({"message": "Chat endpoint is working. Send a POST request with history."})
    
    # ... rest of the POST logic ...

@app.route('/api/health', methods=['GET'])
def health_handler():
    # Your existing handler logic from health.py
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running.",
        "gemini_configured": bool(GEMINI_API_KEY),
        "gcp_configured": bool(GCP_CREDENTIALS_JSON)
    })
