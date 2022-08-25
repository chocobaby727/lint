import os

# Server Socket
bind = "0.0.0.0:" + os.getenv("PORT")

# Worker Processes
workers = 2 * os.cpu_count() + 1
threads = 2 * os.cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Debugging
reload = True

# # SSL
# keyfile = '/run/secrets/ssh_key'
# certfile = '/run/secrets/ssh_crt'
# ciphers = 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256'

# # Logging
# accesslog = './logs/access.log'
# errorlog = './logs/error.log'
# loglevel = 'info'
