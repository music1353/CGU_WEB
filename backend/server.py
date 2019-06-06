# use waitress WSGI server

from waitress import serve
from app import app
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.modules.backup_engine.drive import drive
from app.modules.schedule_func import func

def cloud_backup():
    googledrive = drive()
    googledrive.backup()


scheduler = BackgroundScheduler()
scheduler.add_job(func=func.local_backup, trigger="cron", hour=12, minute=57, second=1)
scheduler.add_job(func=cloud_backup, trigger="cron", hour=12, minute=57, second=5)
scheduler.add_job(func=func.update_week, trigger="cron", hour=0, minute=0, second=1)
# scheduler.add_job(func=update_week, trigger="cron", hour=15, minute=49, second=1)
scheduler.add_job(func=func.init_mission, trigger="cron", hour=0, minute=0, second=2)
scheduler.add_job(func=func.init_users_daily_games, trigger="cron", hour=0, minute=0, second=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

