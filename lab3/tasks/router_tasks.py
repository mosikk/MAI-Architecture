import hashlib
import os

from fastapi import APIRouter, Depends
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

from models.tasks import Task, UpdateTask

mongo_collection = MongoClient(
    f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017/"
).get_database(f"{os.getenv("MONGO_DB")}").get_collection(f"{os.getenv("MONGO_TASKS_COLLECTION")}")

router = APIRouter()


@router.post("/tasks/add")
def add_task(task: UpdateTask):
    try:
        id = str(mongo_collection.insert_one(task.model_dump()).inserted_id)
        return f"Task added with id = {id}"
    except Exception as e:
        print(e)
        return "Can't add task"


@router.get("/tasks/get_task")
def get_tasks(id: str):
    try:
        result = mongo_collection.find_one({"_id": ObjectId(id)})
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            return f"Task with id {id} was not found"
    except Exception as e:
        print(e)


@router.get("/tasks/get_all")
def get_all_tasks():
    try:
        result = []
        for i in mongo_collection.find():
            i["_id"] = str(i["_id"])
            result.append(i)
        return result
    except Exception as e:
        print(e)


@router.delete("/tasks/delete_task")
def delete_task(id: str):
    try:
        mongo_collection.delete_one(filter={"_id": ObjectId(id)}).deleted_count
        return "Task was successfully deleted"
    except Exception as e:
        print(e)


@router.put("/tasks/update_task")
def update_package(id: str, task: UpdateTask):
    try:
        task_dict = task.model_dump()
        task_dict["_id"] = ObjectId(id)
        mongo_collection.update_one(filter={"_id": ObjectId(id)}, update={"$set": task_dict})
        return f"Task with id {id} was successfully updated"
    except Exception as e:
        print(e)
