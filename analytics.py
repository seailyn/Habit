import sqlite3
from datetime import timedelta
from habit import Habit


def calculate_streak(habit_id, period):
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT CAST(checked_time as DATE) FROM checks WHERE habit_id = ?""", habit_id)
        checked_dates = cursor.fetchall()
        sorted_dates = sorted(checked_dates)

        if not sorted_dates:
            Habit.current_streak = 0
            Habit.longest_streak = 0
            return

        current_streak = 1
        longest_streak = 1
        for i in range (1, len(sorted_dates)):
            if period == 'daily':
                if sorted_dates[i] - sorted_dates[i - 1] == timedelta(days = 1):
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

            elif period == 'weekly':
                if sorted_dates[i] - sorted_dates[i - 1] < timedelta(days = 7) and sorted_dates[i].date.weekday() > sorted_dates[i - 1].date.weekday():
                    continue
                elif sorted_dates[i] - sorted_dates[i - 1] < timedelta(days = 7) and sorted_dates[i].date.weekday() < sorted_dates[i - 1].date.weekay() or \
                        sorted_dates[i] - sorted_dates[i - 1] == timedelta(days = 7) or \
                        timedelta(days = 7) < sorted_dates[i] - sorted_dates[i - 1] < timedelta(days = 14) and sorted_dates[i].date.weekday() > sorted_dates[i - 1].date.weekday():
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

            elif period == 'monthly':
                if sorted_dates[i].datetime.month - sorted_dates[i - 1].datetime.month == 1 or \
                        sorted_dates[i].datetime.month - sorted_dates[i - 1].datetime.month == -11 and sorted_dates[i].datetime.year - sorted_dates[i - 1].datetime.year == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

            elif period == 'yearly':
                if sorted_dates[i].datetime.year - sorted_dates[i - 1].datetime.year == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

        Habit.current_streak = current_streak
        Habit.longest_streak = longest_streak