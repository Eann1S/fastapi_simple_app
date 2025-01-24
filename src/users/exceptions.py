from fastapi import HTTPException


user_not_found = HTTPException(status_code=404, detail="user not found")
