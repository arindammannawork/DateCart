from fastapi import APIRouter


router = APIRouter()

@router.get("/todos")

async def read_todos():
    return {"message": "hello world"}