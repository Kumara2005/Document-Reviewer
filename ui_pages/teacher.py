# Teacher dashboard
import streamlit as st
from models.document import Document
from services.storage import load_documents, add_document, update_document
from services.workflow import (
    submit_for_ai_review,
    edit_document,
    send_document,
    retry_send
)
from services.email_service import get_error_message


def teacher_page():
    st.title("👩‍🏫 Teacher Dashboard")

    # ---------------------------
    # CREATE DOCUMENT
    # ---------------------------
    st.subheader("Create New Document")

    title = st.text_input("Title")
    content = st.text_area("Content")

    if st.button("Create Document"):
        if title and content:
            doc = Document(title, content)
            add_document(doc)
            st.success("Document created successfully")
        else:
            st.error("Title and Content are required")

    st.divider()

    # ---------------------------
    # LOAD DOCUMENTS
    # ---------------------------
    docs = load_documents()

    teacher_docs = [doc for doc in docs if doc.owner == "Teacher"]

    st.subheader("Your Documents")

    if not teacher_docs:
        st.info("No documents available")
        return

    for doc in teacher_docs:
        with st.expander(f"{doc.title} | v{doc.version} | {doc.status}"):

            st.write("**Content:**")
            st.write(doc.content)

            st.write(f"**Status:** {doc.status}")
            st.write(f"**Version:** v{doc.version}")

            # ---------------------------
            # SHOW COMMENTS (IF ANY)
            # ---------------------------
            if doc.comments:
                st.write("**Reviewer Comments:**")
                for c in doc.comments:
                    st.warning(f"{c['reason']} ({c['timestamp']})")

            # ---------------------------
            # ACTIONS BASED ON STATUS
            # ---------------------------

            # Draft → Submit
            if doc.status == "Draft":
                if st.button(f"Submit for AI Review - {doc.id}"):
                    msg = submit_for_ai_review(doc)
                    if "AI Review completed" in msg:
                        st.success(msg)
                    else:
                        st.error(msg)

            # Changes Requested → Edit
            if doc.status == "Changes Requested":
                new_content = st.text_area(
                    f"Edit Content - {doc.id}",
                    value=doc.content
                )

                if st.button(f"Update Document - {doc.id}"):
                    msg = edit_document(doc, new_content)
                    st.success(msg)

            # Approved → Send
            if doc.status == "Approved":
                st.success(f"✅ Document Approved! (Reviewed by: {doc.reviewed_by or 'Unknown'})")

                if doc.owner == "Teacher":
                    st.info("Approved and returned to you for action")

                if any("by Admin" in h.get("action", "") for h in doc.history):
                    st.write("**Handled by:** Admin")

                # ---------------------------
                # SEND OPTION
                # ---------------------------
                if st.button(f"Send to Parents - {doc.id}"):
                    result = send_document(doc)

                    if result == "Sent":
                        st.success("Document sent successfully")
                    else:
                        st.error(get_error_message(result))

                st.divider()

                # ---------------------------
                # EDIT OPTION (VISIBLE FIX)
                # ---------------------------
                st.write("✏️ Edit Document Before Sending")

                new_content = st.text_area(
                    "Edit Approved Content",
                    value=doc.content,
                    key=f"edit_approved_{doc.id}"
                )

                if new_content != doc.content:
                    st.warning("⚠️ Editing will require re-approval")

                if st.button(f"Edit & Resubmit - {doc.id}"):
                    msg = edit_document(doc, new_content)
                    st.warning("Approval invalidated. Document moved to Draft.")

            # Send Failed → Retry
            if doc.status == "Send Failed":
                st.error("Last send attempt failed")

                if st.button(f"Retry Send - {doc.id}"):
                    result = retry_send(doc)

                    if result == "Sent":
                        st.success("Retry successful")
                    else:
                        st.error(get_error_message(result))

            # Sent → Show confirmation
            if doc.status == "Sent":
                st.success("Document successfully sent to parents")

            # Rejected → Show reason and edit
            if doc.status == "Rejected":
                st.error("🚫 Document Rejected due to severe violation.")
                st.write("✏️ Edit Document to resolve issues:")
                new_content = st.text_area(
                    "Edit Rejected Content",
                    value=doc.content,
                    key=f"edit_rejected_{doc.id}"
                )

                if st.button(f"Edit & Resubmit - {doc.id}"):
                    msg = edit_document(doc, new_content)
                    st.warning("Document moved back to Draft.")
                    
            # Needs Human Review → Show status
            if doc.status == "Needs Human Review":
                st.info("⏳ Document requires human review. It is currently with the Reviewer.")

            # ---------------------------
            # HISTORY (Audit Trail)
            # ---------------------------
            if doc.history:
                st.write("**History:**")
                for h in doc.history:
                    st.text(f"{h['timestamp']} - {h['action']} (v{h['version']})")