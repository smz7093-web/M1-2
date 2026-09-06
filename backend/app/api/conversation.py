from fastapi import APIRouter, HTTPException
from app.core.firebase import get_db
from app.schemas.chat import ConversationResponse
from typing import List

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("", response_model=List[ConversationResponse])
def get_conversations():
    db = get_db()
    docs = db.collection('conversations').order_by("created_at", direction="DESCENDING").stream()
    result = []
    for d in docs:
        item = d.to_dict()
        item['id'] = d.id
        if 'messages' not in item:
            item['messages'] = []
        result.append(item)
    return result

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str):
    db = get_db()
    doc_ref = db.collection('conversations').document(conversation_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    item = doc.to_dict()
    item['id'] = doc.id
    return item

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str):
    db = get_db()
    doc_ref = db.collection('conversations').document(conversation_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "대화 삭제 완료", "id": conversation_id}