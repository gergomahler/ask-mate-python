from datetime import datetime
import connection


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

@connection.connection_handler
def find_questions_and_answers(cursor, search_phrase):
    cursor.execute("""
                    SELECT  DISTINCT id, submission_time, title FROM question
                    
                    WHERE message LIKE  %(search_phrase)s OR title LIKE %(search_phrase)s
                    OR id IN (SELECT question_id FROM answer WHERE message LIKE %(search_phrase)s)
                    ORDER BY submission_time DESC;
                   """,
                   {'search_phrase': '%' + search_phrase + '%'})
    questions = cursor.fetchall()
    return questions
