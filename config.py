"""全局配置

所有可变项都从环境变量读取，本地开发用默认值，CI 里用 workflow 覆盖。
这样同一套代码既能在本地跑，也能在 GitHub Actions 里跑。
"""

import os

# 被测系统前端地址（本地默认 8081，CI 里同样跑在 8081）
BASE_URL = os.getenv("BASE_URL", "http://localhost:8081")

# 是否无头模式。本地调试设为 false（能看见浏览器），CI 里必须为 true
HEADLESS = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes")

# Redis 连接信息（用于读取验证码答案）
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None
