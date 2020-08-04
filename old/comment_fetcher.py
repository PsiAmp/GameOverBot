import my_db_lib
import my_reddit_lib

# Init DB connection
cnx = my_db_lib.get_db_connection()
cursor = cnx.cursor()
sqlFormula = "INSERT IGNORE INTO comments (comment_id, author, creation_date) VALUES (%s, %s, %s)"

# Init PRAW reddit connection
reddit = my_reddit_lib.get_reddit()

# Create subreddit object
pikabuSub = reddit.subreddit("pikabu")

# Stream comments from subreddit
for comment in pikabuSub.stream.comments():
    # Output comment data in console
    my_reddit_lib.output_comment(comment)
    # Create comment object that will be stored in comments table
    comment_db_obj = (comment.id, comment.author.name, comment.created_utc)
    # Store comment in DB
    cursor.execute(sqlFormula, comment_db_obj)
    cnx.commit()
