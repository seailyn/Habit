import sqlite3
from datetime import timedelta, date


class Habit:

    DB_NAME = "habits.db"

    def __init__(self, habit_id = None, name = None, description = None, period = None, creation_time = None):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.period = period
        self.creation_time = creation_time
        self.current_streak = 0
        self.longest_streak = 0
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.DB_NAME) as con:
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habit (
            id INTEGER,
            name VARCHAR(255),
            description VARCHAR(255),
            period VARCHAR(7),
            creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id))
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checks (
            id INTEGER AUTO_INCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            checked_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            FOREIGN KEY (habit_id) REFERENCES habit (id) ON UPDATE CASCADE ON DELETE CASCADE)
            """)

            con.commit()


    def add_habit(self):

        if not db.check_for_habit_by_name(self.name):
            db.create(self.habit_id, self.name, self.description, self.period)
            return True

        elif db.check_for_habit_by_name(self.name):
            return False

        else:
            return None

    def edit_habit(self):

        if db.check_for_habit_by_id(self.habit_id):
            db.edit(self.habit_id, self.name, self.description, self.period)
            return True

        elif not db.check_for_habit_by_id(self.habit_id):
            return False

        else:
            return None


    def delete_habit(self):

        if db.check_for_habit_by_name(self.name):
            db.delete(self.habit_id)
            return True

        elif not db.check_for_habit_by_name(self.name):
            return False

        else:
            return None

    def calculate_streak(self):
        sorted_dates = sorted(db.get_habit_dates(self.habit_id))
        period = db.get_period_by_id(self.habit_id)

        if not sorted_dates:
            self.current_streak = 0
            self.longest_streak = 0

        current_streak = 1
        longest_streak = 1

        if period == 'daily':
            for i in range(1, len(sorted_dates)):
                date_i = date.fromisoformat(sorted_dates[i])
                date_zero = date.fromisoformat(sorted_dates[i - 1])

                if date_i - date_zero == timedelta(days=1):
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

        elif period == 'weekly':
            for i in range(1, len(sorted_dates)):
                date_i = date.fromisoformat(sorted_dates[i])
                date_zero = date.fromisoformat(sorted_dates[i - 1])
                date_i_weekday = date.fromisoformat(sorted_dates[i]).weekday()
                date_zero_weekday = date.fromisoformat(sorted_dates[i - 1]).weekday()

                if (date_i - date_zero < timedelta (days=7) and
                        date_i_weekday > date_zero_weekday):
                    continue

                elif (date_i - date_zero < timedelta(days=7) and date_i_weekday < date_zero_weekday or
                    date_i - date_zero == timedelta(days=7) or
                    timedelta(days=7) < date_i - date_zero < timedelta(days=14) and date_i_weekday > date_zero_weekday):
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                        current_streak = 1

        elif period == 'monthly':
            for i in range(1, len(sorted_dates)):
                date_i_month = date.fromisoformat(sorted_dates[i]).month
                date_zero_month = date.fromisoformat(sorted_dates[i - 1]).month
                date_i_year = date.fromisoformat(sorted_dates[i]).year
                date_zero_year = date.fromisoformat(sorted_dates[i - 1]).year

                if (date_i_month - date_zero_month == 1
                        or date_i_month - date_zero_month == -11 and date_i_year - date_zero_year == 1):
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

        elif period == 'yearly':
            for i in range(1, len(sorted_dates)):
                date_i_year = date.fromisoformat(sorted_dates[i]).year
                date_zero_year = date.fromisoformat(sorted_dates[i - 1]).year
                if date_i_year - date_zero_year == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

        self.current_streak = current_streak
        self.longest_streak = longest_streak


    def get_current_streak(self):
        self.calculate_streak()
        return self.current_streak


    def get_longest_streak(self):
        self.calculate_streak()
        return self.longest_streak


import db