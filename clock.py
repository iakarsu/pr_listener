from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

from mw import pr_listener, trial

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    pr_listener()
    print('done')

sched.start()