workers = 5    # 定義同時開啟的處理請求的進程數量，根據網站流量適當調整
worker_class = "gevent"   # 採用gevent，支持亦不處理請求，提高吞吐量
bind = "0.0.0.0:5000"    # 監聽IP放寬、以便於Docker之間、Docker和宿主機之間的通信


# apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import *
import atexit
from app import app
from app.modules.schedule_func import func, listener
import pymongo
from config import client

jobstores = {
    'mongo': MongoDBJobStore(client=client),
}
executors = {
    'default': ThreadPoolExecutor(30),
    'processpool': ProcessPoolExecutor(30)
}

scheduler = BackgroundScheduler(misfire_grace_time=300, jobstores=jobstores, executors=executors)
scheduler.add_listener(listener.aps_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)

# TODO: new
scheduler.add_job(func=func.insert_users_complete_records, id="insert_users_complete_records", trigger="cron", hour=23, minute=56, second=1, jobstore='mongo', replace_existing=True)
scheduler.add_job(func=func.local_backup, id="local_backup", trigger="cron", hour=23, minute=57, second=1, jobstore='mongo', replace_existing=True)
scheduler.add_job(func=func.cloud_backup, id="cloud_backup", trigger="cron", hour=23, minute=59, second=30, jobstore='mongo', replace_existing=True)
scheduler.add_job(func=func.update_week, id="update_week", trigger="cron", hour=0, minute=0, second=1, jobstore='mongo', replace_existing=True)
scheduler.add_job(func=func.init_mission, id="init_mission", trigger="cron", hour=0, minute=0, second=2, jobstore='mongo', replace_existing=True)
scheduler.add_job(func=func.init_users_daily_games, id="init_users_daily_games" ,trigger="cron", hour=0, minute=0, second=3, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.check_scheduler_alive, id="check_scheduler_alive_minute", trigger="cron", minute=50, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.check_scheduler_alive, id="check_scheduler_alive_second", trigger="cron", second=30, jobstore='mongo', replace_existing=True)

# test
# scheduler.add_job(func=func.local_backup, id="local_backup", trigger="cron", hour=17, minute=20, second=1, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.local_backup, id="local_backup", trigger="cron", hour=10, minute=12, second=1, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.cloud_backup, id="cloud_backup", trigger="cron", hour=11, minute=14, second=15, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.update_week, id="update_week", trigger="cron", hour=9, minute=49, second=1, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.init_mission, id="init_mission", trigger="cron", hour=9, minute=49, second=2, jobstore='mongo', replace_existing=True)
# scheduler.add_job(func=func.init_users_daily_games, id="init_users_daily_games" ,trigger="cron", hour=9, minute=49, second=3, jobstore='mongo', replace_existing=True)

print(scheduler.get_jobs())
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())