from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def timed_job():
    os.system('get_match_stats.py')

sched.start()