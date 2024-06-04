from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId

from models.tasks import Task, UpdateTask

mongo_collection = MongoClient(f"mongodb://admin:password@mongo:27017/").get_database(f"mongo").get_collection(f"tasks")

router = APIRouter()


@router.post("/tasks/add")
def add_task(task: UpdateTask):
    try:
        id = str(mongo_collection.insert_one(task.model_dump()).inserted_id)
        return f"Task added with id = {id}"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't create task")


@router.get("/tasks/get_task")
def get_tasks(id: str):
    try:
        result = mongo_collection.find_one({"_id": ObjectId(id)})
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            raise HTTPException(status_code=404, detail="[ERROR] Task was not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't find task")


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
        raise HTTPException(status_code=400, detail="[ERROR] Can't get tasks")


@router.delete("/tasks/delete_task")
def delete_task(id: str):
    try:
        mongo_collection.delete_one(filter={"_id": ObjectId(id)}).deleted_count
        return "Task was successfully deleted"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't delete task")


@router.put("/tasks/update_task")
def update_task(id: str, task: UpdateTask):
    try:
        task_dict = task.model_dump()
        task_dict["_id"] = ObjectId(id)
        mongo_collection.update_one(filter={"_id": ObjectId(id)}, update={"$set": task_dict})
        return f"Task with id {id} was successfully updated"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't update task")
