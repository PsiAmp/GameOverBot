from datetime import datetime
import time


class __Score_record(object):
    def __init__(self, score, ratio, timestamp):
        self.score = score
        self.ratio = ratio
        self.timestamp = timestamp


class Submission_model(object):
    def __init__(self,
                 submission_id,
                 title,
                 author_name,
                 created_utc,
                 url,
                 permalink,
                 score=[],
                 ratio=[],
                 timestamp=[]
                ):
        self.submission_id = submission_id
        self.title = title
        self.author_name = author_name
        self.created_utc = created_utc
        self.url = url
        self.permalink = permalink
        self.score = score
        self.ratio = ratio
        self.timestamp = timestamp


    @staticmethod
    def from_dict(source):
        submission = Submission_model(
            submission_id   = source[u'submission_id'],
            title           = source[u'title'],
            author_name     = source[u'author_name'],
            created_utc     = source[u'created_utc'],
            url             = source[u'url'],
            permalink       = source[u'permalink'],
            score           = source[u'score'],
            ratio           = source[u'ratio'],
            timestamp       = source[u'timestamp']
        )

        return submission

    @staticmethod
    def from_reddit_submission(reddit_submission):
        submission = Submission_model(
        submission_id   = reddit_submission.id,
        title           = reddit_submission.title,
        author_name     = reddit_submission.author.name,
        created_utc     = reddit_submission.created_utc,
        url             = reddit_submission.url,
        permalink       = 'https://www.reddit.com' + reddit_submission.permalink,
        score = [reddit_submission.score],
        ratio = [reddit_submission.upvote_ratio],
        timestamp = [time.time()]
        )

        return submission

    def to_dict(self):
        dest = {
            u'submission_id': self.submission_id,
            u'title': self.title,
            u'author_name': self.author_name,
            u'created_utc': self.created_utc,
            u'url': self.url,
            u'permalink': self.permalink,
            u'score': self.score,
            u'ratio': self.ratio,
            u'timestamp': self.timestamp
        }

        return dest

    def __repr__(self):
        return(
            f's_id={self.submission_id}, author={self.author_name},  title={self.title}, url={self.url}, permalink={self.permalink}, created_utc={datetime.fromtimestamp(self.created_utc)}'
        )
