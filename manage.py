import os

import dotenv
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from crud.database import create_tables
from routes import password

dotenv.load_dotenv()

app = FastAPI()

app.include_router(password.router)

URI = os.getenv("URI")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    user_agent = request.headers.get("User-Agent", "").lower()

    return response


@app.on_event("startup")
async def startup_db():
    await create_tables()


@app.get('/')
async def index():
    return {"HELLO"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=25004)
