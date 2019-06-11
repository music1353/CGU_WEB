# use waitress WSGI server

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from waitress import serve
from app import app
import atexit
from app.modules.backup_engine.drive import drive
from app.modules.schedule_func import func
import pymongo
from config import client

def cloud_backup():
    googledrive = drive()
    googledrive.backup()

jobstores = {
    'mongo': MongoDBJobStore(client=client),
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

scheduler = BackgroundScheduler(misfire_grace_time=300, jobstores=jobstores, executors=executors)

scheduler = BackgroundScheduler()
scheduler.add_job(func=func.local_backup, id="local_backup", trigger="cron", hour=23, minute=57, second=1, jobstore='mongo')
scheduler.add_job(func=cloud_backup, id="cloud_backup", trigger="cron", hour=23, minute=59, second=30, jobstore='mongo')
scheduler.add_job(func=func.update_week, id="update_week", trigger="cron", hour=0, minute=0, second=1, jobstore='mongo')
scheduler.add_job(func=func.init_mission, id="init_mission", trigger="cron", hour=0, minute=0, second=2, jobstore='mongo')
scheduler.add_job(func=func.init_users_daily_games, id="init_users_daily_games" ,trigger="cron", hour=0, minute=0, second=3, jobstore='mongo')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

