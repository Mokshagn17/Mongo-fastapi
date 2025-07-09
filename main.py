from fastapi import FastAPI,HTTPException,Query,Depends
from fastapi.encoders import jsonable_encoder
from starlette import status 
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
from models.user import User  
from typing import List,Annotated
from utils.autherization import get_user_token
from routers.auth import router

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["USER-DATABASE"]
mycol = mydb["USER-DATA"]



def serialize_docs(id):
    id["_id"] = str(id["_id"])
    return id

app = FastAPI(title="USER-DATA-MONGO-FASTAPI-APPLICATION")

app.include_router(router)

@app.get("/")
async def home():
    return f"WELCOME TO THE FASTAPI APPLICATION"

@app.post("/user-create",status_code=status.HTTP_201_CREATED)
async def user_create(request:User,current_user:Annotated[str,Depends(get_user_token)]):
    try:
        user_data = jsonable_encoder(request)
        result = mycol.insert_one(user_data)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception as : {e}",status_code=status.HTTP_404_NOT_FOUND)    


@app.get("/find_user_data",status_code=status.HTTP_200_OK)
async def find_user(current_user:Annotated[str,Depends(get_user_token)],name:str=Query(...,description="Enter the firstname of the user")):
    try:
        result = mycol.find_one({"first_name":name})
        if result:
                result["_id"] = str(result["_id"])
                return result 
        raise HTTPException(detail=f"No name in the database {name}",status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception as e {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/find_users_salary",status_code=status.HTTP_200_OK)
async def find_user_salary(current_user:Annotated[str,Depends(get_user_token)],min_salary:float=Query(...,description="Minimum salary"),max_salary:float=Query(...,description="Maximum salary")):
    try:
        names = []
        result = list(mycol.find({"salary":{"$lte":max_salary,"$gte":min_salary}}))
        if result:
            for i in result:
                i["_id"] = str(i["_id"])
                names.append(i["name"])
            return names    
            
        raise HTTPException(detail=f"No name in the database of salary with range {min_salary}  -  {max_salary}",status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
         raise HTTPException(detail=f"Unexpected exception as e {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/find_users_language",status_code=status.HTTP_200_OK)
async def find_user_language(current_user:Annotated[str,Depends(get_user_token)],language:str=Query(...,description="Language")):
    try:
        names = []
        result = mycol.find({"languages_known":{"$in":[language]}})
        for i in result:
            i["_id"] = str(i["_id"])
            names.append(i["name"])
        if not names:
            raise HTTPException(detail=f"No name in the database who speaks language {language}",status_code=status.HTTP_404_NOT_FOUND)
        return names
    except Exception as e:
         raise HTTPException(detail=f"Unexpected exception as e {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
@app.get("/find_user_uuid",status_code=status.HTTP_200_OK)
async def find_user_uuid(current_user:Annotated[str,Depends(get_user_token)],user_uuid:str=Query(...,description="UUID OF USER")):
    try:
        result = mycol.find_one({"uuid":user_uuid})
        if not result:
            raise HTTPException(detail=f"No user with uuid {user_uuid}",status_code=status.HTTP_404_NOT_FOUND)
        serialize_docs(result)
        return result
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.put("/update_user_uuid_salary",status_code=status.HTTP_200_OK)
async def update_salary_user_uuid(current_user:Annotated[str,Depends(get_user_token)],user_uuid:str=Query(...,description="USER UUID"),salary:float=Query(...,description="Salary")):
    try:
        result = mycol.update_one({"uuid":user_uuid},{"$set":{"salary":salary}})
        if result.matched_count==0:
            raise HTTPException(detail=f"No user with uuid {user_uuid}",status_code=status.HTTP_404_NOT_FOUND)
        return f"User salary updated succesfully"
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.put("/update_user_uuid",status_code=status.HTTP_200_OK)
async def update_user_uuid(
    current_user:Annotated[str,Depends(get_user_token)],
    user_uuid:str=Query(...,description="USER UUID"),
    job:str=Query(...,description="JOB"),
    email:str=Query(...,description="email"),
    phone:int=Query(...,description="Phone Number")):
    try:
        result = mycol.update_one({"uuid":user_uuid},{"$set":{"job":job,"email":email,"phone":[phone]}})
        if result.matched_count==0:
            raise HTTPException(detail=f"No user with uuid {user_uuid}",status_code=status.HTTP_404_NOT_FOUND)
        return f"User job,email,phone updated succesfully"
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.delete("/delete_user_uuid",status_code=status.HTTP_200_OK)
async def delete_user_uuid(current_user:Annotated[str,Depends(get_user_token)],user_uuid:str=Query(...,description="USER UUID")):
    try:
        result = mycol.delete_one({"uuid":user_uuid})
        if result.deleted_count == 0:
            raise HTTPException(detail=f"No user with uuid {user_uuid}",status_code=status.HTTP_404_NOT_FOUND)
        return f"User deleted succesfully"
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/search_user_skill",status_code=status.HTTP_200_OK)
async def search_user_skill(current_user:Annotated[str,Depends(get_user_token)],skill_name:List[str]=Query(...,description="skill")):
    try:
        names = []
        result = mycol.find({"skills":{"$in":skill_name}})
        for i in result:
            names.append(i["name"])
        if not names:    
            raise HTTPException(detail=f"No user with skills {skill_name}",status_code=status.HTTP_404_NOT_FOUND)
        return names
    except Exception as e:
        raise HTTPException(detail=f"Unexpected exception : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/average_salary_users",status_code=status.HTTP_200_OK)
async def avg_sal_user(current_user:Annotated[str,Depends(get_user_token)]):
    try:
        pipeline = [
            {"$group":{"_id":None,"salary":{"$avg":"$salary"}}}
        ]
        result = list(mycol.aggregate(pipeline))
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return {"salary": result[0]["salary"]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected exception: {e}")


@app.get("/count_users_notice_period",status_code=status.HTTP_200_OK)
async def notice_users(current_user:Annotated[str,Depends(get_user_token)],notice_period:int=Query(...,description="Notice period")):
    try:
        pipeline = [
            {"$match":{"notice_period":notice_period}},
            {"$group":{"_id":"$notice_period", "total_users" : {"$sum" : 1}}}
        ]
        result = list(mycol.aggregate(pipeline))
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return {"total_users": result[0]["total_users"]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected exception: {e}")

