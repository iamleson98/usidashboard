from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.employee import EmployeeRouter
from api.attendance import CheckingEventApiRouter
from api.job import JobRouter
from configs.env import env
from metadata.tags import Tags
from modules.workers.data_crawler import execute_data_crawler
from modules.workers.stale_checking_event_clean_worker import clear_stale_events
from models.base import init
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from api.ws import SocketRouter
from api.abnormals import AbnormalRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # checking data crawler job
    scheduler.add_job(execute_data_crawler, IntervalTrigger(seconds=env.DATA_CRAWLER_INTERVAL_SECS))
    # clear stale checking events job
    scheduler.add_job(clear_stale_events, CronTrigger(hour=0, minute=0))
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
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(EmployeeRouter)
app.include_router(CheckingEventApiRouter)
app.include_router(SocketRouter)
app.include_router(JobRouter)
app.include_router(AbnormalRouter)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
