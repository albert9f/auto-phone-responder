# Auto Phone Responder

An intelligent phone call responder powered by Google AI Studio and Google Cloud Platform services, built for Ceuric.

## Overview

This project implements an automated phone responder that uses conversational AI to handle incoming phone calls. It integrates Google Cloud Functions, Dialogflow, and Google AI Studio (Gemini 2.0 Flash) to provide natural, intelligent responses to callers in real-time.

## Architecture

The system consists of the following components:

1. **Dialogflow**: Handles phone call integration and natural language understanding
2. **Google Cloud Functions**: Serverless HTTP endpoint that processes webhook requests
3. **Google AI Studio (Gemini 2.0 Flash)**: Provides AI-powered conversational responses via API key

### Flow Diagram

```
Incoming Call → Dialogflow → Cloud Function (handle_call) → Google AI Studio (Gemini) → Response → Dialogflow → Caller
```

## Features

- **Serverless Architecture**: Runs on Google Cloud Functions for automatic scaling
- **AI-Powered Responses**: Uses Gemini 2.0 Flash from Google AI Studio for intelligent, contextual responses
- **Dialogflow Integration**: Seamless phone call handling with natural language processing
- **Simple API Key Authentication**: No GCP project setup required - just use your Google AI Studio API key
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful error handling with fallback messages

## Prerequisites

- Google AI Studio API key (get one at https://aistudio.google.com/app/apikey)
- Google Cloud Platform account (for Cloud Functions and Dialogflow)
- Python 3.9 or higher
- Google Cloud CLI (gcloud) installed
- Access to the following GCP services:
  - Cloud Functions
  - Dialogflow

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/albert9f/auto-phone-responder.git
cd auto-phone-responder
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Set the following environment variable:

```bash
export GOOGLE_API_KEY="your-google-ai-studio-api-key"
```

To get your API key:
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and set it as the environment variable

## Configuration

### Google Cloud Project Setup

1. **Enable Required APIs**:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable dialogflow.googleapis.com
   ```

2. **Configure Dialogflow**:
   - Create a Dialogflow agent
   - Set up phone integration (Dialogflow Phone Gateway or CCAI)
   - Configure webhook fulfillment to point to your Cloud Function URL

3. **Deploy the Cloud Function**:
   ```bash
   gcloud functions deploy handle_call \
     --runtime python39 \
     --trigger-http \
     --entry-point handle_call \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your-google-ai-studio-api-key
   ```

## Usage

### Running Locally

For local development and testing:

```bash
# Install Functions Framework
pip install functions-framework

# Run the function locally
export GOOGLE_API_KEY="your-google-ai-studio-api-key"
functions-framework --target=handle_call --debug
```

The function will be available at `http://localhost:8080`

### Testing with curl

```bash
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "queryText": "Hello, how are you?"
    }
  }'
```

## Code Structure

### `main.py`

The main module contains three key functions:

#### `handle_call(request)`
- **Purpose**: HTTP entry point for Cloud Functions
- **Input**: Flask request object with Dialogflow webhook data
- **Output**: Dialogflow fulfillment response with AI-generated text
- **Description**: Parses incoming requests, extracts user queries, calls Gemini API, and formats responses

#### `call_gemini_api(query_text)`
- **Purpose**: Interface with Google AI Studio Gemini model
- **Input**: User's spoken/text query
- **Output**: AI-generated response text
- **Description**: Configures the Google Generative AI library with API key, sends prompts to Gemini 2.0 Flash, and returns responses

#### `create_fulfillment_response(response_text)`
- **Purpose**: Format responses for Dialogflow
- **Input**: AI-generated response text
- **Output**: Dialogflow-compatible JSON response
- **Description**: Wraps response text in the proper Dialogflow fulfillment structure

## API Reference

### Request Format (from Dialogflow)

```json
{
  "queryResult": {
    "queryText": "What is your name?",
    "intent": {...},
    "parameters": {...}
  }
}
```

### Response Format (to Dialogflow)

```json
{
  "fulfillment_response": {
    "messages": [
      {
        "text": {
          "text": ["I am an AI assistant..."]
        }
      }
    ]
  }
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | - | Your Google AI Studio API key for Gemini access |

## Error Handling

The function includes comprehensive error handling:

- **No JSON data**: Returns 400 error with "Invalid request" message
- **Missing query_text**: Returns 400 error with "No query_text provided" message
- **Gemini API errors**: Returns fallback message: "I'm sorry, I'm having trouble processing your request right now."
- **Missing API key**: Raises ValueError if GOOGLE_API_KEY is not set

## Logging

The application uses Python's built-in logging module at INFO level:

- Request parsing and query extraction
- Gemini API calls and responses
- Error conditions and exceptions

## Dependencies

- `functions-framework==3.5.0` - Google Cloud Functions framework
- `google-generativeai==0.8.3` - Google AI Studio client library for Gemini
- `google-cloud-dialogflow==2.26.0` - Dialogflow client library
- `flask==3.0.0` - Web framework (required by functions-framework)

## Security Considerations

- **Authentication**: Consider using `--no-allow-unauthenticated` flag and implement proper authentication
- **API Keys**: Never commit API keys to version control. Use environment variables or secret managers
- **Rate Limiting**: Implement rate limiting for production use
- **Input Validation**: Additional validation may be needed for production deployments

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY environment variable not set"**
   - Ensure the environment variable is set before deployment/execution
   - Get your API key from https://aistudio.google.com/app/apikey

2. **Google AI Studio API errors**
   - Verify your API key is valid and active
   - Check that your API key has not exceeded quota limits
   - Ensure you have access to the Gemini 2.0 Flash model

3. **No response from Gemini**
   - Verify your API key is correctly configured
   - Check quota limits for Google AI Studio

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Specify your license here]

## Contact

For questions or support, please contact the repository maintainer.

## Acknowledgments

Built for Ceuric using Google Cloud Platform services.
