# Escalation and timeout management
from datetime import datetime
from services.storage import update_document
from services.workflow import log_history

def check_review_timeout(doc):
    if doc.status != "Needs Human Review" or not doc.review_deadline:
        return

    now = datetime.now()
    deadline = datetime.strptime(doc.review_deadline, "%Y-%m-%d %H:%M:%S")

    if now > deadline and doc.status == "Needs Human Review":
        # ESCALATION
        doc.owner = "Admin"
        doc.status = "Escalated"
        doc.review_deadline = None  # prevent repeated escalation

        log_history(doc, "Escalated due to timeout")
        update_document(doc)
