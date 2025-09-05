## **FastAPI의 핵심을 이루는 5가지**

- **타입 힌트 (Type Hints):** FastAPI 기능의 기반이 되는 문법적 초석입니다.
- **Pydantic 데이터 모델:** 타입 힌트를 강력한 데이터 유효성 검사 및 직렬화 스키마로 변환합니다.
- **데코레이터와 경로 작동 (Decorators and Path Operations):** HTTP 요청을 파이썬 함수에 연결하는 마법과 같은 메커니즘입니다.
- **비동기 프로그래밍 (Asynchronous Programming):** 고성능 I/O 처리의 핵심입니다.
- **의존성 주입 (Dependency Injection):** 깔끔하고 재사용 가능하며 테스트하기 쉬운 코드를 작성하기 위한 아키텍처 패턴입니다.

## **타입 힌트 (타입 어노테이션)**

전통적으로 파이썬은 **동적 타입 언어**이다. 변수의 타입이 컴파일 시점이 아닌, 코드가 실행되는 **런타임에 결정**된다. 

```python
def total_price(price_1: int, price_2: int) -> int:
    return price_1 + price_2
```

타입을 명시해준다고 정적 타입 언어가 되는 것은 아니지만 FastAPI는 타입 힌트들을 검사해 전체 애플리케이션을 설정하고 구동한다. 3가지 핵심적인 이점이 있다. 

1. **자동 데이터 유효성 검사 및 파싱 :** `item_id: int` 와 같이 타입 힌트를 선언하면 “foo”와 같이 정수가 아닌 값이 들어오면 **HTTP 422 (Unprocessable Entity) 응답을 반환해준다**. 
2. **자동 API 문서화** : 타입 힌트를 사용하여 Swagger UI 및 ReDoc을 자동으로 생성한다. 
3. **개발 생산성 향상 :** 자동 완성, 실시간 타입 검사, 리팩토링 지원

### 제네릭 타입 (Generics)

---

**리스트, 튜플, 세트**

```python
from fastapi import FastAPI
from typing import List, Dict # Python 3.8 이하 호환성을 위해

app = FastAPI()

# Python 3.9+ 현대 문법
@app.post("/items/")
def create_items(items: list[str], prices: dict[str, float]):
    return {"items": items, "prices": prices}

# Python 3.8 이하 레거시 문법 ( typing 모듈이 있어야 사용 가능 )
@app.post("/legacy/items/")
def create_items_legacy(items: List[str], prices: Dict[str, float]):
    return {"items": items, "prices": prices}
```

### Nullable 및 유니온 타입 처리

- python 3.10이상이면 **Union 대신 `|` 를 쓰고, Optional은 쓰지마라.**
    
    파이썬 3.10 이상에서는 수직선(`|`) 연산자를 사용하여 두 타입의 유니온(Union)을 간결하게 표현할 수 있습니다. 이는 가독성이 매우 뛰어나 권장되는 방식입니다.
    
    `str | None`은 해당 변수가 문자열이거나 `None`일 수 있음을 의미합니다.
    
    이전 버전에서는 `typing` 모듈의 `Union`과 `Optional`을 사용해야 합니다. `Optional[str]`은 내부적으로 `Union[str, None]`과 동일하게 처리됩니다.
    
    여기서 한 가지 미묘하지만 중요한 점이 있습니다. FastAPI 공식 문서의 저자는 `Optional[str]`보다 `Union[str, None]`을 선호한다고 주관적인 의견을 밝힙니다. 그 이유는 'Optional'이라는 단어가 매개변수 자체가 선택적(optional)이라는 의미로 오해될 수 있기 때문입니다. 하지만 타입 힌트에서 `Optional`은 값이 `None`일 수 있음을 의미할 뿐, 매개변수가 선택적인지 여부는 `= None`과 같은 기본값의 유무로 결정됩니다. 이 구분은 API의 동작을 정확하게 이해하는 데 매우 중요합니다.
    

