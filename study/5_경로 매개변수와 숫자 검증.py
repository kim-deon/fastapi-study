"""
Query를 사용하여 쿼리 매개변수에 더 많은 검증과 메타데이터를 선언하는 것처럼
Path를 사용하여 경로 매개변수에 검증과 메타데이터를 같은 타입으로 선언할 수 있다. 
"""

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(
        title="The ID of the item to get",
        description="A unique integer that identifies the item",
        ge=1  # greater than or equal to 1
    ),
    q: str = Query(
        default=None, 
        alias="item-query",
        title="Item Query",
        description="Query string for searching items"
    ),
):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    return results



# * = 그 뒤 파라미터들은 키워드 인자로만 받겠다는 파이썬 문법.
# Query / Path 매핑 충돌 방지 및 가독성을 올려준다. 
@app.get("/items2/{item_id}")
# item_id = xxx, q=xxx 이런식으로 필수로 키워드를 넣어줘야함. 
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



# Path도 Query랑 똑같이 유효성 검사하고 동작함
@app.get("/items3/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results