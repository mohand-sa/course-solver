"""
Topological sort implementation for course prerequisite graphs.
Handles cycle detection and generates valid course sequences.
"""

from collections import defaultdict, deque
from typing import Dict, List

class CourseGraph:
    def __init__(self, courses: Dict[str, Dict]):
        self.courses = courses
        self.graph = defaultdict(list)
        self.in_degree = {cid: 0 for cid in courses}
        self._build_graph()
    
    def _build_graph(self):
        for course_id, info in self.courses.items():
            for prereq in info.get("prereqs", []):
                self.graph[prereq].append(course_id)
                self.in_degree[course_id] += 1
    
    def topological_sort(self) -> List[str]:
        queue = deque([cid for cid, degree in self.in_degree.items() if degree == 0])
        order = []
        
        while queue:
            current = queue.popleft()
            order.append(current)
            
            for neighbor in self.graph[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != len(self.courses):
            raise ValueError("Cycle detected in prerequisite graph")
        
        return order

if __name__ == "__main__":
    sample = {
        "A": {"prereqs": []},
        "B": {"prereqs": ["A"]},
        "C": {"prereqs": ["A"]},
        "D": {"prereqs": ["B", "C"]}
    }
    graph = CourseGraph(sample)
    print(graph.topological_sort())