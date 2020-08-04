import matplotlib.pyplot as plt
import old.my_db_lib
import math


# Get top upvoted comments from DB
def get_top_comments():
    cnx = my_db_lib.get_db_connection()
    cursor = cnx.cursor()
    top_comment_query = 'SELECT comment_id FROM upvote_history WHERE ups=(SELECT MAX(ups) FROM upvote_history);'
    cursor.execute(top_comment_query)
    return cursor.fetchall()


# Get comment history
def get_comment_history(comment):
    cnx = my_db_lib.get_db_connection()
    cursor = cnx.cursor()
    top_comment_query = 'SELECT time, ups FROM upvote_history WHERE comment_id = %s;'
    comment_id = comment[0]
    cursor.execute(top_comment_query, (comment_id,))
    return cursor.fetchall()


top_comments = get_top_comments()
top_comment = top_comments[0]
comment_history = get_comment_history(top_comment)

# Draw plot x-time y-upvotes
first_recorded_time = comment_history[0][0]
testList2 = [((elem1 - first_recorded_time)/60, elem2) for elem1, elem2 in comment_history]

testList3 = [((elem1 - first_recorded_time)/60, elem2) for elem1, elem2 in comment_history]

# Calculate rate of chane of the function
rate_of_change = list()
i = 1
for i in range(1, len(comment_history)-1):
    x = comment_history[i][0] - first_recorded_time
    y = comment_history[i][1]
    x0 = comment_history[i-1][0] - first_recorded_time
    y0 = comment_history[i-1][1]
    rate = (y-y0) / (x-x0)
    rate_of_change.append((x, rate))

plt.plot(*zip(*testList2))
# plt.plot(*zip(*rate_of_change))
plt.show()

print()
