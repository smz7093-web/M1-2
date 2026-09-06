from fastapi import APIRouter, HTTPException
from app.core.firebase import get_db
from app.schemas.data import DataCreate, DataUpdate, DataResponse, DataSummaryResponse
from app.services.data_service import calculate_summary
from typing import List

router = APIRouter(prefix="/api/data", tags=["Data"])

@router.get("/summary", response_model=DataSummaryResponse)
def get_data_summary():
    return calculate_summary()

@router.post("", response_model=DataResponse)
def create_data(data: DataCreate):
    db = get_db()
    doc_ref = db.collection('data').document()
    doc_data = data.model_dump()
    doc_ref.set(doc_data)
    return {"id": doc_ref.id, **doc_data}

@router.get("", response_model=List[DataResponse])
def list_data(limit: int = 100):
    db = get_db()
    docs = db.collection('data').order_by("date", direction="DESCENDING").limit(limit).stream()
    result = []
    for d in docs:
        item = d.to_dict()
        item['id'] = d.id
        result.append(item)
    return result

@router.put("/{data_id}", response_model=DataResponse)
def update_data(data_id: str, data: DataUpdate):
    db = get_db()
    doc_ref = db.collection('data').document(data_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
    doc_ref.update(update_dict)
    updated_doc = doc_ref.get().to_dict()
    return {"id": data_id, **updated_doc}

@router.delete("/{data_id}")
def delete_data(data_id: str):
    db = get_db()
    doc_ref = db.collection('data').document(data_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "삭제 완료", "id": data_id}