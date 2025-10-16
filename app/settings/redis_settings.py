import os

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 1)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", None)
