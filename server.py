from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
def main_page():
    questions = data_manager.get_latest_questions()
    return render_template('list.html', questions=questions, link=True)


@app.route('/list')
def list_all_questions():
    questions = data_manager.get_questions()
    if request.args.get('order') is not None:
        questions = data_manager.sort_questions(request.args.get('sort'), request.args.get('order'), questions)

    return render_template('list.html', questions=questions, link=False)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    question_id = data_manager.add_new_question(request.form)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>')
def show_question_details(question_id):
    question = data_manager.get_question_details(question_id)
    question_comments = data_manager.get_comments_for_question(question_id)
    answers = data_manager.get_answers_for_question(question_id)
    data_manager.update_view_number(question_id)

    return render_template('question.html', question=question, question_comments=question_comments, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id)

    data_manager.add_new_answer(request.form, question_id)

    return redirect(f'/question/{question_id}')


@app.route('/search')
def search():
    search_phrase = request.args.get('q')
    search_results = data_manager.find_questions_and_answers(search_phrase)
    return render_template('list.html', questions= search_results)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_details(question_id)
    if request.method == 'GET':
        return render_template('edit-question.html', question_id=question_id, question=question)

    data_manager.edit_question(request.form, question_id)

    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = data_manager.get_answer(answer_id)
        return render_template('edit-answer.html', answer=answer)

    data_manager.edit_answer(request.form, answer_id)
    question_id = data_manager.get_question_id_from_answer(answer_id)

    return redirect(f'/question/{ question_id }')


@app.route('/question/<question_id>/delete')
def delete_a_question(question_id):
    answer_id = data_manager.get_answers_for_question(question_id)
    data_manager.delete_question(question_id, answer_id)

    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def delete_an_answer(answer_id):
    question_id = data_manager.get_question_id_from_answer(answer_id)
    data_manager.delete_answer(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)

    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    data_manager.vote_up_answer(answer_id)
    question_id = data_manager.get_question_id_from_answer(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    data_manager.vote_down_answer(answer_id)
    question_id = data_manager.get_question_id_from_answer(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add-comment-question.html', question_id=question_id)

    data_manager.add_comment_to_question(request.form, question_id)

    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
