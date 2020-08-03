import firebasedb as firebasedb
import praw_auth as praw_auth
import praw
from praw.models.reddit.submission import Submission
from submission_model import Submission_model
from datetime import datetime
import time
import sched
import threading


def fetch_submissions(reddit):
    subreddit = reddit.subreddit("Pikabu")
    for reddit_submission in subreddit.stream.submissions():
        submission = Submission_model.from_reddit_submission(reddit_submission)
        print("FETCHED SUBMISSION: ",submission)
        firebasedb.add_active_submission(submission)


def update_submissions(reddit):
    # Get a list of active submissions
    active_submissions = firebasedb.get_active_submissions()
    print(f"Updating {len(active_submissions)} submissions")

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
    print(f"REMOVING {len(stale_submission_ids)} STALE SUBMISSIONS")
    firebasedb.remove_stale_submissions(stale_submission_ids)

    # Store submissions with timestamps in database
    print(f"Storing {len(submissions)} timestamps")
    firebasedb.record_submission_timestamps(submissions)

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
    # connect db
    firebasedb.init_db_connection()

    # reddit login
    reddit = praw_auth.authenticate()

    # update submissions
    update_submissions(reddit)

    # fetch submissions
    fetch_submissions(reddit)