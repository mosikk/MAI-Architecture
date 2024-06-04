import datetime
import hashlib
import psycopg2

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import jwt

from utils.postgres_utils import PostgresDB, init_postgres
from models.user import User, UpdateUser


init_postgres()
connection = PostgresDB(db_name="users_db")

security = HTTPBasic()
SECRET_KEY = "aboba"

router = APIRouter()


@router.get("/users/auth")
def auth(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = payload["user_id"]
    except:
        raise HTTPException(status_code=402, detail="[ERROR] Can't auth")
    return {"user_id": current_user}


@router.get("/users/login")
def login(credentials: HTTPBasicCredentials = Depends(security), cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        if credentials.username and credentials.password:
            cmd = f"SELECT id, password FROM users WHERE users.login = %s"
            cursor.execute(cmd, (credentials.username,))
            result = cursor.fetchone()
            cursor.close()
            if not result:
                return []
            
            hashed_password: str = hashlib.sha256(credentials.password.encode()).hexdigest()
            token = jwt.encode({'user_id': result[0], 'exp': datetime.datetime.now() + datetime.timedelta(minutes=10)}, SECRET_KEY, algorithm="HS256")

            if hashed_password == result[1]:
                return {"token": token}
            else:
                return {"message": "[ERROR] Incorrect password"}
            
        else:
            return {"message": "[ERROR] Incorrect login or password"}
    except:
        raise HTTPException(status_code=402, detail="[ERROR] Can't login")


@router.post("/users/add")
async def add_user(user: UpdateUser, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cmd = "INSERT INTO users (login, name, surname, password) VALUES (%s, %s, %s, %s)"
        data = (
            user.login, 
            user.name, 
            user.surname,
            hashlib.sha256(user.password.encode()).hexdigest(),
        )
        cursor.execute(cmd, data)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        raise HTTPException(status_code=400, detail="[ERROR] Can't create user")
    return {"message": "User created"}


@router.get("/users/find_by_login")
async def find_user_by_login(login: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cmd = f"SELECT id, login, name, surname from users WHERE login LIKE '{login}'"
        cursor.execute(cmd)
        result = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.close()
        raise HTTPException(status_code=400, detail="[ERROR] Can't find user")
    return result


@router.get("/users/find_by_mask")
async def find_user_by_mask(name: str, surname: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cmd = f"SELECT id, login, name, surname from users WHERE name LIKE '%{name}%' AND surname LIKE '%{surname}%'"
        cursor.execute(cmd)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        cursor.close()
        raise HTTPException(status_code=400, detail="[ERROR] Can't find user")
    return result


@router.delete("/users/delete")
async def delete_user(id: int, token: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cur_user = auth(token=token)
        print(cur_user)
        if cur_user.get("user_id", "") == id:
            cmd = f"DELETE FROM users WHERE id={id}"
            cursor.execute(cmd)
            cursor.connection.commit()
        else:
            raise HTTPException(status_code=402, detail="[ERROR] Invalid auth data") 
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        raise HTTPException(status_code=400, detail="[ERROR] Can't delete user")
    return {"message": "User deleted"}


@router.put("/users/update")
async def update_user(id: int, user_upd: UpdateUser, token: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cur_user = auth(token=token)
        print(cur_user)
        if cur_user.get("user_id", "") == id:
            user_upd.password = hashlib.sha256(user_upd.password.encode()).hexdigest()
            user_upd_dict = UpdateUser.model_dump(user_upd, exclude_none=True, exclude=["id"])

            cmd = f"UPDATE users SET {', '.join([f"{key} = %s" for key in user_upd_dict.keys()])} WHERE id = %s RETURNING id"
            cursor.execute(cmd, list(user_upd_dict.values()) + [id])
            if cursor.fetchone():
                return {"message": "User updated"}
            else:
                raise Exception
        else:
            raise HTTPException(status_code=402, detail="[ERROR] Invalid auth data") 
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(status_code=400, detail="[ERROR] Can't update user")
