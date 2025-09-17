from abc import ABC, abstractmethod

class Entry(ABC):
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    @abstractmethod
    def get_amount(self):
        pass

    def __str__(self):
        return f"{self.description}: ${self.amount}"


class IncomeEntry(Entry):
    def get_amount(self):
        return self.amount


class ExpenseEntry(Entry):
    def get_amount(self):
        return self.amount


class BudgetMaster:
    def __init__(self, income_list=None, expense_list=None):
        self.income_list = income_list if income_list else []
        self.expense_list = expense_list if expense_list else []

    def add_income(self, entry: IncomeEntry):
        self.income_list.append(entry)

    def add_expense(self, entry: ExpenseEntry):
        self.expense_list.append(entry)

    def get_total_income(self):
        return sum(income.get_amount() for income in self.income_list)

    def get_total_expense(self):
        return sum(expense.get_amount() for expense in self.expense_list)

    def get_net_total(self):
        return self.get_total_income() - self.get_total_expense()
