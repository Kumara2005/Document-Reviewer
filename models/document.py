# Document structure (class / schema)
import uuid
from datetime import datetime

class Document:
    def __init__(self, title, content):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        
        self.version = 1
        self.status = "Draft"
        self.owner = "Teacher"
        self.reviewed_by = None
        
        self.comments = []  # reviewer comments
        self.history = []   # audit trail
        
        self.review_deadline = None
        
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "version": self.version,
            "status": self.status,
            "owner": self.owner,
            "reviewed_by": self.reviewed_by,
            "comments": self.comments,
            "history": self.history,
            "review_deadline": self.review_deadline,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        doc = Document(data["title"], data["content"])
        doc.id = data["id"]
        doc.version = data["version"]
        doc.status = data["status"]
        doc.owner = data["owner"]
        doc.reviewed_by = data.get("reviewed_by")
        doc.comments = data.get("comments", [])
        doc.history = data.get("history", [])
        doc.review_deadline = data.get("review_deadline")
        doc.created_at = data.get("created_at")
        doc.updated_at = data.get("updated_at")
        return doc