from fastapi import APIRouter,HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from models.admin import Admin
from starlette import status 
from pymongo import MongoClient
from utils.authentication import hash_password,verify_password
from utils.autherization import generate_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["USER-DATABASE"]
admin_col = mydb["Admin-Data"]

router = APIRouter(tags=["User-Registration"])

@router.post("/register",status_code=status.HTTP_200_OK)
async def register(request_data:Admin):
    try:
        admin_data = request_data.model_dump()
        admin_data["password"] = hash_password(admin_data["password"])
        result = admin_col.insert_one(jsonable_encoder(admin_data))  
        return {"message": "Admin registered successfully","admin_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception as : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    try:
        username_result = admin_col.find_one({"username": request.username})
        
        if not username_result:
            raise HTTPException(
                detail="No admin registered with that username",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if verify_password(request.password, username_result["password"]):
            username_result["_id"] = str(username_result["_id"])
            token = generate_token(data={"username": username_result["username"], "admin_id": username_result["_id"]}, expire_delta=timedelta(minutes=30))
            return {
                "access_token": token,
                "token_type": "bearer"
            }

        raise HTTPException(
            detail="Password authentication failed",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    except Exception as e:
        raise HTTPException(
            detail=f"Unexpected exception: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
