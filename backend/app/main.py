from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

from app import services
from app.schema import UserIn, BaseResponse, UserListOut

app = FastAPI()

# Custom Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency (seconds)", ["method", "endpoint"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration)
    return response

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/")
async def index():
    return {"message": "Hello from FastAPI – metrics active!"}

@app.post("/users", response_model=BaseResponse)
async def user_create(user: UserIn):
    try:
        services.add_userdata(user.dict())
        return {"success": True}
    except:
        return {"success": False}

@app.get("/users", response_model=UserListOut)
async def get_users():
    return services.read_usersdata()

