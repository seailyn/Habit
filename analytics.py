import sqlite3
from habit import Habit


def return_questionary_choice_habits():
    """
    Returns a list of all habits in the format used by questionary.

    :return: list of habit information
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT id from habit""")
        count = len(cursor.fetchall())
        cursor.execute("""SELECT id, name, description from habit""")

        result = []

        for i in range(0, count):
            habits = cursor.fetchone()
            result.append(f'{str(habits)}')

        return result


def return_habits_by_period(period):
    """
    Returns the information of all habits of a periodicity as a list of tuples.

    :return: habit information of a period
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT * from habit WHERE period = ?""", (period,))
        result = cursor.fetchall()
        return result


def return_overall_longest_streak():
    """
    Gets the identifier of all habits from the database, calculates the streaks of the habits, and
    returns the overall longest streak.

    :return: longest streak of all habits
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT id FROM habit""")
        count = len(cursor.fetchall())
        cursor.execute("""SELECT id FROM habit""")
        streaks = []
        for i in range(0,count):
            habits = str(cursor.fetchone())
            split = habits.split(',')[0]
            habit_id = split[1:]
            habit = Habit(habit_id = habit_id)
            streaks.append(habit.get_longest_streak())
        longest_streak = max(streaks)

        return longest_streak
