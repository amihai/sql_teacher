"""Helper functions"""


def get_conversations(session):
    """Extract and format conversations from session data"""

    conversation_info = []
    print(session["events"])

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