# Course Solver: University Degree Prerequisite Optimizer

An algorithmic tool that generates valid, optimized semester-by-semester degree plans by modeling course prerequisites as directed acyclic graphs.

## Features
- **Topological Sort**: Detects prerequisite cycles and generates valid course sequences
- **Constraint Solver**: Respects credit limits, semester availability, and graduation requirements
- **Optimization**: Minimizes time-to-graduation or balances workload across semesters
- **Visualization**: Interactive graph rendering of degree roadmaps

## Quick Start
```bash
pip install -r requirements.txt
python main.py --university data/politecnico_di_milano.json