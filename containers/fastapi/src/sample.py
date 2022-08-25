"""this is a sample app."""
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main() -> Dict[str, str]:
    """ハローワールド！！ ."""
    return {"msg": "Hello World"}
