# AI review service

def ai_review_document(content):
    content_lower = content.lower()

    # 1. TEMPLATE CHECK (Minor issues -> Changes Requested)
    required_sections = [
        "subject",
        "dear parents",
        "thank you"
    ]

    missing = []
    for section in required_sections:
        if section not in content_lower:
            missing.append(section)

    if missing:
        return {
            "status": "Changes Requested",
            "reason": f"Missing sections: {', '.join(missing)}"
        }

    # 2. PROHIBITED CONTENT (Severe violation -> Rejected)
    prohibited_words = ["banned", "illegal", "hate speech"]
    for word in prohibited_words:
        if word in content_lower:
            return {
                "status": "Rejected",
                "reason": f"Prohibited content detected: {word}"
            }

    # 3. RISKY / SENSITIVE CONTENT (Uncertain -> Needs Human Review)
    risky_words = ["suspended", "violence", "legal", "injury"]
    for word in risky_words:
        if word in content_lower:
            return {
                "status": "Needs Human Review",
                "reason": f"Sensitive keyword detected: {word}"
            }

    # 4. APPROVED
    return {
        "status": "Approved",
        "reason": "Template and content validated"
    }
