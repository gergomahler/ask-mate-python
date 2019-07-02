from datetime import datetime
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


@connection.connection_handler
def update_view_number(cursor, question_id):
    cursor.execute("""
                        UPDATE question
                        SET view_number = view_number + 1
                        WHERE id = %(question_id)s;
                       """,
                   {'question_id': question_id})


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
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, NULL);
                   """,
                   {'title': request_form['Title'],
                    'message': request_form['Message'],
                    'submission_time': datetime.now()})
    last_id = cursor.lastrowid
    return last_id


@connection.connection_handler
def add_new_answer(cursor, request_form, question_id):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (submission_time, 0, %(question_id)s, %(message)s, NULL)
                   """,
                   {'question_id': request_form['question_id'],
                    'message': request_form['Message'],
                    'submission_time': datetime.now()})


@connection.connection_handler
def edit_question(cursor, request_form, question_id):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s,
                        view_number = 0,
                        vote_number = 0,
                        title = %(title)s,
                        message = %(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': int(question_id),
                    'title': request_form['Title'],
                    'message': request_form['Message'],
                    'submission_time': str(datetime.now())})
