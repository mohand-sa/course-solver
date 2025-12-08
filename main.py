import json
import sys
from solver.toposort import CourseGraph
from solver.scheduler import SemesterScheduler, validate_schedule
from visualizer.degree_chart import create_degree_roadmap, create_workload_chart

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
    
    try:
        # Ask user for optimization preference
        print("Choose optimization strategy:")
        print("1. Fastest graduation (minimize semesters)")
        print("2. Balanced workload (spread difficulty evenly)")
        choice = input("Enter 1 or 2 [default: 1]: ").strip() or "1"
        optimize = "balanced" if choice == "2" else "fastest"
        
        # Generate schedule
        scheduler = SemesterScheduler(
            courses, 
            max_credits=metadata['max_credits_per_semester'],
            optimize=optimize
        )
        schedule = scheduler.schedule_semesters()
        
        # Validate
        is_valid, message = validate_schedule(courses, schedule)
        print(f"✓ Schedule validation: {message}\n")
        
        # Display
        for i, semester in enumerate(schedule, 1):
            total_credits = sum(courses[c]["credits"] for c in semester)
            print(f"--- Semester {i} ({total_credits} credits) ---")
            for course in semester:
                info = courses[course]
                offered = ", ".join(info.get("offered", ["fall", "spring"]))
                print(f"  {course}: {info['name']} ({info['credits']} cr) [Offered: {offered}]")
            print()
        
        # Visualize
        print("🎨 Generating degree roadmap...")
        roadmap_path = create_degree_roadmap(courses, schedule)
        print(f"✓ Saved: {roadmap_path}")
        
        print("📊 Generating workload chart...")
        chart_path = create_workload_chart(schedule, courses)
        print(f"✓ Saved: {chart_path}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nVisualization skipped by user.")
    except Exception as e:
        print(f"Warning: Could not generate charts: {e}")

if __name__ == "__main__":
    main()