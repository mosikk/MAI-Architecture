import hashlib
import psycopg2

from fastapi import APIRouter, Depends, HTTPException

from utils.postgres_utils import PostgresDB, init_postgres
from models.user import User, UpdateUser


init_postgres()
connection = PostgresDB(db_name="users_db")

router = APIRouter()


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
async def delete_user(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        cmd = f"DELETE FROM users WHERE id={id}"
        cursor.execute(cmd)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        raise HTTPException(status_code=400, detail="[ERROR] Can't delete user")
    return {"message": "User deleted"}


@router.put("/users/update")
async def update_user(user_upd: UpdateUser, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        user_id = user_upd.user_id
        user_upd.password = hashlib.sha256(user_upd.password.encode()).hexdigest()
        user_upd_dict = UpdateUser.model_dump(user_upd, exclude_none=True, exclude=["user_id"])

        cmd = f"UPDATE users SET {', '.join([f"{key} = %s" for key in user_upd_dict.keys()])} WHERE user_id = %s RETURNING user_id"
        cursor.execute(cmd, user_upd_dict.value() + [user_id])
        if cursor.fetchone():
            return {"message": "User updated"}
        else:
            raise Exception
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(status_code=400, detail="[ERROR] Can't update user")
