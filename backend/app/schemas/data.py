from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DataCreate(BaseModel):
    date: str = Field(..., example="2024-12-31", description="날짜 (YYYY-MM-DD 또는 YYYY)")
    value: float = Field(..., example=19850, description="빈집 수치(호)")
    memo: str = Field(..., example="전남 빈집 수 (호)", description="지역 및 비고")

class DataUpdate(BaseModel):
    date: Optional[str] = None
    value: Optional[float] = None
    memo: Optional[str] = None

class DataResponse(DataCreate):
    id: str

class DataSummaryResponse(BaseModel):
    total_count: int
    period: str
    latest_total_value: int
    growth_10yr_pct: float
    top_regions: List[str]
    capital_share_pct: float
    non_capital_share_pct: float
    trend_status: str