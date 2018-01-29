from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', start_date='2018-1-29 15:04', hours=6)
def timed_job():
    os.system('get_match_stats.py')

sched.start()