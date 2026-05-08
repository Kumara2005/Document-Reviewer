# Admin view (optional)
import streamlit as st
from services.storage import load_documents, update_document
from services.workflow import log_history, approve_document
from services.escalation_service import check_review_timeout
from datetime import datetime


def admin_page():
    st.title("🛠️ Admin Dashboard")

    docs = load_documents()

    for doc in docs:
        check_review_timeout(doc)

    if not docs:
        st.info("No documents available")
        return

    escalated_docs = [doc for doc in docs if doc.status == "Escalated"]

    if escalated_docs:
        st.subheader("⚠️ Escalated Documents")

        for doc in escalated_docs:
            with st.expander(f"{doc.title} | Escalated"):
                st.write(doc.content)

                # ---------------------------
                # OPTION 1: REASSIGN TO REVIEWER
                # ---------------------------
                if st.button(f"Reassign to Reviewer - {doc.id}"):
                    doc.status = "Needs Human Review"
                    doc.owner = "Reviewer"
                    doc.review_deadline = None  # reset deadline
                    doc.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_history(doc, "Reassigned to Reviewer by Admin")
                    update_document(doc)
                    st.success("Document reassigned to reviewer")

                # ---------------------------
                # OPTION 2: ADMIN APPROVES DIRECTLY
                # ---------------------------
                if st.button(f"Approve Directly - {doc.id}"):
                    approve_document(doc, reviewer="Admin")
                    st.success("Document approved by Admin")

    st.subheader("All Documents")

    for doc in docs:
        with st.expander(f"{doc.title} | v{doc.version} | {doc.status}"):

            st.write(f"**Owner:** {doc.owner}")
            st.write(f"**Status:** {doc.status}")
            st.write(f"**Version:** v{doc.version}")

            # ---------------------------
            # HANDLE SEND FAILURE
            # ---------------------------
            if doc.status == "Send Failed":
                st.error("Send failure detected")

            # ---------------------------
            # REASSIGN REVIEWER (SIMULATION)
            # ---------------------------
            if doc.status == "Needs Human Review":
                if st.button(f"Reassign Reviewer - {doc.id}"):
                    doc.owner = "Reviewer"
                    update_document(doc)
                    st.success("Reviewer reassigned")

            # ---------------------------
            # VIEW HISTORY
            # ---------------------------
            if doc.history:
                st.write("**History:**")
                for h in doc.history:
                    st.text(f"{h['timestamp']} - {h['action']} (v{h['version']})")