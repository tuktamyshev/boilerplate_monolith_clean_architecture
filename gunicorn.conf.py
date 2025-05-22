bind = "0.0.0.0:8000"
workers = 1
loglevel = "debug"
graceful_timeout = 300
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
forwarded_allow_ips = "*"
