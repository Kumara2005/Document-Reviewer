import streamlit as st
from services.storage import load_documents


def parent_page():
    st.title("👨‍👩‍👧 Parent Dashboard")

    docs = load_documents()

    sent_docs = [doc for doc in docs if doc.status == "Sent"]

    if not sent_docs:
        st.info("No announcements available")
        return

    # Sort latest first
    sent_docs = sorted(sent_docs, key=lambda x: x.updated_at, reverse=True)

    # ---------------------------
    # NEW ANNOUNCEMENTS
    # ---------------------------
    st.subheader("📢 New Announcements")

    for doc in sent_docs[:3]:  # latest 3
        with st.expander(f"{doc.title} | v{doc.version}"):
            st.write(doc.content)
            st.write(f"Sent on: {doc.updated_at}")

    # ---------------------------
    # HISTORY
    # ---------------------------
    st.subheader("📜 Announcement History")

    for doc in sent_docs[3:]:
        with st.expander(f"{doc.title} | v{doc.version}"):
            st.write(doc.content)
            st.write(f"Sent on: {doc.updated_at}")