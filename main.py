import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import users, auth, avatar
from src.conf.config import settings

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(avatar.router, prefix='/api')

origins = [ 
    "http://127.0.0.1:3000", "http://127.0.0.1:5000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the server starts up.
    It's a good place to initialize things that are needed by your app, such as database connections.
    
    :return: A fastapilimiter instance
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is a function that returns the message &quot;Welcome to FastAPI!&quot; if the database connection is successful.
    If there's an error connecting to the database, it will return a 500 status code with an error message.
    
    :param db: Session: Get the database connection from the dependency
    :return: A dict with a message
    :doc-author: Trelent
    """
    try:
        result = db.execute("SELECT 1").fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
