# In-memory / JSON storage
import json
import os
from models.document import Document

DATA_FILE = "data/documents.json"


def load_documents():
    """Load all documents from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
            return [Document.from_dict(doc) for doc in data]
        except json.JSONDecodeError:
            return []


def save_documents(documents):
    """Save all documents to JSON file"""
    with open(DATA_FILE, "w") as file:
        json.dump([doc.to_dict() for doc in documents], file, indent=4)


def add_document(document):
    """Add a new document"""
    docs = load_documents()
    docs.append(document)
    save_documents(docs)


def update_document(updated_doc):
    """Update an existing document"""
    docs = load_documents()

    for i, doc in enumerate(docs):
        if doc.id == updated_doc.id:
            docs[i] = updated_doc
            break

    save_documents(docs)


def get_document_by_id(doc_id):
    """Fetch a single document"""
    docs = load_documents()
    for doc in docs:
        if doc.id == doc_id:
            return doc
    return None