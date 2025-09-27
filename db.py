import sqlite3
from habit import Habit

def initialize_db():
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit (
            id INTEGER,
            name VARCHAR(255),
            description VARCHAR(255),
            creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id))
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checks (
            id INTEGER AUTO INCREMENT,
            habit_id INTEGER NOT NULL,
            checked_time TIMESTAMP NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY(habit_id) REFERENCES habit(id))
        """)

        con.commit()

def edit(habit_id, name, description):
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        if habit_id:
            cursor.execute("""
                UPDATE habit SET name = ?, description = ?, WHERE id = ?
            """, (name, description, habit_id))

        else:
            cursor.execute("""
                INSERT INTO habit (name, description) VALUES(?, ?)
            """, (name, description))
            Habit.habit_id = cursor.lastrowid

        con.commit()

def check_date(habit_id, date):
    """Determines if the given date is already checked off.
    """
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT CAST(checked_time AS DATE) FROM checks WHERE habit_id = ?""", habit_id)
        checked_dates = cursor.fetchall()

        if date in checked_dates:
            return True

        else:
            return False

def check(habit_id, date):
    with sqlite3.connect(Habit.DB_NAME) as con:
        cursor = con.cursor()

        if check_date(habit_id, date):
            cursor.execute("""
                DELETE FROM checks WHERE habit_id = ? AND checked_date = ?           
            """, (habit_id, date))

        elif not check_date(habit_id, date):
            cursor.execute("""
                INSERT INTO checks (habit_id, checked_date) VALUES(?, ?)
            """, (habit_id, date))


        con.commit()
