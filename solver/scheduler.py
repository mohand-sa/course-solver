
from typing import List, Dict, Tuple
from .toposort import CourseGraph

class SemesterScheduler:
    def __init__(self, courses: Dict[str, Dict], max_credits: int = 36):
        self.courses = courses
        self.max_credits = max_credits
        self.graph = CourseGraph(courses)
    
    
   
    def schedule_semesters(self) -> List[List[str]]:
        """Schedules courses into semesters respecting credit limits AND semester availability."""
        course_order = self.graph.topological_sort()
        completed = set()
        semesters = []
        empty_semester_count = 0  # Track consecutive empty semesters
        
        semester_counter = 0
        
        while course_order:
            is_fall = semester_counter % 2 == 0
            current_semester = []
            current_credits = 0
            
            # Try to schedule courses for this semester
            for course in list(course_order):
                info = self.courses[course]
                
                # Check if all prereqs are completed
                if all(prereq in completed for prereq in info.get("prereqs", [])):
                    # Check if course is offered this semester
                    offered = info.get("offered", ["fall", "spring"])
                    current_semester_type = "fall" if is_fall else "spring"
                    
                    if current_semester_type in offered:
                        # Check credit limit
                        if current_credits + info["credits"] <= self.max_credits:
                            current_semester.append(course)
                            current_credits += info["credits"]
                            course_order.remove(course)
            
            if not current_semester:
                # No courses scheduled this semester
                empty_semester_count += 1
                if empty_semester_count >= 4:  # Give up after 4 empty semesters
                    raise ValueError(f"Cannot schedule remaining courses: {course_order}")
            else:
                empty_semester_count = 0  # Reset when we make progress
            
            # Add semester (even if empty, we track the slot)
            semesters.append(current_semester)
            completed.update(current_semester)
            semester_counter += 1
            
            # Safety break
            if semester_counter > len(self.courses) * 3:
                raise ValueError("Too many semesters created")
        
        # Filter out empty semesters
        return [s for s in semesters if s]

def validate_schedule(courses: Dict, schedule: List[List[str]]) -> Tuple[bool, str]:
    
    all_courses = set(courses.keys())
    scheduled = {course for semester in schedule for course in semester}
    
    if scheduled != all_courses:
        missing = all_courses - scheduled
        return False, f"Missing courses: {missing}"
    
    # Check prerequisites
    for semester_idx, semester in enumerate(schedule):
        for course in semester:
            for prereq in courses[course].get("prereqs", []):
                prereq_scheduled = False
                for earlier_semester in schedule[:semester_idx]:
                    if prereq in earlier_semester:
                        prereq_scheduled = True
                        break
                if not prereq_scheduled:
                    return False, f"Course {course} scheduled before prerequisite {prereq}"
    
    # Check credit limits
    for i, semester in enumerate(schedule):
        total_credits = sum(courses[c]["credits"] for c in semester)
        if total_credits > 36:
            return False, f"Semester {i+1} exceeds credit limit: {total_credits}"
    
    return True, "Schedule is valid"