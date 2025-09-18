from flask import Flask, render_template, request, session, redirect, url_for, flash


from models import IncomeEntry, ExpenseEntry, BudgetManager, format_price

app = Flask(__name__)
app.secret_key = "fdsfdf"
app.jinja_env.filters["format_price"] = format_price

# single budget manager instance
budget_manager = BudgetManager()
expense_list = []
income_list = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/summary', methods=["POST"])
def summary():
    income = request.form['income']
    expense = request.form['expense']
    income_desc = request.form['income_desc']
    expense_desc = request.form['expense_desc']

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

    print(income_list)
    print(expense_list)

    if income and expense:
        income_list.append({ "description": income_entry.description, "amount": income_entry.amount })

        print(income_list)
        expense_list.append({ "description": expense_entry.description, "amount": expense_entry.amount })
        print(expense_list)
        session['incomes'] = income_list
        session['expenses'] = expense_list
        session['total_income'] = budget_manager.get_total_income()
        session['total_expense'] = budget_manager.get_total_expense()
        session['net_total'] = budget_manager.get_net_total()
        return render_template('summary.html')
    return redirect(url_for('summary'))

@app.route('/reset')
def reset():
    session.clear()
    print(session)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)