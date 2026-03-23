import os
import sys

print("CURRENT DIR:", os.getcwd())
print("FILES IN BACKEND:", os.listdir(os.path.dirname(__file__)))

from fastapi import FastAPI
from backend.search import router

app = FastAPI()

app.include_router(router)