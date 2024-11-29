import redis
import uuid
from loguru import logger
from lib.settings import get_settings

redis_client = redis.Redis(host=get_settings().redis_host, password=get_settings().redis_password, port=6379, decode_responses=True)

@logger.catch
def set_temporary_image_token(snapshot_id: str, expire:int = 60*60*24) -> str: 
    generated_uuid = str(uuid.uuid4())
    logger.info("Setting image token {generated_uuid} for snapshot {snapshot_id}")
    redis_client.set(generated_uuid, snapshot_id, ex=expire)
    logger.info("Image token set")
    # redis entry expires in 24 hours by default
    return generated_uuid

@logger.catch
def get_snapshot_id(image_token: str) -> str:
    stored_id = redis_client.get(image_token)
    return stored_id
