import praw

def authenticate():
    authentication = praw.Reddit(site_name='GameOverBot', user_agent='REDDIT_USER_AGENT')
    print(f'_Authenticated as {authentication.user.me()}\n')
    return authentication
