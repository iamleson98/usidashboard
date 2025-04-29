from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.employee import EmployeeRouter
from api.attendance import CheckingEventApiRouter
from api.breaking import BreakApiRouter
from configs.env import get_environment_variables
from metadata.tags import Tags
from modules.workers.data_crawler import CRAWLER_WORKER
from models.base import init
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from api.ws import SocketRouter


env = get_environment_variables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    trigger = IntervalTrigger(minutes=env.DATA_CRAWLER_INTERVAL_MINS)
    scheduler.add_job(CRAWLER_WORKER.execute, trigger)
    scheduler.start()
    init()
    yield
    scheduler.shutdown()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(EmployeeRouter)
app.include_router(CheckingEventApiRouter)
app.include_router(BreakApiRouter)
app.include_router(SocketRouter)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
