import firebasedb
import praw_auth
from submission_model import Submission_model
import argparse
import logger_creator


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug


def fetch_submissions(reddit):
    subreddit = reddit.subreddit("Pikabu")
    for reddit_submission in subreddit.stream.submissions(skip_existing=True):
        submission = Submission_model.from_reddit_submission(reddit_submission)
        log.info(f"GameOverBot_fetcher fetched submission: {submission}")
        try:
            firebasedb.add_active_submission(submission)
        except Exception as e:
            log.error(f"GameOverBot_fetcher error in add_active_submission: {e}")


if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    global log
    log = logger_creator.init_logger("GameOverBot_fetcher_logger", is_debug)
    log.info("[[[[[  GameOverBot_fetcher v0.9  ]]]]]")

    # connect db
    try:
        firebasedb.init_db_connection()
    except Exception as e:
        log.error(e)

    # reddit login
    reddit = praw_auth.authenticate()
    log.info(f"[[[[[  GameOverBot_fetcher authenticated as  {reddit.user.me()}  ]]]]]")

    # fetch submissions
    fetch_submissions(reddit)