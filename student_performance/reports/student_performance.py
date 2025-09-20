"""Отчёт student-performance: средние оценки студентов."""

from collections import defaultdict
from ..registry import register


@register('student-performance')
def build_student_performance(rows):
    """Формирует отчёт со средними оценками студентов по всем предметам."""
    sums = defaultdict(float)
    counts = defaultdict(int)
    for r in rows:
        name = str(r['student_name']).strip()
        grade = float(r['grade'])
        sums[name] += grade
        counts[name] += 1
    result = []
    for name in sums:
        avg = round(sums[name] / counts[name], 1)
        result.append((name, avg))
    result.sort(key=lambda x: (-x[1], x[0]))
    return ('student_name', 'grade'), result
