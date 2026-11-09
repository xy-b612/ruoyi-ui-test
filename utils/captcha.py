import json
import redis

def get_captcha(uuid):
    r = redis.Redis(
        host="localhost", port=6379, db=0, decode_responses=True, protocol=2
    )
    val = r.get(f"captcha_codes:{uuid}")
    if val is None:
        raise RuntimeError(f"Redis 中未找到验证码，uuid={uuid}")
    try:
        return json.loads(val)
    except Exception:
        return val
