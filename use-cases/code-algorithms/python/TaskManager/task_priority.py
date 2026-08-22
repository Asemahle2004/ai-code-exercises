from datetime import datetime

from models import TaskStatus, TaskPriority


def calculate_task_score(task):
    """Calculate a numerical importance score for a task.

    The score combines base priority with due-date urgency, task status,
    important tags, and recent activity.

    Args:
        task: A Task-like object with ``priority``, ``due_date``, ``status``,
            ``tags``, and ``updated_at`` attributes.

    Returns:
        int: The calculated importance score. Higher values indicate greater
        importance.

    Scoring rules:
        - LOW = 10, MEDIUM = 20, HIGH = 40, URGENT = 60.
        - Overdue = +35; due today = +20; due within 2 days = +15;
          due within 7 days = +10.
        - DONE = -50; REVIEW = -15.
        - At least one ``blocker``, ``critical``, or ``urgent`` tag = +8.
        - Updated less than one day ago = +5.

    Notes:
        Tag matching is case-sensitive. The important-tag bonus is applied
        only once. The result can be negative and depends on ``datetime.now``.
    """
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6,
    }

    score = priority_weights.get(task.priority, 0) * 10

    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += 35
        elif days_until_due == 0:
            score += 20
        elif days_until_due <= 2:
            score += 15
        elif days_until_due <= 7:
            score += 10

    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks):
    """Return tasks sorted from highest to lowest calculated importance."""
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    return [
        task
        for _, task in sorted(task_scores, key=lambda item: item[0], reverse=True)
    ]


def get_top_priority_tasks(tasks, limit=5):
    """Return up to ``limit`` tasks with the highest importance scores."""
    return sort_tasks_by_importance(tasks)[:limit]
