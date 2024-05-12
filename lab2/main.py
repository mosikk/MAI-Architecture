from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from api.router_users import router as router_users
from utils.postgres_utils import init_postgres


async def startup():
    await init_postgres()


load_dotenv()

app = FastAPI()

# app.add_event_handler("startup", startup)
app.include_router(router_users, prefix="/profiru")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
