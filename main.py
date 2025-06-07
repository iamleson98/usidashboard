from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.employee import EmployeeRouter
from api.attendance import CheckingEventApiRouter
from api.breaking import BreakApiRouter
from api.job import JobRouter
from configs.env import get_environment_variables
from metadata.tags import Tags
from modules.workers.data_crawler import CRAWLER_WORKER
from modules.workers.stale_checking_event_clean_worker import STALE_CHECKING_EVENT_CLEANER
from models.base import init
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from api.ws import SocketRouter
from api.abnormals import AbnormalRouter
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


env = get_environment_variables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # checking data crawler job
    scheduler.add_job(CRAWLER_WORKER.execute, IntervalTrigger(seconds=120))
    # clear stale checking events job
    scheduler.add_job(STALE_CHECKING_EVENT_CLEANER.execute, CronTrigger(hour=0, minute=0))
    scheduler.start()
    init()

    # redis
    redis = aioredis.from_url(env.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
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
app.include_router(BreakApiRouter)
app.include_router(SocketRouter)
app.include_router(JobRouter)
app.include_router(AbnormalRouter)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
