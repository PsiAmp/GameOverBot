import old.my_db_lib as my_db_lib
import old.my_reddit_lib as my_reddit_lib

# Init DB connection
cnx = my_db_lib.get_db_connection()
cursor = cnx.cursor()
sqlFormula = "INSERT IGNORE INTO submissions " \
             "(id, author, created_utc, subreddit, num_comments, shortlink, title) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s)"

# Init PRAW reddit connection
reddit = my_reddit_lib.get_reddit()

# Create subreddit object
subreddit = reddit.subreddit('pikabu')

# Stream submissions from subreddit
for submission in subreddit.stream.submissions():
    # Output submission data in console
    my_reddit_lib.output_submission(submission)
    # Create submission object that will be stored in submissions table
    submission_db_object = (submission.id,
                            submission.author.name,
                            submission.created_utc,
                            submission.subreddit.display_name,
                            submission.num_comments,
                            submission.shortlink,
                            submission.title)
    # Store submission in DB
    cursor.execute(sqlFormula, submission_db_object)
    cnx.commit()
