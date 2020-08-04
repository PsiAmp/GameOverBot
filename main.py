import firebasedb as firebasedb
import praw_auth as praw_auth
from submission_model import Submission_model
import time
import threading
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
import argparse

# Is assigned to a platform logger
log = logging.getLogger('cloudLogger')


# Parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-debug', action="store_true", default=False)
args, unknown = parser.parse_known_args()
is_debug = args.debug


# Init logger that will be visible in Global scope
def init_logger():
    log.setLevel(logging.INFO)
    if not is_debug:
        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)
        log.addHandler(handler)


def fetch_submissions(reddit):
    subreddit = reddit.subreddit("Pikabu")
    for reddit_submission in subreddit.stream.submissions():
        submission = Submission_model.from_reddit_submission(reddit_submission)
        log.info(f"GameOverBot fetched submission: {submission}")
        try:
            firebasedb.add_active_submission(submission)
        except Exception as e:
            log.error(f"GameOverBot error in add_active_submission: {e}")



def update_submissions(reddit):
    # Get a list of active submissions
    active_submissions = []
    try:
        active_submissions = firebasedb.get_active_submissions()
    except Exception as e:
        log.error(f"GameOverBot error in add_active_submission: {e}")
    log.info(f"GameOverBot updating {len(active_submissions)} submissions")

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
    log.info(f"GameOverBot removing {len(stale_submission_ids)} stale submissions")
    try:
        firebasedb.remove_stale_submissions(stale_submission_ids)
    except Exception as e:
        log.error(f"GameOverBot error in remove_stale_submissions: {e}")

    # Store submissions with timestamps in database
    log.info(f"GameOverBot storing {len(submissions)} timestamps")
    try:
        firebasedb.record_submission_timestamps(submissions)
    except Exception as e:
        log.error(f"GameOverBot error in record_submission_timestamps: {e}")

    # Schedule anonther call in 60 seconds
    threading.Timer(60.0, update_submissions, (reddit,)).start()


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
    if submission_age > 1 * 60 * 60 and reddit_submission.score < 30:
        return True

    return False


if __name__ == '__main__':
    init_logger()

    log.info("[[[[[  GameOverBot v0.9  ]]]]]")
    # connect db
    try:
        firebasedb.init_db_connection()
    except Exception as e:
        log.error(e)

    # reddit login
    reddit = praw_auth.authenticate()
    log.info(f"[[[[[  GameOverBot authenticated as  {reddit.user.me()}  ]]]]]")

    # update submissions
    update_submissions(reddit)

    # fetch submissions
    fetch_submissions(reddit)