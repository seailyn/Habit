import sqlite3
from habit import Habit


def check_for_habit_by_id(habit_id):
    """
    Determines if a habit identifier exists in the database.

    :param habit_id: unique identifier of the habit
    :return: bool, True if the habit identifier exists in the database, False if not
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute("""
                       SELECT id
                       FROM habit
                       """)

        for i in cursor.fetchall():
            ids = str(i).split(",")[0]
            if str(habit_id) == ids[1:]:
                return True
            else:
                continue

        return False


def check_for_habit_by_name(name):
    """
    Determines if a habit name exists in the database.

    :param name: name of the habit
    :return: bool, True if the habit name exists in the database, False if not
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute("""
                       SELECT name
                       FROM habit
                       """)

        habit_names = cursor.fetchall()

        for i in habit_names:
            if name == i[0]:
                return True

            else:
                continue

        return False


def check_date(habit_id, date):
    """
    Determines if a date already exists in the database for a habit.

    :param habit_id: unique identifier of the habit
    :param date: the date checked against the database
    :return: bool, True if the date exists for a habit in the database, False if not
    """
    count = get_habit_completion_count(habit_id)

    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
                       SELECT completed_date
                       FROM checks
                       WHERE habit_id = ?
                       """,
            (habit_id,),
        )

        for i in range(0, count):
            checked_times = str(cursor.fetchone())
            checked_dates = checked_times[2:12]

            if str(date) in checked_dates:
                return True

        return False


def get_habit_by_id(habit_id):
    """
    Searches for and returns habit information stored in the database.

    :param habit_id: unique identifier of the habit
    :return: habit information as a class instance
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
                       SELECT *
                       FROM habit
                       WHERE id = ?
                       """,
            (habit_id,),
        )

        data = cursor.fetchone()

        return Habit(
            habit_id=data[0],
            name=data[1],
            description=data[2],
            period=data[3],
            creation_time=data[4],
        )


def get_habit_dates(habit_id):
    """
    Returns all dates marked complete for a habit.

    :param habit_id: unique identifier of the habit
    :return: list of all dates marked complete for a habit
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
                       SELECT completed_date
                       FROM checks
                       WHERE habit_id = ?
                       """,
            (habit_id,),
        )

        checked_dates = []

        for i in cursor.fetchall():
            checked_dates.append(i[0])

        return checked_dates


def get_period_by_id(habit_id):
    """
    Returns the periodicity of a habit as a string.

    :param habit_id: unique identifier of the habit
    :return: period of a habit as a string
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
                       SELECT period
                       from habit
                       WHERE id = ?
                       """,
            (habit_id,),
        )

        period = str(cursor.fetchone())
        result = period[2:-3]

        return result


def get_habit_completion_count(habit_id):
    """
    Returns the amount of dates marked complete for a habit.

    :param habit_id: unique identifier of the habit
    :return: length of the list of completed dates for a habit
    """
    count = len(get_habit_dates(habit_id))

    return count


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
            result.append(f"{str(habits)}")

        return result


def return_habits_by_period(period):
    """
    Returns the information of all habits of a periodicity as a list of tuples.

    :return: habit information of a period
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        if period is not None:
            cursor.execute("""SELECT * FROM habit WHERE period = ?""", (period,))
            habits = cursor.fetchall()

        else:
            cursor.execute("""SELECT * from habit""")
            habits = cursor.fetchall()

        return habits


def print_habits(habits):
    print(
        "__________________________________________________________________________________"
    )
    print(
        "|{:^6} {:^21} {:^21} {:^7} {:^21}|".format(
            "ID", "Name", "Description", "Period", "Creation Time"
        )
    )
    print(
        "|________________________________________________________________________________|"
    )
    for i in habits:
        print(
            "|{:^5}| {:^20}| {:^20}| {:7}| {:19} |".format(i[0], i[1], i[2], i[3], i[4])
        )
    overline = 82 * "\u203e"
    print(overline)


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

        for i in range(0, count):
            habits = str(cursor.fetchone())
            split = habits.split(",")[0]
            habit_id = split[1:]
            habit = Habit(habit_id=habit_id)
            streaks.append(habit.get_longest_streak())
        longest_streak = max(streaks)

        return longest_streak
