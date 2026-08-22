import unittest
from datetime import datetime, timedelta

from models import Task, TaskPriority, TaskStatus
from task_priority import (
    calculate_task_score,
    get_top_priority_tasks,
    sort_tasks_by_importance,
)


class TestTaskPriority(unittest.TestCase):
    def test_medium_task_gets_base_and_recent_update_bonus(self):
        task = Task("Medium", priority=TaskPriority.MEDIUM)
        self.assertEqual(calculate_task_score(task), 25)

    def test_important_tag_bonus_is_applied_once(self):
        task = Task("Tagged", priority=TaskPriority.HIGH, tags=["critical", "urgent"])
        self.assertEqual(calculate_task_score(task), 53)

    def test_done_status_reduces_score(self):
        task = Task("Done", priority=TaskPriority.URGENT)
        task.status = TaskStatus.DONE
        self.assertEqual(calculate_task_score(task), 15)

    def test_due_within_week_adds_bonus(self):
        task = Task(
            "Soon",
            priority=TaskPriority.LOW,
            due_date=datetime.now() + timedelta(days=4),
        )
        self.assertEqual(calculate_task_score(task), 25)

    def test_sort_tasks_by_importance_orders_highest_first(self):
        low = Task("Low", priority=TaskPriority.LOW)
        urgent = Task("Urgent", priority=TaskPriority.URGENT)
        high = Task("High", priority=TaskPriority.HIGH)

        ordered = sort_tasks_by_importance([low, urgent, high])

        self.assertEqual(
            [task.title for task in ordered],
            ["Urgent", "High", "Low"],
        )

    def test_top_priority_respects_limit(self):
        tasks = [
            Task("Low", priority=TaskPriority.LOW),
            Task("Medium", priority=TaskPriority.MEDIUM),
            Task("High", priority=TaskPriority.HIGH),
            Task("Urgent", priority=TaskPriority.URGENT),
        ]

        top = get_top_priority_tasks(tasks, limit=2)

        self.assertEqual(
            [task.title for task in top],
            ["Urgent", "High"],
        )


if __name__ == "__main__":
    unittest.main()
