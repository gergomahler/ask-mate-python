from datetime import datetime
import connection

question_file = 'sample_data/question.csv'
answer_file = 'sample_data/answer.csv'


def change_unix_to_utc(questions):
    for question in questions:
        timestamp = int(question["submission_time"])
        question["submission_time"] = \
            datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return questions


def sorting_by_submission_time(questions):

    return sorted(questions, key=lambda k: k['submission_time'], reverse=True)


def get_questions():
    questions = connection.read_from_file(question_file)
    sorted_questions = sorting_by_submission_time(questions)

    return change_unix_to_utc(sorted_questions)



"""
def add_new_question():
    question = {}
    keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
"""
