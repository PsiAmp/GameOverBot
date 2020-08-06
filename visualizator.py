import matplotlib.pyplot as plt
import firebasedb as firebasedb

def show_submissions():
    firebasedb.init_db_connection()

    submissions = firebasedb.get_submissions()
    line = None
    plt.xscale('log')
    plt.yscale('log')

    for submission in submissions:
        if len(submission.score) > 60 and submission.score[-1] > 200:
            timestamps = [int((elem1 - submission.created_utc) / 60) for elem1 in submission.timestamp]
            if line:
                line[0].set_alpha(0.1)
            line = plt.plot(timestamps, submission.score)
            plt.suptitle(f'{submission.author_name} {submission.title}')
            print(submission)
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