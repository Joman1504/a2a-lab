# server/handlers.py
async def handle_task(request) -> str:
    
    print(type(request.message.parts[0]))
    print(request.message.parts[0])

    text_parts = [p.text for p in request.message.parts if p.type == 'text']
    combined = ' '.join(text_parts)

    if not combined:
        return ""
    
    # Split first word to detect command
    first_word = combined.split()[0].lower()
    # SUMMARIZE skill
    if first_word == "!summarize":
        return "A system of cells interlinked within cells interlinked within cells interlinked within one stem."

    # ECHO skill: return the input unchanged
    return combined