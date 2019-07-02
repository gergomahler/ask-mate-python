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
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question


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


@connection.connection_handler
def add_new_question(cursor, request_form):

    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (0, 0, 0, %(title)s, %(message)s, NULL);
                   """,
                   {'title': request_form['Title'],
                    'message': request_form['Message']})
    last_id = cursor.lastrowid()
    return last_id


@connection.connection_handler
def add_new_answer(cursor, request_form, question_id):

    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (0, 0, %(question_id)s, %(message)s, NULL)
                   """,
                   {'question_id': request_form['question_id'],
                    'message': request_form['Message']})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s
                   """,
                   {'question_id': question_id})



# @connection.connection_handler
# def delete_answer(cursor, answer_id):
#     cursor.execute("""
#                     DELETE FROM answer
#                     WHERE id = %(answer_id)s
#                    """,
#                    {'answer_id': answer_id})