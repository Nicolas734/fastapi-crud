from typing import Union
from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel
from config import Config
from db.db import engine
from models.base import Base


config = Config()

project_name =      config._g.get("SERVER", "PROJECT_NAME")
project_version =   config._g.get("SERVER", "PROJECT_VERSION")

app = FastAPI(title=project_name, version=project_version)


def create_tables():
    Base.metadata.create_all(bind=engine)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"msg":"hello"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q:Union[str, None] = None):
    return {"item_id":item_id, "q":q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}



if __name__ == "__main__":
    host = config._g.get("SERVER", "HOST")
    port = config._g.get("SERVER", "PORT")
    log_level = config._g.get("SERVER", "LOG_LEVEL")
    create_tables()
    run(app, host="0.0.0.0", port=8001, log_level="debug")