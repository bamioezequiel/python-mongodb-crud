from fastapi import APIRouter, HTTPException, Response, status
from config.db import connection
from schemas.user import user_entity, users_entity
from models.user import User
from passlib.hash import sha256_crypt as pass_crypt
from bson import ObjectId

user = APIRouter()

@user.get("/users", response_model=list[User], tags=["users"])
async def find_all_user():
    try:
        users = users_entity(connection.users.find()) 
        return users
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=error.args[0])

@user.post("/users", response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    del new_user["id"]
    new_user["password"] = pass_crypt.encrypt(new_user["password"])
    id = connection.users.insert_one(new_user).inserted_id

    return user_entity(connection.users.find_one({"_id": id}))

@user.get("/users/{id}", response_model=User, tags=["users"])
async def find_user(id: str):
    try:
        return user_entity(connection.users.find_one({"_id": ObjectId(id)}))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=error.args[0])

@user.put("/users/{id}", response_model=User, tags=["users"])
async def update_user(id: str, user: User):
    try:
        connection.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
        user = connection.users.find_one({"_id": ObjectId(id)})
    
        return user_entity(user)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=error.args[0])

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    user_entity(connection.users.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=status.HTTP_204_NO_CONTENT)