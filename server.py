from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
def main_page():
    questions = data_manager.get_questions()

    return render_template('list.html', questions=questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        question_id = data_manager.add_new_question(request.form)
        return redirect('/question/{{ question_id }}')


@app.route('/question/<question_id>')
def show_question_details(question_id):
    question = data_manager.get_question_details(question_id)

    return render_template('question.html', question=question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id)
    else:
        answer = data_manager.vmi()
        data_manager.vmi(answer)

        return redirect('/question/<question_id>')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )