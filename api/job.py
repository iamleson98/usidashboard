from fastapi import APIRouter, Depends, status
from modules.workers.data_crawler import CRAWLER_WORKER


JobRouter = APIRouter(
    prefix="/v1/jobs", tags=["job"]
)

@JobRouter.put("/", response_model=bool)
def toggle_attendance_crawler_job(on: bool = False):
    CRAWLER_WORKER.toggle_status(on)
    return True
