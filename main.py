"""
Conversational AI Phone Responder using Google Cloud Functions.

This module provides the entry point for handling phone calls using
Vertex AI (Gemini) and Dialogflow for conversational AI capabilities.
"""

import functions_framework
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def handle_call(request):
    """
    HTTP Cloud Function entry point for handling Dialogflow webhook requests.
    
    This function receives a JSON request from Dialogflow, extracts the user's
    spoken text (query_text), sends it to Gemini 2.5 Flash for AI processing,
    and returns a properly formatted fulfillment response.
    
    Args:
        request (flask.Request): The request object containing Dialogflow webhook data.
        
    Returns:
        A JSON response in Dialogflow fulfillment format with the AI-generated reply.
    """
    # Parse request data from Dialogflow
    request_json = request.get_json(silent=True)
    
    if not request_json:
        logger.error("Invalid request: No JSON data received")
        return {"error": "Invalid request"}, 400
    
    # Extract query_text from Dialogflow request format
    # Dialogflow sends data in the format: { "queryResult": { "queryText": "..." } }
    query_result = request_json.get("queryResult", {})
    query_text = query_result.get("queryText", "")
    
    # Log the extracted query text
    logger.info(f"Extracted query_text from Dialogflow: {query_text}")
    
    if not query_text:
        logger.warning("No query_text found in request")
        return {"error": "No query_text provided"}, 400
    
    # Send the query_text to Gemini and get AI response
    try:
        ai_response = call_gemini_api(query_text)
        logger.info(f"Gemini response: {ai_response}")
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        ai_response = "I'm sorry, I'm having trouble processing your request right now."
    
    # Format response in Dialogflow fulfillment format
    fulfillment_response = create_fulfillment_response(ai_response)
    
    return fulfillment_response, 200


def call_gemini_api(query_text: str) -> str:
    """
    Call the Gemini 2.5 Flash model using Vertex AI library.
    
    This function sends the user's query text as a prompt to Gemini 2.5 Flash
    and returns the AI-generated text response. This is a non-streaming,
    simple text-in, text-out call.
    
    Args:
        query_text: The user's spoken/text input to send to Gemini
        
    Returns:
        AI-generated text response from Gemini
    """
    # Get configuration from environment variables
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set")
    
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    
    # Initialize Gemini 2.5 Flash model
    model = GenerativeModel("gemini-2.5-flash")
    
    # Generate response (non-streaming)
    response = model.generate_content(query_text)
    
    # Extract and return the text from the response
    return response.text


def create_fulfillment_response(response_text: str) -> dict:
    """
    Create a Dialogflow fulfillment response with the AI-generated text.
    
    This function formats the response in the specific JSON structure that
    Dialogflow expects for a fulfillment response, telling Dialogflow what
    text to say back to the caller.
    
    Args:
        response_text: The text response from Gemini to send back to the caller
        
    Returns:
        A dictionary in Dialogflow fulfillment response format
    """
    return {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [response_text]
                    }
                }
            ]
        }
    }
