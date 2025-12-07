import pytest
from solver.toposort import CourseGraph
from solver.scheduler import SemesterScheduler, validate_schedule

def test_simple_toposort():
    courses = {
        "A": {"prereqs": []},
        "B": {"prereqs": ["A"]},
        "C": {"prereqs": ["A"]},
        "D": {"prereqs": ["B", "C"]}
    }
    graph = CourseGraph(courses)
    order = graph.topological_sort()
    assert order.index("A") < order.index("B")
    assert order.index("A") < order.index("C")
    assert order.index("B") < order.index("D")
    assert order.index("C") < order.index("D")

def test_cycle_detection():
    courses = {
        "A": {"prereqs": ["B"]},
        "B": {"prereqs": ["A"]}
    }
    graph = CourseGraph(courses)
    with pytest.raises(ValueError, match="Cycle detected"):
        graph.topological_sort()

def test_scheduler():
    courses = {
        "A": {"prereqs": [], "credits": 12},
        "B": {"prereqs": ["A"], "credits": 12},
        "C": {"prereqs": ["A"], "credits": 12},
        "D": {"prereqs": ["B", "C"], "credits": 12}
    }
    scheduler = SemesterScheduler(courses, max_credits=24)
    schedule = scheduler.schedule_semesters()
    
    assert len(schedule) >= 3
    is_valid, msg = validate_schedule(courses, schedule)
    assert is_valid, msg

if __name__ == "__main__":
    pytest.main([__file__])