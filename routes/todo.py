from fastapi import APIRouter,Depends,requests,Request


router = APIRouter()





def func(re:Request):
    print(re.headers)
    return "abc"
@router.get("/todos")
async def read_todos(q:str =Depends(func)):
    return {"message": "hello world"}