from fastapi import FastAPI, Depends
from auth import get_api_key
from functions.math_ops import add_numbers, multiply_numbers
from functions.string_ops import reverse_string, to_uppercase
from functions.utils import greet_user

app = FastAPI(title="My API Server", version="1.0")

# Math Routes
@app.get("/add")
def add(a: int, b: int, api_key: str = Depends(get_api_key)):
    return {"result": add_numbers(a, b)}

@app.get("/multiply")
def multiply(a: int, b: int, api_key: str = Depends(get_api_key)):
    return {"result": multiply_numbers(a, b)}

# String Routes
@app.get("/reverse")
def reverse(text: str, api_key: str = Depends(get_api_key)):
    return {"result": reverse_string(text)}

@app.get("/uppercase")
def uppercase(text: str, api_key: str = Depends(get_api_key)):
    return {"result": to_uppercase(text)}

# Utils
@app.get("/greet")
def greet(name: str, api_key: str = Depends(get_api_key)):
    return {"message": greet_user(name)}
