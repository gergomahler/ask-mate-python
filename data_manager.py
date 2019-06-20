from datetime import datetime
import time
import connection


QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_FILE = 'sample_data/question.csv'
ANSWER_FILE = 'sample_data/answer.csv'


def change_unix_to_utc(list_of_dicts):
    for question in list_of_dicts:
        timestamp = float(question["submission_time"]) + 7200
        question["submission_time"] = \
            datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return list_of_dicts


def sorting_by_submission_time(questions):

    return sorted(questions, key=lambda k: k['submission_time'], reverse=True)


def get_questions():
    questions = connection.read_from_file(QUESTION_FILE)
    sorted_questions = sorting_by_submission_time(questions)

    return sorted_questions


def generate_id(for_which_file=0):
    if for_which_file == 0:
        return len(connection.read_from_file(QUESTION_FILE))
    else:
        return len(connection.read_from_file(ANSWER_FILE))


def get_question_details(question_id):
    questions = get_questions()
    increase_view_number(question_id, questions)
    questions_utc = change_unix_to_utc(questions)
    needed_question = None
    for question in questions_utc:
        if question['id'] == question_id:
            needed_question = question
    if get_answers_for_question(question_id) != None:
        needed_question['answers'] = get_answers_for_question(question_id)
    else:
        needed_question['answers'] = {}
    return needed_question


def increase_view_number(question_id, questions):
    for question in questions:
        if question['id'] == question_id:
            question['view_number'] = int(question['view_number']) + 1
            connection.write_to_file(QUESTION_FILE, questions, QUESTION_KEYS)


def get_answers_for_question(question_id):
    answers = connection.read_from_file(ANSWER_FILE)
    needed_answers = []
    for answer in answers:
        if answer['question_id'] == question_id:
            needed_answers.append(answer)
    return change_unix_to_utc(needed_answers)


def add_new_question(request_form):
    new_question = {'id': generate_id(), 'submission_time': str(time.time()), 'view_number': 0,
                    'vote_number': 0, 'title': request_form['Title'], 'message': request_form['Message'], 'image': None}

    connection.append_to_file(QUESTION_FILE, new_question, QUESTION_KEYS)

    return new_question['id']


def add_new_answer(request_form):
    new_answer = {'id': generate_id(1), 'submission_time': str(time.time()),
                    'vote_number': 0,'question_id': request_form['question_id'], 'message': request_form['Message'], 'image': None}

    connection.append_to_file(ANSWER_FILE, new_answer, ANSWER_KEYS)
