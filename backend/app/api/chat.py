import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from app.core.firebase import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.data_service import calculate_summary

router = APIRouter(prefix="/api/chat", tags=["Chat"])
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("", response_model=ChatResponse)
def chat_with_data(req: ChatRequest):
    db = get_db()
    summary = calculate_summary()
    
    system_prompt = f"""
너는 대한민국 전국 빈집 현황 및 시계열 분석 전문가 AI 비서야.
아래에 제공된 최신 요약 데이터를 반드시 바탕으로 수치와 근거를 명확히 들어 답변해:
- 관측 기간: {summary['period']} (총 {summary['total_count']}건)
- 최신 연도 전국 빈집 총합: {summary['latest_total_value']:,}호 (10개년간 {summary['growth_10yr_pct']}% 증가)
- 상위 누적 지역: {', '.join(summary['top_regions'])}
- 수도권 vs 비수도권 비중: 비수도권 {summary['non_capital_share_pct']}%, 수도권 {summary['capital_share_pct']}%
- 트렌드: {summary['trend_status']}
"""
    conversation_id = req.conversation_id
    messages_history = []
    conv_ref = None

    if conversation_id:
        conv_ref = db.collection('conversations').document(conversation_id)
        conv_doc = conv_ref.get()
        if conv_doc.exists:
            messages_history = conv_doc.to_dict().get('messages', [])
    else:
        conv_ref = db.collection('conversations').document()
        conversation_id = conv_ref.id

    openai_msgs = [{"role": "system", "content": system_prompt}]
    for m in messages_history[-6:]:
        openai_msgs.append({"role": m['role'], "content": m['content']})
    openai_msgs.append({"role": "user", "content": req.message})

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_msgs,
            temperature=0.3
        )
        reply_text = completion.choices[0].message.content
    except Exception as e:
        print(f"[OpenAI 에러 발생]: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI 호출 에러: {str(e)}")

    # 대화 기록 저장
    messages_history.append({"role": "user", "content": req.message})
    messages_history.append({"role": "assistant", "content": reply_text})

    conv_ref.set({
        "title": req.message[:25] + ("..." if len(req.message) > 25 else ""),
        "created_at": datetime.utcnow().isoformat(),
        "messages": messages_history
    })

    # 반드시 "reply"라는 키로 반환해야 합니다.
    return {"conversation_id": conversation_id, "reply": reply_text}