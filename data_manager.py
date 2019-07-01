from datetime import datetime
import time
import connection


def change_unix_to_utc(list_of_dicts):
    for question in list_of_dicts:
        timestamp = float(question["submission_time"]) + 7200
        question["submission_time"] = \
            datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return list_of_dicts


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT id, submission_time, title FROM question
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
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers
