import praw_auth
import argparse
import json
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug


def fetch_comments(reddit, user_name, limit=None, max_days=None):
    comments = []
    for comment in reddit.redditor(user_name).comments.new(limit=limit):
        comments.append(comment)

        if max_days is not None and max_days <= days_old(comment.created_utc):
            break

    return comments


def fetch_submissions(reddit, user_name, limit=None, max_days=None):
    submissions = []
    for submission in reddit.redditor(user_name).submissions.new(limit=limit):
        submissions.append(submission)

        if max_days is not None and max_days >= days_old(submission.created_utc):
            break

    return submissions


def days_old(t_utc):
    today_date = datetime.today().date()
    timestamp_date = datetime.fromtimestamp(t_utc)
    days_diff = (today_date - timestamp_date.date()).days
    return days_diff


def store_user_comments(reddit, user_name, max_comments=None, max_days=None):
    comment_data = []
    comments = fetch_comments(reddit, user_name, max_comments, max_days=max_days)

    for comment in comments:
        t_utc = comment.created_utc
        timestamp_date = datetime.fromtimestamp(t_utc)
        comment_data.append([comment.id, comment.created_utc, comment.body, comment.body_html])

    json.dump(comment_data, open(user_name + f"_comments_dump_{datetime.today().strftime('%Y-%m-%d %H-%M')}.json", 'w'))


if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    # reddit login
    reddit = praw_auth.authenticate()

    store_user_comments(reddit, user_name="psiamp", max_comments=None, max_days=30)
