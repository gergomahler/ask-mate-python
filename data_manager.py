from datetime import datetime
import time
import connection


def change_unix_to_utc(list_of_dicts):
    for question in list_of_dicts:
        timestamp = float(question["submission_time"]) + 7200
        question["submission_time"] = \
            datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return list_of_dicts


def sorting_by_submission_time(questions):

    return sorted(questions, key=lambda k: k['submission_time'], reverse=True)


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT submission_time, title FROM question
                    ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_details(cursor, question_id):
   cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                  """,
                  {'question_id': question_id})
   question = cursor.fetchall()
   return question


# def increase_view_number(question_id, questions):
#     for question in questions:
#         if question['id'] == question_id:
#             question['view_number'] = int(question['view_number']) + 1
#             connection.write_to_file(QUESTION_FILE, questions, QUESTION_KEYS)


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, message FROM answer
                    LEFT JOIN question
                    ON answer.question_id = question.id
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
                   """)
    answers = cursor.fetchall()
    return answers


# def add_new_question(request_form):
#
#     new_question = {'id': generate_question_id(),
#                     'submission_time': str(time.time()),
#                     'view_number': 0,
#                     'vote_number': 0,
#                     'title': request_form['Title'],
#                     'message': request_form['Message'],
#                     'image': None
#     }
#
#     connection.append_to_file(QUESTION_FILE, new_question, QUESTION_KEYS)
#
#     return new_question['id']
#
#
# def add_new_answer(request_form, question_id):
#     new_answer = {'id': generate_answer_id(question_id), 'submission_time': str(time.time()),
#                   'vote_number': 0,'question_id': request_form['question_id'],
#                   'message': request_form['Message'], 'image': None}


