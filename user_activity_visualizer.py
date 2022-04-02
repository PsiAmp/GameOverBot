import praw_auth
import argparse
from datetime import datetime, timedelta
import plotly.graph_objects as go


class UserActivityScanner:

    def __init__(self, username: str, date_from: datetime, date_to: datetime, scan_comments: bool, scan_submissions: bool):
        self.username = username
        self.date_from = date_from
        self.date_to = date_to
        self.scan_comments = scan_comments
        self.scan_submissions = scan_submissions

        # reddit login
        self.reddit = praw_auth.authenticate()

        # fetch submissions
        self.user_data = self.scan_user()

        # create data
        self.show_graph()

    def scan_user(self):
        user_submissions = []
        if self.scan_comments:
            comments = self.fetch_comments()
            user_submissions.extend(comments)
        if self.scan_submissions:
            submissions = self.fetch_submissions()
            user_submissions.extend(submissions)
        return user_submissions

    def fetch_comments(self, limit=None):
        comments = []
        for comment in self.reddit.redditor(self.username).comments.new(limit=limit):
            date = datetime.fromtimestamp(comment.created_utc)
            if self.date_from and date < self.date_from:
                break
            if self.date_to and self.date_to < date:
                continue

            comments.append(comment)

        return comments

    def fetch_submissions(self, limit=None):
        submissions = []
        for submission in self.reddit.redditor(self.username).submissions.new(limit=limit):
            date = datetime.fromtimestamp(submission.created_utc)
            if self.date_from and date < self.date_from:
                break
            if self.date_to and self.date_to < date:
                continue

            submissions.append(submission)

        return submissions

    def days_old(self, t_utc: str):
        today_date = datetime.today().date()
        timestamp_date = datetime.fromtimestamp(t_utc)
        days_diff = (today_date - timestamp_date.date()).days
        return days_diff

    def days_delta(self, d1: datetime, d2: datetime):
        return abs((d1 - d2).days)

    def create_z_data(self):
        z = [[0] * 24 for _ in range(self.days_delta(self.date_to, self.date_from) + 1)]

        for post in self.user_data:
            hour = datetime.fromtimestamp(post.created_utc).hour
            day_num = self.days_delta(self.date_to, datetime.fromtimestamp(post.created_utc))

            try:
                z[day_num][hour] += 1
            except IndexError as e:
                print(f'd:{day_num}; h:{hour}')

            if z[day_num][hour] > 10:
                z[day_num][hour] = 10

        return z

    def show_graph(self):
        x = list(range(24))

        y = []
        for days in range(0, self.days_delta(self.date_to, self.date_from)):
            d = self.date_to - timedelta(days=days)
            y.append(d.strftime('%Y-%m-%d'))

        z = self.create_z_data()

        # show graph
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=x,
            y=y,
            hoverongaps=False,
            zmax=10
        ))
        #html = fig.to_html()
        #fig.write_image(f'{self.username}.png')
        fig.show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    global is_debug
    is_debug = args.debug


if __name__ == '__main__':
    # Parsing command line arguments
    parse_args()

    u = UserActivityScanner(username='ace13pikabu',
                            date_from=datetime(2022, 2, 1),
                            date_to=datetime.today(),
                            scan_comments=True,
                            scan_submissions=True)
