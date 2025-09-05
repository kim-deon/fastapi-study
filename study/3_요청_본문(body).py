from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

@app.post("/items/")
async def create_itme(item:Item):
    return item
"""
1. HTTP 요청의 본문을 JSON으로 읽습니다.
2. JSON 데이터를 `Item` 모델에 전달합니다.
3. Pydantic이 데이터의 유효성을 검사합니다. 예를 들어, `price` 필드에 문자열이 들어오면 `float`으로 변환을 시도하고, 변환이 불가능하면 오류를 발생시킵니다.
4. 유효성 검사에 성공하면, 데이터로 채워진 `Item` 모델의 인스턴스를 생성하여 경로 작동 함수에 인자로 전달합니다.
5. 유효성 검사에 실패하면, FastAPI는 자동으로 어떤 필드에서 어떤 오류가 발생했는지 상세한 정보를 담은 JSON과 함께 422 Unprocessable Entity 응답을 반환합니다.

→ 개발자는 들어오는 JSON을 파싱하고, 필수 필드가 있는지 확인하고, 각 필드의 타입을 검사하는 작업을 할 필요가 없게 된다.
"""