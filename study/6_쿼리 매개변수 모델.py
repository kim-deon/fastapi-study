"""
Field(...)와 Query(...) 차이
- Field : Pydantic 모델 내부에서 필드의 기본값 검증, 규칙 메타데이터를 지정할 때 사용
(주로 request body 모델에 쓰인다)

- Query : 경로 함수 파라미터에서 그 파라미터가 쿼리 파라미터임을 명시
"""

from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# 쿼리 파라미터(limit, offset, order_by, tags) 를 하나의 "모델"로 묶어서 받기 
class FilterParams(BaseModel):
    # 아래를 추가하면 쿼리 매개변수로 추가적인 데이터를 보내려고하면 에러응답. 
    # model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    # Literal을 사용함으로 들어올 수 있는 값을 정해준다. 
    order_by: Literal["created_at", "updated_at"] = "created_at"
    # tags: list[str] = [] -> 빈 리스트를 기본값으로 쓰면 mutable 기본값 문제 발생할 수 있음 주의
    # 권장 : default_factory=list
    tags: list[str] = Field(default_factory=list)


@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
# http://localhost:8000/items/?limit=10&tags=hi&tags=hello&tags=nihao
# -> {"limit":10,"offset":0,"order_by":"created_at","tags":["hi","hello","nihao"]}
