import time
import connection

question_file = 'sample_data/question.csv'
answer_file = 'sample_data/answer.csv'


def get_questions():
    return connection.read_from_file(question_file)


"""
def add_new_question():
    question = {}
    keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
"""
