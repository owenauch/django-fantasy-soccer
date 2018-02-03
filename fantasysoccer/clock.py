from apscheduler.schedulers.blocking import BlockingScheduler
import get_match_stats
import datetime

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def timed_job():
    print("Running match stat collection job")
    get_match_stats.get_match_stats(datetime.datetime.today().strftime('%Y-%m-%d'))

sched.start()
print('Scheduler started')
