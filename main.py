"""
Conversational AI Phone Responder using Google Cloud Functions.

This module provides the entry point for handling phone calls using
Vertex AI (Gemini) and Dialogflow for conversational AI capabilities.
"""

import functions_framework
from google.cloud import aiplatform
from google.cloud import dialogflow_v2 as dialogflow
import json
import os


@functions_framework.http
def handle_call(request):
    """
    HTTP Cloud Function entry point for handling phone call interactions.
    
    Args:
        request (flask.Request): The request object.
        
    Returns:
        A JSON response with the AI-generated reply.
    """
    # Parse request data
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return {"error": "Invalid request"}, 400
    
    # Extract user input from the request
    user_input = request_json.get("input", "")
    session_id = request_json.get("session_id", "default-session")
    
    if not user_input:
        return {"error": "No input provided"}, 400
    
    # Process the input with Dialogflow or Vertex AI
    response_text = process_conversation(user_input, session_id)
    
    return {
        "response": response_text,
        "session_id": session_id
    }, 200


def process_conversation(user_input: str, session_id: str) -> str:
    """
    Process user input using Dialogflow and/or Vertex AI.
    
    Args:
        user_input: The user's spoken/text input
        session_id: Unique session identifier for the conversation
        
    Returns:
        AI-generated response text
    """
    # Get configuration from environment variables
    project_id = os.environ.get("GCP_PROJECT_ID")
    
    if not project_id:
        return "Configuration error: GCP_PROJECT_ID not set"
    
    # Example: Use Dialogflow for intent detection
    # This is a placeholder - actual implementation would depend on specific requirements
    try:
        # Initialize Dialogflow session client
        session_client = dialogflow.SessionsClient()
        session_path = session_client.session_path(project_id, session_id)
        
        # Create text input
        text_input = dialogflow.TextInput(text=user_input, language_code="en-US")
        query_input = dialogflow.QueryInput(text=text_input)
        
        # Detect intent
        response = session_client.detect_intent(
            request={"session": session_path, "query_input": query_input}
        )
        
        return response.query_result.fulfillment_text
        
    except Exception as e:
        # Fallback or error handling
        return f"Sorry, I encountered an error: {str(e)}"


def generate_with_gemini(prompt: str) -> str:
    """
    Generate response using Vertex AI Gemini model.
    
    Args:
        prompt: The input prompt for Gemini
        
    Returns:
        Generated text response
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)
    
    # Use Gemini for text generation
    # This is a placeholder for actual Gemini API usage
    # Actual implementation would use the generative AI endpoint
    
    return "Generated response using Gemini"
