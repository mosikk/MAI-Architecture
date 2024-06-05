from fastapi import FastAPI
import uvicorn

from router_orders import router as router_orders


app = FastAPI()

app.include_router(router_orders, prefix="/profiru")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
