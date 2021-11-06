from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='fr@nc!s623486', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully conencted to server.")
        break
    except Exception as error:
        print("Failed to connect to server")
        print(f"Error was {error}")
        time.sleep(2)

my_posts = [
    {"title": "Post 1", "content": "post 1 content", "id": 1},
    {"title": "Post 2", "content": "post 2 content", "id": 2},
    {"title": "Post 3", "content": "post 3 content", "id": 3},
    {"title": "Post 4", "content": "post 4 content", "id": 4},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to Post"}


@app.get("/post")
def get_post():
    return {"posts": my_posts}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 999999)
    my_posts.append(post_dict)
    return {"posts": my_posts}


@app.get("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"detail": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
