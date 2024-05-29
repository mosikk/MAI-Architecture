from fastapi import FastAPI
import uvicorn

from router_users import router as router_users


app = FastAPI()

app.include_router(router_users, prefix="/profiru")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
