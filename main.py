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
        semester_types = ["Fall", "Spring"] * (len(schedule) // 2 + 1)
        for i, semester in enumerate(schedule, 1):
            total_credits = sum(courses[c]["credits"] for c in semester)
            sem_type = semester_types[i-1] if i-1 < len(semester_types) else "Semester"
            print(f"--- {sem_type} {i} ({total_credits} credits) ---")
            for course in semester:
                info = courses[course]
                offered = ", ".join(info.get("offered", ["fall", "spring"]))
                print(f"  {course}: {info['name']} ({info['credits']} credits) [Offered: {offered}]")
            print()
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()