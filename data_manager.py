from datetime import datetime
import connection
import passhash


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT id, submission_time, title, vote_number, view_number FROM question
                    ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_id_from_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchone()['question_id']
    return question_id


@connection.connection_handler
def get_question_id_from_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment
                    WHERE id = %(comment_id)s
                    """,
                   {'comment_id': comment_id})
    question_id = cursor.fetchone()['question_id']
    return question_id


@connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})
    answer = cursor.fetchall()
    return answer


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
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time DESC;
                   """,
                   {'question_id': question_id})

    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_user_id_from_username(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username=%(username)s
                    """,
                   {'username': username})

    user_id = cursor.fetchone()['id']

    return user_id


@connection.connection_handler
def add_new_question(cursor, request_form, username):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, NULL, %(user_id)s)
                   """,
                   {'title': request_form['Title'],
                    'message': request_form['Message'],
                    'submission_time': get_current_time(),
                    'user_id': get_user_id_from_username(username)})
    cursor.execute("""
                   SELECT id FROM question
                   WHERE message = %(message)s AND title = %(title)s;
                   """,
                   {'message': request_form['Message'],
                    'title': request_form['Title']})
    question_id = cursor.fetchone()['id']
    return question_id


@connection.connection_handler
def add_new_answer(cursor, request_form, question_id, username):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                    VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, NULL, %(user_id)s)
                   """,
                   {'question_id': question_id,
                    'message': request_form['Message'],
                    'submission_time': get_current_time(),
                    'user_id': get_user_id_from_username(username)})


@connection.connection_handler
def edit_question(cursor, request_form, question_id):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s,
                        title = %(title)s,
                        message = %(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': int(question_id),
                    'title': request_form['Title'],
                    'message': request_form['Message'],
                    'submission_time': get_current_time()})


@connection.connection_handler
def edit_answer(cursor, request_form, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET submission_time = %(submission_time)s,
                        message = %(message)s
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id,
                    'message': request_form['message'],
                    'submission_time': get_current_time()})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s
                   """,
                   {'answer_id': answer_id})
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s
                   """,
                   {'answer_id': answer_id})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id IN (SELECT answer_id FROM answer WHERE answer.question_id = %(question_id)s) 
                    OR question_id = %(question_id)s
                   """,
                   {'question_id': question_id})
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s
                   """,
                   {'question_id': question_id})
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s
                   """,
                   {'question_id': question_id})
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s
                   """,
                   {'question_id': question_id})


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


@connection.connection_handler
def get_latest_questions(cursor):
    cursor.execute("""
                    SELECT id, submission_time, title FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def vote_up_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def vote_up_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})


@connection.connection_handler
def vote_down_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def vote_down_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})


@connection.connection_handler
def get_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment
                    ORDER BY submission_time DESC;
                    """)

    comments = cursor.fetchall()

    return comments


@connection.connection_handler
def add_comment_to_question(cursor, request_form, question_id, username):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, 0, %(user_id)s)
                    """,
                   {'question_id': question_id,
                    'message': request_form['message'],
                    'submission_time': get_current_time(),
                    'user_id': get_user_id_from_username(username)})


@connection.connection_handler
def add_comment_to_answer(cursor, request_form, answer_id, question_id, username):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, NULL, %(user_id)s)
                    """,
                   {'question_id': question_id,
                    'answer_id': answer_id,
                    'message': request_form['message'],
                    'submission_time': get_current_time(),
                    'user_id': get_user_id_from_username(username)})


@connection.connection_handler
def add_image_to_question(cursor, request_form, question_id):
    cursor.execute("""
                    UPDATE question
                    SET image = %(image)s
                    WHERE id = %(question_id)s
                    """,
                   {'question_id': question_id,
                    'image': request_form['image']})


@connection.connection_handler
def add_image_to_answer(cursor, request_form, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET image = %(image)s
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id,
                    'image': request_form['image']})


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s
                    """,
                   {'comment_id': comment_id})


def sort_questions(sort_by, order, questions):
    order_by = order == 'Desc'
    questions = sorted(questions, key=lambda x: x[sort_by], reverse=order_by)
    return questions


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                   SELECT id, question_id, answer_id, submission_time, message FROM comment
                   WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})

    comment = cursor.fetchone()

    return comment


@connection.connection_handler
def edit_comment(cursor, request_form, comment_id):
    cursor.execute("""
                    UPDATE comment
                    SET submission_time = %(submission_time)s,
                        message = %(message)s,
                        edited_count = edited_count + 1
                    WHERE id = %(comment_id)s;
                   """,
                   {'submission_time': get_current_time(),
                    'message': request_form['message'],
                    'comment_id': comment_id})


@connection.connection_handler
def get_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag
                    """)

    tags = cursor.fetchall()

    return tags


@connection.connection_handler
def create_new_tag(cursor, request_form):
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES (%(name)s)
                    """,
                   {'name': request_form['new-tag']})


@connection.connection_handler
def get_selected_tag_id(cursor, request_form):
    cursor.execute("""
                    SELECT id FROM tag
                    WHERE name = %(name)s
                    """,
                   {'name': request_form})

    tag_id = cursor.fetchone()['id']

    return tag_id


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s)
                    """,
                   {'question_id': question_id,
                    'tag_id': tag_id})


@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE id IN (SELECT tag_id FROM question_tag WHERE question_id = %(question_id)s)
                   """,
                   {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute("""
                   DELETE FROM question_tag
                   WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s;
                   """,
                   {'question_id': question_id,
                    'tag_id': tag_id})


@connection.connection_handler
def create_user(cursor, request_form):
    cursor.execute("""
                    INSERT INTO users (username, password, registration_time)
                    VALUES (%(username)s, %(password)s, %(registration_time)s)
                    """,
                   {'username': request_form['username'],
                    'password': passhash.hash_password(request_form['password']),
                    'registration_time': get_current_time()})


@connection.connection_handler
def find_user(cursor, request_form):
    cursor.execute("""
                    SELECT username, password FROM users
                    WHERE username = %(username)s 
                   """,
                   {'username': request_form['username']})
    user = cursor.fetchone()
    return user


@connection.connection_handler
def get_user_id_from_qac(cursor, what, id_):
    cursor.execute("""
                    SELECT user_id FROM %(what)s
                    WHERE id=%(id)
                    """,
                   {'what': what,
                    'id': id_})

    user_id = cursor.fetchone()['user_id']

    return user_id
