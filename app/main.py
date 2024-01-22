from fastapi import FastAPI
from .import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



#models.Base.metadata.create_all(bind=engine)


app = FastAPI()
# & e:/Backend/fastapi_venv/Scripts/Activate.ps1
# fastapi_venv\Scripts\activate.bat
# uvicorn app.main:app --reload
#& e:/Backend/fastapi_venv/Scripts/Activate.ps1
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": " Welcome to My API!!!"}

# select users.id, users.email, COUNT(posts.id) from posts RIGHT JOIN users ON posts.owner_id = users.id group by users.id
# SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id where post_id = 10 GROUP BY posts.id;
