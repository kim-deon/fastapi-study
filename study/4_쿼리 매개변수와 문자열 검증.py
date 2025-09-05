from fastapi import FastAPI, Query

app = FastAPI()

results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
# 최소, 최대 길이 + 정규식 
@app.get("/items/")
async def read_items(
    q: str|None = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    ),
):
    if q:
        results.update({"q": q})
    return results


@app.get("/items2/")
async def read_items(q: str = Query(default="fixedquery", min_length=3)):
    if q:
        results.update({"q": q})
    return results

"""
쿼리 매개변수 리스트 / 다중 값 
- Query와 함께 명시적으로 선언할 때, 값들의 리스트나 다른 방법으로 여러 값을 받도록 선언 가능
- URL에서 여러번 나오는 q 쿼리 매개변수 받으려면 아래와 같이해야함
- http://localhost:8000/items3/?q=foo&q=bar 

결과
{
  "q": [
    "foo",
    "bar"
  ]
}

위에 예와 같이 list 자료형으로 쿼리 매개변수를 선언하려면 Query를 명시적으로 사용해야 한다. 
"""
@app.get("/items3/")
async def read_items(q:list[str]|None=Query(default=None)):
    if q:
        results.update({"q": q})
    return results


@app.get("/items4/")
async def read_items(q: list = Query(default=[])):
    query_items = {"q": q}
    return query_items




@app.get("/items5/")
async def read_items(
    q: str|None= Query(
        default=None, 
        title="Query string", 
        description="Query string for the items to search in the database that have a good match",
        min_length=3),
):
    if q:
        results.update({"q": q})
    return results

"""
itme-query 라는 변수를 파이썬은 만들 수 없다. 
하지만 꼭 itme-query라는 매개변수로 사용하고 싶다면 alias를 사용한다. 
"""
@app.get("/items6/")
async def read_items(
    q : str|None = Query(default=None, alias="item-query")
):
    if q:
        results.update({"q":q})
    return results



@app.get("/items7/")
async def read_items(
    q: str|None = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",
        deprecated=True,
    ),
):
    if q:
        results.update({"q": q})
    return results