```python
from fastapi import FastAPI
from typing import Optional, Union # Python < 3.10 호환성

app = FastAPI()

# --- 현대적인 방식 (Python 3.10+) ---
@app.get("/users/{user_id}")
def get_user(user_id: int, company: str | None = None):
    # 'company'는 문자열이거나 None일 수 있으며, 기본값이 있으므로 매개변수 자체가 선택적입니다.
    # 예: /users/123 또는 /users/123?company=MyCorp
    return {"user_id": user_id, "company": company}

# --- 레거시 방식 (Python < 3.10) ---
@app.get("/legacy/users/{user_id}")
def get_user_legacy(user_id: int, company: Optional[str] = None):
    # Optional[str]은 Union[str, None]과 기능적으로 동일합니다.
    return {"user_id": user_id, "company": company}

# 'Optional'의 오해를 피하는 예시
@app.post("/items")
def add_item(name: Optional[str]):
    # 이 경우 'name'의 값은 str 또는 None이 될 수 있지만,
    # 기본값이 없으므로 요청 본문에 'name' 키가 반드시 포함되어야 합니다.
    # {"name": "Spoon"} -> 유효
    # {"name": null} -> 유효
    # {} -> 오류 발생 (필수 필드 누락)
    return {"name": name}
```

### 타입으로서의 클래스

---

변수의 타입을 클래스로 선언 가능하다. 

```python
class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person):
    return one_person.name
```

## Pydantic 모델을 이용한 데이터 유효성 검사 및 직렬화

Pydantic은 파이썬의 타입 힌트를 사용하여 데이터 스키마를 정의하고 유효성 검사하는 라이브러리이다. 핵심은 **`BaseModel` 클래스를 상속함으로 데이터 모델을 정의**한다. 

> FastAPI는 웹 계층 담당, Pydantic은 데이터 유효성 검사 엔진 역할을 한다.
> 
- 경로 작동 함수의 매개변수 타입 힌트에서 `BaseModel` 의 하위 클래스를 발견
- Pydantic이 파싱, 유효성 검사, 타입 강제 변환 수행

### 요청 본문 스키마 정의

데이터가 “body” 에 담겨오면 Pydantic 모델이 body의 구조와 타입을 정의한다. 

```python
# 예시 코드 
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    # 여기서 'item'은 클라이언트가 보낸 JSON 본문이 성공적으로
    # 유효성 검사를 통과한 후 생성된 Pydantic 모델 인스턴스입니다.
    # 이제 item.name, item.price와 같이 타입이 보장된 속성에 접근할 수 있습니다.
    print(f"새 아이템 생성: {item.name}, 가격: ${item.price}")
    return {"item_name": item.name, "item_price": item.price, "description": item.description}
```

`BaseModel`을 상속하는 간단한 `Item` 모델을 만들어 `POST` 요청으로 기대하는 JSON의 형태를 정의할 수 있다. FastAPI는 이 모델을 타입 힌트로 사용하는 매개변수를 발견하면 자동으로 다음 작업을 수행한다.

1. HTTP 요청의 본문을 JSON으로 읽습니다.
2. JSON 데이터를 `Item` 모델에 전달합니다.
3. Pydantic이 데이터의 유효성을 검사합니다. 예를 들어, `price` 필드에 문자열이 들어오면 `float`으로 변환을 시도하고, 변환이 불가능하면 오류를 발생시킵니다.
4. 유효성 검사에 성공하면, 데이터로 채워진 `Item` 모델의 인스턴스를 생성하여 경로 작동 함수에 인자로 전달합니다.
5. 유효성 검사에 실패하면, FastAPI는 자동으로 어떤 필드에서 어떤 오류가 발생했는지 상세한 정보를 담은 JSON과 함께 422 Unprocessable Entity 응답을 반환합니다.

→ 개발자는 들어오는 JSON을 파싱하고, 필수 필드가 있는지 확인하고, 각 필드의 타입을 검사하는 작업을 할 필요가 없게 된다. 

### 응답 스키마 정의 (`response_model`)

