# FastAPI 게시판 프로젝트

이 프로젝트는 FastAPI를 사용하여 간단한 CRUD (생성, 읽기, 수정, 삭제) 기능을 제공하는 게시판 API입니다.

## 주요 기능

- 게시글 생성 (`POST /posts`)
- 전체 게시글 목록 조회 (`GET /posts`)
- 특정 게시글 조회 (`GET /posts/{post_id}`)
- 게시글 수정 (`PUT /posts/{post_id}`)
- 게시글 삭제 (`DELETE /posts/{post_id}`)

## 기술 스택

- Python 3.13+
- FastAPI
- Uvicorn
- SQLAlchemy (현재 코드에서는 직접 사용되지 않음)
- Poetry (의존성 관리)

## 설치 및 실행

1.  **Poetry 설치**

    아직 Poetry가 없다면 아래 공식 문서에 따라 설치합니다.
    > [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

2.  **프로젝트 의존성 설치**

    프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 필요한 라이브러리를 설치합니다.
    ```bash
    poetry install
    ```

3.  **개발 서버 실행**

    아래 명령어를 사용하여 Uvicorn 개발 서버를 실행합니다. `--reload` 옵션 덕분에 코드가 변경될 때마다 서버가 자동으로 재시작됩니다.
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
    서버가 실행되면 http://127.0.0.1:8000 에서 API를 확인할 수 있습니다.

4.  **API 문서 확인**

    서버 실행 후 아래 URL로 접속하면 자동으로 생성된 Swagger UI 문서를 통해 API를 테스트해볼 수 있습니다.
    -   Swagger UI: http://127.0.0.1:8000/docs
    -   ReDoc: http://127.0.0.1:8000/redoc

## 테스트

프로젝트에 포함된 테스트를 실행하려면 아래 명령어를 사용하세요.
```bash
poetry run pytest
```


