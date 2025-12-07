import json
import sys
from solver.toposort import CourseGraph
from solver.scheduler import SemesterScheduler, validate_schedule

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
    metadata = data["metadata"]
    courses = data["courses"]
    
    print(f"Analyzing {metadata['university']}...")
    print(f"Total courses: {len(courses)}")
    print(f"Max credits per semester: {metadata['max_credits_per_semester']}\n")
    
    # Generate semester schedule
    try:
        scheduler = SemesterScheduler(
            courses, 
            max_credits=metadata['max_credits_per_semester']
        )
        schedule = scheduler.schedule_semesters()
        
        # Validate schedule
        is_valid, message = validate_schedule(courses, schedule)
        print(f"✓ Schedule validation: {message}\n")
        
        # Display semester plan
        for i, semester in enumerate(schedule, 1):
            total_credits = sum(courses[c]["credits"] for c in semester)
            print(f"--- Semester {i} ({total_credits} credits) ---")
            for course in semester:
                info = courses[course]
                print(f"  {course}: {info['name']} ({info['credits']} credits)")
            print()
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()