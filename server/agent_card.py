# server/agent_card.py
AGENT_CARD = {
    "id":           "echo-agent-v1",
    "name":         "Echo Agent",
    "version":      "1.0.0",
    "description":  "A simple agent that echoes back any text it receives.",
    # "url":          "http://localhost:8000",    # will be updated at deploy time
    "url":          "https://echo-a2a-agent-1095504584646.us-central1.run.app",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id":           "echo",
            "name":         "Echo",
            "description":  "Returns the user message verbatim.",
            "inputModes":   ["text/plain"],
            "outputModes":  ["text/plain"]
        },
        {
            "id":           "summarise",
            "name":         "Summarise",
            "description":  "Returns a concise summary of the provided text.",
            "inputModes":   ["text/plain"],
            "outputModes":  ["text/plain"]
        }
    ],
    "contact": {
        "email": "jhenson1504@gmail.com"    # this is just my email
    }
}

def validate_card(card: dict) -> bool:
    """Validates whether all required fields are present in an agent's card or not.
    
    Args:
        card (dict): dictionary containing an agent's fields

    Returns:
        bool: Boolean value (True/False) depending on whether the agent card has all the required fields
    """
    
    # Required top-level fields
    required_fields = [
        "id",
        "name",
        "version",
        "description",
        "url",
        "capabilities",
        "defaultInputModes",
        "defaultOutputModes",
        "skills",
        "contact"
    ]

    # ---- Validate required fields ---- #
    for field in required_fields:
        if field not in card:
            return False
        
    # -- Validate capabilities -- #
    if not isinstance(card["capabilities"], dict):
        return False
    
    if "streaming" not in card["capabilities"] or "pushNotifications" not in card["capabilities"]:
        return False
    
    # -- Validate contact -- #
    if not isinstance(card["contact"], dict):
        return False
    
    if "email" not in card["contact"]:              # might be updated later to accommodate for other contact methods, i.e. phone
        return False
    
    # -- Validate skills -- #
    if not isinstance(card["skills"], list) or len(card["skills"]) == 0:
        return False
    
    required_skill_fields = [
        "id",
        "name",
        "description",
        "inputModes",
        "outputModes"
    ]

    for skill in card["skills"]:
        for field in required_skill_fields:
            if field not in skill:
                return False
            
    return True
