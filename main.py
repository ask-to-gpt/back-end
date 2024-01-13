from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)

from starlette.exceptions import HTTPException as StarletteHTTPException
from domain.chat.router import router as chat_router
from config.config import config

app = FastAPI()

###### CORS Middleware Options ######
origins = [
    config["FRONTEND"]
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###### Error Handlers ######
@app.exception_handler(RequestValidationError)
async def validation_excpetion_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(StarletteHTTPException)
async def http_excpetion_handler(request: Request, exc: StarletteHTTPException):
    return await http_exception_handler(request, exc)

###### Routers ######
app.include_router(chat_router)