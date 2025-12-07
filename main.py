import json
import sys
from solver.toposort import CourseGraph

def load_university_data(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        sys.exit(1)

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--university":
        print("Usage: python main.py --university <path_to_json>")
        sys.exit(1)
    
    data = load_university_data(sys.argv[2])
    courses = data["courses"]
    
    print(f"Analyzing {data['metadata']['university']}...")
    print(f"Total courses: {len(courses)}")
    
    try:
        graph = CourseGraph(courses)
        order = graph.topological_sort()
        print("\nValid course sequence:")
        for i, course in enumerate(order, 1):
            print(f"{i}. {course}: {courses[course]['name']}")
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()