import praw_auth
from submission_model import Submission_model
import argparse
import logger_creator
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug


def fetch_comments(reddit, user_name):
    dct = []
    for comment in reddit.redditor(user_name).comments.hot(limit=None):
        if comment.body and comment.id:
            dct.append([comment.id, comment.created_utc, comment.body, comment.body_html])

    json.dump(dct, open(user_name + "_comments_dump.json", 'w'))

if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    # reddit login
    reddit = praw_auth.authenticate()

    # fetch submissions
    fetch_comments(reddit, "johndoe")