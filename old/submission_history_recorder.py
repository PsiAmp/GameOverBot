import time
import threading
import old.my_reddit_lib as my_reddit_lib
import old.my_db_lib as my_db_lib


def record_submission(submission_data, history_list, stale_list):
    # Skip submission with hidden score (created less than 1 hour?)
    submission_creation_date = submission_data[2]
    if time.time() - submission_creation_date < 3600 or time.time() - submission_creation_date > 3600 * 24:
        return
    # Init reddit instance
    reddit = my_reddit_lib.get_reddit()
    # Get current submission data by id from Reddit
    submission_id = submission_data[0]
    reddit_submission = reddit.reddit_submission(submission_id)
    # Check if submission is 'stale' and should be deleted
    if comment_cleaner.check_if_stale(reddit_submission):
        stale_list.append(reddit_submission.id)
        return
    # Create submission history record
    history_record = (submission_id, reddit_submission.ups, reddit_submission.num_comments, int(time.time()))
    # Append history record to list
    history_list.append(history_record)


def run_recorder():
    # Init DB connection
    cnx = my_db_lib.get_db_connection()
    cursor = cnx.cursor()

    # Get all stored submissions from DB
    cursor.execute('SELECT * FROM submissions')
    submissions = cursor.fetchall()

    # List where all executed threads
    threads = list()
    # List of comment history records
    submissions_history_list = list()
    # List of stale submissions to be deleted
    stale_submissions_id_list = list()
    # Create timer to measure performance
    t = time.time()

    # Create and start a thread for each comment to record its current state in history
    for submission_item in submissions:
        x = threading.Thread(target=record_submission, args=(submission_item, submissions_history_list, stale_submissions_id_list))
        threads.append(x)
        x.start()

    # Join all threads to wait for the last one to finish before proceeding
    for thread in threads:
        thread.join()

    # Store history in DB
    add_history_item_query = 'INSERT IGNORE INTO upvote_history (comment_id, ups, downs, time) VALUES (%s, %s, %s, %s);'
    for submission_history_item in submissions_history_list:
        cursor.execute(add_history_item_query, submission_history_item)
    cnx.commit()
    print('Added ', len(submissions_history_list), ' history records')

    # Delete stale submissions and history from DB
    comment_cleaner.delete_comments(stale_submissions_id_list)
    print('Cleaned ', len(stale_submissions_id_list), ' stale submissions')

    # Print time took to fetch data from Reddit and store it in DB
    print('In ', round(time.time() - t, 2), ' seconds')
