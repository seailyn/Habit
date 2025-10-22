import sqlite3
import datetime
from habit import Habit


def adapt_date_iso(val):
    """
    As of python 3.12 the datetime adapter is deprecated. This converts the date into an isoformat.

    :param val: date, that is to be transformed
    :return: transformed date
    """
    return val.isoformat()


sqlite3.register_adapter(datetime.date, adapt_date_iso)


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

        cursor.execute(
            """
            INSERT INTO habit (id, name, description, period) VALUES (?, ?, ?, ?)
        """,
            (habit_id, name, description, period),
        )

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

        cursor.execute(
            """
            UPDATE habit SET name = ?, description = ?, period = ? WHERE id = ?
        """,
            (name, description, period, habit_id),
        )

    con.commit()


def delete(habit_id):
    """
    Deletes a database entry via their identifier.
    Ensures the deletion of completed dates by enabling foreign keys.

    :param habit_id: unique identifier of the habit
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute(
            """
            DELETE FROM habit WHERE id = ?
        """,
            (habit_id,),
        )

        con.commit()


def mark_complete(habit_id, date):
    """
    Adds a date and identifier to the database.

    :param habit_id: unique identifier of the habit
    :param date: the date the user marks as complete
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
            INSERT INTO checks (habit_id, completed_date) VALUES(?, ?)
        """,
            (habit_id, date),
        )

        con.commit()


def mark_incomplete(habit_id, date):
    """
    Removes a date marked as completed from the database.

    :param habit_id: unique identifier of the habit
    :param date: the date the user marks as incomplete
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        cursor.execute(
            """
            DELETE FROM checks WHERE habit_id = ? AND completed_date = ?
        """,
            (habit_id, date),
        )

        con.commit()
