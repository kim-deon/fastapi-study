from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id} # item_id에 str이 들어가면 Http 오류 발생

"""
/users/me 가 앞에 있어야 정상 작동하는 코드이다. 
만약 /users/me 가 /users/{user_id} 보다 아래에 있다면
/users/{user_id}는 /users/me요청 또한 매개변수 user_id의 값이 "me"인 것으로 "생각하게" 됩니다.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


""" 
사전 정의 값 (Enum)
Enum의 멤버(ModelName.alexnet, ModelName.resnet 등)는 프로그램 전체에서 단 하나만 존재하는 객체(싱글톤)입니다.
"""
from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


"""
경로 변환기 - path (/files/{file_path:path})
- path는 FastAPI의 기반이 되는 Starlette 프레임워크가 미리 정의해 둔 경로 변환기(Path Converter)라는 특별한 키워드
- http://127.0.0.1:8000/files/home/johndoe/myfile.txt → {"file_path":"home/johndoe/myfile.txt"}
"""