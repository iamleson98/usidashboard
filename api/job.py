from fastapi import APIRouter, Depends, status
from repositories.job import SettingRepo
from dto.settings import SettingValue, SettingType, SettingKey, SettingSchema


JobRouter = APIRouter(
    prefix="/v1/settings", tags=["job"]
)

@JobRouter.put("/data_crawler", response_model=SettingSchema)
def toggle_attendance_crawler_job(run_status: SettingValue, svc: SettingRepo = Depends()):
    """set to true to keep the job running, false otherwise"""
    result = svc.update_by_type_and_key(SettingType.data_crawler.value, SettingKey.run_data_crawler.value, run_status.value)
    if result:
        return result.normalize()
    return None
