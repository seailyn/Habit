from datetime import date, datetime
import questionary
from habit import Habit
from analytics import return_questionary_choice_habits, return_overall_longest_streak, return_habits_by_period
from db import check_date, mark_incomplete, mark_complete, get_habit_by_id, get_habit_completion_count


def main_menu():
    """
    Command line interface based on questionary to display the menu of the habit tacking application.
    Lets the user select between seven optional choices.
    """
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
    """
    Prompts the user with a selection choice of all habits.
    Asks the user what date they want to check.
    Determines if the date was already checked for the selected habit.
    Asks the user for confirmation to uncheck, if it's already been checked.
    Marks the date as completed, if it hasn't already been checked.
    """
    print(f'Please select the habit you want to complete.')
    habits = questionary.select('These are your current habits:',
                                choices=
                                return_questionary_choice_habits()
                                ).ask()

    split = habits.split(',')[0]
    habit_id = split[1:]
    today = questionary.confirm('Would you like to check today?').ask()

    if today:

        date_today = date.today().strftime("%Y-%m-%d")

        if check_date(habit_id, date_today):
            uncheck_today = questionary.confirm(
                f'Habit has already been checked for {date_today}. Do you want to uncheck {date_today}?').ask()

            if uncheck_today:
                mark_incomplete(habit_id, date_today)
                print(f'Habit has been successfully unchecked for {date_today}.')
                main_menu()

            elif not uncheck_today:
                main_menu()

        elif not check_date(habit_id, date_today):
            mark_complete(habit_id, date_today)
            print(f'Habit has been successfully checked for {date_today}.')
            main_menu()

    if not today:
        entered_date = questionary.text('Please enter the date(YYYY-MM-DD) you want to check').ask()

        try:
            date_format = bool(datetime.strptime(entered_date, '%Y-%m-%d'))
        except ValueError:
            date_format = False

        if not date_format:
            print('Please enter the date you want to check in this format: YYYY-MM-DD')
            main_menu()

        approval = check_date(habit_id, entered_date)

        if approval:
            uncheck_date = questionary.confirm(
                f'Habit has already been checked for {entered_date}. Do you want to uncheck?').ask()

            if uncheck_date:
                mark_incomplete(habit_id, entered_date)
                print(f'Habit has been successfully unchecked for {entered_date}.')
                main_menu()

            if not uncheck_date:
                main_menu()

        elif not approval:
            mark_complete(habit_id, entered_date)
            print(f'Habit has been successfully checked for {entered_date}.')
            main_menu()


def main_create():
    """
    Asks the user for the name, description, and period of the habit to be created.
    Creates both a habit instance and a database entry.
    """
    name = questionary.text('What is the name of your Habit?').ask()
    description = questionary.text('What is the description of your Habit?').ask()
    period = questionary.select(
        'In what periodicity should your Habit be tracked?',
        choices=[
            'daily',
            'weekly',
            'monthly',
            'yearly'
        ]
    ).ask()

    habit = Habit(name=name, description=description, period=period)

    habit.add_habit()
    print('Habit created!')
    main_menu()


def main_edit():
    """
    Prompts the user with a selection choice of all habits.
    Retrieves old habit data and asks the user for the new information.
    Edits both the habit instance and the database entry.
    """
    habits = questionary.select('These are your current habits:',
                                choices=
                                return_questionary_choice_habits()
                                ).ask()

    split = habits.split(',')[0]
    habit_id = split[1:]

    old_habit = get_habit_by_id(habit_id)

    name = questionary.text(f'Please enter the new habit name(current: {old_habit.name}):').ask()
    description = questionary.text(f'Please enter the new habit description:(current: {old_habit.description}):').ask()
    period = questionary.select('In what periodicity should your Habit be tracked?',
        choices=[
            'daily',
            'weekly',
            'monthly',
            'yearly'
        ]
    ).ask()

    habit = Habit(habit_id=habit_id, name=name, description=description, period=period)
    habit.edit_habit()
    print('Habit edited!')
    main_menu()


def main_delete():
    """
    Prompts the user with a selection choice of all habits.
    Retrieves the habit data and asks the user for confirmation.
    Deletes the habit after confirmation.
    """
    print(f'Please select the habit you want to delete.')
    habits = questionary.select('These are your current habits:',
                                choices=
                                return_questionary_choice_habits()
                                ).ask()

    split = habits.split(',')[0]
    habit_id = split[1:]

    habit = get_habit_by_id(habit_id)

    approval = questionary.confirm(f'Are you sure you want to delete Habit: {habit.name}?').ask()
    if approval:
        habit.delete_habit()
        print('Habit deleted!')

    main_menu()


def main_analyze():
    """
    Prompts the user with a selection choice of all habits.
    Retrieves all the information of the habit.
    Presents the information to the user.
    """
    print(f'Please select the habit you want to analyze.')
    habits = questionary.select('These are your current habits:',
                                choices=
                                return_questionary_choice_habits()
                                ).ask()

    split = habits.split(',')[0]
    habit_id = split[1:]

    habit_data = get_habit_by_id(habit_id)
    habit = Habit(habit_id = habit_id)
    current_streak = habit.get_current_streak()
    longest_streak = habit.get_longest_streak()
    completed_dates = get_habit_completion_count(habit_id)

    print(f'Habit ID:               {habit_data.habit_id}\n'
          f'Habit Name:             {habit_data.name}\n'
          f'Habit Description:      {habit_data.description}\n'
          f'Habit Period:           {habit_data.period}\n'
          f'Habit Creation Time:    {habit_data.creation_time}\n'
          f'Habit Checked:          {completed_dates} times\n')
    print(f'Current Habit streak: {current_streak}')
    print(f'Longest Habit streak: {longest_streak}')


def main_stats():
    """
    Presents habit tracking information not tied to any singular habit instance.
    """
    print(f'These are your current daily habits: \n {return_habits_by_period('daily')} \n'
        f'These are your current weekly habits: \n {return_habits_by_period('weekly')} \n'
        f'These are your current monthly habits: \n {return_habits_by_period('monthly')} \n'
        f'These are your current yearly habits: \n {return_habits_by_period('yearly')} \n')
    print(f'This is your overall longest streak: {return_overall_longest_streak()}')
    main_menu()


if __name__ == '__main__':
    main_menu()

