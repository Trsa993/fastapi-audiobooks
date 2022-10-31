from urllib import request
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, books, login
from . import models
from .database import engine
import psycopg2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

app.include_router(books.router)
app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
def home_page():
    return {"message": "Hello world"}



