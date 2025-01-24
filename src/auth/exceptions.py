from fastapi import HTTPException


invalid_access_token = HTTPException(status_code=401, detail="invalid access token")
invalid_credentials = HTTPException(status_code=401, detail="invalid credentials")
user_already_exists = HTTPException(status_code=400, detail="user already exists")
