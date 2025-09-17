from flask import Flask, render_template, request, session, redirect, url_for, flash

from Budget_Buddy.Entry import IncomeEntry, ExpenseEntry

app = Flask(__name__)
app.secret_key = "fdsfdf"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/summary', methods=["POST"])
def summary():
    income = request.form['income']
    expense = request.form['expense']
    income_desc = request.form['income_desc']
    expense_desc = request.form['expense_desc']
    if income and expense:
        if income_desc == "":
            income_desc = "Item Description Unfilled"
        if expense_desc == "":
            expense_desc = "Expense Description Unfilled"
        new_income_entry = IncomeEntry(income_desc, income)
        new_expense_entry = ExpenseEntry(expense_desc, expense)

        return render_template('summary.html', new_income_entry=new_income_entry, new_expense_entry=new_expense_entry)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
