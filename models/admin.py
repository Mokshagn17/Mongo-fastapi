from pydantic import BaseModel,ConfigDict,EmailStr

class Admin(BaseModel):
    username : str
    email : EmailStr 
    password : str 

    model_config = ConfigDict(
        json_schema_extra = {
            "example" : {
                "username" : "Mokshagna17",
                "email" : "moksha.padmashali@gmail.com",
                "password" : "test@123"                           

            }
        }
    )