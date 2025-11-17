from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str


@app.get('/')
def home():
    return {'message': 'Hello FastAPI!!!'}


@app.get('/user', response_model=User)
# response_model tells what type of response is to be returned
def get_user():
    return User(id=1, name='Bruce')
