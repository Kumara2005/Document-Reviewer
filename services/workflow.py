from datetime import datetime, timedelta
from services.storage import update_document
from services.email_service import send_email
from services.ai_review_service import ai_review_document


def log_history(doc, action):
    """Add action to document history"""
    doc.history.append({
        "action": action,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": doc.version
    })


# ---------------------------
# SUBMIT FOR AI REVIEW
# ---------------------------
def submit_for_ai_review(doc):
    if doc.status != "Draft":
        return "Only Draft documents can be submitted"

    # Briefly simulate AI Reviewing state
    doc.status = "AI Reviewing"
    log_history(doc, "Submitted for AI Review")
    
    # Perform AI Review
    ai_result = ai_review_document(doc.content)
    new_status = ai_result["status"]
    reason = ai_result["reason"]
    
    doc.status = new_status
    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if new_status == "Approved":
        doc.reviewed_by = "AI"
        doc.owner = "Teacher"
        log_history(doc, f"AI Approved: {reason}")
    elif new_status == "Rejected":
        doc.reviewed_by = "AI"
        doc.owner = "Teacher"
        doc.comments.append({"reason": reason, "timestamp": doc.updated_at})
        log_history(doc, f"AI Rejected: {reason}")
    elif new_status == "Changes Requested":
        doc.reviewed_by = "AI"
        doc.owner = "Teacher"
        doc.comments.append({"reason": reason, "timestamp": doc.updated_at})
        log_history(doc, f"AI Changes Requested: {reason}")
    elif new_status == "Needs Human Review":
        doc.owner = "Reviewer"
        # Set deadline for human reviewer
        doc.review_deadline = (datetime.now() + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        log_history(doc, f"Needs Human Review: {reason} (Deadline Set)")

    update_document(doc)
    return f"AI Review completed: {new_status}"


# ---------------------------
# APPROVE DOCUMENT
# ---------------------------
def approve_document(doc, reviewer="Reviewer"):
    if doc.status != "Needs Human Review":
        return "Document not pending review"

    doc.status = "Approved"
    doc.owner = "Teacher"
    doc.reviewed_by = reviewer
    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_history(doc, f"Approved by {reviewer}")
    update_document(doc)

    return "Approved successfully"


# ---------------------------
# REJECT DOCUMENT / REQUEST CHANGES
# ---------------------------
def reject_document(doc, reason, reviewer="Reviewer"):
    if doc.status != "Needs Human Review":
        return "Document not pending review"

    if not reason:
        return "Reason required"

    # Human reviewers typically request changes rather than hard reject
    doc.status = "Changes Requested"
    doc.owner = "Teacher"
    doc.reviewed_by = reviewer
    doc.comments.append({
        "reason": reason,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_history(doc, f"Changes Requested by {reviewer}: {reason}")
    update_document(doc)

    return "Changes requested successfully"


# ---------------------------
# EDIT DOCUMENT (VERSION UPDATE)
# ---------------------------
def edit_document(doc, new_content):
    # editing always resets approval
    doc.content = new_content
    doc.version += 1
    doc.status = "Draft"
    doc.owner = "Teacher"

    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_history(doc, "Edited → New Version Created")
    update_document(doc)

    return "Document updated"


# ---------------------------
# SEND DOCUMENT
# ---------------------------
def send_document(doc):
    if doc.status != "Approved":
        return "Only approved documents can be sent"

    result = send_email(doc)

    if result == "Sent":
        doc.status = "Sent"
        log_history(doc, "Sent to Parents")

    else:
        doc.status = "Send Failed"
        log_history(doc, "Send Failed")

    doc.owner = "Teacher"
    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_document(doc)

    return result


# ---------------------------
# RETRY SEND
# ---------------------------
def retry_send(doc):
    if doc.status != "Send Failed":
        return "Retry only allowed for failed sends"

    return send_document(doc)

