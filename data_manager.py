from datetime import datetime
import time
import connection

#QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
QUESTION_FILE = 'sample_data/question.csv'
ANSWER_FILE = 'sample_data/answer.csv'


def change_unix_to_utc(questions):
    for question in questions:
        timestamp = int(question["submission_time"])
        question["submission_time"] = \
            datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return questions


def sorting_by_submission_time(questions):

    return sorted(questions, key=lambda k: k['submission_time'], reverse=True)


def get_questions():
    questions = connection.read_from_file(QUESTION_FILE)
    sorted_questions = sorting_by_submission_time(questions)

    return change_unix_to_utc(sorted_questions)


def generate_id():
    return len(connection.read_from_file(QUESTION_FILE))


def add_new_question(request_form):
    new_question = {'id': generate_id(), 'submission_time': time.time(), 'view_number': 0,
                    'vote_number': 0, 'title': request_form['Title'], 'message': request_form['Message'], 'image': None}

    connection.append_to_file(QUESTION_FILE, new_question)

    return new_question['id']
