import praw
from datetime import datetime


def get_reddit():
    return praw.Reddit()


def output_comment_by_id(reddit, comment_id):
    comment = reddit.comment(comment_id)
    output_comment(comment)


def output_comment(comment, text=''):
    print(text, datetime.fromtimestamp(comment.created_utc), comment, comment.body)


def output_submission(submission):
    print(datetime.fromtimestamp(submission.created_utc), submission.subreddit, submission.id, submission.title)
