from fastapi import APIRouter
from models.app_config_model import AppConfigModel
from lib.app_config import get_app_config

router = APIRouter(
    prefix="/api/v1",
    tags=["v1/application-configuration"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/application-configuration", status_code=200, response_model=AppConfigModel)
async def get_application_configuration():
    return get_app_config()

