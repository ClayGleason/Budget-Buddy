from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "fdsfdf"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/summary', methods=["POST"])
def summary():
    income = request.form['income']
    expense = request.form['expense']
    if income and expense:
        session['income'] = income
        session['expense'] = expense
        return render_template('summary.html', income=income, expense=expense)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
