import matplotlib.pyplot as plt
import numpy as np
import old.my_db_lib
import old.my_reddit_lib as my_reddit_lib

reddit = my_reddit_lib.get_reddit()
comment = reddit.comment('fjs3a1l')
print(comment.body)



for post in reddit.subreddit('funny').stream.submissions():
    print(post.subreddit, post.title)
