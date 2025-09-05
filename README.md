

    프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 필요한 라이브러리를 설치합니다.
    ```bash
    poetry install
    ```


    아래 명령어를 사용하여 Uvicorn 개발 서버를 실행합니다. `--reload` 옵션 덕분에 코드가 변경될 때마다 서버가 자동으로 재시작됩니다.
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
    -   Swagger UI: http://127.0.0.1:8000/docs
    -   ReDoc: http://127.0.0.1:8000/redoc



