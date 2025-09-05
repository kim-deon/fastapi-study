from typing import Literal
from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/products/{product_id}")
async def find_product(
    *,
    product_id: int = Path(ge=1, le=1000),
    q: str = Query(min_length=2, max_length=20),
    size: float = Query(gt=0, lt=100),
):
    return {"product_id": product_id, "q": q, "size": size}

class SearchParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    tags: list[str] = Field(default_factory=list)
    order: Literal["asc", "desc"] = "asc"

@app.get("/search/")
async def search(params: SearchParams = Depends()):
    return params
