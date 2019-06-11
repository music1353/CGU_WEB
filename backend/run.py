# -*- coding: UTF-8 -*-

# from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app import app
from app.modules.backup_engine.drive import drive
from app.modules.schedule_func import func

from flask_apscheduler import APScheduler

def cloud_backup():
    # google drive 備份
    googledrive = drive()
    googledrive.backup()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.apscheduler.add_job(func=func.local_backup, id="local_backup", trigger="cron", hour=16, minute=52, second=1)
app.apscheduler.add_job(func=func.update_week, id="update_week", trigger="cron", hour=16, minute=56, second=1)
print(app.apscheduler.get_jobs())

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=func.local_backup, trigger="cron", hour=12, minute=58, second=1)
# scheduler.add_job(func=cloud_backup, trigger="cron", hour=12, minute=59, second=30)
# scheduler.add_job(func=func.update_week, trigger="cron", hour=0, minute=0, second=1)
# scheduler.add_job(func=func.init_mission, trigger="cron", hour=0, minute=0, second=2)
# scheduler.add_job(func=func.init_users_daily_games, trigger="cron", hour=0, minute=0, second=3)
# scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(use_reloader=False)
    # app.run(debug=True) # 會執行兩次