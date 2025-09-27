from analytics import calculate_streak
from db import initialize_db, edit, check_date, check, delete


class Habit:

    DB_NAME = 'habits.db'

    def __init__ (self, habit_id, name, description, period = 'daily'):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.period = period
        self.current_streak = 0
        self.longest_streak = 0
        initialize_db()

    def get_current_streak(self):
        calculate_streak(self.habit_id, self.period)
        return self.current_streak

    def get_longest_streak(self):
        calculate_streak(self.habit_id, self.period)
        return self.longest_streak

    def edit_habit(self):
        edit(self.habit_id, self.name, self.description)

    def check_habit(self, date):
        check(self.habit_id, date)
        
    def delete_habit(self):
        delete(self.habit_id)

class Weekly(Habit):

    def __init__(self, habit_id, name, description):
        super().__init__(habit_id, name, description, 'weekly')

class Monthly(Habit):

    def __init__(self, habit_id, name, description):
        super().__init__(habit_id, name, description, 'monthly')

class Yearly(Habit):

    def __init__(self, habit_id, name, description):
        super().__init__(habit_id, name, description, 'yearly')


