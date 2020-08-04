import sched
import time
import old.comment_upvote_history_recorder as comment_upvote_history_recorder


def launch_recorder(sc):
    comment_upvote_history_recorder.run_recorder()
    sc.enter(60, 1, launch_recorder, (sc,))


recorder_scheduler = sched.scheduler(time.time, time.sleep)
recorder_scheduler.enter(5, 1, launch_recorder, (recorder_scheduler,))
recorder_scheduler.run()
