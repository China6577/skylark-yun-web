import os

# 任务队列的链接地址
broker_url = f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:6379/15"
# 结果队列的链接地址
result_backend = f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:6379/14"
