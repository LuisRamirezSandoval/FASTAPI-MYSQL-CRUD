from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=list[User])
def show_users():
    lista = conn.execute(users.select()).fetchall()
    rows = []
    for t in lista:
        id = t[0]
        name = t[1]
        email = t[2]
        password = t[3]
        rows.append({"id": id, "name": name, "email": email, "password": password})
    return rows

@user.post("/users", response_model=User)
def add_user(user: User):
    new_user = {"name": user.name, "email":user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    r = conn.execute(users.insert().values(new_user))
    u = users.select().where(users.c.ID == r.inserted_primary_key[0])

    lista = conn.execute(u).fetchall()

    rows = []
    for t in lista:
        id = t[0]
        name = t[1]
        email = t[2]
        password = t[3]
        rows.append(
            {"id": id, "name": name, "email": email, "password": password})
    return rows

@user.get("/users/{id}")
def show_user(id: str):
    u = users.select().where(users.c.ID == id)
    lista = conn.execute(u).fetchall()
    rows = []
    for t in lista:
        id = t[0]
        name = t[1]
        email = t[2]
        password = t[3]
        rows.append(
            {"id": id, "name": name, "email": email, "password": password})
    return rows
    
@user.delete("/users/{id}")
def delete_user(id:str):
    u = conn.execute(users.delete().where(users.c.ID == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}")
def update_user(id:str, user: User):
    conn.execute(users.update().values(
        name = user.name,
        email = user.email,
        password = f.encrypt(user.password.encode("utf-8"))).where(users.c.ID == id))
    return "done update"