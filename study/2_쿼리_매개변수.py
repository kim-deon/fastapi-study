"""
유튜브에 “fastapi” 검색시의 예시 url :[`https://www.youtube.com/results?search_query=fastapi`](https://www.youtube.com/results?search_query=fastapi)

- `/results` : 필수 경로 매개변수
- `?search_query=fastapi` : 쿼리 매개변수
"""

"""
페이지네이션
- `limit`: 한 페이지에 몇 개(limit)의 아이템을 보여줄지 결정합니다.
- `skip`: 앞에서부터 몇 개(skip)의 아이템을 건너뛸지 결정합니다.
"""
from fastapi import FastAPI

app = FastAPI()

# 가짜 데이터베이스
fake_items_db = [{"item_name": "Apple"}, {"item_name": "Banana"}, {"item_name": "Cherry"}, {"item_name": "Durian"}]

@app.get("/items/")
# skip의 기본값은 0, limit의 기본값은 10으로 설정
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


"""
선택적 매개변수
- 아래에서는 Union을 썼지만 python 3.10 이상이면 | 를써라
"""
from typing import Union

from fastapi import FastAPI
app = FastAPI()

# {item_id}는 URL 경로의 일부인 '경로 매개변수'입니다.
@app.get("/items/{item_id}")
# 함수에 선언된 매개변수 중, 경로에 없는 것들은 '쿼리 매개변수'가 됩니다.
# q:Union[str, None] = None -> q: str | None = None
async def read_item(item_id: str, q: Union[str, None] = None):
    # 만약 쿼리 매개변수 q가 존재한다면 (None이 아니라면)
    if q:
        # q도 함께 반환
        return {"item_id": item_id, "q": q}
    # q가 없다면 item_id만 반환
    return {"item_id": item_id}


"""
필수 쿼리 매개변수 
[`http://127.0.0.1:8000/items/foo-item`](http://127.0.0.1:8000/items/foo-item) → 입력시 오류 발생. 
[`http://127.0.0.1:8000/items/foo-item?needy=sooooneedy`](http://127.0.0.1:8000/items/foo-item?needy=sooooneedy) → 정상 작동
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


