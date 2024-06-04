from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId

from models.order import Order, UpdateOrder

mongo_collection = MongoClient(f"mongodb://admin:password@mongo:27017/").get_database(f"mongo").get_collection(f"orders")

router = APIRouter()


@router.post("/orders/add")
def add_order(order: UpdateOrder):
    try:
        id = str(mongo_collection.insert_one(order.model_dump()).inserted_id)
        return f"Order added with id = {id}"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't create order")


@router.get("/orders/get_order")
def get_orders(id: str):
    try:
        result = mongo_collection.find_one({"_id": ObjectId(id)})
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            raise HTTPException(status_code=404, detail="[ERROR] Order was not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't find order")


@router.get("/orders/get_all")
def get_all_orders():
    try:
        result = []
        for i in mongo_collection.find():
            i["_id"] = str(i["_id"])
            result.append(i)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't get orders")
    

@router.get("/orders/get_all_for_user")
def get_all_orders_for_user(user_id: int):
    try:
        result = []
        for i in mongo_collection.find({'user_id': user_id}):
            i["_id"] = str(i["_id"])
            result.append(i)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't get orders for this user")


@router.delete("/orders/delete_orders")
def delete_order(id: str):
    try:
        mongo_collection.delete_one(filter={"_id": ObjectId(id)}).deleted_count
        return "Order was successfully deleted"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't delete order")


@router.put("/orders/update_order")
def update_order(id: str, order: UpdateOrder):
    try:
        order_dict = order.model_dump()
        order_dict["_id"] = ObjectId(id)
        mongo_collection.update_one(filter={"_id": ObjectId(id)}, update={"$set": order_dict})
        return f"Order with id {id} was successfully updated"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="[ERROR] Can't update order")
