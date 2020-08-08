import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from submission_model import Submission_model


def init_db_connection():
    global db
    cred = credentials.Certificate("gameoverbot.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()


def add_active_submission(submission):
    db.collection(u'active_submissions_test').document(submission.submission_id).set(submission.to_dict())


def add_submission(submission):
    db.collection(u'frozen_submissions').document(submission.submission_id).set(submission.to_dict())


def get_active_submissions():
    docs = db.collection(u'active_submissions').stream()
    submissions = []
    for doc in docs:
        submission = Submission_model.from_dict(doc.to_dict())
        submissions.append(submission)
    return submissions


def record_submission_timestamps(submissions):
    batch = db.batch()
    for submission in submissions:
        db_ref = db.collection(u'active_submissions').document(submission.submission_id)
        doc = db_ref.get()
        sub = Submission_model.from_dict(doc.to_dict())
        score = sub.score
        score.extend(submission.score)
        ratio = sub.ratio
        ratio.extend(submission.ratio)
        timestamp = sub.timestamp
        timestamp.extend(submission.timestamp)
        batch.update(db_ref, {u'score': score, u'ratio': ratio, u'timestamp': timestamp})
    batch.commit()


def remove_stale_submissions(stale_submission_ids):
    batch = db.batch()
    for submission_id in stale_submission_ids:
        db_ref = db.collection(u'active_submissions').document(submission_id)
        batch.delete(db_ref)
    batch.commit()


def clear_database():
    docs = db.collection(u'frozen_submissions').stream()
    for doc in docs:
        history_docs = doc.collection(u'score_history').stream()
        for his_doc in history_docs:
            his_doc.reference.delete()
        doc.delete()


def get_submissions():
    docs = db.collection(u'frozen_submissions').stream()
    submissions = []
    for doc in docs:
        submission = Submission_model.from_dict(doc.to_dict())
        submissions.append(submission)
    return submissions

def get_submission(submission_id):
    doc_ref = db.collection(u'frozen_submissions').document(submission_id)
    doc = doc_ref.get()
    if doc.exists:
        return Submission_model.from_dict(doc.to_dict())
    return None



