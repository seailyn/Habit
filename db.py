import sqlite3


def create(habit_id, name, description, period):
    """
    Creates a database entry with habit information.

    :param habit_id: unique identifier of the habit
    :param name: name of the habit
    :param description: description of the habit
    :param period: periodicity of the habit(i.e. 'daily', 'weekly', 'monthly', 'year')
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        if not habit_id:
            cursor.execute("""
                INSERT INTO habit (id, name, description, period) VALUES (?, ?, ?, ?)
            """, (habit_id, name, description, period))

        con.commit()

def edit(habit_id, name, description, period):
    """
    Updates a database entry with new habit information.

    :param habit_id: unique identifier of the habit
    :param name: name of the habit
    :param description: description of the habit
    :param period: periodicity of the habit(i.e. 'daily', 'weekly', 'monthly', 'year')
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute("""
            UPDATE habit SET name = ?, description = ?, period = ? WHERE id = ?
        """, (name, description, period, habit_id))

    con.commit()

def delete(habit_id):
    """
    Deletes a database entry via their identifier.

    :param habit_id: unique identifier of the habit
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute("""
            DELETE FROM habit WHERE id = ?
        """, (habit_id,))

        con.commit()


def mark_complete(habit_id, date):
    """
    Adds a date and identifier to the database.

    :param habit_id: unique identifier of the habit
    :param date: the date the user marks as complete
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO checks (habit_id, completed_date) VALUES(?, ?)
        """, (habit_id, date))

        con.commit()



def mark_incomplete(habit_id, date):
    """
    Removes a date marked as completed from the database.

    :param habit_id: unique identifier of the habit
    :param date: the date the user marks as incomplete
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM checks WHERE habit_id = ? AND completed_date = ?
        """, (habit_id, date))

        con.commit()


def check_for_habit_by_id(habit_id):
    """
    Determines if a habit identifier exists in the database.

    :param habit_id: unique identifier of the habit
    :return: bool, True if the habit identifier exists in the database, False if not
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT id FROM habit
        """)
        result = False

        for i in cursor.fetchall():
            ids = str(i).split(',')[0]
            if habit_id == ids[1:]:
                result = True
                break
            else:
                continue

        return result


def check_for_habit_by_name(name):
    """
    Determines if a habit name exists in the database.

    :param name: name of the habit
    :return: bool, True if the habit name exists in the database, False if not
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT name FROM habit
        """)
        result = False
        habit_names = cursor.fetchall()
        for i in habit_names:
            if name == i[0]:
                result = True
                break

            else:
                continue

        return result


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
        cursor.execute("""SELECT completed_date FROM checks WHERE habit_id = ?""", (habit_id,))
        result = False

        for i in range(0, count):
            checked_times = str(cursor.fetchone())
            checked_dates = checked_times[2:12]

            if str(date) in checked_dates:
                result = True
                break

        return result


def get_habit_by_id(habit_id):
    """
    Searches for and returns habit information stored in the database.

    :param habit_id: unique identifier of the habit
    :return: habit information as a class instance
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM habit WHERE id = ?
        """, (habit_id,))
        data = cursor.fetchone()
        return Habit(habit_id = data[0], name = data[1],
                     description = data[2], period = data[3], creation_time = data[4])

def get_habit_dates(habit_id):
    """
    Returns all dates marked complete for a habit.

    :param habit_id: unique identifier of the habit
    :return: list of all dates marked complete for a habit
    """
    with (sqlite3.connect(Habit.DB_NAME) as con):
        cursor = con.cursor()
        cursor.execute("""
            SELECT completed_date FROM checks WHERE habit_id = ?
        """, (habit_id,))

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
        cursor.execute("""
            SELECT period from habit WHERE id = ?
        """, (habit_id,))
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



from habit import Habit