함수가 반환하는 객체를 FastAPI가 받아서 `response_model` 로 지정된 스키마에 맞게 변환한다. 

- 응답 dto라 생각하면 될 것 같다.
- `response_model` 에 정의되지 않은 필드는 자동으로 응답에서 제외된다.
- 내부 데이터 구조나 비밀번호 해시와 같은 민감한 정보를 클라이언트에게 노출하는 것을 방지하는 중요한 보안 기능이다.

```python
from pydantic import BaseModel

class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserOut(BaseModel):
    username: str
    email: str

# 가상의 데이터베이스
fake_user_db = {
    "john": {
        "username": "john",
        "email": "john@example.com",
        "hashed_password": "supersecretpasswordhash"
    }
}

@app.get("/users/{username}", response_model=UserOut)
async def get_user(username: str):
    # 데이터베이스에서 UserInDB 모델에 해당하는 데이터를 가져옵니다.
    user_data = fake_user_db.get(username)
    if not user_data:
        #... 오류 처리
        pass
    
    # 함수는 비밀번호가 포함된 전체 데이터를 반환하지만,
    # FastAPI가 response_model=UserOut에 따라 'hashed_password'를 필터링합니다.
    return user_data
```

### `Field`를 이용한 고급 필드 유효성 검사

단순한 타입 검사를 넘어 추가적인 유효성 검사 규칙을 추가하고 싶다면 Pydantic의 `Field` 함수를 사용한다.

- 숫자범위 : `gt` , `lt` , `ge` , `le`
- 문자열 길이 : `min_length` , `max_length`
- 정규식 패턴 등 제공
- `title`, `description`, `example` 을 통해 OpenAPI 문서에 표시될 추가 메타데이터를 제공할 수 있다.

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(
       ...,  #...은 이 필드가 필수임을 나타내는 특별한 값입니다.
        title="Name of the item",
        max_length=50,
        example="Gaming Mouse"
    )
    price: float = Field(
       ...,
        gt=0,  # 0보다 커야 함 (greater than)
        le=100000,  # 100,000보다 작거나 같아야 함 (less than or equal to)
        description="The price of the item must be a positive number.",
        example=79.99
    )
    description: str | None = Field(
        default=None,  # 기본값이 None이므로 선택적 필드
        title="Description",
        max_length=300
    )
```

### 중첩 모델 스키마 구성

Pydantic은 한 Pydantic 모델을 다른 모델의 타입 힌트로 사용하여 이러한 복잡한 구조를 쉽게 정의할 수 있도록 지원한다. 

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    order_id: int
    customer: User      # User 모델을 중첩하여 사용
    items: list[Item]   # Item 모델의 리스트를 중첩하여 사용
```

Order→ User 객체 + 여러 Item객체일 때 원래는 아래와 같이 복잡한 JSON 요청 본문을 자동으로 파싱하고 유효성 검사할 수 있다. 

```python
# json
{
  "order_id": 12345,
  "customer": {
    "username": "johndoe",
    "email": "johndoe@example.com"
  },
  "items": [
    {
      "name": "Laptop",
      "price": 1200.00
    },
    {
      "name": "Mouse",
      "price": 25.50
    }
  ]
}
```

## API 엔드포인트 정의 - 데코레이터와 경로 작동

**@ 문법, 데코레이터**

데코레이터는 본질적으로 다른 함수를 인자로 받아, 기존 함수의 코드를 수정하지 않고 새로운 기능을 추가하거나 동작을 변경한 뒤, 새로운 함수를 반환하는 함수이다. 

```python
score=[(100,100),(95,90),(65,20),(60,90),(100,60)]

def password_check(func):
    def wrapper(*args,**kwargs):
        password="1234"
        check = input()
        if password==check:
            result = func(*args, **kwargs)
        else:
            result = "잘못된비번"
        return result
    return wrapper

@password_check
def get_avg(score:list):
    for index,point in enumerate(score):
        print(f'{index+1}번, 평균 : {sum(point)/len(point)}')

print(get_avg(score))
```