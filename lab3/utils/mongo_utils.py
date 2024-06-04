import os

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


mongo_client: AsyncIOMotorClient = None


async def connect_and_init_mongo():
    global mongo_client
    # mongo_uri = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017/"
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db = os.getenv('MONGO_DB')
    mongo_tasks_collection = os.getenv('MONGO_TASKS_COLLECTION')
    mongo_orders_collection = os.getenv('MONGO_ORDERS_COLLECTION')

    try:
        mongo_client = AsyncIOMotorClient(mongo_uri)
        await mongo_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')

        if mongo_db not in await mongo_client.list_database_names():
            await mongo_client.get_database(mongo_db).create_collection(mongo_tasks_collection)
            print(f'Collection {mongo_tasks_collection} created', flush=True)

            await mongo_client.get_database(mongo_db).create_collection(mongo_orders_collection)
            print(f'Collection {mongo_orders_collection} created', flush=True)

            mongo_tasks_collection = mongo_client.get_database(mongo_db).get_collection(mongo_tasks_collection)
            mongo_orders_collection = mongo_client.get_database(mongo_db).get_collection(mongo_orders_collection)

            print(f'Database {mongo_db} created', flush=True)

    except Exception as ex:
        print(f'Cant connect to mongo: {ex}', flush=True)


def close_mongo_connect():
    global mongo_client
    if mongo_client is None:
        return
    mongo_client.close()
