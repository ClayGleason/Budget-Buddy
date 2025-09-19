import flask
from models import IncomeEntry, ExpenseEntry, BudgetManager, format_price

app = flask.Flask(__name__)
app.secret_key = "fdsfdf"
app.jinja_env.filters["format_price"] = format_price

budget_manager = BudgetManager()
expense_list = []
income_list = []

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/summary', methods=["POST", "GET"])
def summary():
    if flask.request.method == "POST":
        income = flask.request.form['income']
        expense = flask.request.form['expense']
        income_desc = flask.request.form['income_desc']
        expense_desc = flask.request.form['expense_desc']

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
            income_entry = IncomeEntry(income_desc, income)
            budget_manager.add_income(IncomeEntry(income_desc, income))

        if expense > 0:
            if not expense_desc:
                expense_desc = "Expense (no description)"
            expense_entry = ExpenseEntry(expense_desc, expense)
            budget_manager.add_expense(ExpenseEntry(expense_desc, expense))

        if income and expense:
            income_list.append({ "description": income_entry.description, "amount": income_entry.amount })

            expense_list.append({ "description": expense_entry.description, "amount": expense_entry.amount })

            flask.session['incomes'] = income_list
            flask.session['expenses'] = expense_list
            flask.session['total_income'] = budget_manager.get_total_income()
            flask.session['total_expense'] = budget_manager.get_total_expense()
            flask.session['net_total'] = budget_manager.get_net_total()

            return flask.render_template('summary.html')
        return flask.redirect(flask.url_for('summary'))

    if flask.request.method == "GET":
        return flask.render_template('summary.html')

@app.route('/reset')
def reset():
    global income_list, expense_list, budget_manager
    budget_manager = BudgetManager()
    income_list = []
    expense_list = []
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)