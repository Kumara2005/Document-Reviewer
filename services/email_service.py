# Simulate sending emails
import random
from datetime import datetime


def send_email(doc):
    """
    Simulate sending email.
    Returns:
    - "Sent"
    - "Failed"
    - "Bounced"
    """

    # simulate different outcomes
    outcome = random.choices(
        ["Sent", "Failed", "Bounced"],
        weights=[0.7, 0.2, 0.1],  # mostly success
        k=1
    )[0]

    return outcome


def get_error_message(status):
    """Return human-readable error messages"""
    if status == "Failed":
        return "Network error: Unable to send email"
    elif status == "Bounced":
        return "Invalid recipient email address"
    return None