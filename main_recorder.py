import firebasedb
import praw_auth
import logger_creator
from submission_model import Submission_model
import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug

def update_submissions(reddit):
    # Get a list of active submissions
    active_submissions = []
    try:
        active_submissions = firebasedb.get_active_submissions()
    except Exception as e:
        log.error(f"GameOverBot_recorder error in add_active_submission: {e}")
    log.info(f"GameOverBot_recorder updating {len(active_submissions)} submissions")

    active_submission_ids = []
    active_submissions_dict = {}
    for sub in active_submissions:
        # Collect submissions
        active_submission_ids.append('t3_' + sub.submission_id)
        # build dictionary
        active_submissions_dict[sub.submission_id] = sub

    submissions = []
    stale_submission_ids = []
    for reddit_submission in reddit.info(active_submission_ids):
        # Collect stale submissions
        if is_stale(reddit_submission):
            stale_submission_ids.append(reddit_submission.id)
        # Ignore submission with less than 1 upvote
        elif not is_update_needed(reddit_submission, active_submissions_dict[reddit_submission.id]):
            continue
        else:
            # Create submission with current timestamp
            submission = Submission_model.from_reddit_submission(reddit_submission)
            submissions.append(submission)

    # Remove stale submissions from db
    log.info(f"GameOverBot_recorder removing {len(stale_submission_ids)} stale submissions")
    try:
        firebasedb.remove_stale_submissions(stale_submission_ids)
    except Exception as e:
        log.error(f"GameOverBot_recorder error in remove_stale_submissions: {e}")

    # Store submissions with timestamps in database
    log.info(f"GameOverBot_recorder storing {len(submissions)} timestamps")
    try:
        firebasedb.record_submission_timestamps(submissions)
    except Exception as e:
        log.error(f"GameOverBot_recorder error in record_submission_timestamps: {e}")


# Check if submission has an update
def is_update_needed(reddit_submission, submission):
    if reddit_submission.score <= 1:
        return False
    if len(submission.score) == 0:
        return True
    if reddit_submission.score - submission.score[-1] < 2:
        return False
    return True


def is_stale(reddit_submission):
    submission_age = time.time() - reddit_submission.created_utc

    # Submission is too old
    if submission_age > 6 * 60 * 60:
        return True

    # Not enough upvotes in the first hour
    if submission_age > 1 * 60 * 60 and reddit_submission.score < 20:
        return True

    return False


if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    global log
    log = logger_creator.init_logger("GameOverBot_recorder_logger", is_debug)
    log.info("[[[[[  GameOverBot_recorder v0.9  ]]]]]")

    # reddit login
    reddit = praw_auth.authenticate()
    log.info(f"[[[[[  GameOverBot_recorder authenticated as  {reddit.user.me()}  ]]]]]")

    # connect db
    try:
        firebasedb.init_db_connection()
    except Exception as e:
        log.error(e)

    # update submissions
    update_submissions(reddit)

