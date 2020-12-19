import scipy.signal
import matplotlib.pyplot as plt
import firebasedb as firebasedb
import numpy as np
from collections import defaultdict
import json

def show_submissions():
    online = False

    if online:
        firebasedb.init_db_connection()
        submissions = firebasedb.get_frozen_submissions()

    # Dictionary for aggregating submissions author_submissions_data by author
    # Key - author_name
    # Value - list of [timestamp, score] tuples
    author_data = defaultdict(list)

    # Dictionary for counting author submissions
    # Key - author_name
    # Value - submission counter
    author_submission_counter = defaultdict(int)

    if online:
        # Aggregate all submission author_submissions_data by author
        for submission in submissions:
            # Filter out submissions that don't have author_name (deleted submissions)
            # Filter out submissions with less than 200 score
            if submission.author_name and 100 <= submission.score[-1]:
                author_submission_counter[submission.author_name] += 1
                # Timestamp normalization
                timestamps = [int((timestamp - submission.created_utc) / 60) for timestamp in submission.timestamp]
                for i in range(0, len(timestamps)):
                    # Create [timestamp, score] tuple and append it to the list by the author name key
                    author_data[submission.author_name].append((timestamps[i], submission.score[i]))

    if online:
        # Serialize object
        json.dump(author_data, open("submissions_dump.json", 'w'))
        json.dump(author_submission_counter, open("author_submission_counter_dump.json", 'w'))
    else:
        # Restore serialized object
        author_data = json.load(open("submissions_dump.json", 'r'))
        author_submission_counter = json.load(open("author_submission_counter_dump.json", 'r'))

    line1 = None
    fig, ax1 = plt.subplots()
    ax1.set_xscale('log')
    #ax1.set_yscale('log')

    # Iterate through author_data keys
    for author_name in author_data:
        # Filter out authors with less than 10 submissions
        if len(author_data[author_name]) > 51 and author_submission_counter[author_name] >= 40:
            author_submissions_data = author_data[author_name]

            # Sort author_submissions_data by timestamp
            author_submissions_data.sort(key=lambda tup: tup[0])

            # Apply Savitzky-Golay filter
            # window size 51, polynomial order 3
            xhat = scipy.signal.savgol_filter(list(zip(*author_submissions_data))[0], 51, 3)
            #xhat = list(zip(*author_submissions_data))[0]
            # window size 51, polynomial order 3
            yhat = scipy.signal.savgol_filter(list(zip(*author_submissions_data))[1], 51, 3)

            plt.suptitle(f'{author_name} - {author_submission_counter[author_name]}')
            if author_name == "Eugen0242":
                ax1.plot(xhat, yhat, color='tab:blue')
            else:
                line1 = ax1.plot(xhat, yhat, color='tab:green')

            if line1[0]:
                line1[0].set_alpha(0.1)

            plt.show()

    print('the end')


#i3iqn4
if __name__ == '__main__':
    #show_submission('i3iqn4')
    show_submissions()
    print('end')