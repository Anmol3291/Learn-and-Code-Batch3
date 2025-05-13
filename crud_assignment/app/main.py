from fastapi import FastAPI
from app.routers.book_router import router as book_router


def create_app() -> FastAPI:
    app = FastAPI(title="Book CRUD API")

    try:
        app.include_router(book_router)

        @app.get("/")
        def root():
            return {"status": "API is running"}

    except Exception as e:
        print(f"Error initializing application: {e}")
        raise

    return app


app = create_app()
