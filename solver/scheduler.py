
from typing import List, Dict, Tuple
from .toposort import CourseGraph

class SemesterScheduler:
    
    def __init__(self, courses: Dict, max_credits: int = 36, optimize: str = "fastest"):
     """
     optimize: "fastest" (minimize semesters) or "balanced" (even workload)
     """
     self.courses = courses
     self.max_credits = max_credits
     self.optimize = optimize
     self.graph = CourseGraph(courses)
   
    def schedule_semesters(self) -> List[List[str]]:
     """Schedule courses respecting prerequisites, credits, and offered semesters."""
     course_order = self.graph.topological_sort()
     completed = set()
     semesters = []
    
     semester_counter = 0
    
     while course_order:
        is_fall = semester_counter % 2 == 0
        current_semester = []
        current_credits = 0
        
        # Create list of available courses for this semester
        available = []
        for course in list(course_order):
            info = self.courses[course]
            # All prereqs done?
            if all(prereq in completed for prereq in info.get("prereqs", [])):
                # Offered this semester?
                offered = info.get("offered", ["fall", "spring"])
                current_semester_type = "fall" if is_fall else "spring"
                if current_semester_type in offered:
                    available.append(course)
        
        # Sort available courses based on optimization strategy
        if self.optimize == "balanced":
            # Sort by difficulty descending (hard courses spread out)
            available.sort(key=lambda c: self.courses[c].get("difficulty", 1), reverse=True)
        else:  # fastest
            # Sort by number of dependent courses (critical path first)
            def count_dependents(course):
                return sum(1 for c, info in self.courses.items() if course in info.get("prereqs", []))
            available.sort(key=count_dependents, reverse=True)
        
        # Fill semester
        for course in available:
            info = self.courses[course]
            if current_credits + info["credits"] <= self.max_credits:
                current_semester.append(course)
                current_credits += info["credits"]
                course_order.remove(course)
        
        # If no courses fit, advance semester
        if not current_semester:
            semester_counter += 1
            if semester_counter > len(course_order) * 3:  # Safety break
                raise ValueError("Cannot schedule remaining courses within constraints")
            continue
        
        # Add semester
        semester_label = f"{'Fall' if is_fall else 'Spring'} {semester_counter//2 + 1}"
        semesters.append((semester_label, current_semester))
        completed.update(current_semester)
        semester_counter += 1
    
     # Extract just the course lists (remove labels)
     return [sem[1] for sem in semesters]

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