from fastapi import FastAPI
from routes.user import user

app = FastAPI(title="REST API with FastApi and MongoDB", 
              description="This is a simple REST API using fastapi and mongodb",
              version="1.0.0")

app.include_router(user)

@app.get("/")
async def root():
    return {"message": "Welcome to my API with MongoDB"}