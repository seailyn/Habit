import db
import analytics
from habit import Habit
from datetime import date


class TestHabit:
    def test_create_habit(self):
        habit_data = Habit(
            habit_id=999, name="name", description="description", period="daily"
        )
        habit_data.add_habit()

        test_habit = analytics.get_habit_by_id(habit_data.habit_id)
        assert test_habit.name == habit_data.name
        assert test_habit.description == habit_data.description
        assert test_habit.period == habit_data.period

    def test_complete_date(self):
        completed_date = date.today()
        test_date_1 = analytics.check_date(999, completed_date)
        db.mark_complete(999, completed_date)

        test_date_2 = analytics.check_date(999, completed_date)
        assert not test_date_1
        assert test_date_2

    def test_incomplete_date(self):
        incompleted_date = date.today()
        test_date_1 = analytics.check_date(999, incompleted_date)
        db.mark_incomplete(999, incompleted_date)

        test_date_2 = analytics.check_date(999, incompleted_date)
        assert test_date_1
        assert not test_date_2

    def test_calculate_daily_streak(self):
        habit = Habit(habit_id=999)

        db.mark_complete(999, "2025-09-01")
        test_habit_streak_1 = habit.get_current_streak()

        db.mark_complete(999, "2025-09-02")
        test_habit_streak_2 = habit.get_current_streak()

        db.mark_complete(999, "2025-09-04")
        test_habit_streak_3 = habit.get_current_streak()
        test_habit_streak_4 = habit.get_longest_streak()

        assert test_habit_streak_1 == 1
        assert test_habit_streak_2 == 2
        assert test_habit_streak_3 == 1
        assert test_habit_streak_4 == 2

    def test_calculate_weekly_streak(self):
        habit = Habit(habit_id=999, period="weekly")
        habit.edit_habit()

        test_weekly_streak_1 = habit.get_current_streak()

        db.mark_complete(999, "2025-09-12")
        test_weekly_streak_2 = habit.get_current_streak()

        db.mark_complete(999, "2025-09-22")
        test_weekly_streak_3 = habit.get_current_streak()

        assert test_weekly_streak_1 == 1
        assert test_weekly_streak_2 == 2
        assert test_weekly_streak_3 == 1

    def test_calculate_monthly_streak(self):
        habit = Habit(habit_id=999, period="monthly")
        habit.edit_habit()

        test_monthly_streak_1 = habit.get_current_streak()

        db.mark_complete(999, "2025-10-01")
        test_monthly_streak_2 = habit.get_current_streak()

        db.mark_complete(999, "2025-12-01")
        test_monthly_streak_3 = habit.get_current_streak()

        assert test_monthly_streak_1 == 1
        assert test_monthly_streak_2 == 2
        assert test_monthly_streak_3 == 1

    def test_calculate_yearly_streak(self):
        habit = Habit(habit_id=999, period="yearly")
        habit.edit_habit()

        test_yearly_streak_1 = habit.get_current_streak()

        db.mark_complete(999, "2026-01-01")
        test_yearly_streak_2 = habit.get_current_streak()

        db.mark_complete(999, "2028-01-01")
        test_yearly_streak_3 = habit.get_current_streak()

        assert test_yearly_streak_1 == 1
        assert test_yearly_streak_2 == 2
        assert test_yearly_streak_3 == 1

    def test_edit_habit(self):
        edit_habit_data = Habit(
            habit_id=999,
            name="edited_name",
            description="edited_description",
            period="edited",
        )
        edit_habit_data.edit_habit()

        test_habit = analytics.get_habit_by_id(edit_habit_data.habit_id)
        assert test_habit.name == edit_habit_data.name
        assert test_habit.description == edit_habit_data.description
        assert test_habit.period == edit_habit_data.period

    def test_delete_habit(self):
        delete_habit_data = Habit(habit_id=999, name="edited_name")
        delete_habit_data.delete_habit()

        test_habit = analytics.check_for_habit_by_id(delete_habit_data.habit_id)
        assert not test_habit

    def test_calculate_streak(self):
        current_streaks = [3, 13, 1, 1, 2]
        longest_streaks = [10, 14, 10, 2, 2]

        for i in range(1, 5):
            habit = Habit(habit_id=i)

            test_current_streak = habit.get_current_streak()
            test_longest_streak = habit.get_longest_streak()

            assert test_current_streak == current_streaks[i - 1]
            assert test_longest_streak == longest_streaks[i - 1]

    def test_overall_longest_streak(self):
        test_overall_longest_streak = analytics.return_overall_longest_streak()

        assert test_overall_longest_streak == 14

    def test_date_count(self):
        habit_counts = [25, 27, 24, 5, 5]

        for i in range(1, 5):
            count = analytics.get_habit_completion_count(i)

            assert count == habit_counts[i - 1]

    def test_habit_period(self):
        daily_habits = analytics.return_habits_by_period("daily")
        weekly_habits = analytics.return_habits_by_period("weekly")
        all_habits = analytics.return_habits_by_period(None)

        for i in daily_habits:
            assert i[3] == "daily"
        for i in weekly_habits:
            assert i[3] == "weekly"

        assert len(all_habits) == 5

