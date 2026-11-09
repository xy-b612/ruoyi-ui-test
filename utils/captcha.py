import json
import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


def get_captcha(uuid):
    """根据 uuid 从 Redis 读取验证码答案"""
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        password=REDIS_PASSWORD,
        decode_responses=True,
        protocol=2,
    )
    val = r.get(f"captcha_codes:{uuid}")
    if val is None:
        raise RuntimeError(f"Redis 中未找到验证码，uuid={uuid}")
    try:
        return json.loads(val)
    except Exception:
        return val
