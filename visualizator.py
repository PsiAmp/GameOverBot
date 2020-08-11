import matplotlib.pyplot as plt
import firebasedb as firebasedb

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
    ax1.set_xlim([0, 360])
    ax1.set_ylim([0, 1000])

    ax2 = ax1.twinx()
    ax2.set_ylabel('ratio')
    ax2.set_ylim([0.0, 1.1])
    ax2.set_xscale('log')

    plt.show()

    for submission in submissions:
        if len(submission.score) > 60 and submission.score[-1] > 200 or True:
            timestamps = [int((elem1 - submission.created_utc) / 60) for elem1 in submission.timestamp]

            if line1 is not None:
                line1[0].set_alpha(0.1)
            if line2 is not None:
                line2[0].set_alpha(0.1)

            line1 = ax1.plot(timestamps, submission.score, color='tab:green')
            line2 = ax2.plot(timestamps, submission.ratio, color='tab:red')

            plt.suptitle(f'{submission.author_name} {submission.title}')

            print(submission)
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