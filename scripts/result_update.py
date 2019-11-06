import csv
import os

from flask import Flask, render_template, url_for
from flask_weasyprint import render_pdf


app = Flask(__name__)
base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, 'database')


@app.route('/update/', defaults={'mat_no': 'ENG1503886', 'session': '2016'})
@app.route('/update/<mat_no>/<session>')
def get_name(mat_no, session):
    results = []
    row_number, column_number = 0, 0
    scores = open(os.path.join(base_dir, 'templates', 'Score_Sheet.csv'), 'r')
    csv_reader = csv.reader(scores, delimiter=',')
    for row in csv_reader:
        if (row[column_number+2] == mat_no) and (row[column_number+1] == session):
            results.append((row[column_number], row[column_number+3]))
    return render_template('result_update.html', name=mat_no, results=results, session=session)


@app.route('/update_<mat_no>_<session>.pdf')
def get_pdf(mat_no, session):
    # Make a PDF from another view
    return render_pdf(url_for('get_name', mat_no=mat_no, session=session))


if __name__ == '__main__':
    app.run(debug=True)
