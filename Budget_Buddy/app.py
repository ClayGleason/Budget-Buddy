import flask
from models import IncomeEntry, ExpenseEntry, BudgetManager, format_price

app = flask.Flask(__name__)
app.secret_key = "fdsfdf"
app.jinja_env.filters["format_price"] = format_price

# single budget manager instance
budget = BudgetManager()

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/summary', methods=["GET", "POST"])
def summary():
    income = flask.request.form.get('income')
    expense = flask.request.form.get('expense')
    income_desc = flask.request.form.get('income_desc', '').strip()
    expense_desc = flask.request.form.get('expense_desc', '').strip()

    # Convert safely
    try:
        income = float(income) if income else 0
    except ValueError:
        income = 0
    try:
        expense = float(expense) if expense else 0
    except ValueError:
        expense = 0

    if income > 0:
        if not income_desc:
            income_desc = "Income (no description)"
        budget.add_income(IncomeEntry(income_desc, income))

    if expense > 0:
        if not expense_desc:
            expense_desc = "Expense (no description)"
        budget.add_expense(ExpenseEntry(expense_desc, expense))

    return flask.render_template(
        'summary.html',
        incomes=budget.incomes,
        expenses=budget.expenses,
        total_income=budget.get_total_income(),
        total_expense=budget.get_total_expense(),
        net_total=budget.get_net_total()
    )

@app.route('/reset')
def reset():
    global budget
    budget = BudgetManager()
    return flask.redirect(flask.url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
