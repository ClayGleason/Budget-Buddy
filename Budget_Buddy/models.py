from abc import ABC, abstractmethod

def format_price(value):
    return f"{value:,.2f}"

class Entry(ABC):
    def __init__(self, description: str, amount: float):
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
        return -self.amount  # negative for expenses


class BudgetManager:
    def __init__(self):
        self.incomes = []
        self.expenses = []

    def add_income(self, entry: IncomeEntry):
        self.incomes.append(entry)

    def add_expense(self, entry: ExpenseEntry):
        self.expenses.append(entry)

    def get_total_income(self):
        return sum(e.get_amount() for e in self.incomes)

    def get_total_expense(self):
        return -sum(e.get_amount() for e in self.expenses)  # make positive

    def get_net_total(self):
        return self.get_total_income() - self.get_total_expense()
