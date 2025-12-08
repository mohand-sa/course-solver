import pytest
import os
from solver.toposort import CourseGraph
from solver.scheduler import SemesterScheduler, validate_schedule
from visualizer.degree_chart import create_degree_roadmap, create_workload_chart

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

def test_semester_availability():
    courses = {
        "A": {"prereqs": [], "credits": 12, "offered": ["fall"]},
        "B": {"prereqs": ["A"], "credits": 12, "offered": ["spring"]},
        "C": {"prereqs": ["B"], "credits": 12, "offered": ["fall"]}
    }
    scheduler = SemesterScheduler(courses, max_credits=24)
    schedule = scheduler.schedule_semesters()
    is_valid, msg = validate_schedule(courses, schedule)
    assert is_valid, msg
    # Should be 3 semesters (Fall-Spring-Fall)
    assert len(schedule) == 3

def test_visualization():
    """Test that visualization functions create PNG files."""
    courses = {
        "A": {"name": "Course A", "prereqs": [], "credits": 12, "offered": ["fall"], "difficulty": 1},
        "B": {"name": "Course B", "prereqs": ["A"], "credits": 12, "offered": ["spring"], "difficulty": 2},
        "C": {"name": "Course C", "prereqs": ["B"], "credits": 12, "offered": ["fall"], "difficulty": 3}
    }
    scheduler = SemesterScheduler(courses, max_credits=24)
    schedule = scheduler.schedule_semesters()
    
    # Test roadmap
    roadmap_path = create_degree_roadmap(courses, schedule, "docs/test_roadmap.png")
    assert os.path.exists(roadmap_path), "Roadmap PNG not created"
    
    # Test workload chart
    chart_path = create_workload_chart(schedule, courses, "docs/test_workload.png")
    assert os.path.exists(chart_path), "Workload PNG not created"
    
    # Cleanup
    os.remove(roadmap_path)
    os.remove(chart_path)

if __name__ == "__main__":
    pytest.main([__file__])