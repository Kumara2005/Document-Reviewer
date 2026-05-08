# Reviewer dashboard
import streamlit as st
from services.storage import load_documents
from services.workflow import approve_document, reject_document
from services.escalation_service import check_review_timeout

def reviewer_page():
    st.title("🧑‍💼 Reviewer Dashboard")

    # ---------------------------
    # LOAD DOCUMENTS
    # ---------------------------
    docs = load_documents()
    
    for doc in docs:
        check_review_timeout(doc)

    review_docs = [doc for doc in docs if doc.status == "Needs Human Review"]

    st.subheader("Documents for Review")

    if not review_docs:
        st.info("No documents pending review")
        return

    for doc in review_docs:
        with st.expander(f"{doc.title} | v{doc.version}"):

            st.write("**Content:**")
            st.write(doc.content)

            st.write(f"**Version:** v{doc.version}")
            st.write(f"**Status:** {doc.status}")

            # ---------------------------
            # APPROVE
            # ---------------------------
            if st.button(f"Approve - {doc.id}"):
                msg = approve_document(doc)
                st.success(msg)

            # ---------------------------
            # REJECT / REQUEST CHANGES
            # ---------------------------
            reason = st.text_area(
                f"Reason for Changes - {doc.id}",
                key=f"reason_{doc.id}"
            )

            if st.button(f"Request Changes - {doc.id}"):
                msg = reject_document(doc, reason, reviewer="Reviewer")

                if "required" in msg:
                    st.error(msg)
                else:
                    st.warning(msg)

            # ---------------------------
            # HISTORY (Audit Trail)
            # ---------------------------
            if doc.history:
                st.write("**History:**")
                for h in doc.history:
                    st.text(f"{h['timestamp']} - {h['action']} (v{h['version']})")