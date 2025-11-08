# Auto Phone Responder

An intelligent phone call responder powered by Google Cloud Platform services, built for Ceuric.

## Overview

This project implements an automated phone responder that uses conversational AI to handle incoming phone calls. It integrates Google Cloud Functions, Dialogflow, and Vertex AI (Gemini 2.5 Flash) to provide natural, intelligent responses to callers in real-time.

## Architecture

The system consists of the following components:

1. **Dialogflow**: Handles phone call integration and natural language understanding
2. **Google Cloud Functions**: Serverless HTTP endpoint that processes webhook requests
3. **Vertex AI (Gemini 2.5 Flash)**: Provides AI-powered conversational responses

### Flow Diagram

```
Incoming Call → Dialogflow → Cloud Function (handle_call) → Vertex AI (Gemini) → Response → Dialogflow → Caller
```

## Features

- **Serverless Architecture**: Runs on Google Cloud Functions for automatic scaling
- **AI-Powered Responses**: Uses Gemini 2.5 Flash for intelligent, contextual responses
- **Dialogflow Integration**: Seamless phone call handling with natural language processing
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful error handling with fallback messages

## Prerequisites

- Google Cloud Platform account
- Python 3.9 or higher
- Google Cloud CLI (gcloud) installed
- Access to the following GCP services:
  - Cloud Functions
  - Vertex AI
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

Set the following environment variables:

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_LOCATION="us-central1"  # Optional, defaults to us-central1
```

## Configuration

### Google Cloud Project Setup

1. **Enable Required APIs**:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable aiplatform.googleapis.com
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
     --set-env-vars GCP_PROJECT_ID=your-project-id,GCP_LOCATION=us-central1
   ```

## Usage

### Running Locally

For local development and testing:

```bash
# Install Functions Framework
pip install functions-framework

# Run the function locally
export GCP_PROJECT_ID="your-project-id"
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
- **Purpose**: Interface with Vertex AI Gemini model
- **Input**: User's spoken/text query
- **Output**: AI-generated response text
- **Description**: Initializes Vertex AI, sends prompts to Gemini 2.5 Flash, and returns responses

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
| `GCP_PROJECT_ID` | Yes | - | Your Google Cloud Project ID |
| `GCP_LOCATION` | No | `us-central1` | GCP region for Vertex AI |

## Error Handling

The function includes comprehensive error handling:

- **No JSON data**: Returns 400 error with "Invalid request" message
- **Missing query_text**: Returns 400 error with "No query_text provided" message
- **Gemini API errors**: Returns fallback message: "I'm sorry, I'm having trouble processing your request right now."

## Logging

The application uses Python's built-in logging module at INFO level:

- Request parsing and query extraction
- Gemini API calls and responses
- Error conditions and exceptions

## Dependencies

- `functions-framework==3.5.0` - Google Cloud Functions framework
- `google-cloud-aiplatform==1.38.1` - Vertex AI client library
- `google-cloud-dialogflow==2.26.0` - Dialogflow client library
- `flask==3.0.0` - Web framework (required by functions-framework)

## Security Considerations

- **Authentication**: Consider using `--no-allow-unauthenticated` flag and implement proper authentication
- **API Keys**: Never commit GCP credentials to version control
- **Rate Limiting**: Implement rate limiting for production use
- **Input Validation**: Additional validation may be needed for production deployments

## Troubleshooting

### Common Issues

1. **"GCP_PROJECT_ID environment variable not set"**
   - Ensure the environment variable is set before deployment/execution

2. **Vertex AI initialization fails**
   - Verify that Vertex AI API is enabled in your project
   - Check that your service account has proper permissions

3. **No response from Gemini**
   - Verify your project has access to Gemini 2.5 Flash model
   - Check quota limits for Vertex AI

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
