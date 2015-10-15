import multiprocessing
import os

bind = "127.0.0.1:{}".format(os.getenv('PORT', 8000))
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'aiohttp.worker.GunicornWebWorker'
reload = True
accesslog = '-'
errorlog = '-'
proc_name = 'emergency'
