from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from typing import Annotated
from jose import JWTError,jwt,ExpiredSignatureError
from fastapi import Depends
from datetime import timedelta,timezone,datetime 
from starlette import status

ALGORITHM = "HS256"
EXPIRE_TIME = 30
SECRET_KEY = "IamIronmanIloveu3000"


oauth_schema = OAuth2PasswordBearer(tokenUrl="/login")

def generate_token(data:dict,expire_delta:timedelta | None):
    to_encode = data.copy()
    if not expire_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    else:
        expire = datetime.now(timezone.utc) + expire_delta

    to_encode.update({"exp":expire,"sub":data.get("username")})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def get_user_token(token: Annotated[str, Depends(oauth_schema)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid: missing username",
            )

        return username

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected exception: {e}"
        )
