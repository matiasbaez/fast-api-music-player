from fastapi import Header, HTTPException
import jwt

def auth_middleware(x_auth_token = Header()):

    try:
        if not x_auth_token:
            raise HTTPException(401, "Token is required")

        token = jwt.decode(x_auth_token, "password_secret", algorithms=["HS256"])

        if not token:
            raise HTTPException(401, "Invalid token")

        uid = token.get("id")

        return {"uid": uid, "token": x_auth_token}

    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")