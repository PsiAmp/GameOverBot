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


def fetch_comments(reddit, user_name, limit=None, date_start=None, date_end=None):
    comments = []
    for comment in reddit.redditor(user_name).comments.new(limit=limit):
        date = datetime.fromtimestamp(comment.created_utc)
        if date_start and date < date_start:
            break
        if date_end and date_end < date:
            continue

        comments.append(comment)

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


def days_delta(d1, d2):
    return abs((d1 - d2).days)


def create_z_data(posts, date_start, date_end):
    z = [[0] * 24 for _ in range(days_delta(date_end, date_start) + 1)]

    for post in posts:
        hour = datetime.fromtimestamp(post.created_utc).hour
        day_num = days_delta(date_end, datetime.fromtimestamp(post.created_utc))

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

    date_end = datetime(2022, 3, 23)
    date_start = datetime(2022, 2, 15)
    username = 'username'

    # fetch submissions
    comments = fetch_comments(reddit, username, date_start=date_start, date_end=date_end)
    #submissions = fetch_submissions(reddit, username, max_days=max_days)
    #comments.extend(submissions)

    # create data
    x = list(range(24))

    y = []
    for days in range(0, days_delta(date_end, date_start)):
        d = date_end - timedelta(days=days)
        y.append(d.strftime('%Y-%m-%d'))

    z = create_z_data(comments, date_start=date_start, date_end=date_end)

    # show graph
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        hoverongaps=False,
        zmax=10
    ))
    fig.show()
