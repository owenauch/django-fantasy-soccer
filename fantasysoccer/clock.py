from apscheduler.schedulers.blocking import BlockingScheduler
import get_match_stats

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def timed_job():
    get_match_stats.get_match_stats()

sched.start()