1. FastAPI에서 Body를 사용하는 이유는 무엇인가? BaseModel과 함께 사용했을 때 얻는 장점 두 가지를 설명하라. 【참고: 3_요청_본문(body).py】
- POST/PUT 요청에서는 클라이언트가 body에 JSON 데이터를 담아 보낸다.
- FastAPI는 이를 **Pydantic BaseModel**로 받는데, 이때 자동으로 파싱 + 검증 + 직렬화가 이루어진다.
- 개발자가 일일이 json.loads() 하거나 타입 검증할 필요가 없다.

---
2. Query와 Field의 차이를 설명하라. 각각 언제 사용하는가? 【참고: 4_쿼리 매개변수와 문자열 검증.py vs 6_쿼리 매개변수 모델.py】
- Query(): 경로 함수의 인자에서, 값이 쿼리 파라미터임을 명시할 때 사용한다. 검증(최소/최대 길이 등)과 메타데이터도 추가 가능하다.
- Field(): Pydantic 모델 내부에서 필드의 기본값, 검증, 메타데이터를 지정할 때 사용한다. 주로 request body 모델에서 사용된다.

---
3. Path와 Query 모두 유효성 검증 옵션(ge, le, min_length, pattern 등)을 제공한다. 두 가지의 차이를 간단히 설명하라. 【참고: 5_경로 매개변수와 숫자 검증.py】
- Path는 경로 매개변수를 검증할 때 사용한다. (예: /items/{item_id})
- Query는 쿼리 매개변수를 검증할 때 사용한다. (예: /items/?q=value)
- 공통점: 둘 다 ge, le, min_length, pattern 같은 검증 옵션을 쓸 수 있다.
- 차이점: 어디서 값을 가져오는지 (URL Path vs Query String).
---
4. 결과 예상
```
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, min_length=3, max_length=10)):
    return {"q": q}
```
- 요청: GET /items/?q=hi -> 422
- 요청: GET /items/?q=helloworld -> 422
- 요청: GET /items/?q=fast -> {"q":"fast"}


---
5. 다음 코드에서 order_by 파라미터는 어떤 값만 허용되는가? 잘못된 값이 들어왔을 때 FastAPI는 어떤 HTTP 상태 코드를 반환하는가? 【참고: 6_쿼리 매개변수 모델.py】

class FilterParams(BaseModel):
    order_by: Literal["created_at", "updated_at"] = "created_at"

> "created_at", "updated_at" 이 두가지만 허용가능하고, 잘못들어왔을시 422가 반환된다.

6. 아래 요청 시 서버가 반환하는 응답(JSON)을 쓰시오. 【참고: 4_쿼리 매개변수와 문자열 검증.py】

@app.get("/items/")
async def read_items(q: list[str] | None = Query(default=None)):
    return {"q": q}


요청: GET /items/?q=foo&q=bar
```json
{
  "q": ["foo", "bar"]
}
```

---
7. 왜 FastAPI 함수 파라미터 정의 시 *를 사용하는 경우가 있는가? (힌트: Python 문법 + FastAPI 의도)
- *는 그 뒤 인자들은 반드시 키워드 인자로만 받도록 강제하는 Python 문법이다.

- FastAPI에서는 Path/Query 같은 선언적 파라미터가 혼동되지 않도록 명시적 키워드 인자로만 받게 하는 의도에서 사용된다.
---
8. tags: list[str] = [] 와 같이 리스트를 기본값으로 두는 것이 위험한 이유를 설명하라. 이를 방지하기 위해 Pydantic에서는 어떤 방식을 권장하는가?
- `[]` 이렇게 선언하면 기본값이 mutable 하게 계속 같은 주소를 참조한다. `default_factory=list` 사용을 권장한다.

9. alias="item-query" 를 사용하는 경우는 언제 필요한가? 실제 예시 URL과 함수 파라미터 이름을 들어 설명하라. 【참고: 4_쿼리 매개변수와 문자열 검증.py】
- Python 식별자에는 - 같은 문자가 들어갈 수 없다.

- 하지만 API 스펙에서 꼭 item-query라는 쿼리 파라미터 이름을 써야 한다면, FastAPI에서 alias="item-query"를 사용한다.

- 그러면 함수 파라미터는 q로 두고, 실제 요청은 /items/?item-query=value로 받을 수 있다.

10. FastAPI는 유효성 검증에 실패하면 422 Unprocessable Entity를 반환한다. 400 Bad Request가 아니라 422를 선택한 이유를 HTTP 표준 관점에서 설명해보라.
- 400 Bad Request는 "요청 자체가 잘못되었다(구문 오류 등)"일 때 쓴다.
- 422 Unprocessable Entity는 "요청 형식은 맞지만, 의미적으로 처리할 수 없음"일 때 쓴다.
- FastAPI는 JSON 파싱에는 성공했지만, 값이 검증 조건에 맞지 않을 때(예: limit=-1) 422를 반환한다.