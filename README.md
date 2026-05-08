# 📄 Document Reviewer System

A Streamlit-based workflow application for managing document creation, AI-assisted review, human review, and parent notifications.

## 🛠️ Technologies Used
*   **Frontend / UI:** [Streamlit](https://streamlit.io/)
*   **Backend Logic:** Python
*   **Data Storage:** File-based JSON storage (`data/documents.json`)
*   **External Services:** Simulated AI Review Service and Email Service

## 🎭 User Roles
1.  **👩‍🏫 Teacher:** Creates documents, handles AI and reviewer feedback, and ultimately sends the approved documents to parents.
2.  **🧑‍💼 Reviewer:** Steps in to review documents flagged by the AI as "risky" or "sensitive."
3.  **🛠️ Admin:** Steps in when a document gets stuck or a reviewer misses their deadline (escalation).
4.  **👨‍👩‍👧 Parent:** The end recipient who consumes the finalized, sent announcements.

## 🔄 The Full Workflow (Start to End)

### 1. Document Creation
*   **Role:** Teacher
*   **Action:** The Teacher logs in, enters a title and content, and creates a new document.
*   **System State:** The document is initialized with the status **"Draft"**, version `1`, and the owner is set to `"Teacher"`. It is saved to the JSON storage.

### 2. AI Review Stage
*   **Role:** Teacher / System AI
*   **Action:** The Teacher clicks **"Submit for AI Review"**.
*   **System State:** The AI service evaluates the content based on a rule-based logic system. It returns one of four outcomes:
    *   **🔴 Rejected:** The document contains prohibited words (e.g., "banned", "illegal", "hate speech"). The Teacher must edit and resubmit.
    *   **🟠 Changes Requested:** The document is missing required template sections (e.g., "subject", "dear parents", "thank you"). The Teacher must edit and resubmit.
    *   **🟡 Needs Human Review:** The document contains risky/sensitive keywords (e.g., "suspended", "violence"). The owner changes to `"Reviewer"`, and a **2-minute deadline** is set for human review.
    *   **🟢 Approved:** The document passes all checks and is ready to send. The owner remains `"Teacher"`.

### 3. Human Review & Escalation Stage (If Flagged)
*   **Role:** Reviewer / Admin
*   **Action:** If the document status is **"Needs Human Review"**, it appears on the Reviewer dashboard.
    *   **Option A (Reviewer acts):** The Reviewer can either **Approve** the document or **Request Changes** (providing a reason). If changes are requested, it goes back to the Teacher to edit (reverting to a "Draft").
    *   **Option B (Reviewer times out):** The system checks deadlines upon loading dashboards. If 2 minutes pass without action, the document is **Escalated**. The owner becomes `"Admin"`. The Admin can then either reassign it to a Reviewer or bypass them and **Approve Directly**.

### 4. Editing & Versioning Loop
*   **Role:** Teacher
*   **Action:** Whenever a document is Rejected, has Changes Requested, or is edited by the Teacher *after* being approved, the system forces a reset.
*   **System State:** Editing the content bumps the `version` number (e.g., v1 -> v2), wipes the approval, and returns the status to **"Draft"**, ensuring the new content must go through the AI/Review pipeline again.

### 5. Sending to Parents
*   **Role:** Teacher
*   **Action:** Once a document status is **"Approved"** (whether by AI, Reviewer, or Admin), the Teacher has the option to **"Send to Parents"**.
*   **System State:** The system calls the simulated email service, which randomly determines success based on weighted probabilities:
    *   **70% Chance:** Succeeds. Status becomes **"Sent"**.
    *   **30% Chance:** Fails (Network Error or Bounced Email). Status becomes **"Send Failed"**. The Teacher is notified and must click **"Retry Send"** until it succeeds.

### 6. Parent Consumption
*   **Role:** Parent
*   **Action:** Parents view their dashboard.
*   **System State:** The dashboard only fetches documents with the **"Sent"** status. It orders them chronologically (latest first), displaying the 3 newest under "📢 New Announcements" and older ones under "📜 Announcement History". 

## 📜 Audit Trail
Throughout this entire lifecycle, every status change, edit, and approval is logged in the document's **History**, providing full transparency on who touched the document and when.
