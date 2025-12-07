import pytest
from solver.toposort import CourseGraph

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

if __name__ == "__main__":
    pytest.main([__file__])