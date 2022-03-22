import praw_auth
import argparse
from datetime import datetime, timedelta
import plotly.graph_objects as go


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug


def fetch_comments(reddit, user_name, limit=None, max_days=None):
    md = 0
    comments = []
    for comment in reddit.redditor(user_name).comments.new(limit=limit):
        if max_days is not None and max_days < days_old(comment.created_utc):
            break

        comments.append(comment)
        md = max(md, days_old(comment.created_utc))
    print(md)

    return comments


def fetch_submissions(reddit, user_name, limit=None, max_days=None):
    submissions = []
    for submission in reddit.redditor(user_name).submissions.new(limit=limit):
        if max_days is not None and max_days < days_old(submission.created_utc):
            break

        submissions.append(submission)

    return submissions


def days_old(t_utc):
    today_date = datetime.today().date()
    timestamp_date = datetime.fromtimestamp(t_utc)
    days_diff = (today_date - timestamp_date.date()).days
    return days_diff


def is_date_in_range(date_start, date_end, date):

    return False

def create_z_data(posts):
    z = [[0] * 24 for _ in range(max_days + 1)]

    for post in posts:
        hour = datetime.fromtimestamp(post.created_utc).hour
        day_num = days_old(post.created_utc)

        try:
            z[day_num][hour] += 1
        except IndexError as e:
            print(f'd:{day_num}; h:{hour}')

        if z[day_num][hour] > 10:
            z[day_num][hour] = 10

    return z


if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    # reddit login
    reddit = praw_auth.authenticate()

    max_days = 1000
    username = 'lowrussianprice'

    # fetch submissions
    comments = fetch_comments(reddit, username)
    #submissions = fetch_submissions(reddit, username, max_days=max_days)
    #comments.extend(submissions)

    # create data
    x = list(range(24))

    y = []
    for days_delta in range(0, max_days):
        d = datetime.today() - timedelta(days=days_delta)
        y.append(d.strftime('%Y-%m-%d'))

    z = create_z_data(comments)

    # show graph
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        hoverongaps=False,
        zmax=10
    ))
    fig.show()
