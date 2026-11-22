import datetime
import jwt
from typing import List
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from ninja.errors import HttpError
from .models import Todo

api = NinjaAPI(title="Fullstack Todo API")

HARDCODED_USER = "admin"
HARDCODED_PASS = "secret123"
ALGORITHM = "HS256"

# --- Schemas ---
class LoginIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str

class TodoIn(Schema):
    title: str
    completed: bool = False

class TodoOut(Schema):
    id: int
    title: str
    completed: bool

# --- JWT Auth Dependency ---
class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("sub") == HARDCODED_USER:
                return payload["sub"]
        except jwt.PyJWTError:
            return None
        return None

# --- Endpoints ---
@api.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    if data.username != HARDCODED_USER or data.password != HARDCODED_PASS:
        raise HttpError(401, "Invalid username or password")
    
    payload = {
        "sub": data.username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

@api.get("/todos", response=List[TodoOut], auth=JWTAuth())
def list_todos(request):
    return Todo.objects.all().order_by("-id")

@api.post("/todos", response=TodoOut, auth=JWTAuth())
def create_todo(request, data: TodoIn):
    return Todo.objects.create(**data.dict())

@api.put("/todos/{todo_id}", response=TodoOut, auth=JWTAuth())
def update_todo(request, todo_id: int, data: TodoIn):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.title = data.title
    todo.completed = data.completed
    todo.save()
    return todo

@api.delete("/todos/{todo_id}", auth=JWTAuth())
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return {"success": True}
