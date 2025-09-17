from abc import ABC, abstractmethod


class Entry(ABC):
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    @abstractmethod
    def get_amount(self):
        pass

class IncomeEntry(Entry):
    def get_amount(self):
        return self.amount


class ExpenseEntry(Entry):
    def get_amount(self):
        return self.amount


class BudgetMaster():
    def __init__(self, income_list, expense_list):
        self.income_list = income_list
        self.expense_list = expense_list

    def add_income(self, entry: IncomeEntry):
        return self.income_list.append(entry)

    def add_expense(self, entry: ExpenseEntry):
        return self.expense_list.append(entry)

    def get_total_income(self):
        total = 0
        for income in self.income_list:
            total += income.get_amount()
        return total

    def get_total_expense(self):
        total = 0
        for expense in self.expense_list:
            total += expense.get_amount()
        return total

    def get_net_total(self):
        income_total = 0
        expense_total = 0

        for income in self.income_list:
            income_total += income.get_amount()

        for expense in self.expense_list:
            expense_total += expense.get_amount()

        return income_total - expense_total
