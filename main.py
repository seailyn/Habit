from datetime import date, datetime
import questionary
from habit import Habit, Weekly, Monthly, Yearly
from analytics import get_habits
from db import check_date, get_habit_all


def main_menu():
    choice = questionary.select(
        "Welcome to the Habit tracking application. What would you like to do?",
        choices=[
            'Complete Habit',
            'Create Habit',
            'Edit Habit',
            'Delete Habit',
            'Analyze Habit',
            'Stats',
            'Exit'
        ]
    ).ask()

    if choice == 'Complete Habit':
        main_check()
    elif choice == 'Create Habit':
        main_create()
    elif choice == 'Edit Habit':
        main_edit()
    elif choice == 'Delete Habit':
        main_delete()
    elif choice == 'Analyze Habit':
        main_analyze()
    elif choice == 'Stats':
        main_stats()
    elif choice == 'Exit':
        exit()

def main_check():
    habit_id = questionary.text(f'Please enter the id of the habit you want to check off. \
        These are your current habits:{get_habits(period = 'full')}').ask()

    habit = Habit.get_habit(habit_id)

    if not habit:
        print('No such habit.')
        main_menu()

    today = questionary.confirm('Would you like to check today?').ask()

    if today == 'Yes':
        approval = check_date(habit_id, date.today())

        if approval:
            uncheck_today = questionary.confirm(
                'Habit has already been checked for today. Do you want to uncheck today?').ask()

            if uncheck_today:
                Habit.check_habit(habit_id, date.today())
                print('Habit has been successfully unchecked.')
                main_menu()

            if not uncheck_today:
                main_menu()

        if not approval:
            Habit.check_habit(habit_id, datetime.today())
            print('Habit has been successfully checked.')
            main_menu()

    if not today:
        entered_date = questionary.text('Please enter the date(YYYY-MM-DD) you want to check').ask()
        approval = check_date(habit_id, entered_date)

        if approval:
            uncheck_date = questionary.confirm(
                f'Habit has already been checked for {entered_date}. Do you want to uncheck?').ask()

            if uncheck_date:
                Habit.check_habit(habit_id, entered_date)
                print(f'Habit has been successfully unchecked for {entered_date}.')
                main_menu()

            if not uncheck_date:
                main_menu()

        if not approval:
            Habit.check_habit(habit_id, entered_date)
            print(f'Habit has been successfully checked for {entered_date}.')
            main_menu()

def main_create():
    name = questionary.text('What is the name of your Habit?').ask()
    description = questionary.text('What is the description of your Habit?').ask()
    period = questionary.select(
        'In what periodicity should your Habit be tracked? Beware this cannot be changed ',
        choices=[
            'daily',
            'weekly',
            'monthly',
            'yearly'
        ]
    ).ask()

    if period == 'daily':
        habit = Habit(name = name, description = description)
    elif period == 'weekly':
        habit = Weekly(name = name, description = description)
    elif period == 'monthly':
        habit = Monthly(name = name, description = description)
    elif period == 'yearly':
        habit = Yearly(name = name, description = description)

    habit.create_habit()
    print('Habit created!')
    main_menu()

def main_edit():
    habit_id = questionary.text(
        f'Please enter the ID of the habit you want to edit? These are your current habits: {get_habits(period = 'full')}'
    ).ask()
    habit = Habit.get_habit(habit_id)

    if not habit:
        print('Habit not found!')
        main_menu()
        return

    name = questionary.text(f'Please enter the new habit name(current: {habit.name}):')
    description = questionary.text(f'Please enter the new habit description:(current: {habit.description}):')

    habit.name = name
    habit.description = description
    habit.edit_habit()
    print('Habit edited!')
    main_menu()

def main_delete():
    habit_id = questionary.text(
        f'Please enter the ID of the habit you want to delete? These are your current habits: {get_habits(period = 'full')}'
    ).ask()
    habit = Habit.get_habit(habit_id)

    if not habit:
        print('Habit not found!')
        main_menu()
        return

    approval = questionary.confirm(f'Are you sure you want to delete {habit.name}?')
    if approval:
        habit.delete_habit()
        print('Habit deleted!')

    main_menu()


def main_analyze():
    habit_id = questionary.text(
        f'Please enter the id of the habit you want to analyze?'
        f' These are your current habits: {get_habits(period = 'full')}').ask()
    habit = Habit.get_habit(habit_id)

    if not habit:
        print('Habit not found!')
        main_menu()
        return

    habit_data = get_habit_all(habit_id)
    current_streak = Habit.get_current_streak(habit_id)
    longest_streak = Habit.get_longest_streak(habit_id)

    print(habit_data)
    print(f'Your current_streak is {current_streak}')
    print(f'Your longest streak is {longest_streak}')


def main_stats():
    print(f'These are your daily habits: {get_habits(period = 'daily')}')
    print(f'These are your weekly habits: {get_habits(period = 'weekly')}')
    print(f'These are your monthly habits: {get_habits(period = 'monthly')}')
    print(f'These are your yearly habits: {get_habits(period = 'yearly')}')

if __name__ == '__main__':
    main_menu()
