from datetime import datetime

def document_model(data):
    return {
        "user_id": data["user_id"],
        "title": data["title"],
        "content": data["content"],
        "content_hash": data["content_hash"],
        "status": "queued",
        "summary": None,
        "created_at": datetime.utcnow()
    }