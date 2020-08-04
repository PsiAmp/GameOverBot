import time
import threading
import old.my_reddit_lib as my_reddit_lib
import old.my_db_lib as my_db_lib


def record_comment(comment_data, history_list, stale_list):
    # Skip comment with hidden score (created less than 1 hour?)
    comment_creation_date = comment_data[2]
    if time.time() - comment_creation_date < 3600 or time.time() - comment_creation_date > 3600 * 24:
        return
    # Init reddit instance
    reddit = my_reddit_lib.get_reddit()
    # Get current comment data by id from Reddit
    comment_id = comment_data[0]
    reddit_comment = reddit.comment(comment_id)
    # Check if comment is 'stale' and should be deleted
    if check_if_stale(reddit_comment):
        stale_list.append(reddit_comment.id)
        return
    # Create comment history record
    history_record = (comment_id, reddit_comment.ups, reddit_comment.downs, int(time.time()))
    # Append history record to list
    history_list.append(history_record)


def run_recorder():
    # Init DB connection
    cnx = my_db_lib.get_db_connection()
    cursor = cnx.cursor()

    # Get all stored comments from DB
    cursor.execute('SELECT * FROM comments')
    comments = cursor.fetchall()

    # List where all executed threads
    threads = list()
    # List of comment history records
    comments_history_list = list()
    # List of stale comments to be deleted
    stale_comment_id_list = list()
    # Create timer to measure performance
    t = time.time()

    # Create and start a thread for each comment to record its current state in history
    for comment_item in comments:
        x = threading.Thread(target=record_comment, args=(comment_item, comments_history_list, stale_comment_id_list))
        threads.append(x)
        x.start()

    # Join all threads to wait for the last one to finish before proceeding
    for thread in threads:
        thread.join()

    # Store history in DB
    add_history_item_query = 'INSERT IGNORE INTO upvote_history (comment_id, ups, downs, time) VALUES (%s, %s, %s, %s);'
    for comment_history_item in comments_history_list:
        cursor.execute(add_history_item_query, comment_history_item)
    cnx.commit()
    print('Added ', len(comments_history_list), ' history records')

    # Delete stale comments and history from DB
    delete_comments(stale_comment_id_list)
    print('Cleaned ', len(stale_comment_id_list), ' stale comments')

    # Print time took to fetch data from Reddit and store it in DB
    print('In ', round(time.time() - t, 2), ' seconds')


ups_threshold = 10
downs_threshold = -5
duration_threshold = 7200


def check_if_stale(comment):
    # Check comment upvote threshold and if it is new
    if comment.ups < ups_threshold \
            and comment.downs > downs_threshold \
            and time.time() - comment.created_utc > duration_threshold:
        return True
    return False


def delete_comments(comment_id_list):
    # Init DB connection
    cnx = my_db_lib.get_db_connection()
    cursor = cnx.cursor()

    for comment_id in comment_id_list:
        # Delete from upvote_history table
        delete_history_query = 'DELETE FROM upvote_history WHERE comment_id = %s'
        cursor.execute(delete_history_query, (comment_id,))
        # Delete from comments table
        delete_comment_query = 'DELETE FROM comments WHERE comment_id = %s'
        cursor.execute(delete_comment_query, (comment_id,))
    # Execute queries
    cnx.commit()