"""Helper functions"""


def get_conversations(session):
    """Extract and format conversations from session data"""

    conversation_info = []

    for conversation in session["events"]:
        if "text" in conversation["content"]["parts"][0]:
            conversation_info.append({
                conversation["content"]["role"]: conversation["content"]["parts"][0]["text"]
            })

    merged = {}
    for i in range(0, len(conversation_info), 2):
        if i + 1 < len(conversation_info):
            merged[i // 2] = {**conversation_info[i], **conversation_info[i + 1]}
        else:
            merged[i // 2] = conversation_info[i]

    return merged


def get_first_user_question(session):
    """Return the first 20 chars from the
    first user question in a session"""
    if session["events"]:
        if "text" in session["events"][0]["content"]["parts"][0]:
            return session["events"][0]["content"]["parts"][0]["text"][0:20]


def extract_model_response_text(response):
    """Extract the model's text response from ADK API response
    
    Args:
        response: The response dictionary from ADK API send_message call
        
    Returns:
        str: The extracted text content from the model's response, or string 
             representation of response if structure is unexpected
    """
    try:
        # Handle response with events array (similar to session structure)
        if isinstance(response, dict):
            if "events" in response:
                # Look for the last model response in events
                for event in reversed(response["events"]):
                    if (event.get("content", {}).get("role") == "model" and
                        "parts" in event.get("content", {}) and
                        len(event["content"]["parts"]) > 0 and
                        "text" in event["content"]["parts"][0]):
                        return event["content"]["parts"][0]["text"]
            
            # Handle direct response structure
            if "content" in response:
                if (response["content"].get("role") == "model" and
                    "parts" in response["content"] and
                    len(response["content"]["parts"]) > 0 and
                    "text" in response["content"]["parts"][0]):
                    return response["content"]["parts"][0]["text"]
            
            # Handle response with parts directly
            if "parts" in response and len(response["parts"]) > 0:
                if "text" in response["parts"][0]:
                    return response["parts"][0]["text"]
        
        # Fallback: return the response as string
        return str(response)
    except (KeyError, IndexError, TypeError):
        # If structure is unexpected, return the response as string
        return str(response)


