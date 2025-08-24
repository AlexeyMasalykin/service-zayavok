# Gunicorn configuration file

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'service_zayavok'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn/service_zayavok.pid'
user = 'alex2061'
group = 'alex2061'
tmp_upload_dir = None

# SSL (если нужен HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
