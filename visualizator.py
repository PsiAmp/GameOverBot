import matplotlib.pyplot as plt
import firebasedb as firebasedb
import numpy as np

import scipy.signal

def show_submissions():
    firebasedb.init_db_connection()

    submissions = firebasedb.get_frozen_submissions()
    line1 = None
    line2 = None
    #plt.xscale('log')
    #plt.yscale('log')
    fig, ax1 = plt.subplots()
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    #ax1.set_xlim([0, 360])
    #ax1.set_ylim([0, 1000])

    ax2 = ax1.twinx()
    ax2.set_ylabel('ratio')
    ax2.set_ylim([0.0, 1.1])
    ax2.set_xscale('log')

    # aggregate all submission data by a single author
    total = []
    for submission in submissions:
        if submission.author_name and submission.author_name == "Lighthouse-scout":
            timestamps = [int((timestamp - submission.created_utc) / 60) for timestamp in submission.timestamp]
            for i in range(0, len(timestamps)):
                total.append((timestamps[i], submission.score[i], submission.ratio[i]))

    print(total)

    # filter data by Savitzky-Golay filter
    x = []
    y = []
    for t in total:
        x.append(t[0])
        y.append(t[1])

    yhat = scipy.signal.savgol_filter(total[0], 51, 3)  # window size 51, polynomial order 3

    d = []
    for submission in submissions:
        author_subs = []
        if d[submission.author_name]:
           author_subs = d[submission.author_name]
        author_subs.append(submission)

    for key in d:
        submissions = d[key]


    for submission in submissions:
        if len(submission.score) > 60 and submission.score[-1] > 200 or True:
            timestamps = [int((elem1 - submission.created_utc) / 60) for elem1 in submission.timestamp]

            if submission.author_name and submission.author_name == "Lighthouse-scout":
                line1 = ax1.plot(timestamps, submission.score, color='tab:blue')
                line2 = ax2.plot(timestamps, submission.ratio, color='tab:cyan')
                #line1[0].set_alpha(0.1)
                #line2[0].set_alpha(0.1)
            else:
                line1 = ax1.plot(timestamps, submission.score, color='tab:green')
                line2 = ax2.plot(timestamps, submission.ratio, color='tab:red')
                line1[0].set_alpha(0.1)
                line2[0].set_alpha(0.1)



            plt.suptitle(f'{submission.author_name} {submission.title}')
            #print(submission)

    plt.show()
    print('the end')


def show_submission(submission_id):
    firebasedb.init_db_connection()
    submission = firebasedb.get_submission(submission_id)
    if submission:
        timestamps = [int((elem1 - submission.created_utc) / 60) for elem1 in submission.timestamp]
        line = plt.plot(timestamps, submission.score)
        plt.suptitle(f'{submission.author_name} {submission.title}')
        plt.show()

#i3iqn4
if __name__ == '__main__':
    #show_submission('i3iqn4')
    show_submissions()
    print('end')